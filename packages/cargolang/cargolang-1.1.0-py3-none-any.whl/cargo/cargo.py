import string, os, osascript, webbrowser, random, time

#######################################
# CONSTANTS
#######################################

def stringWithArrows(text, posStart, posEnd):
    result = ''

    idxStart = max(text.rfind('\n', 0, posStart.idx), 0)
    idxEnd = text.find('\n', idxStart + 1)
    if idxEnd < 0: idxEnd = len(text)

    lineCount = posEnd.ln - posStart.ln + 1
    for i in range(lineCount):
        line = text[idxStart:idxEnd]
        colStart = posStart.col if i == 0 else 0
        colEnd = posEnd.col if i == lineCount - 1 else len(line) - 1

        result += line + '\n'
        result += ' ' * colStart + '^' * (colEnd - colStart)

        idxStart = idxEnd
        idxEnd = text.find('\n', idxStart + 1)
        if idxEnd < 0: idxEnd = len(text)

    return result.replace('\t', '')

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, posStart, posEnd, errorName, details):
        self.posStart = posStart
        self.posEnd = posEnd
        self.errorName = errorName
        self.details = details

    def asString(self):
        result = f'{self.errorName}: {self.details}\n'
        result += f'File {self.posStart.fn}, line {self.posStart.ln + 1}'
        result += '\n\n' + stringWithArrows(self.posStart.ftxt, self.posStart, self.posEnd)
        return result

class IllegalCharError(Error):
    def __init__(self, posStart, posEnd, details):
        super().__init__(posStart, posEnd, 'Illegal Character', details)

class ExpectedCharError(Error):
    def __init__(self, posStart, posEnd, details):
        super().__init__(posStart, posEnd, 'Expected Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, posStart, posEnd, details=''):
        super().__init__(posStart, posEnd, 'Invalid Syntax', details)

class RTError(Error):
    def __init__(self, posStart, posEnd, details, context):
        super().__init__(posStart, posEnd, 'Runtime Error', details)
        self.context = context

    def asString(self):
        result = self.generateTraceback()
        result += f'{self.errorName}: {self.details}'
        result += '\n\n' + stringWithArrows(self.posStart.ftxt, self.posStart, self.posEnd)
        return result

    def generateTraceback(self):
        result = ''
        pos = self.posStart
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.displayName}\n' + result
            pos = ctx.parentEntryPos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result

#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, currentChar=None):
        self.idx += 1
        self.col += 1

        if currentChar == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################

TT_INT          = 'INT'
TT_FLOAT        = 'FLOAT'
TT_STRING       = 'STRING'
TT_IDENTIFIER   = 'IDENTIFIER'
TT_KEYWORD      = 'KEYWORD'
TT_PLUS         = 'PLUS'
TT_MINUS        = 'MINUS'
TT_MUL          = 'MUL'
TT_DIV          = 'DIV'
TT_POW          = 'POW'
TT_EQ           = 'EQ'
TT_LPAREN       = 'LPAREN'
TT_RPAREN       = 'RPAREN'
TT_LSQPAR       = 'LSQPAR'
TT_RSQPAR       = 'RSQPAR'
TT_EE           = 'EE'
TT_NE           = 'NE'
TT_LT           = 'LT'
TT_GT           = 'GT'
TT_LTE          = 'LTE'
TT_GTE          = 'GTE'
TT_COMMA        = 'COMMA'
TT_ARROW        = 'ARROW'
TT_NEWLINE      = 'NEWLINE'
TT_EOF          = 'EOF'

KEYWORDS = [
    'var',
    'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'for',
    'to',
    'step',
    'while',
    'fnc',
    '{',
    '}',
    'break',
    'pass',
    'return',
]

class Token:
    def __init__(self, type_, value=None, posStart=None, posEnd=None):
        self.type = type_
        self.value = value

        if posStart:
            self.posStart = posStart.copy()
            self.posEnd = posStart.copy()
            self.posEnd.advance()

        if posEnd:
            self.posEnd = posEnd.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.currentChar = None
        self.advance()

    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def makeTokens(self):
        tokens = []

        while self.currentChar != None:
            if self.currentChar in ' \t':
                self.advance()
            elif self.currentChar == '#':
                self.skipComment()
            elif self.currentChar in '\n' or self.currentChar in ';\n':
                tokens.append(Token(TT_NEWLINE, posStart=self.pos))
                self.advance()
            elif self.currentChar in DIGITS:
                tokens.append(self.makeNumber())
            elif self.currentChar in LETTERS + '{' + '}':
                tokens.append(self.makeIdentifier())
            elif self.currentChar == "'":
                tokens.append(self.makeStringSingle())
            elif self.currentChar == '"':
                tokens.append(self.makeStringDouble())
            elif self.currentChar == '+':
                tokens.append(Token(TT_PLUS, posStart=self.pos))
                self.advance()
            elif self.currentChar == '-':
                tokens.append(self.makeMinusOrArrow())
            elif self.currentChar == '*':
                tokens.append(Token(TT_MUL, posStart=self.pos))
                self.advance()
            elif self.currentChar == '/':
                tokens.append(Token(TT_DIV, posStart=self.pos))
                self.advance()
            elif self.currentChar == '^':
                tokens.append(Token(TT_POW, posStart=self.pos))
                self.advance()
            elif self.currentChar == '(':
                tokens.append(Token(TT_LPAREN, posStart=self.pos))
                self.advance()
            elif self.currentChar == ')':
                tokens.append(Token(TT_RPAREN, posStart=self.pos))
                self.advance()
            elif self.currentChar == '[':
                tokens.append(Token(TT_LSQPAR, posStart=self.pos))
                self.advance()
            elif self.currentChar == ']':
                tokens.append(Token(TT_RSQPAR, posStart=self.pos))
                self.advance()
            elif self.currentChar == '!':
                token, error = self.makeNotEquals()
                if error: return [], error
                tokens.append(token)
            elif self.currentChar == '=':
                tokens.append(self.makeEquals())
            elif self.currentChar == '<':
                tokens.append(self.makeLessThan())
            elif self.currentChar == '>':
                tokens.append(self.makeGreaterThan())
            elif self.currentChar == ',':
                tokens.append(Token(TT_COMMA, posStart=self.pos))
                self.advance()
            else:
                posStart = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(posStart, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, posStart=self.pos))
        return tokens, None

    def makeStringSingle(self):
        string = ''
        posStart = self.pos.copy()
        escapeCharacter = False
        self.advance()

        escapeCharacters = {
            'n': '\n',
            't': '\t'
        }

        while self.currentChar != None and (escapeCharacter or self.currentChar != "'"):
            if self.currentChar == '\\':
                self.advance()
                if self.currentChar == ' ':
                    escapeCharacter = False
                    string += '\ '
                    self.advance()
                elif self.currentChar == 'n':
                    escapeCharacter = False
                    string += '\n'
                    self.advance()
                elif self.currentChar == 't':
                    escapeCharacter = False
                    string += '\t'
                    self.advance()
                else:
                    escapeCharacter = False
                    string += self.currentChar
                    self.advance()
            else:
                string += self.currentChar
                self.advance()
            escapeCharacter = False

        self.advance()
        return Token(TT_STRING, string, posStart, self.pos)

    def makeStringDouble(self):
        string = ''
        posStart = self.pos.copy()
        escapeCharacter = False
        self.advance()

        escapeCharacters = {
            'n': '\n',
            't': '\t'
        }

        while self.currentChar != None and (escapeCharacter or self.currentChar != '"'):
            #if escapeCharacter:
            #    string += escapeCharacters.get(self.currentChar, self.currentChar)
            #else:
            if self.currentChar == '\\':
                self.advance()
                if self.currentChar == ' ':
                    escapeCharacter = False
                    string += '\ '
                    self.advance()
                elif self.currentChar == 'n':
                    escapeCharacter = False
                    string += '\n'
                    self.advance()
                elif self.currentChar == 't':
                    escapeCharacter = False
                    string += '\t'
                    self.advance()
                else:
                    escapeCharacter = False
                    string += self.currentChar
                    self.advance()
            else:
                string += self.currentChar
                self.advance()
            escapeCharacter = False

        self.advance()
        return Token(TT_STRING, string, posStart, self.pos)

    def makeNumber(self):
        numStr = ''
        dotCount = 0
        posStart = self.pos.copy()

        while self.currentChar != None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if dotCount == 1: break
                dotCount += 1
            numStr += self.currentChar
            self.advance()

        if dotCount == 0:
            return Token(TT_INT, int(numStr), posStart, self.pos)
        else:
            return Token(TT_FLOAT, float(numStr), posStart, self.pos)

    def makeIdentifier(self):
        idStr = ''
        posStart = self.pos.copy()

        while self.currentChar != None and self.currentChar in LETTERS_DIGITS + '_' + '{' + '}':
            idStr += self.currentChar
            self.advance()

        tokType = TT_KEYWORD if idStr in KEYWORDS else TT_IDENTIFIER
        return Token(tokType, idStr, posStart, self.pos)

    def makeMinusOrArrow(self):
        tokType = TT_MINUS
        posStart = self.pos.copy()
        self.advance()

        if self.currentChar == '>':
            self.advance()
            tokType = TT_ARROW

        return Token(tokType, posStart=posStart, posEnd=self.pos)

    def makeNotEquals(self):
        posStart = self.pos.copy()
        self.advance()

        if self.currentChar == '=':
            self.advance()
            return Token(TT_NE, posStart=posStart, posEnd=self.pos), None

        self.advance()
        return None, ExpectedCharError(posStart, self.pos, "'=' (after '!')")

    def makeEquals(self):
        tokType = TT_EQ
        posStart = self.pos.copy()
        self.advance()

        if self.currentChar == '=':
            self.advance()
            tokType = TT_EE

        return Token(tokType, posStart=posStart, posEnd=self.pos)

    def makeLessThan(self):
        tokType = TT_LT
        posStart = self.pos.copy()
        self.advance()

        if self.currentChar == '=':
            self.advance()
            tokType = TT_LTE

        return Token(tokType, posStart=posStart, posEnd=self.pos)

    def makeGreaterThan(self):
        tokType = TT_GT
        posStart = self.pos.copy()
        self.advance()

        if self.currentChar == '=':
            self.advance()
            tokType = TT_GTE

        return Token(tokType, posStart=posStart, posEnd=self.pos)

    def skipComment(self):
        self.advance()
        while self.currentChar != '\n':
            self.advance()
        self.advance()

