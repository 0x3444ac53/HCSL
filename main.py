import readline
from os import path
import importlib
import slisp

while True:
    try:
        repl_input = input("⊃ ")
        if repl_input == "reload":
            importlib.reload(slisp)
            continue
        """
        slisp.lexer.input(repl_input)           # lexes the repl_input
        [print(i) for i in slisp.lexer]         # print lexed input

        slisp.lexer.input(repl_input)           # printing may verywell consume tokens, so relex
        print(slisp.parser.parse(repl_input))   # parsed
        """        
        print(slisp.evaluate(
                slisp.parser.parse(repl_input)
            ))

    except KeyboardInterrupt:
        exit(1)
