import readline
from os import path
import importlib
import slisp
import sys

def execute(text):
    parsed = slisp.parser.parse(text)
    return slisp.evaluate(parsed)

def repl():
    while True:
        try:
            repl_input = input("⊃ ")
            if repl_input == "reload":
                importlib.reload(slisp)
                continue
            print(execute(repl_input))

        except KeyboardInterrupt:
            exit(1)

def runFile(filePath):
    with open(filePath) as f:
        for line in f.readlines():
            a = execute(line)
            print(a)

if __name__ == "__main__":
    if not not len(sys.argv[1:]):
        runFile(sys.argv[1])
    else:
        repl()