#######################################
# NODES
#######################################

class StringNode:
    def __init__(self, tok):
        self.tok = tok

        self.posStart = self.tok.posStart
        self.posEnd = self.tok.posEnd

    def __repr__(self):
        return f'{self.tok}'

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.posStart = self.tok.posStart
        self.posEnd = self.tok.posEnd

    def __repr__(self):
        return f'{self.tok}'

class ListNode:
    def __init__(self, elementNodes, posStart, posEnd):
        self.elementNodes = elementNodes

        self.posStart = posStart
        self.posEnd = posEnd

class VarAccessNode:
    def __init__(self, varNameTok):
        self.varNameTok = varNameTok

        self.posStart = self.varNameTok.posStart
        self.posEnd = self.varNameTok.posEnd

class VarAssignNode:
    def __init__(self, varNameTok, valueNode):
        self.varNameTok = varNameTok
        self.valueNode = valueNode

        self.posStart = self.varNameTok.posStart
        self.posEnd = self.valueNode.posEnd

class BinOpNode:
    def __init__(self, leftNode, opTok, rightNode):
        self.leftNode = leftNode
        self.opTok = opTok
        self.rightNode = rightNode

        self.posStart = self.leftNode.posStart
        self.posEnd = self.rightNode.posEnd

    def __repr__(self):
        return f'({self.leftNode}, {self.opTok}, {self.rightNode})'

class UnaryOpNode:
    def __init__(self, opTok, node):
        self.opTok = opTok
        self.node = node

        self.posStart = self.opTok.posStart
        self.posEnd = node.posEnd

    def __repr__(self):
        return f'({self.opTok}, {self.node})'

class IfNode:
    def __init__(self, cases, elseCase):
        self.cases = cases
        self.elseCase = elseCase

        self.posStart = self.cases[0][0].posStart
        self.posEnd = (self.elseCase or self.cases[len(self.cases) - 1])[0].posEnd

class ForNode:
    def __init__(self, varNameTok, startValueNode, endValueNode, stepValueNode, bodyNode, shouldReturnNull):
        self.varNameTok = varNameTok
        self.startValueNode = startValueNode
        self.endValueNode = endValueNode
        self.stepValueNode = stepValueNode
        self.bodyNode = bodyNode
        self.shouldReturnNull = shouldReturnNull

        self.posStart = self.varNameTok.posStart
        self.posEnd = self.bodyNode.posEnd

class WhileNode:
    def __init__(self, conditionNode, bodyNode, shouldReturnNull):
        self.conditionNode = conditionNode
        self.bodyNode = bodyNode
        self.shouldReturnNull = shouldReturnNull

        self.posStart = self.conditionNode.posStart
        self.posEnd = self.bodyNode.posEnd

class FuncDefNode:
    def __init__(self, varNameTok, argNameToks, bodyNode, shouldAutoReturn):
        self.varNameTok = varNameTok
        self.argNameToks = argNameToks
        self.bodyNode = bodyNode
        self.shouldAutoReturn = shouldAutoReturn

        if self.varNameTok:
            self.posStart = self.varNameTok.posStart
        elif len(self.argNameToks) > 0:
            self.posStart = self.argNameToks[0].posStart
        else:
            self.posStart = self.bodyNode.posStart

        self.posEnd = self.bodyNode.posEnd

class CallNode:
    def __init__(self, nodeToCall, argNodes):
        self.nodeToCall = nodeToCall
        self.argNodes = argNodes

        self.posStart = self.nodeToCall.posStart

        if len(self.argNodes) > 0:
            self.posEnd = self.argNodes[len(self.argNodes) - 1].posEnd
        else:
            self.posEnd = self.nodeToCall.posEnd

class ReturnNode:
    def __init__(self, nodeToReturn, posStart, posEnd):
        self.nodeToReturn = nodeToReturn

        self.posStart = posStart
        self.posEnd = posEnd

class ContinueNode:
    def __init__(self, posStart, posEnd):
        self.posStart = posStart
        self.posEnd = posEnd

class BreakNode:
    def __init__(self, posStart, posEnd):
        self.posStart = posStart
        self.posEnd = posEnd

#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.lastRegisteredAdvanceCount = 0
        self.advanceCount = 0
        self.toReverseCount = 0

    def registerAdvancement(self):
        self.lastRegisteredAdvanceCount = 1
        self.advanceCount += 1

    def register(self, res):
        self.lastRegisteredAdvanceCount = res.advanceCount
        self.advanceCount += res.advanceCount
        if res.error: self.error = res.error
        return res.node

    def tryRegister(self, res):
        if res.error:
            self.toReverseCount = res.advanceCount
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.lastRegisteredAdvanceCount == 0:
            self.error = error
        return self

