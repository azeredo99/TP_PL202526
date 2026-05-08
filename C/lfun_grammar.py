"""
	Processamento de Linguagens
	Licenciatura em Engenharia de Sistemas Informáticos
	2025/2026

	LFunGrammar - Analisador Sintático para a linguagem LFun
	Fase C: expressões + let + funções + if
"""
# lfun_grammar.py
from lfun_lexer import LFunLexer
from ast_nodes import (
	Program, ExprStmt, LetStmt, FunSig, FunDef,
	NumberLiteral, BoolLiteral, VarExpr,
	BinOp, UnaryOp, IfExpr, CallExpr,
)
import ply.yacc as pyacc


class LFunGrammar:

	# especificação da gramática:
	# Rule 0   Program  -> StmtList
	# Rule 1   StmtList -> Stmt
	# Rule 2   StmtList -> StmtList Stmt
	# Rule 3   Stmt     -> E ;
	# Rule 4   Stmt     -> LET ID : Type = E ;
	# Rule 5   Stmt     -> FUN ID : Type -> Type ;
	# Rule 6   Stmt     -> LET ID ID = E ;
	# Rule 7   Type     -> TINT
	# Rule 8   Type     -> TBOOL
	# Rule 9   E        -> E op E
	# Rule 10  E        -> - E
	# Rule 11  E        -> ( E )
	# Rule 12  E        -> NUMBER
	# Rule 13  E        -> TRUE
	# Rule 14  E        -> FALSE
	# Rule 15  E        -> ID
	# Rule 16  E        -> IF E THEN E ELSE E
	# Rule 17  E        -> ID ( E )

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
	# ─────────────────────────────────────────────

	def p_program(self, p):
		""" Program : StmtList """
		p[0] = Program(p[1])

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
		p[0] = ExprStmt(p[1])

	def p_stmt_let_val(self, p):
		""" Stmt : LET ID ':' Type '=' E ';' """
		# definição de valor: let x : Int = 3 + 4;
		p[0] = LetStmt(p[2], p[4], p[6])

	def p_stmt_fun_sig(self, p):
		""" Stmt : FUN ID ':' Type ARROW Type ';' """
		# assinatura de função: fun dobro : Int -> Int;
		p[0] = FunSig(p[2], p[4], p[6])

	def p_stmt_fun_def(self, p):
		""" Stmt : LET ID ID '=' E ';' """
		# definição de função: let dobro n = n * 2;
		p[0] = FunDef(p[2], p[3], p[5])

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
		# operação binária
		p[0] = BinOp(p[2], p[1], p[3])

	def p_expr_uminus(self, p):
		""" E : '-' E %prec UMINUS """
		# menos unário: -3
		p[0] = UnaryOp('neg', p[2])

	def p_expr_pare(self, p):
		""" E : '(' E ')' """
		#   0    1  2  3
		# parênteses: apenas passa o valor interno
		p[0] = p[2]

	def p_expr_num(self, p):
		""" E : NUMBER """
		p[0] = NumberLiteral(p[1])

	def p_expr_true(self, p):
		""" E : TRUE """
		p[0] = BoolLiteral(True)

	def p_expr_false(self, p):
		""" E : FALSE """
		p[0] = BoolLiteral(False)

	def p_expr_var(self, p):
		""" E : ID """
		# referência a uma variável
		p[0] = VarExpr(p[1])

	def p_expr_if(self, p):
		""" E : IF E THEN E ELSE E """
		# condicional: if n < 0 then 0 - n else n
		p[0] = IfExpr(p[2], p[4], p[6])

	def p_expr_call(self, p):
		""" E : ID '(' E ')' """
		# chamada de função: dobro(7)
		p[0] = CallExpr(p[1], p[3])

	# ─────────────────────────────────────────────
	#  ERRO SINTÁTICO
	# ─────────────────────────────────────────────

	def p_error(self, p):
		if p:
			print(f"Syntax error: unexpected '{p.type}' na linha {p.lineno}")
		else:
			print("Syntax error: unexpected end of file")