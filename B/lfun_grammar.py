"""
	Processamento de Linguagens
	Licenciatura em Engenharia de Sistemas Informáticos
	2025/2026

	LFunGrammar - Analisador Sintático para a linguagem LFun
	Fase B: expressões aritméticas + booleanas + let
"""
# lfun_grammar.py
from lfun_lexer import LFunLexer
import ply.yacc as pyacc


class LFunGrammar:

	# especificação da gramática:
	# Rule 0   Program  -> StmtList
	# Rule 1   StmtList -> Stmt
	# Rule 2   StmtList -> StmtList Stmt
	# Rule 3   Stmt     -> E ;
	# Rule 4   Stmt     -> LET ID : Type = E ;
	# Rule 5   Type     -> TINT
	# Rule 6   Type     -> TBOOL
	# Rule 7   E        -> E op E
	# Rule 8   E        -> - E
	# Rule 9   E        -> ( E )
	# Rule 10  E        -> NUMBER
	# Rule 11  E        -> TRUE
	# Rule 12  E        -> FALSE
	# Rule 13  E        -> ID

	# ─────────────────────────────────────────────
	#  PRECEDÊNCIA DOS OPERADORES
	#  Da menor para a maior prioridade (de cima para baixo)
	# ─────────────────────────────────────────────
	precedence = (
		('left', 'OR'),                      # level=1  ||
		('left', 'AND'),                     # level=2  &&
		('left', 'EQ', 'NEQ'),               # level=3  == !=
		('left', '<', '>', 'LE', 'GE'),      # level=4  < > <= >=
		('left', '+', '-'),                  # level=5  + -
		('left', '*', '/'),                  # level=6  * /
		('right', 'UMINUS'),                 # level=7  - unário
	)

	def __init__(self):
		self.yacc   = None
		self.lexer  = None
		self.tokens = None

	def build(self, **kwargs):
		# inicializa o analisador léxico e sintático
		self.lexer  = LFunLexer()
		self.lexer.build(**kwargs)
		self.tokens = self.lexer.tokens
		self.yacc   = pyacc.yacc(module=self, **kwargs)

	def parse(self, string):
		# inicia a análise sintática
		self.lexer.input(string)
		return self.yacc.parse(lexer=self.lexer.lexer)

	# ─────────────────────────────────────────────
	#  PROGRAMA
	#  Um programa é uma sequência de instruções
	# ─────────────────────────────────────────────

	def p_program(self, p):
		""" Program : StmtList """
		p[0] = {'op': 'program', 'stmts': p[1]}

	def p_stmtlist_head(self, p):
		""" StmtList : Stmt """
		p[0] = [p[1]]

	def p_stmtlist_tail(self, p):
		""" StmtList : StmtList Stmt """
		p[0] = p[1] + [p[2]]

	# ─────────────────────────────────────────────
	#  INSTRUÇÕES
	# ─────────────────────────────────────────────

	def p_stmt_expr(self, p):
		""" Stmt : E ';' """
		# expressão simples: 3 + 4;
		p[0] = {'op': 'expr', 'args': [p[1]]}

	def p_stmt_let_val(self, p):
		""" Stmt : LET ID ':' Type '=' E ';' """
		# definição de valor: let x : Int = 3 + 4;
		# args = [nome, tipo, expr]
		p[0] = {'op': 'let', 'args': [p[2], p[4], p[6]]}

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
	#  EXPRESSÕES
	# ─────────────────────────────────────────────

	def p_expr_op(self, p):
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
		# operação binária: args = [esquerda, direita]
		p[0] = {'op': p[2], 'args': [p[1], p[3]]}

	def p_expr_uminus(self, p):
		""" E : '-' E %prec UMINUS """
		# menos unário: -3
		p[0] = {'op': 'neg', 'args': [p[2]]}

	def p_expr_pare(self, p):
		""" E : '(' E ')' """
		# parênteses: apenas passa o valor interno
		p[0] = p[2]

	def p_expr_num(self, p):
		""" E : NUMBER """
		# valor inteiro diretamente
		p[0] = p[1]

	def p_expr_true(self, p):
		""" E : TRUE """
		p[0] = True

	def p_expr_false(self, p):
		""" E : FALSE """
		p[0] = False

	def p_expr_var(self, p):
		""" E : ID """
		# referência a uma variável: x
		p[0] = {'var': p[1]}

	# ─────────────────────────────────────────────
	#  ERRO SINTÁTICO
	# ─────────────────────────────────────────────

	def p_error(self, p):
		if p:
			print(f"Syntax error: unexpected '{p.type}' na linha {p.lineno}")
		else:
			print("Syntax error: unexpected end of file")