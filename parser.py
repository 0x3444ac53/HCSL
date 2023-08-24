from ply.lex import lex
from ply.yacc import yacc 

tokens = ('ID',  # var name
          'RPAREN',     #)
          'LPAREN',     #(
          'STRING',     #"
          'COMMENT'
          )

schar = r'a-zA-Z_0-9\$\*\{\}\','
t_STRING = r'"([^"]*?)"'
t_ID = '[%s][%s]*' % (schar, schar)
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore_COMMENT = r'\;.*'
t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex()

def p_lisperal(p):
    '''
    lisperal : LPAREN lisperal arguments RPAREN
             | LPAREN lisperal RPAREN
             | ID 
             | STRING
    '''
    if len(p) == 5:
        p[0] = [p[2], p[3]]
    if len(p) == 4:
        p[0] = [p[2]]
    if len(p) == 2:
        p[0] = p[1]

def p_arguments(p):
    'arguments : argument arguments'
    p[0] = [p[1]] + p[2]

def p_argument(p):
    '''
    argument : lisperal

    '''
    if type(p[1]) == str:
        p[0] = p[1].replace('"', '')
    if type(p[1]) == list:
        p[0] = p[1]

def p_arguments_empty(p):
    'arguments : '
    p[0] = []

def p_error(p):
    pass

parser = yacc()
