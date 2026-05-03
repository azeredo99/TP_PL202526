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

def p_expr_neg_num(p):
    'expr : MINUS NUMBER'
    p[0] = ('num', -p[2])



# ---------------- CHAMADA DE FUNÇÃO ----------------

def p_expr_call(p):
    'expr : ID LPAREN expr RPAREN'
    fname = p[1]
    if fname not in functions:
        print(f"Erro: função", fname, "não definida")
        p[0] = ('num', 0)
        return

    argname, body = functions[fname]
    p[0] = ('call', argname, body, p[3])


# ---------------- LET VAR ----------------

def p_let_var(p):
    'statement : LET ID EQ expr SEMI'
    env[p[2]] = eval_expr(p[4])
    print(f"{p[2]} = {env[p[2]]}")

# ---------------- ASSINATURA (IGNORADA) ----------------

def p_fun_signature(p):
    'statement : FUN ID COLON TYPE ARROW TYPE SEMI'
    print(f"Assinatura registada: {p[2]} : {p[4]} -> {p[6]}")

# ---------------- DEFINIÇÃO DE FUNÇÃO ----------------

def p_fun_def(p):
    'statement : LET ID ID EQ expr SEMI'
    fname = p[2]
    arg = p[3]
    body = p[5]
    functions[fname] = (arg, body)
    print(f"Função {fname} definida.")


# ---------------- IF ----------------

def p_if(p):
    'expr : IF expr THEN expr ELSE expr'
    p[0] = ('if', p[2], p[4], p[6])

# ---------------- EXPRESSÃO COMO STATEMENT ----------------

def p_statement_expr(p):
    'statement : expr'
    print("Resultado:", eval_expr(p[1]))

# ---------------- AVALIADOR ----------------

def eval_expr(tree, local_arg=None, local_val=None):
    kind = tree[0]

    if kind == 'num':
        return tree[1]

    if kind == 'bool':
        return tree[1]

    if kind == 'id':
        name = tree[1]
        if name == local_arg:
            return local_val
        return env.get(name, 0)

    if kind == 'binop':
        op, left, right = tree[1], tree[2], tree[3]
        l = eval_expr(left, local_arg, local_val)
        r = eval_expr(right, local_arg, local_val)
        return l + r if op == '+' else l - r if op == '-' else l * r

    if kind == 'cmp':
        op, left, right = tree[1], tree[2], tree[3]
        l = eval_expr(left, local_arg, local_val)
        r = eval_expr(right, local_arg, local_val)
        return l < r if op == '<' else l > r if op == '>' else l == r

    if kind == 'if':
        cond = eval_expr(tree[1], local_arg, local_val)
        return eval_expr(tree[2], local_arg, local_val) if cond else eval_expr(tree[3], local_arg, local_val)

    if kind == 'call':
        argname, body, argexpr = tree[1], tree[2], tree[3]
        val = eval_expr(argexpr, local_arg, local_val)
        return eval_expr(body, argname, val)

parser = yacc.yacc()
