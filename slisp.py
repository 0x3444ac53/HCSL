import subprocess
from pprint import pprint
from . import parser
from pathlib import Path
import shlex
from shutil import copy
import re

def define_function(function_def):
    functions[function_def[0]] = function_def[1:]
    return f"{function_def=}"

def run_file(args):
    script = evaluate(*args)
    process = subprocess.run(script,
                             shell=True, 
                             text=True, 
                             capture_output=True)
    return process.stdout

def print_functions(x):
    pprint(functions)
    pprint(slisp_stack)
    return f"Debugged with {print_functions}"

def process_slisp_file(inFile):
    print(f"Processing {inFile}")
    with open(inFile) as f:
        source = f.read()
    try:
        replacements = (
            (i, evaluate(parser.parser.parse(i[2:-2]))) for i in re.findall(r'\$<.*>\$', source))
        for i in replacements:
            source = re.sub(re.escape(i[0]), i[1], source, count=1)
    except Exception as e:
        print(e)
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
    if inFile.is_dir():
        return "\n".join([template_single(file, outFile / Path("/".join(file.parts[1:]))) for file in inFile.rglob("**/*")])
            

def slisp_map(args):
    global slisp_stack
    for i in args:
        try:
            function_def = functions[i][0]
            slisp_stack = list(map(function_def.format, slisp_stack))
        except TypeError:
            function_def = functions[i]
            slisp_stack = list(map(function_def, slisp_stack))
    return f"mapped {function_def}"
    
def concat(join_on):
    global slisp_stack
    returnval = ""
    join_on = [evaluate(i) if type(i) == list else i for i in join_on]
    if len(join_on) > 1:
        for i in join_on[1:]:
            returnval = returnval + join_on[0] + i
    else:
        for i in range(len(slisp_stack)):
            if i > 0:
                returnval = returnval + join_on[0] + slisp_stack.pop()
            else:
                returnval = returnval + slisp_stack.pop()
    return returnval

def load_file(x):
    for file in x:
        with open(file) as f:
            for i in f.readlines():
                slisp_stack.append(i)
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
    return shlex.quote(evaluate(*x))

def slisp_push(x):
    slisp_stack.append(evaluate(*x))
    return f"pushed {slisp_stack[-1]}"

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
        return function_def.format(*args, dq='"').replace("\\n", "\n")
    if type(function_def) == list:
        return evaluate(function_def).format(*args)

slisp_stack = []

functions = {
        "func"          : define_function,                  # function_def
        "exit"          : lambda x: exit(int(*x)),            # repl exit
        "source"        : source_file, 
        "execute"       : lambda x: run_file(x),
        "debug"         : print_functions,
        "map"           : lambda x: slisp_map(x),
        "concat"        : concat,
        "shell_quote"   : shell_quote,
        "template"      : template,
        "push"          : slisp_push,
        "pop"           : lambda x: slisp_stack.pop(),
        "read"          : load_file,
        "eval"          : lambda x: evaluate(parser.parser.parse(x))
    }
