import ply.lex as lex

tokens = (
    'LET', 'FUN',
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES',
    'LT', 'GT',
    'EQEQ', 'EQ',
    'LPAREN', 'RPAREN',
    'SEMI', 'COLON', 'ARROW',
    'BOOL',
    'IF', 'THEN', 'ELSE',
    'TYPE'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_LT = r'<'
t_GT = r'>'
t_EQEQ = r'=='
t_EQ = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_COLON = r':'
t_ARROW = r'->'

# PALAVRAS RESERVADAS (ANTES DO ID)

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FUN(t):
    r'fun'
    return t

def t_LET(t):
    r'let'
    return t

def t_TYPE(t):
    r'Int|Bool'
    return t

def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == "true" else False
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print("Erro léxico:", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()