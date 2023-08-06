import cargo, click

@click.command()
@click.option('fileName')
def cargo(fileName):
    if fileName != None and fileName != '':
        result, error = cargo.run('script', 'run("' + fileName + '")')
        if error: print(error.asString())
        if result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
    else:
        while True:
            text = input('<-> ')
            if text.strip() == '': continue
            if text == 'exit':
                break

            result, error = cargo.run('script', text)
            if error: print(error.asString())
            if result:
                if len(result.elements) == 1:
                    print(repr(result.elements[0]))
                else:
                    print(repr(result))