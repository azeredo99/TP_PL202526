import sys

import ply.yacc as yacc

from lexer import LFunLexer
from ast_nodes import (
	NumberLiteral,
	BoolLiteral,
	VarExpr,
	IfExpr,
	MatchExpr,
	Case,
	IntPattern,
	WildcardPattern,
	VarPattern,
	BinOp,
	UnaryOp,
	CallExpr,
	LetStmt,
	LetExpr,
	FunExpr,
	FunDef,
	Signature,
)


tokens = LFunLexer.tokens
start = "program"

_parser = None
parser = None

precedence = (
	("left", "OR"),
	("left", "AND"),
	("left", "EQ", "NEQ"),
	("left", "<", ">", "LE", "GE"),
	("left", "+", "-"),
	("left", "*", "/"),
	("right", "UMINUS"),
)


def p_program_single(p):
	"program : statement"
	p[0] = [p[1]]


def p_program_multi(p):
	"program : program statement"
	p[0] = p[1] + [p[2]]


def p_statement_expr(p):
	"""statement : expr opt_semi"""
	p[0] = p[1]


def p_statement_let_typed(p):
	"""statement : LET ID ':' type '=' expr opt_semi"""
	p[0] = LetStmt(p[2], p[4], p[6])


def p_statement_fun_def(p):
	"""statement : LET ID ID '=' expr opt_semi"""
	p[0] = FunDef(p[2], p[3], p[5])


def p_statement_fun_signature(p):
	"""statement : FUN ID ':' type ARROW type opt_semi"""
	p[0] = Signature(p[2], p[4], p[6])


def p_opt_semi_present(p):
	"opt_semi : ';'"


def p_opt_semi_empty(p):
	"opt_semi :"


def p_type_int(p):
	"type : TINT"
	p[0] = "Int"


def p_type_bool(p):
	"type : TBOOL"
	p[0] = "Bool"


def p_expr_binop(p):
	"""expr : expr '+' expr
			| expr '-' expr
			| expr '*' expr
			| expr '/' expr
			| expr '<' expr
			| expr '>' expr
			| expr LE expr
			| expr GE expr
			| expr EQ expr
			| expr NEQ expr
			| expr AND expr
			| expr OR expr"""
	p[0] = BinOp(p[2], p[1], p[3])


def p_expr_uminus(p):
	"expr : '-' expr %prec UMINUS"
	p[0] = UnaryOp('neg', p[2])


def p_expr_group(p):
	"expr : '(' expr ')'"
	p[0] = p[2]


def p_expr_let_in(p):
	"expr : LET ID '=' expr IN expr"
	p[0] = LetExpr(p[2], p[4], p[6])


def p_expr_fun(p):
	"expr : FUN '(' ID ':' type ')' ARROW expr"
	p[0] = FunExpr(p[3], p[5], p[8])


def p_expr_call(p):
	"expr : ID '(' expr ')'"
	p[0] = CallExpr(p[1], p[3])


def p_expr_if(p):
	"expr : IF expr THEN expr ELSE expr"
	p[0] = IfExpr(p[2], p[4], p[6])


def p_expr_when(p):
	"expr : WHEN '(' expr ')' IS case_list END"
	p[0] = MatchExpr(p[3], p[6])


def p_expr_when_braces(p):
	"expr : WHEN expr '{' case_list '}'"
	p[0] = MatchExpr(p[2], p[4])


def p_expr_number(p):
	"expr : NUMBER"
	p[0] = NumberLiteral(p[1])


def p_expr_true(p):
	"expr : TRUE"
	p[0] = BoolLiteral(True)


def p_expr_false(p):
	"expr : FALSE"
	p[0] = BoolLiteral(False)


def p_expr_id(p):
	"expr : ID"
	p[0] = VarExpr(p[1])


def p_case_list_multi(p):
	"case_list : case_list case"
	p[0] = p[1] + [p[2]]


def p_case_list_single(p):
	"case_list : case"
	p[0] = [p[1]]


def p_case(p):
	"case : pattern_list ARROW expr ';'"
	p[0] = Case(p[1], p[3])


def p_pattern_list_multi(p):
	"pattern_list : pattern_list ',' pattern"
	p[0] = p[1] + [p[3]]


def p_pattern_list_single(p):
	"pattern_list : pattern"
	p[0] = [p[1]]


def p_pattern_number(p):
	"pattern : NUMBER"
	p[0] = IntPattern(p[1])


def p_pattern_negative_number(p):
	"pattern : '-' NUMBER"
	p[0] = IntPattern(-p[2])


def p_pattern_true(p):
	"pattern : TRUE"
	p[0] = BoolLiteral(True)


def p_pattern_false(p):
	"pattern : FALSE"
	p[0] = BoolLiteral(False)


def p_pattern_wildcard(p):
	"pattern : '_'"
	p[0] = WildcardPattern()


def p_pattern_id(p):
	"pattern : ID"
	p[0] = VarPattern(p[1])


def p_error(p):
	if p:
		raise SyntaxError(f"Syntax error at token {p.type}({p.value}) line {p.lineno}")
	raise SyntaxError("Syntax error at EOF")


def build(**kwargs):
	global _parser, parser
	_parser = yacc.yacc(module=sys.modules[__name__], write_tables=False, debug=False, **kwargs)
	parser = _parser
	return _parser


def parse(text):
	global _parser
	if _parser is None:
		build()

	lexer = LFunLexer()
	lexer.build()
	return _parser.parse(text, lexer=lexer.lexer)


build()


