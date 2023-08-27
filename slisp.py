import subprocess
from pprint import pprint
from . import parser
from pathlib import Path
import shlex
from shutil import copy
import re

def define_function(function_def):
    functions[function_def[0]] = function_def[1:]
    return functions[function_def[0]]

def run_file(args):
    script = evaluate(*args)
    process = subprocess.run(script,
                             shell=True, 
                             text=True, 
                             capture_output=True)
    return process.stdout

def print_functions(x): 
    pprint(functions)
    pprint(stack)

def process_slisp_file(inFile):
    with open(inFile) as f:
        source = f.read()
    replacements = (
        (i, evaluate(parser.parser.parse(i[2:-2]))) for i in re.findall(r'\$<.*>\$', source))
    for i in replacements:
        source = source.replace(i[0], i[1])
    return source

def template_single(inFile, outFile):
    outFile.parents[0].mkdir(parents=True, exist_ok=True)
    if inFile.suffix == '.slisp':
        processed = process_slisp_file(inFile)
        outFile = outFile.with_name(outFile.stem) 
        with outFile.open('w') as f:
            f.write(processed)
            returnString = f"SlispFile {inFile} to {outFile}"
    else:
        try:
            copy(inFile, outFile)
            return f"{inFile} to {outFile}"
        except IsADirectoryError:
            returnString = f"skipping {outFile}: is a directory"
    return returnString


def template(args):
    args = [Path(evaluate(i))
                for i in args]
    inFile, outFile = args
    if inFile.is_dir() and outFile.is_dir():
        return "\n".join([template_single(file, outFile / Path("/".join(file.parts[1:]))) for file in inFile.rglob("**/*")])
            

def slisp_map(args):
    function, args = args
    function_def = functions[function][0]
    iterate_on = evaluate(args).split('\n')
    return '\n'.join(
            map(function_def.format,
                filter(lambda x: x, iterate_on)))
    
def concat(args):
    args = [i if type(i) == str else evaluate(i) for i in args]
    return args[0].join(args[1:])

def load_file(x):
    for file in x:
        with open(file) as f:
            for i in f.readlines():
                stack.append(evaluate(parser.parser.parse(i)))
    return ""

def source_file(x):
    for file in x:
        try:
            with open(file) as f:
                a = [evaluate(parser.parser.parse(i)) for i in f.readlines()]
                return "\n".join(a)
        except FileNotFoundError as e:
            print(e)
    return ""

def shell_quote(x):
    args = evaluate(x)
    return shlex.quote(args)

def evaluate(args):
    if not args:
        return ""
    if type(args) == str:
        return args
    
    try:
        func_name, args = args
    except ValueError:
        func_name = args[0]
    
    try:
        return functions[func_name](args)
    except TypeError:
        pass
    except KeyError:
        pass  

    try:
        function_def = functions[func_name][0]
    except TypeError:
        function_def = functions[func_name]
    except KeyError:
        return " ".join([func_name] + args)
    
    args = [evaluate(i) for i in args]
    
    if type(function_def) == str:
        return bytes(function_def.format(*args), 'utf-8').decode('unicode_escape')
    if type(function_def) == list:
        return evaluate(function_def).format(*args)

stack = []

functions = {
        "func"          : define_function,                  # function_def
        "exit"          : lambda x: exit(int(*x)),            # repl exit
        "source"        : source_file, 
        "execute"       : lambda x: run_file(x),
        "debug"         : print_functions,
        "map"           : lambda x: slisp_map(x),
        "concat"        : concat,
        "shell_quote"   : lambda x: shell_quote(*x),
        "template"      : template,
        "push"          : lambda x: stack.append(evaluate(*x)),
        "pop"           : lambda x: stack.pop(),
        "read"          : load_file
    }