#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokIdx = -1
        self.advance()

    def advance(self):
        self.tokIdx += 1
        self.updateCurrentTok()
        return self.currentTok

    def reverse(self, amount=1):
        self.tokIdx -= amount
        self.updateCurrentTok()
        return self.currentTok

    def updateCurrentTok(self):
        if self.tokIdx >= 0 and self.tokIdx < len(self.tokens):
            self.currentTok = self.tokens[self.tokIdx]

    def parse(self):
        res = self.statements()
        if not res.error and self.currentTok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                "Expected statement" #'+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'and' or 'or'
            ))
        return res

    def statements(self):
        res = ParseResult()
        statements = []
        posStart = self.currentTok.posStart.copy()

        while self.currentTok.type == TT_NEWLINE:
            res.registerAdvancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        moreStatements = True

        while True:
            newLineCount = 0
            while self.currentTok.type == TT_NEWLINE:
                res.registerAdvancement()
                self.advance()
                newLineCount += 1
            if newLineCount == 0:
                moreStatements = False
            if not moreStatements: break
            statement = res.tryRegister(self.statement())
            if not statement:
                self.reverse(res.toReverseCount)
                moreStatements = False
                continue
            statements.append(statement)
        return res.success(ListNode(
            statements, posStart, self.currentTok.posEnd.copy()
        ))

    def statement(self):
        res = ParseResult()
        posStart = self.currentTok.posStart.copy()

        if self.currentTok.matches(TT_KEYWORD, 'return'):
            res.registerAdvancement()
            self.advance()

            expr = res.tryRegister(self.expr())
            if not expr:
                self.reverse(res.toReverseCount)
            return res.success(ReturnNode(expr, posStart, self.currentTok.posStart.copy()))

        if self.currentTok.matches(TT_KEYWORD, 'pass'):
            res.registerAdvancement()
            self.advance()
            return res.success(ContinueNode(posStart, self.currentTok.posStart.copy()))

        if self.currentTok.matches(TT_KEYWORD, 'break'):
            res.registerAdvancement()
            self.advance()
            return res.success(BreakNode(posStart, self.currentTok.posStart.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                "Expected 'return', 'pass', 'break', 'var', 'if', 'for', 'while', 'fnc', int, float, identifier, '+', '-', '(', '[' or 'not'"
            ))
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        if self.currentTok.matches(TT_KEYWORD, 'var'):
            res.registerAdvancement()
            self.advance()

            if self.currentTok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    "Expected identifier"
                ))

            varName = self.currentTok
            res.registerAdvancement()
            self.advance()

            if self.currentTok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    "Expected '='"
                ))

            res.registerAdvancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(varName, expr))

        node = res.register(self.binOp(self.compExpr, ((TT_KEYWORD, 'and'), (TT_KEYWORD, 'or'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                "Expected 'var', 'if', 'for', 'while', 'fnc', int, float, identifier, '+', '-', '(', '[' or 'not'"
            ))

        return res.success(node)

    def compExpr(self):
        res = ParseResult()

        if self.currentTok.matches(TT_KEYWORD, 'not'):
            opTok = self.currentTok
            res.registerAdvancement()
            self.advance()

            node = res.register(self.compExpr())
            if res.error: return res
            return res.success(UnaryOpNode(opTok, node))

        node = res.register(self.binOp(self.arithExpr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                "Expected int, float, identifier, '+', '-', '(', '[' or 'not'"
            ))

        return res.success(node)

    def arithExpr(self):
        return self.binOp(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.binOp(self.factor, (TT_MUL, TT_DIV))

    def factor(self):
        res = ParseResult()
        tok = self.currentTok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.registerAdvancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def power(self):
        return self.binOp(self.call, (TT_POW,), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.currentTok.type == TT_LPAREN:
            res.registerAdvancement()
            self.advance()
            argNodes = []

            if self.currentTok.type == TT_RPAREN:
                res.registerAdvancement()
                self.advance()
            else:
                argNodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.currentTok.posStart, self.currentTok.posEnd,
                        "Expected ')', 'var', 'if', 'for', 'while', 'fnc', int, float, identifier, '+', '-', '(', '' or 'not'"
                    ))

                while self.currentTok.type == TT_COMMA:
                    res.registerAdvancement()
                    self.advance()

                    argNodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.currentTok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.currentTok.posStart, self.currentTok.posEnd,
                        f"Expected ',' or ')'"
                    ))

                res.registerAdvancement()
                self.advance()
            return res.success(CallNode(atom, argNodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.currentTok

        if tok.type in (TT_INT, TT_FLOAT):
            res.registerAdvancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.registerAdvancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.registerAdvancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.registerAdvancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.currentTok.type == TT_RPAREN:
                res.registerAdvancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    "Expected ')'"
                ))

        elif tok.type == TT_LSQPAR:
            listExpr = res.register(self.listExpr())
            if res.error: return res
            return res.success(listExpr)

        elif tok.matches(TT_KEYWORD, 'if'):
            ifExpr = res.register(self.ifExpr())
            if res.error: return res
            return res.success(ifExpr)

        elif tok.matches(TT_KEYWORD, 'for'):
            forExpr = res.register(self.forExpr())
            if res.error: return res
            return res.success(forExpr)

        elif tok.matches(TT_KEYWORD, 'while'):
            whileExpr = res.register(self.whileExpr())
            if res.error: return res
            return res.success(whileExpr)

        elif tok.matches(TT_KEYWORD, 'fnc'):
            funcDef = res.register(self.funcDef())
            if res.error: return res
            return res.success(funcDef)

        return res.failure(InvalidSyntaxError(
            tok.posStart, tok.posEnd,
            "Expected int, float, identifier, '+', '-', '(', '[', 'if', 'for', 'while', 'fnc'"
        ))

    def listExpr(self):
        res = ParseResult()
        elementNodes = []
        posStart = self.currentTok.posStart.copy()

        if self.currentTok.type != TT_LSQPAR:
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                'Expected "["'
            ))

        res.registerAdvancement()
        self.advance()

        if self.currentTok.type == TT_RSQPAR:
            res.registerAdvancement()
            self.advance()
        else:
            elementNodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    "Expected ']', 'var', 'if', 'for', 'while', 'fnc', int, float, identifier, '+', '-', '(', '[' or 'not'"
                ))

            while self.currentTok.type == TT_COMMA:
                res.registerAdvancement()
                self.advance()

                elementNodes.append(res.register(self.expr()))
                if res.error: return res

            if self.currentTok.type != TT_RSQPAR:
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    f"Expected ',' or ']'"
                ))

            res.registerAdvancement()
            self.advance()
        return res.success(ListNode(
            elementNodes,
            posStart,
            self.currentTok.posEnd.copy()
        ))

    def ifExpr(self):
        res = ParseResult()

        allCases = res.register(self.ifExprCases('if'))
        if res.error: return res
        cases, elseCase = allCases
        return res.success(IfNode(cases, elseCase))

    def ifExprB(self):
        return self.ifExprCases('elif')

    def ifExprC(self):
        res = ParseResult()
        elseCase = None

        if self.currentTok.matches(TT_KEYWORD, 'else'):
            res.registerAdvancement()
            self.advance()

            if self.currentTok.type == TT_NEWLINE:
                res.registerAdvancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error: return res
                elseCase = (statements, True)

                if self.currentTok.matches(TT_KEYWORD, '}'):
                    res.registerAdvancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.currentTok.posStart, self.currentTok.posEnd,
                        'Expected "}"'
                    ))
            else:
                expr = res.register(self.statement())
                if res.error: return res
                elseCase = (expr, False)
        return res.success(elseCase)

    def ifExprBOrC(self):
        res = ParseResult()
        cases, elseCase = [], None

        if self.currentTok.matches(TT_KEYWORD, 'elif'):
            allCases = res.register(self.ifExprB())
            if res.error: return res
            cases, elseCase = allCases
        else:
            elseCase = res.register(self.ifExprC())
            if res.error: return res

        return res.success((cases, elseCase))

    def ifExprCases(self, caseKeyword):
        res = ParseResult()
        cases = []
        elseCase = None

        if not self.currentTok.matches(TT_KEYWORD, caseKeyword):
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                f'Expected "{caseKeyword}"'
            ))
        res.registerAdvancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.currentTok.matches(TT_KEYWORD, '{'):
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                'Expected "{"'
            ))
        res.registerAdvancement()
        self.advance()

        if self.currentTok.type == TT_NEWLINE:
            res.registerAdvancement()
            self.advance()
            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.currentTok.matches(TT_KEYWORD, '}'):
                res.registerAdvancement()
                self.advance()
            else:
                allCases = res.register(self.ifExprBOrC())
                if res.error: return res
                newCases, elseCase = allCases
                cases.extend(newCases)
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))

            allCases = res.register(self.ifExprBOrC())
            if res.error: return res
            newCases, elseCase = allCases
            cases.extend(newCases)

        return res.success((cases, elseCase))

    def forExpr(self):
        res = ParseResult()

        if not self.currentTok.matches(TT_KEYWORD, 'for'):
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                f"Expected 'for'"
            ))

        res.registerAdvancement()
        self.advance()

        if self.currentTok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                f"Expected identifier"
            ))

        varName = self.currentTok
        res.registerAdvancement()
        self.advance()

        if self.currentTok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                f"Expected '='"
            ))

        res.registerAdvancement()
        self.advance()

        startValue = res.register(self.expr())
        if res.error: return res

        if not self.currentTok.matches(TT_KEYWORD, 'to'):
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                f"Expected 'to'"
            ))

        res.registerAdvancement()
        self.advance()

        endValue = res.register(self.expr())
        if res.error: return res

        if self.currentTok.matches(TT_KEYWORD, 'step'):
            res.registerAdvancement()
            self.advance()

            stepValue = res.register(self.expr())
            if res.error: return res
        else:
            stepValue = None

        if not self.currentTok.matches(TT_KEYWORD, '{'):
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                "Expected '{'"
            ))

        res.registerAdvancement()
        self.advance()

        if self.currentTok.type == TT_NEWLINE:
            res.registerAdvancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.currentTok.matches(TT_KEYWORD, '}'):
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    'Expected "}"'
                ))

            res.registerAdvancement()
            self.advance()

            return res.success(ForNode(varName, startValue, endValue, stepValue, body, True))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(varName, startValue, endValue, stepValue, body, False))

    def whileExpr(self):
        res = ParseResult()

        if not self.currentTok.matches(TT_KEYWORD, 'while'):
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                f"Expected 'while'"
            ))

        res.registerAdvancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.currentTok.matches(TT_KEYWORD, '{'):
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                "Expected '{'"
            ))

        res.registerAdvancement()
        self.advance()
        if self.currentTok.type == TT_NEWLINE:
            res.registerAdvancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.currentTok.matches(TT_KEYWORD, '}'):
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    'Expected "}"'
                ))

            res.registerAdvancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))
        body = res.register(self.statement())
        if res.erro: return res

        return res.success(WhileNode(condition, body, False))

    def funcDef(self):
        res = ParseResult()

        if not self.currentTok.matches(TT_KEYWORD, 'fnc'):
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                f"Expected 'fnc'"
            ))

        res.registerAdvancement()
        self.advance()

        if self.currentTok.type == TT_IDENTIFIER:
            varNameTok = self.currentTok
            res.registerAdvancement()
            self.advance()
            if self.currentTok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    f"Expected '('"
                ))
        else:
            varNameTok = None
            if self.currentTok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    f"Expected identifier or '('"
                ))

        res.registerAdvancement()
        self.advance()
        argNameToks = []

        if self.currentTok.type == TT_IDENTIFIER:
            argNameToks.append(self.currentTok)
            res.registerAdvancement()
            self.advance()

            while self.currentTok.type == TT_COMMA:
                res.registerAdvancement()
                self.advance()

                if self.currentTok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.currentTok.posStart, self.currentTok.posEnd,
                        f"Expected identifier"
                    ))

                argNameToks.append(self.currentTok)
                res.registerAdvancement()
                self.advance()

            if self.currentTok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.currentTok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.currentTok.posStart, self.currentTok.posEnd,
                    f"Expected identifier or ')'"
                ))

        res.registerAdvancement()
        self.advance()

        if self.currentTok.type == TT_ARROW:
            res.registerAdvancement()
            self.advance()
            if self.currentTok.type == TT_NEWLINE:
                res.registerAdvancement()
                self.advance()
            body = res.register(self.expr())
            if res.error: return res

            return res.success(FuncDefNode(
                varNameTok,
                argNameToks,
                body, True
            ))
        if self.currentTok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                'Expected "->"'
            ))
        res.registerAdvancement()
        self.advance()
        body = res.register(self.statements())
        if res.error: return res

        if not self.currentTok.matches(TT_KEYWORD, '}'):
            return res.failure(InvalidSyntaxError(
                self.currentTok.posStart, self.currentTok.posEnd,
                'Expected "}..."'
            ))
        res.registerAdvancement()
        self.advance()

        return res.success(FuncDefNode(
            varNameTok, argNameToks, body, False
        ))

    def binOp(self, funcA, ops, funcB=None):
        if funcB == None:
            funcB = funcA

        res = ParseResult()
        left = res.register(funcA())
        if res.error: return res

        while self.currentTok.type in ops or (self.currentTok.type, self.currentTok.value) in ops:
            opTok = self.currentTok
            res.registerAdvancement()
            self.advance()
            right = res.register(funcB())
            if res.error: return res
            left = BinOpNode(left, opTok, right)

        return res.success(left)

