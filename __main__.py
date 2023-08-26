import readline
from os import path
import importlib
import slisp
import sys
import re
import parser 

def execute(text):
    parsed = parser.parser.parse(text)
    evald = slisp.evaluate(parsed)
    if type(evald) == str and evald != 'None': 
        return evald + '\n'
    else:
        return ''

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
            print(a, end='')

def template(file):
    with open(file) as f:
        code = re.findall(r'\$<.*>\$', f.read())
    print(code)

    
    

if __name__ == "__main__":
    if not not len(files := sys.argv[1:]):
        for i in files:
            if i.endswith('.html.slisp'):
                template(i)
            elif i.endswith('.slisp'):
                runFile(i)
    else:
        repl()
