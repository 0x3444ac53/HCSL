from parser import parser
import subprocess

def define_function(function_def):
    functions[function_def[0]] = function_def[1:]
    return functions[function_def[0]]

def run_file(args, file=False, join=''):
    if file:
        with open(args) as target:
            script = target.read()
    else:
        script = args
    process = subprocess.run(script,
                             shell=True, 
                             text=True, 
                             capture_output=True)
    return process.stdout

def print_functions(): print(functions)

def slisp_map(function, slist, sep='\n', join='\n'):
    function_def = functions[function][0]
    iterate_on = evaluate(slist).split(sep)
    return join.join(
            map(function_def.format,
                filter(lambda x: x, iterate_on)))
    
def evaluate(args):
    if not args:
        return ""
    if type(args) == str:
        return args
    func_name, args = args
    
    try:
        return functions[func_name](args)
    except TypeError:
        pass

    try:
        function_def = functions[func_name][0]
    except TypeError:
        function_def = functions[func_name]
    except KeyError:
        print(f"undefined function {func_name}")
    
    args = [evaluate(i) for i in args]
    
    if type(function_def) == str:
        return function_def.format(*args)
    if type(function_def) == list:
        return evaluate(function_def).format(*args)

functions = {
        "func"    : define_function,                  # function_def
        "exit"    : lambda x: exit(int(*x)),            # repl exit
        "execute" : lambda x: run_file(*x, file=True),
        "eval"    : lambda x: run_file(*x),
        "debug"   : lambda : print_functions(),
        "map"     : lambda x: slisp_map(*x)
    }
