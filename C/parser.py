import ply.yacc as yacc
from lexer import tokens

env = {}
functions = {}

start = 'statement'

# ---------------- EXPRESSÕES ----------------

def p_expr_bin(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expr_cmp(p):
    '''expr : expr LT expr
            | expr GT expr
            | expr EQEQ expr'''
    p[0] = ('cmp', p[2], p[1], p[3])

def p_expr_group(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_expr_num(p):
    'expr : NUMBER'
    p[0] = ('num', p[1])

def p_expr_bool(p):
    'expr : BOOL'
    p[0] = ('bool', p[1])

def p_expr_id(p):
    'expr : ID'
    p[0] = ('id', p[1])

def p_expr_neg(p):
    'expr : MINUS NUMBER'
    p[0] = ('num', -p[2])

# ---------------- FUNÇÕES ----------------

def p_expr_call(p):
    'expr : ID LPAREN expr RPAREN'
    fname = p[1]

    if fname not in functions:
        print("Erro: função não definida")
        p[0] = ('num', 0)
        return

    argname, body = functions[fname]
    p[0] = ('call', argname, body, p[3])

# ---------------- LET ----------------

def p_let_var(p):
    'statement : LET ID EQ expr SEMI'
    env[p[2]] = eval_expr(p[4])
    print(f"{p[2]} = {env[p[2]]}")

# ---------------- ASSINATURA ----------------

def p_fun_signature(p):
    'statement : FUN ID COLON TYPE ARROW TYPE SEMI'
    print(f"Assinatura registada: {p[2]}")

# ---------------- DEFINIÇÃO ----------------

def p_fun_def(p):
    'statement : LET ID ID EQ expr SEMI'
    functions[p[2]] = (p[3], p[5])
    print(f"Função {p[2]} definida")

# ---------------- IF ----------------

def p_if(p):
    'expr : IF expr THEN expr ELSE expr'
    p[0] = ('if', p[2], p[4], p[6])

# ---------------- EXPRESSÃO ----------------

def p_statement_expr(p):
    'statement : expr SEMI'
    print("Resultado:", eval_expr(p[1]))

# ---------------- AVALIADOR ----------------

def eval_expr(tree, local_arg=None, local_val=None):
    kind = tree[0]

    if kind == 'num':
        return tree[1]

    if kind == 'bool':
        return tree[1]

    if kind == 'id':
        if tree[1] == local_arg:
            return local_val
        return env.get(tree[1], 0)

    if kind == 'binop':
        l = eval_expr(tree[2], local_arg, local_val)
        r = eval_expr(tree[3], local_arg, local_val)
        return l + r if tree[1] == '+' else l - r if tree[1] == '-' else l * r

    if kind == 'cmp':
        l = eval_expr(tree[2], local_arg, local_val)
        r = eval_expr(tree[3], local_arg, local_val)
        return l < r if tree[1] == '<' else l > r if tree[1] == '>' else l == r

    if kind == 'if':
        cond = eval_expr(tree[1], local_arg, local_val)
        return eval_expr(tree[2], local_arg, local_val) if cond else eval_expr(tree[3], local_arg, local_val)

    if kind == 'call':
        argname, body, argexpr = tree[1], tree[2], tree[3]
        val = eval_expr(argexpr, local_arg, local_val)
        return eval_expr(body, argname, val)

parser = yacc.yacc()