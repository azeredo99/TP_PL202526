"""
	Processamento de Linguagens
	Licenciatura em Engenharia de Sistemas Informáticos
	2025/2026

	AST Nodes - Representação Intermédia da linguagem LFun
	Fase B: literais, expressões aritméticas/booleanas
"""
# ast_nodes.py


# ─────────────────────────────────────────────
#  CLASSE BASE
# ─────────────────────────────────────────────

class Node:
	pass


# ─────────────────────────────────────────────
#  LITERAIS
# ─────────────────────────────────────────────

class NumberLiteral(Node):
	def __init__(self, value):
		self.value = int(value)
	def __repr__(self):
		return f"Number({self.value})"

class BoolLiteral(Node):
	def __init__(self, value):
		self.value = bool(value)
	def __repr__(self):
		return f"Bool({self.value})"


# ─────────────────────────────────────────────
#  EXPRESSÕES
# ─────────────────────────────────────────────

class VarExpr(Node):
	# referência a uma variável: x
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return f"Var({self.name})"

class BinOp(Node):
	# operação binária: E op E
	def __init__(self, op, left, right):
		self.op    = op
		self.left  = left
		self.right = right
	def __repr__(self):
		return f"BinOp({self.op}, {self.left}, {self.right})"

class UnaryOp(Node):
	# operação unária: - E
	def __init__(self, op, operand):
		self.op      = op
		self.operand = operand
	def __repr__(self):
		return f"UnaryOp({self.op}, {self.operand})"


# ─────────────────────────────────────────────
#  INSTRUÇÕES
# ─────────────────────────────────────────────

class Program(Node):
	# programa: lista de instruções
	def __init__(self, stmts):
		self.stmts = stmts
	def __repr__(self):
		return f"Program({self.stmts})"

class ExprStmt(Node):
	# instrução de expressão: E ;
	def __init__(self, expr):
		self.expr = expr
	def __repr__(self):
		return f"ExprStmt({self.expr})"

class LetStmt(Node):
	# definição de valor: let x : Int = E ;
	def __init__(self, name, type_, expr):
		self.name  = name
		self.type  = type_
		self.expr  = expr
	def __repr__(self):
		return f"Let({self.name} : {self.type} = {self.expr})"
