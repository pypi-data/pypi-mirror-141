from setuptools import setup

setup(
    name='cargolang',
    author='Cargo',
    version='1.0.0',
    packages=['shell', 'cargo'],
    install_requires=['click', 'osascript', 'KvK'],
    entry_points='''
    [console_script]
    cargo=shell:cargo
    '''
)