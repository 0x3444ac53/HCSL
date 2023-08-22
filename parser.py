from ply.lex import lex
from ply.yacc import yacc 

# Define the lexer
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
t_ignore_COMMENT = r'\#;.*'
t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex()

def p_expression(p):
    '''
    expression : LPAREN ID arguments RPAREN
               | LPAREN lisperal RPAREN
               | LPAREN expression RPAREN
    '''
    p[0] = [p[2], p[3]]

def p_arguments(p):
    'arguments : argument arguments'
    p[0] = [p[1]] + p[2]

def p_arguments_empty(p):
    'arguments :'
    p[0] = []

def p_argument(p):
    '''
    argument : ID
             | expression
             | lisperal 
    '''
    p[0] = p[1]

def p_lisperal(p):
    '''
    lisperal : STRING
             | ID
    '''
    p[0] = p[1].replace('"', '')

def p_error(p):
    pass

parser = yacc()
