"""
	Processamento de Linguagens
	Licenciatura em Engenharia de Sistemas Informáticos
	2025/2026

	AST Nodes - Representação Intermédia da linguagem LFun
	Fase C: literais, expressões, let, fun, if, chamadas
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

class IfExpr(Node):
	# condicional: if cond then E else E
	def __init__(self, cond, then_e, else_e):
		self.cond   = cond
		self.then_e = then_e
		self.else_e = else_e
	def __repr__(self):
		return f"If({self.cond}, {self.then_e}, {self.else_e})"

class CallExpr(Node):
	# chamada de função: f(arg)
	def __init__(self, name, arg):
		self.name = name
		self.arg  = arg
	def __repr__(self):
		return f"Call({self.name}, {self.arg})"


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

class FunSig(Node):
	# assinatura de função: fun f : Int -> Int ;
	def __init__(self, name, arg_type, ret_type):
		self.name     = name
		self.arg_type = arg_type
		self.ret_type = ret_type
	def __repr__(self):
		return f"Sig({self.name} : {self.arg_type} -> {self.ret_type})"

class FunDef(Node):
	# definição de função: let f x = E ;
	def __init__(self, name, arg, body):
		self.name = name
		self.arg  = arg
		self.body = body
	def __repr__(self):
		return f"Fun({self.name} {self.arg} = {self.body})"
