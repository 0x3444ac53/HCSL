import readline
from os import path
import importlib
import sys
import re
from pprint import pprint
from pathlib import Path
from . import parser
from . import slisp

def execute(text):
    parsed = parser.parser.parse(text)
    evald = slisp.evaluate(parsed)
    if type(evald) == str and evald != 'None': 
        return evald
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

def template(file, outputDir='.'):
    path = Path(file)
    with open(path) as f:
        source = f.read()
    replacements = (
        (i, execute(i[2:-2])) for i in re.findall(r'\$<.*>\$', source)
        )
    for i in replacements:
        source = source.replace(i[0], i[1])
    with open(Path(outputDir) / path.stem, 'w') as outfile:
        outfile.write(source)
    

    
if __name__ == "__main__":
    if not not len(files := sys.argv[1:]):
        for i in files:
            file = Path(i)
            if file.suffixes.__len__() > 1 and file.suffix == '.slisp':
                template(file, outputDir='docs')
            elif file.suffix == '.slisp':
                runFile(file)
    else:
        repl()