#######################################
# RUNTIME RESULT
#######################################

class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.funcReturnValue = None
        self.loopShouldContinue = False
        self.loopShouldBreak = False

    def register(self, res):
        self.error = res.error #shouldReturn()
        self.funcReturnValue = res.funcReturnValue
        self.loopShouldContinue = res.loopShouldContinue
        self.loopShouldBreak = res.loopShouldBreak
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def successReturn(self, value):
        self.reset()
        self.funcReturnValue = value
        return self

    def successContinue(self):
        self.reset()
        self.loopShouldContinue = True
        return self

    def successBreak(self):
        self.reset()
        self.loopShouldBreak = True
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def shouldReturn(self):
        return (
                self.error or
                self.funcReturnValue or
                self.loopShouldContinue or
                self.loopShouldBreak
        )

#######################################
# VALUES
#######################################

class Value:
    def __init__(self):
        self.setPos()
        self.setContext()

    def setPos(self, posStart=None, posEnd=None):
        self.posStart = posStart
        self.posEnd = posEnd
        return self

    def setContext(self, context=None):
        self.context = context
        return self

    def addedTo(self, other):
        return None, self.illegalOperation(other)

    def subbedBy(self, other):
        return None, self.illegalOperation(other)

    def multedBy(self, other):
        return None, self.illegalOperation(other)

    def divedBy(self, other):
        return None, self.illegalOperation(other)

    def powedBy(self, other):
        return None, self.illegalOperation(other)

    def getComparisonEq(self, other):
        return None, self.illegalOperation(other)

    def getComparisonNe(self, other):
        return None, self.illegalOperation(other)

    def getComparisonLt(self, other):
        return None, self.illegalOperation(other)

    def getComparisonGt(self, other):
        return None, self.illegalOperation(other)

    def getComparisonLte(self, other):
        return None, self.illegalOperation(other)

    def getComparisonGte(self, other):
        return None, self.illegalOperation(other)

    def andedBy(self, other):
        return None, self.illegalOperation(other)

    def oredBy(self, other):
        return None, self.illegalOperation(other)

    def notted(self):
        return None, self.illegalOperation() #other

    def execute(self, args):
        return RTResult().failure(self.illegalOperation())

    def copy(self):
        raise Exception('No copy method defined')

    def isTrue(self):
        return False

    def illegalOperation(self, other=None):
        if not other: other = self
        return RTError(
            self.posStart, other.posEnd,
            'Illegal operation',
            self.context
        )

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def addedTo(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def subbedBy(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def multedBy(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def divedBy(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.posStart, other.posEnd,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def powedBy(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def getComparisonEq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def getComparisonNe(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def getComparisonLt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def getComparisonGt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def getComparisonLte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def getComparisonGte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def andedBy(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def oredBy(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def notted(self):
        return Number(1 if self.value == 0 else 0).setContext(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.setPos(self.posStart, self.posEnd)
        copy.setContext(self.context)
        return copy

    def isTrue(self):
        return self.value != 0

    def __repr__(self):
        if self == Number.false:
            return str('false')
        elif self == Number.true:
            return str('true')
        elif self == Number.null:
            return str('null')
        else:
            return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def addedTo(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).setContext(self.context), None
        else:
            None, Value.illegalOperation(self, other)

    def multedBy(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).setContext(self.context), None
        else:
            None, Value.illegalOperation(self, other)

    def subbedBy(self, other):
        if isinstance(other, Number):
            try:
                element = self.value[other.value]
                self.value.replace(element, '')
                return String(self.value), None
            except:
                return None, RTError(
                    other.posStart, other.posEnd,
                    'Index out of range',
                    self.context
                )
        else:
            None, Value.illegalOperation(self, other)

    def divedBy(self, other):
        if isinstance(other, Number):
            try:
                return String(self.value[other.value]), None
            except:
                return None, RTError(
                    other.posStart, other.posEnd,
                    'Index out of range', self.context
                )
        else:
            None, Value.illegalOperation(self, other)

    def getComparisonEq(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def getComparisonNe(self, other):
        if isinstance(other, String):
            return Number(int(self.value != other.value)).setContext(self.context), None
        else:
            return None, Value.illegalOperation(self, other)

    def isTrue(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.setPos(self.posStart, self.posEnd)
        copy.setContext(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        if self.value != 'Process finalized with exit code 0' and self.value != '':
            return f'"{self.value}"'
        else:
            return f'{self.value}'

String.exitNull = String('Process finalized with exit code 0')
String.exitNone = String('')

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def addedTo(self, other):
        # newList = self.copy()
        self.elements.append(other)
        return self, None

    def multedBy(self, other):
        if isinstance(other, Number):
            newList = self.copy()
            newList.elements.extend(other.elements)
            return newList, None
        else:
            None, Value.illegalOperation(self, other)

    def subbedBy(self, other):
        if isinstance(other, Number):
            try:
                self.elements.pop(other.value)
                return self, None
            except:
                return None, RTError(
                    other.posStart, other.posEnd,
                    'Index out of range',
                    self.context
                )
        else:
            None, Value.illegalOperation(self, other)

    def divedBy(self, other):
        if isinstance(other, Number):
            try:
                ret = self.elements[other.value]
                if isinstance(ret, str):
                    return String(ret), None
                else:
                    return ret, None
            except:
                return None, RTError(
                    other.posStart, other.posEnd,
                    'Index out of range', self.context
                )

        else:
            None, Value.illegalOperation(self, other)

    def __str__(self):
        return str(self.elements)

    def __repr__(self):
        return str(self.elements)

    def copy(self):
        copy = List(self.elements)
        copy.setPos(self.posStart, self.posEnd)
        copy.setContext(self.context)
        return copy

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generateNewContext(self):
        newContext = Context(self.name, self.context, self.posStart)
        newContext.symbolTable = SymbolTable(newContext.parent.symbolTable)
        return newContext

    def checkArgs(self, argNames, args):
        res = RTResult()
        if len(args) > len(argNames):
            return res.failure(RTError(
                self.posStart, self.posEnd,
                f"{len(args) - len(argNames)} too many args passed into '{self.name}'",
                self.context
            ))

        if len(args) < len(argNames):
            return res.failure(RTError(
                self.posStart, self.posEnd,
                f"{len(argNames) - len(args)} too few args passed into '{self.name}'",
                self.context
            ))
        return res.success(None)

    def populateArgs(self, argNames, args, execCtx):
        for i in range(len(args)):
            argName = argNames[i]
            argValue = args[i]
            argValue.setContext(execCtx)
            execCtx.symbolTable.set(argName, argValue)

    def checkAndPopulateArg(self, argNames, args, execCtx):
        res = RTResult()
        res.register(self.checkArgs(argNames, args))
        if res.shouldReturn(): return res
        self.populateArgs(argNames, args, execCtx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, bodyNode, argNode, shouldAutoReturn):
        super().__init__(name)
        self.bodyNode = bodyNode
        self.argNames = argNode
        self.shouldAutoReturn = shouldAutoReturn

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        execCtx = self.generateNewContext()

        res.register(self.checkAndPopulateArg(self.argNames, args, execCtx))
        if res.shouldReturn(): return res

        value = res.register(interpreter.visit(self.bodyNode, execCtx))
        if res.shouldReturn() and res.funcReturnValue == None: return res

        returnValue = (value if self.shouldAutoReturn else None) or res.funcReturnValue or String.exitNull  #Number.null
        return res.success(returnValue)

    def copy(self):
        copy = Function(self.name, self.bodyNode, self.argNames, self.shouldAutoReturn)
        copy.setContext(self.context)
        copy.setPos(self.posStart, self.posEnd)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        execCtx = self.generateNewContext()

        methodName = f'execute{self.name}'
        method = getattr(self, methodName, self.noVisitMethod)

        res.register(self.checkAndPopulateArg(method.argNames, args, execCtx))
        if res.shouldReturn(): return res

        returnValue = res.register(method(execCtx))
        if res.shouldReturn(): return res

        return res.success(returnValue)

    def noVisitMethod(self, node, context):
        raise Exception(f'No execute{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.setContext(self.context)
        copy.setPos(self.posStart, self.posEnd)
        return copy

    def __repr__(self):
        return f'<builtIn function {self.name}>'

    def executeoutput(self, execCtx):
        print(repr(execCtx.symbolTable.get('value')))
        return RTResult().success(value=String.exitNull) #Number.null
    executeoutput.argNames = ['value']  # output()

    def executeoutreturn(self, execCtx):
        return RTResult.success(String(str(execCtx.symbolTable.get('value'))))
    executeoutreturn.argNames = ['value']  # return

    def executeinput(self, execCtx):
        msg = execCtx.symbolTable.get('message')
        if not isinstance(msg, String):
            return RTResult.failure(RTError(
                self.posStart, self.posEnd,
                f'Argument must be string',
                execCtx
            ))

        text = input(msg)
        return RTResult().success(String(text))
    executeinput.argNames = ['message']  # input()

    def executeintput(self, execCtx):
        msg = execCtx.symbolTable.get('message')
        if not isinstance(msg, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                f'Argument must be string',
                execCtx
            ))

        text = input(msg)
        try:
            number = int(text)
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                f'Input must be int',
                execCtx
            ))
        else:
            return RTResult().success(Number(number))
    executeintput.argNames = ['message']  # intput()

    def executefloatput(self, execCtx):
        msg = execCtx.symbolTable.get('message')
        if not isinstance(msg, String):
            return RTResult.failure(RTError(
                self.posStart, self.posEnd,
                f'Argument must be string',
                execCtx
            ))
        text = input(msg)
        try:
            number = float(text)
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                f'Input must be float',
                execCtx
            ))
        return RTResult().success(Number(number))
    executefloatput.argNames = ['message']  # floatput()

    def executeint(self, execCtx):
        element = execCtx.symbolTable.get('value')
        try:
            intElement = int(element.value)
        except ValueError:
            return RTResult.failure(RTError(
                self.posStart, self.posEnd,
                f'Cannot convert "{element}" to an int',
                execCtx
            ))
        else:
            return RTResult().success(Number(intElement))
    executeint.argNames = ['value']  # i()

    def executefloat(self, execCtx):
        element = execCtx.symbolTable.get('value')
        try:
            intElement = float(element.value)
        except ValueError:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                f'Cannot convert "{element}" to an float',
                execCtx
            ))
        else:
            return RTResult().success(Number(intElement))
    executefloat.argNames = ['value']  # f()

    def executestr(self, execCtx):
        element = execCtx.symbolTable.get('value')
        try:
            strElement = str(element.value)
        except ValueError:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                f'Cannot convert "{element}" to an string',
                execCtx
            ))
        else:
            return RTResult().success(Number(strElement))
    executestr.argNames = ['value']  # s()

    def executeclear(self, execCtx):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(String.exitNone) #Number.null
    executeclear.argNames = []  # clear

    def executeisInt(self, execCtx):
        isNumber = isinstance(execCtx.symbolTable.get('value'), Number)
        result = Number.false
        if isNumber:
            num = execCtx.symbolTable.get('value')
            result = Number.true if float(num.value) / int(num.value) == 1 else Number.false
        return RTResult().success(result)
    executeisInt.argNames = ['value']  # isInt()

    def executeisFloat(self, execCtx):
        isNumber = isinstance(execCtx.symbolTable.get('value'), Number)
        result = Number.false
        if isNumber:
            num = execCtx.symbolTable.get('value')
            result = Number.false if float(num.value) / int(num.value) == 1 else Number.true
        return RTResult().success(result)
    executeisFloat.argNames = ['value']  # isFloat()

    def executeisString(self, execCtx):
        isString = isinstance(execCtx.symbolTable.get('value'), Number)
        return RTResult().success(Number.true if isString else Number.false)
    executeisString.argNames = ['value']  # isString()

    def executeisList(self, execCtx):
        isList = isinstance(execCtx.symbolTable.get('value'), List)
        return RTResult().success(Number.true if isList else Number.false)
    executeisList.argNames = ['value']  # isList()

    def executeappend(self, execCtx):
        list_ = execCtx.symbolTable.get('list')
        value = execCtx.symbolTable.get('value')

        if isinstance(list_, List):
            try:
                list_.elements.append(value.value)
            except:
                list_.elements.append(List(value.elements))
            return RTResult().success(list_)  # Number.null
        elif isinstance(list_, String):
            if not isinstance(value, String):
                return RTResult().failure(RTError(
                    self.posStart, self.posEnd,
                    "Second argument must be string, when appending to a string",
                    execCtx
                ))
            list_.value += value.value
            return RTResult().success(list_)
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be list or string",
                execCtx
            ))
    executeappend.argNames = ['list', 'value']  # append()

    def executeremove(self, execCtx):
        list_ = execCtx.symbolTable.get("list")
        index = execCtx.symbolTable.get("index")

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Second argument must be int",
                execCtx
            ))
        if isinstance(list_, List):
            try:
                list_.elements.pop(index.value)
            except:
                return RTResult().failure(RTError(
                    self.posStart, self.posStart,
                    'Index out of range',
                    execCtx
                ))
            return RTResult().success(List(list_))
        elif isinstance(list_, String):
            try:
                element = list_.value[index.value]
            except:
                return RTResult().failure(RTError(
                    self.posStart, self.posStart,
                    'Index out of range',
                    execCtx
                ))
            else:
                i = 0
                returnString = ''
                while(i<len(list_.value)):
                    if i != index.value:
                        returnString += list_.value[i]
                    i += 1
                return RTResult().success(String(returnString))
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be list or string",
                execCtx
            ))
    executeremove.argNames = ['list', 'index']  # remove()

    def executereplace(self, execCtx):
        string_ = execCtx.symbolTable.get('string')
        oldValue = execCtx.symbolTable.get('oldValue')
        newValue = execCtx.symbolTable.get('newValue')
        finalOldValue = None
        finalNewValue = None

        if isinstance(oldValue, String):
            finalOldValue = oldValue
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Second argument must be string",
                execCtx
            ))

        if isinstance(newValue, String):
            finalNewValue = newValue
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Third argument must be string",
                execCtx
            ))

        if isinstance(string_, String):
            if isinstance(finalOldValue, String) and isinstance(finalNewValue, String):
                try:
                    string_.value = string_.value.replace(finalOldValue.value, finalNewValue.value)
                    print(string_.value)
                except:
                    return RTResult().failure(RTError(
                        self.posStart, self.posEnd,
                        f'"{oldValue}" not in string',
                        execCtx
                    ))
                else:
                    return RTResult().success(string_)
            else:
                return RTResult().failure(RTError(
                    self.posStart, self.posEnd,
                    f'replace(String, oldValue, newValue) cannot accept a non-string newValue and a non-string oldValue',
                    execCtx
                ))
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                f'First argument must be string',
                execCtx
            ))
    executereplace.argNames = ['string', 'oldValue', 'newValue']  # replace()

    def executeextend(self, execCtx):
        listA = execCtx.symbolTable.get("firstList")
        listB = execCtx.symbolTable.get('secondList')

        if not isinstance(listA, List):
            return RTResult.failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be list or string",
                execCtx
            ))

        if not isinstance(listB, List):
            return RTResult.failure(RTError(
                self.posStart, self.posEnd,
                "Second argument must be list or string",
                execCtx
            ))

        listA.elements.extend(listB.elements)
        return RTResult().success(String.exitNull) #Number.null
    executeextend.argNames = ['firstList', 'secondList'] # extend()

    def executelength(self, execCtx):
        list_ = execCtx.symbolTable.get('list')
        if isinstance(list_, List):
            return RTResult().success(Number(len(list_.elements)))
        elif isinstance(list_, String):
            return RTResult().success(Number(len(list_.value)))
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument must be list or string",
                execCtx
            ))
    executelength.argNames = ['list'] # length()

    def executeindexOf(self, execCtx):
        list_ = execCtx.symbolTable.get('list')
        element = execCtx.symbolTable.get('element')

        if isinstance(list_, List):
            try:
                index = list_.elements.index(element.value)
            except:
                return RTResult().failure(RTError(
                    self.posStart, self.posEnd,
                    "Element not in list",
                    execCtx
                ))
            else:
                return RTResult().success(Number(index))
        elif isinstance(list_, String):
            try:
                index = list_.value.index(element.value)
            except:
                return RTResult().failure(RTError(
                    self.posStart, self.posEnd,
                    "Element not in string",
                    execCtx
                ))
            else:
                return RTResult().success(Number(index))
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be list or string",
                execCtx
            ))
    executeindexOf.argNames = ['list', 'element'] # indexOf

    def executeisIncluded(self, execCtx):
        list_ = execCtx.symbolTable.get('list')
        element_ = execCtx.symbolTable.get('element')

        if isinstance(list_, List):
            try:
                list_.elements.index(element_.value)
            except:
                return RTResult().success(Number.false)
            else:
                return RTResult().success(Number.true)
        elif isinstance(list_, String):
            try:
                list_.value.index(element_.value)
            except:
                return RTResult().success(Number.false)
            else:
                return RTResult().success(Number.true)
    executeisIncluded.argNames = ['list', 'element']

    def executeterminal(self, execCtx):
        command = execCtx.symbolTable.get('command')
        if not isinstance(command, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument must be string",
                execCtx
            ))
        returnValue = os.system(command.value)
        return RTResult().success(String(returnValue) if returnValue != 0 else String.exitNull)
    executeterminal.argNames = ['command'] # terminal()

    def executeosName(self, execCtx):
        returnValue = os.name
        return RTResult().success(String(returnValue))
    executeosName.argNames = [] # osName()

    def executeappleScript(self, execCtx):
        command = execCtx.symbolTable.get('command')
        if not isinstance(command, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument must be string",
                execCtx
            ))
        returnValue = osascript.osascript(command.value)
        return RTResult().success(String(returnValue))
    executeappleScript.argNames = ['command'] # appleScript()

    def executeopenBrowser(self, execCtx):
        url = execCtx.symbolTable.get('url')
        if not isinstance(url, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument must be string",
                execCtx
            ))
        try:
            url.value.index('http')
        except:
            webbrowser.open(f'https://www.google.com/search?q={url.value}&oq={url.value}')
        else:
            webbrowser.open(url.value)
        return RTResult().success(String.exitNull) # Number.null
    executeopenBrowser.argNames = ['url'] # openBrowser()

    def executerandomChoice(self, execCtx):
        list = execCtx.symbolTable.get('sequence')
        if not isinstance(list, List):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument must be list",
                execCtx
            ))
        try:
            choice = random.choice(list.elements)
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument must be list",
                execCtx
            ))
        else:
            try:
                int(choice)
            except:
                return RTResult().success(String(choice))
            else:
                return RTResult().success(Number(choice))
    executerandomChoice.argNames = ['sequence'] # randomChoice()

    def executerandomInt(self, execCtx):
        rangeStart = execCtx.symbolTable.get('rangeStart')
        rangeEnd = execCtx.symbolTable.get('rangeEnd')

        if not isinstance(rangeStart, Number):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be int",
                execCtx
            ))
        if not isinstance(rangeEnd, Number):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Second argument must be int",
                execCtx
            ))
        if(True if float(rangeStart.value) / int(rangeStart.value) == 1 else False) and (True if float(rangeEnd.value) / int(rangeEnd.value) == 1 else False):
            result = random.randint(rangeStart.value, rangeEnd.value)
            return RTResult().success(Number(result))
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Both arguments must be int",
                execCtx
            ))
    executerandomInt.argNames = ['rangeStart', 'rangeEnd'] # randomInt()

    def executesubString(self, execCtx):
        string_ = execCtx.symbolTable.get('string')
        startIndex_ = execCtx.symbolTable.get('startIndex')
        endIndex_ = execCtx.symbolTable.get('endIndex')

        if not isinstance(startIndex_, Number):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Second argument must be int",
                execCtx
            ))
        if not isinstance(endIndex_, Number):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Third argument must be int",
                execCtx
            ))
        if isinstance(string_, String):
            subString = string_.value[startIndex_.value:endIndex_.value]
            return RTResult().success(String(subString))
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be string",
                execCtx
            ))
    executesubString.argNames = ['string', 'startIndex', 'endIndex'] # subString()

    def executesubList(self, execCtx):
        list_ = execCtx.symbolTable.get('list')
        startIndex_ = execCtx.symbolTable.get('startIndex')
        endIndex_ = execCtx.symbolTable.get('endIndex')

        if not isinstance(startIndex_, Number):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Second argument must be int",
                execCtx
            ))
        if not isinstance(endIndex_, Number):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Third argument must be int",
                execCtx
            ))
        if isinstance(list_, list):
            subList = list_.elements[startIndex_.value:endIndex_.value]
            return RTResult().success(List(subList))
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be list",
                execCtx
            ))
    executesubList.argNames = ['list', 'startIndex', 'endIndex'] #subList()

    def executereadFile(self, execCtx):
        fileName = execCtx.symbolTable.get('path')

        if not isinstance(fileName, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument (file path) must be string",
                execCtx
            ))
        try:
            with open(fileName.value, 'r') as fn:
                returnValue = fn.read()
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File not found",
                execCtx
            ))
        else:
            return RTResult().success(String(returnValue))
    executereadFile.argNames = ['path'] # readFile()

    def executewriteFile(self, execCtx):
        fileName = execCtx.symbolTable.get('path')
        content = execCtx.symbolTable.get('content')

        if not isinstance(fileName, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument (file path) must be string",
                execCtx
            ))
        try:
            with open(fileName.value, 'w') as fn:
                fn.write(content.value)
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File not found",
                execCtx
            ))
        else:
            return RTResult().success(String.exitNull)
    executewriteFile.argNames = ['path', 'content'] # writeFile()

    def executeclearFile(self, execCtx):
        fileName = execCtx.symbolTable.get('path')

        if not isinstance(fileName, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument (file path) must be string",
                execCtx
            ))
        try:
            with open(fileName.value, 'w') as fn:
                fn.write('')
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File not found",
                execCtx
            ))
        else:
            return RTResult().success(String.exitNull)
    executeclearFile.argNames = ['path'] # clearFile()

    def executeaddToFile(self, execCtx):
        fileName = execCtx.symbolTable.get('path')
        content = execCtx.symbolTable.get('content')

        if not isinstance(fileName, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument (file path) must be string",
                execCtx
            ))
        try:
            with open(fileName.value, 'a') as fn:
                fn.write(content.value)
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File not found",
                execCtx
            ))
        else:
            return RTResult().success(String.exitNull)
    executeaddToFile.argNames = ['path', 'content'] # addToFile()

    def executereadBytes(self, execCtx):
        path = execCtx.symbolTable.get('path')
        if not isinstance(path, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument (file path) must be string",
                execCtx
            ))
        try:
            with open(path.value, 'rb') as fn:
                returnValue = fn.read()
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File not found",
                execCtx
            ))
        else:
            return RTResult().success(String(returnValue))
    executereadBytes.argNames = ['path'] # readBytes()

    def executewriteBytes(self, execCtx):
        path = execCtx.symbolTable.get('path')
        content = execCtx.symbolTable.get('content')
        if not isinstance(path, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument (file path) must be string",
                execCtx
            ))
        try:
            with open(path.value, 'wb') as fn:
                fn.write(content.value)
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File not found",
                execCtx
            ))
        else:
            return RTResult().success(String.exitNull)
    executewriteBytes.argNames = ['path', 'content'] # writeBytes()

    def executekvkread(self, execCtx):
        filePath_ = execCtx.symbolTable.get('filePath')
        if not isinstance(filePath_, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument (file path) must be string",
                execCtx
            ))
        if filePath_.value[len(filePath_.value)-4:len(filePath_.value)] != '.kvk':
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File extension must be \".kvk\"",
                execCtx
            ))

        def __getClass__(content, pos):
            tmpList = []
            pos += 5
            while content[pos] == ' ':
                pos += 1
            if content[pos] == '"':
                pos += 1
                className = ''
                while content[pos] != '"':
                    className += content[pos]
                    pos += 1
                pos += 2
                attrList = []
                if content[pos:pos + 3] == '::>':
                    pos += 3
                    while content[pos:pos + 3] != '#>' and content[pos:pos + 5] != 'class':
                        if content[pos] == ' ' or content[pos] == '\t' or content[pos] == '\n':
                            pos += 1
                        elif content[pos] == '(':
                            attr, pos = __attr__(content, pos)
                            attrList.append(attr)
                    tmpList.append(className)
                    tmpList.append(attrList)
                    return tmpList, pos
                else:
                    return RTResult().failure(RTError(
                        self.posStart, self.posEnd,
                        'Expected "::>" after class name',
                        execCtx
                    ))

            else:
                return RTResult().failure(RTError(
                    self.posStart, self.posEnd,
                    'Expected \'\"\' after class declaration'
                ))

        def __attr__(content, pos):
            attrList = []
            pos += 1
            attrName = ''
            while content[pos] == ' ' or content[pos] == '\t' or content[pos] == '\n':
                pos += 1
            while content[pos] != ')':
                attrName += content[pos]
                pos += 1
            pos += 1
            while content[pos] == ' ' or content[pos] == '\t' or content[pos] == '\n':
                pos += 1
            if content[pos:pos + 2] == '->':
                pos += 2
                while content[pos] == ' ':
                    pos += 1
                if content[pos] == '"':
                    attr = ''
                    pos += 1
                    while content[pos] != '"':
                        attr += content[pos]
                        pos += 1
                    attrList.append(attrName)
                    attrList.append(attr)
                    pos += 1
                    return attrList, pos
                else:
                    return RTResult().failure(RTError(
                        self.posStart, self.posEnd,
                        'Expected \'\"\' after ->',
                        execCtx))
            else:
                return RTResult().failure(RTError(
                    self.posStart, self.posEnd,
                    'Expected "->" after attribute name',
                    execCtx))

        file = open(filePath_.value, 'r')
        content = file.read()
        pos = 0
        res = []
        if content[pos:pos + 2] == '<#':
            pos += 2
            while pos < len(content):
                if content[pos] == ' ' or content[pos] == '\t' or content[pos] == '\n':
                    pos += 1
                if content[pos:pos + 5] == 'class':
                    point, pos = __getClass__(content, pos)
                    res.append(point)
                if content[pos:len(content)] == '#>':
                    break
            return RTResult().success(List(res))
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                'KvK file must begin with \"<#\"',
                execCtx
            ))
    executekvkread.argNames = ['filePath']

    def executekvkgetclass(self, execCtx):
        filePath_ = execCtx.symbolTable.get('filePath')
        className_ = execCtx.symbolTable.get('className')

    def executekvkwrite(self, execCtx):
        filePath_ = execCtx.symbolTable.get('filePath')
        content_ = execCtx.symbolTable.get('content')

        if not isinstance(filePath_, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be string",
                execCtx
            ))
        if not isinstance(content_, List):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Second argument must be list",
                execCtx
            ))
        if filePath_.value[len(filePath_.value)-4:len(filePath_.value)] != '.kvk':
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File extension must be \".kvk\"",
                execCtx
            ))

        toWrite = '<#\n'
        for classCont in content_.elements:
            className = classCont.elements.pop(0)
            toWrite += f'    class \"{className}\" ::>\n'
            for attrCont in classCont.elements:
                for attr in attrCont.elements:
                    attrName = attr.elements[0]
                    attrContent = attr.elements[1]
                    toWrite += f'        ({attrName}) -> \"{attrContent}\"\n'
        toWrite += '#>'
        try:
            with open(filePath_.value, 'w') as fp:
                fp.write(toWrite)
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File not found",
                execCtx
            ))
        else:
            return RTResult().success(String.exitNull)
    executekvkwrite.argNames = ['filePath', 'content']

    def executekvkaddattr(self, execCtx):
        filePath_ = execCtx.symbolTable.get('filePath')
        className_ = execCtx.symbolTable.get('className')
        attrName_ = execCtx.symbolTable.get('attrName')
        attrContent_ = execCtx.symbolTable.get('attrContent')

        if not isinstance(filePath_, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be string",
                execCtx
            ))
        if not isinstance(className_, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Second argument must be string",
                execCtx
            ))
        if not isinstance(attrName_, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Third argument must be string",
                execCtx
            ))
        if not isinstance(attrContent_, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Fourth argument must be string",
                execCtx
            ))
        if filePath_.value[len(filePath_.value)-4:len(filePath_.value)] != '.kvk':
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File extension must be \".kvk\"",
                execCtx
            ))

        with open(filePath_.value, 'r') as fp:
            content = fp.read()

        try:
            index = content.index(f'class \"{className_.value}\" ::>')
        except:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                'Class not found',
                execCtx
            ))
        else:
            endIndex = (index + (len(f'class "{className_.value}" ::>'))) - 1
            content = content[0:endIndex+1] + f'\n        ({attrName_.value}) -> "{attrContent_.value}"\n' + content[endIndex+2:len(content)]
            with open(filePath_.value, 'w') as file:
                file.write(content)
            return RTResult().success(String.exitNull)
    executekvkaddattr.argNames = ['filePath', 'className', 'attrName', 'attrContent']

    def executekvkaddclass(self, execCtx):
        filePath_ = execCtx.symbolTable.get('filePath')
        classname_ = execCtx.symbolTable.get('className')

        if not isinstance(filePath_, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "First argument must be string",
                execCtx
            ))
        if not isinstance(classname_, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Second argument must be string",
                execCtx
            ))
        if filePath_.value[len(filePath_.value)-4:len(filePath_.value)] != '.kvk':
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "File extension must be \".kvk\"",
                execCtx
            ))

        with open(filePath_.value, 'r') as fp:
            content = fp.read()

        content = content[0:len(content)-2] + f'    class \"{classname_.value}\" ::>\n#>'
        with open(filePath_.value, 'w') as file:
            file.write(content)
        return RTResult().success(String.exitNull)
    executekvkaddclass.argNames = ['filePath', 'className']

    def executeImport(self, execCtx):
        fileName = execCtx.symbolTable.get('module')

        if not isinstance(fileName, String):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument must be string",
                execCtx
            ))
        if fileName.value[-4:len(fileName.value)] == '.crg':
            try:
                with open(fileName.value, 'r') as mn:
                    moduleContent = mn.read()
            except:
                return RTResult().failure(String(f'ImportError: file "{fileName}" not found'))
            else:
                _, error = run(f'{fileName.value}', moduleContent)
                if error:
                    return RTResult().failure(RTError(
                        self.posStart, self.posEnd,
                        f'Failed loading module \"{fileName.value}\"\n' + error.asString(),
                        execCtx
                    ))
                return RTResult().success(String.exitNull)
        else:
            try:
                with open((f'{fileName.value}.crg'), 'r') as mn:
                    moduleContent = mn.read()
            except:
                #return RTResult().failure(String(f'ImportError: file "{fileName}" not found'))
                return RTResult().failure(RTError(
                    self.posStart, self.posEnd,
                    f'ImportError: file "{fileName.value}" not found',
                    execCtx
                ))
            else:
                _, error = run(f'{fileName.value}', moduleContent)
                if error:
                    return RTResult().failure(RTError(
                        self.posStart, self.posEnd,
                        f'Failed loading module \"{fileName.value}.crg\"\n' + error.asString(),
                        execCtx
                    ))
                return RTResult().success(String.exitNull)
    executeImport.argNames = ['module'] # import()\

    def executewait(self, execCtx):
        seconds = execCtx.symbolTable.get('seconds')

        if not isinstance(seconds, Number):
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                "Argument must be int or float",
                execCtx
            ))
        time.sleep(seconds.value)
        return RTResult().success(String.exitNull)
    executewait.argNames = ['seconds'] #wait()

    def executerun(self, execCtx):
        fn = execCtx.symbolTable.get('fn')

        if not isinstance(fn, String):
            return RTResult().failure(
                RTError(
                    self.posStart, self.poEnd,
                    "Argument must be string",
                    execCtx
                ))

        fn = fn.value
        if fn[-4: len(fn)] == '.crg':
            try:
                with open(fn, 'r') as f:
                    script = f.read()
            except Exception as e:
                return RTResult().failure(RTError(
                    self.posStart, self.posEnd,
                    f'Failed to load script \"{fn}\"\n' + str(e),
                    execCtx
                ))

            _, error = run(fn, script)
            if error:
                return RTResult().failure(RTError(
                    self.posStart, self.posEnd,
                    f'Failed to finish executing script \"{fn}\"\n' + error.asString(),
                    execCtx
                ))
            return RTResult().success(String.exitNull) # Number.null
        else:
            return RTResult().failure(RTError(
                self.posStart, self.posEnd,
                f'File type not allowed \"{fn}\"\n Only ".crg" files are allowed',
                execCtx
            ))
    executerun.argNames = ['fn'] # run()

