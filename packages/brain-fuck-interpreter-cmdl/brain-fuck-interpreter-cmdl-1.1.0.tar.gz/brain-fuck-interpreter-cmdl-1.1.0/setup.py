from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='brain-fuck-interpreter-cmdl',
    author='Cargo',
    version='1.1.0',
    long_description=long_description,
    long_description_type='text/markdown',
    description='Interpreter',
    packages=['brainfuck'],
    install_requires=['click'],
    entry_points='''
    [console_scripts]
    brainfuck=brainfuck:run
    '''
)