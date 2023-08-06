from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='brain-fuck-interpreter-cmdl',
    version='1.1.1',
    author='Cargo',
    packages=['brainfuck'],
    install_requires=['click'],
    description='BrainFuck Interpreter',
    long_description=long_description,
    long_description_type='text/markdown',
    entry_points='''
    [console_scripts]
    brainfuck=brainfuck:run
    '''
)
