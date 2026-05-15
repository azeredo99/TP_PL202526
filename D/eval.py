from ast_nodes import (
	BoolLiteral,
	IfExpr,
	IntPattern,
	LetExpr,
	FunExpr,
	MatchExpr,
	NumberLiteral,
	VarExpr,
	VarPattern,
	WildcardPattern,
)


symbols = {}
functions = {}
signatures = {}


class _Closure:
	def __init__(self, arg_name, body, captured_scope):
		self.arg_name = arg_name
		self.body = body
		self.captured_scope = dict(captured_scope or {})

	def call(self, value):
		next_scope = dict(self.captured_scope)
		next_scope[self.arg_name] = value
		return evaluate(self.body, next_scope)


def _resolve(name, scope=None):
	if scope and name in scope:
		return scope[name]
	if name in symbols:
		return symbols[name]
	raise NameError(f"Unbound variable {name}")


def match_case_pattern(pat, value):
	if isinstance(pat, NumberLiteral):
		pat = pat.value
	elif isinstance(pat, BoolLiteral):
		pat = pat.value
	elif isinstance(pat, IntPattern):
		pat = pat.value

	if isinstance(pat, bool):
		return value is pat, {}

	if type(pat) is int:
		return value == pat, {}

	if pat == "_" or isinstance(pat, WildcardPattern):
		return True, {}

	if isinstance(pat, VarPattern):
		return True, {pat.name: value}

	if isinstance(pat, dict) and "var" in pat:
		return True, {pat["var"]: value}

	if isinstance(pat, str):
		return True, {pat: value}

	return False, {}


def evaluate(ast, scope=None):
	if isinstance(ast, list):
		result = None
		for stmt in ast:
			result = evaluate(stmt, scope)
		return result

	if isinstance(ast, NumberLiteral):
		return ast.value

	if isinstance(ast, BoolLiteral):
		return ast.value

	if isinstance(ast, VarExpr):
		return _resolve(ast.name, scope)

	if isinstance(ast, IfExpr):
		cond = evaluate(ast.cond, scope)
		if type(cond) is not bool:
			raise TypeError("Condition of if must be Bool")
		if cond:
			return evaluate(ast.then_e, scope)
		return evaluate(ast.else_e, scope)

	if isinstance(ast, MatchExpr):
		scrutinee = evaluate(ast.expr, scope)
		for case in ast.cases:
			for pat in case.patterns:
				matched, bindings = match_case_pattern(pat, scrutinee)
				if not matched:
					continue

				next_scope = dict(scope or {})
				next_scope.update(bindings)
				return evaluate(case.expr, next_scope)

		raise ValueError("Non-exhaustive match and no case matched")

	# node objects handling below

	if isinstance(ast, bool) or isinstance(ast, int) or isinstance(ast, str):
		return ast

	# expressions as node classes
	# BinOp
	from ast_nodes import BinOp, UnaryOp, CallExpr, LetStmt, FunDef, Signature, Case

	if isinstance(ast, BinOp):
		left = evaluate(ast.left, scope)
		right = evaluate(ast.right, scope)
		op = ast.op
		if op == "+":
			return left + right
		if op == "-":
			return left - right
		if op == "*":
			return left * right
		if op == "/":
			return left / right
		if op == "<":
			return left < right
		if op == ">":
			return left > right
		if op == "<=":
			return left <= right
		if op == ">=":
			return left >= right
		if op == "==":
			return left == right
		if op == "!=":
			return left != right
		if op == "&&":
			return bool(left) and bool(right)
		if op == "||":
			return bool(left) or bool(right)

	if isinstance(ast, UnaryOp):
		if ast.op == 'neg':
			return -evaluate(ast.operand, scope)

	if isinstance(ast, CallExpr):
		fname = ast.name
		if fname in functions:
			arg_name, body = functions[fname]
			arg_value = evaluate(ast.arg, scope)
			next_scope = dict(scope or {})
			next_scope[arg_name] = arg_value
			return evaluate(body, next_scope)

		callee = _resolve(fname, scope)
		if not isinstance(callee, _Closure):
			raise TypeError(f"{fname} is not callable")
		arg_value = evaluate(ast.arg, scope)
		return callee.call(arg_value)

	if isinstance(ast, FunExpr):
		return _Closure(ast.arg, ast.body, scope)

	if isinstance(ast, LetExpr):
		value = evaluate(ast.expr, scope)
		next_scope = dict(scope or {})
		next_scope[ast.name] = value
		return evaluate(ast.body, next_scope)

	if isinstance(ast, LetStmt):
		value = evaluate(ast.expr, scope)
		symbols[ast.name] = value
		return value

	if isinstance(ast, FunDef):
		functions[ast.name] = (ast.arg, ast.expr)
		if ast.signature is not None:
			signatures[ast.name] = ast.signature
		return None

	if isinstance(ast, Signature):
		signatures[ast.name] = (ast.from_t, ast.to_t)
		return None

	# If we reach here, the node type is not recognized
	raise Exception("Unknown AST node")
