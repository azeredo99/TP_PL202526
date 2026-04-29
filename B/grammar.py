"""
    Processamento de Linguagens
    Licenciatura em Engenharia de Sistemas Informáticos
    2025/2026

    Grammar - Analisador Sintático para a linguagem LFun
    Fase B: expressões aritméticas + definições let
"""
from lexer import LFunLexer
import ply.yacc as pyacc


class LFunGrammar:

    # ─────────────────────────────────────────────
    #  PRECEDÊNCIA DOS OPERADORES
    #  Da menor para a maior prioridade (de cima para baixo).
    # ─────────────────────────────────────────────
    precedence = (
        ('left', 'OR'),               # ||
        ('left', 'AND'),              # &&
        ('left', 'EQ', 'NEQ'),        # == !=
        ('left', '<', '>', 'LE', 'GE'),  # < > <= >=
        ('left', '+', '-'),           # + -
        ('left', '*', '/'),           # * /
        ('right', 'UMINUS'),          # menos unário: -3
    )

    def __init__(self):
        self.lexer = None
        self.yacc  = None
        self.tokens = None

    def build(self, **kwargs):
        self.lexer  = LFunLexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc   = pyacc.yacc(module=self, **kwargs)

    def parse(self, text):
        self.lexer.input(text)
        return self.yacc.parse(lexer=self.lexer.lexer)

    # ─────────────────────────────────────────────
    #  PROGRAMA
    #  Um programa é uma sequência de instruções.
    # ─────────────────────────────────────────────

    def p_program(self, p):
        """ Program : StmtList """
        p[0] = {'op': 'program', 'stmts': p[1]}

    def p_stmtlist_single(self, p):
        """ StmtList : Stmt """
        p[0] = [p[1]]

    def p_stmtlist_multi(self, p):
        """ StmtList : StmtList Stmt """
        p[0] = p[1] + [p[2]]

    # ─────────────────────────────────────────────
    #  INSTRUÇÕES
    # ─────────────────────────────────────────────

    def p_stmt_expr(self, p):
        """ Stmt : E ';' """
        # Expressão simples: 3 + 4;
        p[0] = {'op': 'expr', 'expr': p[1]}

    def p_stmt_let_val(self, p):
        """ Stmt : LET ID ':' Type '=' E ';' """
        # Definição de valor: let x : Int = 3 + 4;
        p[0] = {'op': 'let', 'name': p[2], 'type': p[4], 'expr': p[6]}

    # ─────────────────────────────────────────────
    #  TIPOS
    # ─────────────────────────────────────────────

    def p_type_int(self, p):
        """ Type : TINT """
        p[0] = 'Int'

    def p_type_bool(self, p):
        """ Type : TBOOL """
        p[0] = 'Bool'

    # ─────────────────────────────────────────────
    #  EXPRESSÕES ARITMÉTICAS E BOOLEANAS
    # ─────────────────────────────────────────────

    def p_expr_binop(self, p):
        """ E : E '+' E
              | E '-' E
              | E '*' E
              | E '/' E
              | E '<' E
              | E '>' E
              | E LE  E
              | E GE  E
              | E EQ  E
              | E NEQ E
              | E AND E
              | E OR  E """
        p[0] = {'op': p[2], 'args': [p[1], p[3]]}

    def p_expr_uminus(self, p):
        """ E : '-' E %prec UMINUS """
        # Menos unário: -3  →  {'op': 'neg', 'args': [3]}
        p[0] = {'op': 'neg', 'args': [p[2]]}

    def p_expr_paren(self, p):
        """ E : '(' E ')' """
        #   0    1  2  3
        p[0] = p[2]

    def p_expr_number(self, p):
        """ E : NUMBER """
        p[0] = p[1]   # valor inteiro diretamente

    def p_expr_true(self, p):
        """ E : TRUE """
        p[0] = True

    def p_expr_false(self, p):
        """ E : FALSE """
        p[0] = False

    def p_expr_id(self, p):
        """ E : ID """
        # Referência a uma variável: x
        p[0] = {'var': p[1]}

    # ─────────────────────────────────────────────
    #  ERRO SINTÁTICO
    # ─────────────────────────────────────────────

    def p_error(self, p):
        if p:
            print(f"[Erro Sintático] Token inesperado '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
        else:
            print("[Erro Sintático] Fim de ficheiro inesperado")


# ─────────────────────────────────────────────
#  TESTE
# ─────────────────────────────────────────────
if __name__ == '__main__':
    from pprint import PrettyPrinter
    pp = PrettyPrinter(sort_dicts=False)

    g = LFunGrammar()
    g.build()

    exemplos = [
        "3 + 4;",
        "10 - 2 * 3;",
        "(8 + 2) * 5;",
        "3 < 5;",
        "10 == 7;",
        "let base : Int = 10;",
        "let ativo : Bool = true;",
        "let area : Int = 4 * 5;",
        "let largura : Int = 8; let altura : Int = 5; let area : Int = largura * altura;",
    ]

    for exemplo in exemplos:
        print(f"\n{'='*50}")
        print(f"Código: {exemplo.strip()}")
        print(f"{'='*50}")
        resultado = g.parse(exemplo)
        pp.pprint(resultado)