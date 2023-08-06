# BrainFuck Interpreter

Install:

    $ pip install brain-fuck-interpreter-cmdl

Usage from terminal:

    $ brainfuck -f filePath
    $ brainfuck -f filePath -m true

Replace "filePath" with the path of the file you want to run.\
If you enter "-m true" the memory after execution will be printed.

Usage in python:

    import brainfuck
    brainfuck.interpreter(code='++++.>++++.>>>>++++[.-].')

It returns an array containing the printed values from BrainFuck.