BuiltInFunction.output          = BuiltInFunction('output')
BuiltInFunction.outreturn       = BuiltInFunction('outreturn')
BuiltInFunction.input           = BuiltInFunction('input')
BuiltInFunction.intput          = BuiltInFunction('intput')
BuiltInFunction.floatput         = BuiltInFunction('floatput')
BuiltInFunction.int             = BuiltInFunction('int')
BuiltInFunction.float            = BuiltInFunction('float')
BuiltInFunction.str             = BuiltInFunction('str')
BuiltInFunction.clear           = BuiltInFunction('clear')
BuiltInFunction.isInt           = BuiltInFunction('isInt')
BuiltInFunction.isFloat         = BuiltInFunction('isFloat')
BuiltInFunction.isString        = BuiltInFunction('isString')
BuiltInFunction.isList          = BuiltInFunction('isList')
BuiltInFunction.append          = BuiltInFunction('append')
BuiltInFunction.remove          = BuiltInFunction('remove')
BuiltInFunction.replace         = BuiltInFunction('replace')
BuiltInFunction.extend          = BuiltInFunction('extend')
BuiltInFunction.length          = BuiltInFunction('length')
BuiltInFunction.indexOf         = BuiltInFunction('indexOf')
BuiltInFunction.terminal        = BuiltInFunction('terminal')
BuiltInFunction.osName          = BuiltInFunction('osName')
BuiltInFunction.appleScript     = BuiltInFunction('appleScript')
BuiltInFunction.openBrowser     = BuiltInFunction('openBrowser')
BuiltInFunction.randomChoice    = BuiltInFunction('randomChoice')
BuiltInFunction.randomInt       = BuiltInFunction('randomInt')
BuiltInFunction.Import          = BuiltInFunction('Import')
BuiltInFunction.readFile        = BuiltInFunction('readFile')
BuiltInFunction.writeFile       = BuiltInFunction('writeFile')
BuiltInFunction.clearFile       = BuiltInFunction('clearFile')
BuiltInFunction.readBytes       = BuiltInFunction('readBytes')
BuiltInFunction.writeBytes      = BuiltInFunction('writeBytes')
BuiltInFunction.addToFile       = BuiltInFunction('addToFile')
BuiltInFunction.wait            = BuiltInFunction('wait')
BuiltInFunction.subString       = BuiltInFunction('subString')
BuiltInFunction.subList         = BuiltInFunction('subList')
BuiltInFunction.kvkread         = BuiltInFunction('kvkread')
BuiltInFunction.kvkwrite        = BuiltInFunction('kvkwrite')
BuiltInFunction.kvkaddclass     = BuiltInFunction('kvkaddclass')
BuiltInFunction.kvkaddattr      = BuiltInFunction('kvkaddattr')
BuiltInFunction.run             = BuiltInFunction('run')

