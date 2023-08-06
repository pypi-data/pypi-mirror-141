from setuptools import setup

setup(
    name='cargolang',
    author='Cargo',
    version='1.1.1',
    packages=['shell', 'cargo'],
    install_requires=['click', 'osascript'],
    entry_points='''
    [console_script]
    cargo=shell:cargo
    '''
)