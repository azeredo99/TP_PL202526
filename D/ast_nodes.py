"""
    Processamento de Linguagens
    Licenciatura em Engenharia de Sistemas Informáticos
    2025/2026

    AST Nodes - Representação Intermédia da linguagem LFun
    Fase D: todos os nós (literais, expressões, instruções, padrões)
"""
# ast_nodes.py

class Node:
	pass


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


class VarExpr(Node):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f"Var({self.name})"


class IfExpr(Node):
	def __init__(self, cond, then_e, else_e):
		self.cond = cond
		self.then_e = then_e
		self.else_e = else_e

	def __repr__(self):
		return f"If({self.cond}, {self.then_e}, {self.else_e})"


class MatchExpr(Node):
	def __init__(self, expr, cases):
		self.expr = expr
		self.cases = cases

	def __repr__(self):
		return f"Match({self.expr}, {self.cases})"


class Case(Node):
	def __init__(self, patterns, expr):
		self.patterns = patterns
		self.expr = expr

	def __repr__(self):
		return f"Case({self.patterns}, {self.expr})"


class BinOp(Node):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right

	def __repr__(self):
		return f"BinOp({self.op}, {self.left}, {self.right})"


class UnaryOp(Node):
	def __init__(self, op, operand):
		self.op = op
		self.operand = operand

	def __repr__(self):
		return f"UnaryOp({self.op}, {self.operand})"


class CallExpr(Node):
	def __init__(self, name, arg):
		self.name = name
		self.arg = arg

	def __repr__(self):
		return f"Call({self.name}, {self.arg})"


class LetStmt(Node):
	def __init__(self, name, type_, expr):
		self.name = name
		self.type = type_
		self.expr = expr

	def __repr__(self):
		return f"Let({self.name}, {self.type}, {self.expr})"


class LetExpr(Node):
	def __init__(self, name, expr, body):
		self.name = name
		self.expr = expr
		self.body = body

	def __repr__(self):
		return f"LetExpr({self.name}, {self.expr}, {self.body})"


class FunExpr(Node):
	def __init__(self, arg, arg_type, body):
		self.arg = arg
		self.arg_type = arg_type
		self.body = body

	def __repr__(self):
		return f"FunExpr({self.arg}, {self.arg_type}, {self.body})"


class FunDef(Node):
	def __init__(self, name, arg, expr, signature=None):
		self.name = name
		self.arg = arg
		self.expr = expr
		self.signature = signature

	def __repr__(self):
		return f"Fun({self.name}, {self.arg}, {self.expr}, sig={self.signature})"


class Signature(Node):
	def __init__(self, name, from_t, to_t):
		self.name = name
		self.from_t = from_t
		self.to_t = to_t

	def __repr__(self):
		return f"Sig({self.name}: {self.from_t} -> {self.to_t})"


class Pattern:
	pass


class IntPattern(Pattern):
	def __init__(self, value):
		self.value = int(value)

	def __repr__(self):
		return f"IntPat({self.value})"


class WildcardPattern(Pattern):
	def __repr__(self):
		return "_"


class VarPattern(Pattern):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f"VarPat({self.name})"