#######################################
# CONTEXT
#######################################

class Context:
    def __init__(self, displayName, parent=None, parentEntryPos=None):
        self.displayName = displayName
        self.parent = parent
        self.parentEntryPos = parentEntryPos
        self.symbolTable = None

#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

#######################################
# INTERPRETER
#######################################

class Interpreter:
    def visit(self, node, context):
        methodName = f'visit{type(node).__name__}'
        method = getattr(self, methodName, self.noVisitMethod)
        return method(node, context)

    def noVisitMethod(self, node, context):
        raise Exception(f'No visit{type(node).__name__} method defined')

    def visitNumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).setContext(context).setPos(node.posStart, node.posEnd)
        )

    def visitStringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).setContext(context).setPos(node.posStart, node.posEnd)
        )

    def visitListNode(self, node, context):
        res = RTResult()
        elements = []
        for elementNode in node.elementNodes:
            elements.append(res.register(self.visit(elementNode, context)))
            if res.shouldReturn(): return res

        return res.success(
            List(elements).setContext(context).setPos(node.posStart, node.posEnd)
        )

    def visitVarAccessNode(self, node, context):
        res = RTResult()
        varName = node.varNameTok.value
        value = context.symbolTable.get(varName)

        if not value:
            return res.failure(RTError(
                node.posStart, node.posEnd,
                f"'{varName}' is not defined",
                context
            ))

        value = value.copy().setPos(node.posStart, node.posEnd).setContext(context)
        return res.success(value)

    def visitVarAssignNode(self, node, context):
        res = RTResult()
        varName = node.varNameTok.value
        value = res.register(self.visit(node.valueNode, context))
        if res.shouldReturn(): return res

        context.symbolTable.set(varName, value)
        return res.success(value)

    def visitBinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.leftNode, context))
        if res.shouldReturn(): return res
        right = res.register(self.visit(node.rightNode, context))
        if res.shouldReturn(): return res

        if node.opTok.type == TT_PLUS:
            result, error = left.addedTo(right)
        elif node.opTok.type == TT_MINUS:
            result, error = left.subbedBy(right)
        elif node.opTok.type == TT_MUL:
            result, error = left.multedBy(right)
        elif node.opTok.type == TT_DIV:
            result, error = left.divedBy(right)
        elif node.opTok.type == TT_POW:
            result, error = left.powedBy(right)
        elif node.opTok.type == TT_EE:
            result, error = left.getComparisonEq(right)
        elif node.opTok.type == TT_NE:
            result, error = left.getComparisonNe(right)
        elif node.opTok.type == TT_LT:
            result, error = left.getComparisonLt(right)
        elif node.opTok.type == TT_GT:
            result, error = left.getComparisonGt(right)
        elif node.opTok.type == TT_LTE:
            result, error = left.getComparisonLte(right)
        elif node.opTok.type == TT_GTE:
            result, error = left.getComparisonGte(right)
        elif node.opTok.matches(TT_KEYWORD, 'and'):
            result, error = left.andedBy(right)
        elif node.opTok.matches(TT_KEYWORD, 'or'):
            result, error = left.oredBy(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.setPos(node.posStart, node.posEnd))

    def visitUnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.shouldReturn(): return res

        error = None

        if node.opTok.type == TT_MINUS:
            number, error = number.multedBy(Number(-1))
        elif node.opTok.matches(TT_KEYWORD, 'not'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.setPos(node.posStart, node.posEnd))

    def visitIfNode(self, node, context):
        res = RTResult()

        for condition, expr, shouldReturnNull in node.cases:
            conditionValue = res.register(self.visit(condition, context))
            if res.shouldReturn(): return res

            if conditionValue.isTrue():
                exprValue = res.register(self.visit(expr, context))
                if res.shouldReturn(): return res
                return res.success(String.exitNull if shouldReturnNull else exprValue) # Number.null

        if node.elseCase:
            expr, shouldReturnNull = node.elseCase
            elseValue = res.register(self.visit(expr, context))
            if res.shouldReturn(): return res
            return res.success(String.exitNull if shouldReturnNull else elseValue) # Number.null

        return res.success(String.exitNull) # Number.null

    def visitForNode(self, node, context):
        res = RTResult()
        elements = []

        startValue = res.register(self.visit(node.startValueNode, context))
        if res.shouldReturn(): return res

        endValue = res.register(self.visit(node.endValueNode, context))
        if res.shouldReturn(): return res

        if node.stepValueNode:
            stepValue = res.register(self.visit(node.stepValueNode, context))
            if res.shouldReturn(): return res
        else:
            stepValue = Number(1)

        i = startValue.value

        if stepValue.value >= 0:
            condition = lambda: i < endValue.value
        else:
            condition = lambda: i > endValue.value

        while condition():
            context.symbolTable.set(node.varNameTok.value, Number(i))
            i += stepValue.value

            value = (res.register(self.visit(node.bodyNode, context)))
            if res.shouldReturn() and res.loopShouldContinue == False and res.loopShouldBreak == False: return res

            if res.loopShouldContinue:
                continue

            if res.loopShouldBreak:
                break

            elements.append(value)

        return res.success(
            String.exitNull if node.shouldReturnNull else #Number.null
            List(elements).setContext(context).setPos(node.posStart, node.posEnd)
        )

    def visitWhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.conditionNode, context))
            if res.shouldReturn(): return res

            if not condition.isTrue(): break

            value = (res.register(self.visit(node.bodyNode, context)))
            if res.shouldReturn() and res.loopShouldContinue == False and res.loopShouldBreak == False: return res

            if res.loopShouldContinue:
                continue

            if res.loopShouldBreak:
                break

            elements.append(value)

        return res.success(
            String.exitNull if node.shouldReturnNull else # Number.null
            List(elements).setContext(context).setPos(node.posStart, node.posEnd)
        )

    def visitFuncDefNode(self, node, context):
        res = RTResult()

        funcName = node.varNameTok.value if node.varNameTok else None
        bodyNode = node.bodyNode
        argNames = [argName.value for argName in node.argNameToks]
        funcValue = Function(funcName, bodyNode, argNames, node.shouldAutoReturn).setContext(context).setPos(
            node.posStart,
            node.posEnd)

        if node.varNameTok:
            context.symbolTable.set(funcName, funcValue)

        return res.success(funcValue)

    def visitCallNode(self, node, context):
        res = RTResult()
        args = []

        valueToCall = res.register(self.visit(node.nodeToCall, context))
        if res.shouldReturn(): return res
        valueToCall = valueToCall.copy().setPos(node.posStart, node.posEnd)

        for argNode in node.argNodes:
            args.append(res.register(self.visit(argNode, context)))
            if res.shouldReturn(): return res

        returnValue = res.register(valueToCall.execute(args))
        if res.shouldReturn(): return res
        returnValue = returnValue.copy().setPos(node.posStart, node.posEnd).setContext(context)
        return res.success(returnValue)

    def visitReturnNode(self, node, context):
        res = RTResult()

        if node.nodeToReturn:
            value = res.register(self.visit(node.nodeToReturn, context))
            if res.shouldReturn(): return res
        else:
            value = String.exitNull #Number.null

        return res.successReturn(value)

    def visitContinueNode(self, node, context):
        return RTResult().successContinue()

    def visitBreakNode(self, node, context):
        return RTResult().successBreak()

#######################################
# RUN
#######################################

globalSymbolTable = SymbolTable()
globalSymbolTable.set("null",           Number.null)
globalSymbolTable.set("false",          Number.false)
globalSymbolTable.set("true",           Number.true)
globalSymbolTable.set('print',          BuiltInFunction.output)
globalSymbolTable.set('input',          BuiltInFunction.input)
globalSymbolTable.set('intput',         BuiltInFunction.intput)
globalSymbolTable.set('floatput',        BuiltInFunction.floatput)
globalSymbolTable.set('int',            BuiltInFunction.int)
globalSymbolTable.set('float',           BuiltInFunction.float)
globalSymbolTable.set('str',            BuiltInFunction.str)
globalSymbolTable.set('clear',          BuiltInFunction.clear)
globalSymbolTable.set('isInt',          BuiltInFunction.isInt)
globalSymbolTable.set('isFloat',        BuiltInFunction.isFloat)
globalSymbolTable.set('isString',       BuiltInFunction.isString)
globalSymbolTable.set('isList',         BuiltInFunction.isList)
globalSymbolTable.set('append',         BuiltInFunction.append)
globalSymbolTable.set('remove',         BuiltInFunction.remove)
globalSymbolTable.set('replace',        BuiltInFunction.replace)
globalSymbolTable.set('extend',         BuiltInFunction.extend)
globalSymbolTable.set('length',         BuiltInFunction.length)
globalSymbolTable.set('indexOf',        BuiltInFunction.indexOf)
globalSymbolTable.set('terminal',       BuiltInFunction.terminal)
globalSymbolTable.set('osName',         BuiltInFunction.osName)
globalSymbolTable.set('appleScript',    BuiltInFunction.appleScript)
globalSymbolTable.set('openBrowser',    BuiltInFunction.openBrowser)
globalSymbolTable.set('randomChoice',   BuiltInFunction.randomChoice)
globalSymbolTable.set('randomInt',      BuiltInFunction.randomInt)
globalSymbolTable.set('import',         BuiltInFunction.Import)
globalSymbolTable.set('readFile',       BuiltInFunction.readFile)
globalSymbolTable.set('writeFile',      BuiltInFunction.writeFile)
globalSymbolTable.set('clearFile',      BuiltInFunction.clearFile)
globalSymbolTable.set('addToFile',      BuiltInFunction.addToFile)
globalSymbolTable.set('readBytes',      BuiltInFunction.readBytes)
globalSymbolTable.set('writeBytes',     BuiltInFunction.writeBytes)
globalSymbolTable.set('wait',           BuiltInFunction.wait)
globalSymbolTable.set('subList',        BuiltInFunction.subList)
globalSymbolTable.set('subString',      BuiltInFunction.subString)
globalSymbolTable.set('kvkread',        BuiltInFunction.kvkread)
globalSymbolTable.set('kvkwrite',       BuiltInFunction.kvkwrite)
globalSymbolTable.set('kvkaddclass',    BuiltInFunction.kvkaddclass)
globalSymbolTable.set('kvkaddattr',     BuiltInFunction.kvkaddattr)
globalSymbolTable.set('run',            BuiltInFunction.run)

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.makeTokens()
    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context('<script>')
    context.symbolTable = globalSymbolTable
    result = interpreter.visit(ast.node, context)

    return result.value, result.error