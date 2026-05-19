"""
	Processamento de Linguagens
	Licenciatura em Engenharia de Sistemas Informáticos
	2025/2026

	LFunLexer - Analisador Léxico para a linguagem LFun
"""
# lfun_lexer.py
import ply.lex as plex


class LFunLexer:

	# ─────────────────────────────────────────────
	#  PALAVRAS RESERVADAS
	#  Se um identificador for uma destas palavras,
	#  o seu tipo muda automaticamente (ver t_ID)
	# ─────────────────────────────────────────────
	reserved = {
		'let'   : 'LET',
		'in'    : 'IN',
		'fun'   : 'FUN',
		'if'    : 'IF',
		'then'  : 'THEN',
		'else'  : 'ELSE',
		'when'  : 'WHEN',
		'is'    : 'IS',
		'end'   : 'END',
		'true'  : 'TRUE',
		'false' : 'FALSE',
		'int'   : 'TINT',
		'bool'  : 'TBOOL',
		'Int'   : 'TINT',
		'Bool'  : 'TBOOL',
	}

	# ─────────────────────────────────────────────
	#  TOKENS
	#  Tudo o que o lexer pode reconhecer.
	#  Os literais (caracteres simples) ficam à parte.
	# ─────────────────────────────────────────────
	tokens = (
		'NUMBER',     # inteiros: 0, 1, 42, ...
		'ID',         # identificadores: x, base, dobro, ...
		'EQ',         # ==
		'NEQ',        # !=
		'LE',         # <=
		'GE',         # >=
		'AND',        # &&
		'OR',         # ||
		'ARROW',      # ->
	) + tuple(dict.fromkeys(reserved.values()))

	# Literais: caracteres simples reconhecidos diretamente
	literals = ['+', '-', '*', '/', '<', '>',
				'=', ':', ';', ',', '(', ')', '_', '{', '}']

	# Espaços e tabs ignorados
	t_ignore = ' \t'

	# ─────────────────────────────────────────────
	#  REGRAS COM FUNÇÕES
	# ─────────────────────────────────────────────

	def t_COMMENT_BLOCK(self, t):
		r'\{-(.|\n)*?-\}'
		# Comentários multi-linha {- ... -}
		# conta newlines para o número de linha ficar correto
		t.lexer.lineno += t.value.count('\n')
  

	def t_COMMENT_LINE(self, t):
		r'--[^\n]*'
		# Comentários de linha -- ...
		pass  # não retorna → token ignorado

	def t_newline(self, t):
		r'\n+'
		# atualiza o número de linha
		t.lexer.lineno += len(t.value)
		# não retorna → newlines ignoradas

	def t_NUMBER(self, t):
		r'\d+'
		# converte string "42" para inteiro 42
		t.value = int(t.value)
		return t

	def t_ID(self, t):
		r'[a-zA-Z][a-zA-Z0-9_]*'
		# verifica se é palavra reservada
		# se não for, fica como ID
		t.type = LFunLexer.reserved.get(t.value, 'ID')
		return t

	# tokens com múltiplos caracteres
	# têm de estar antes dos literais simples
	def t_EQ(self, t):
		r'=='
		return t

	def t_NEQ(self, t):
		r'!='
		return t

	def t_LE(self, t):
		r'<='
		return t

	def t_GE(self, t):
		r'>='
		return t

	def t_AND(self, t):
		r'&&'
		return t

	def t_OR(self, t):
		r'\|\|'
		return t

	def t_ARROW(self, t):
		r'->'
		return t

	def t_error(self, t):
		print(f"[Erro Léxico] Caractere inesperado '{t.value[0]}' na linha {t.lexer.lineno}")
		t.lexer.skip(1)

	# ─────────────────────────────────────────────
	#  BUILD e interface do lexer
	# ─────────────────────────────────────────────

	def __init__(self):
		self.lexer = None

	def build(self, **kwargs):
		# inicializa o analisador léxico
		self.lexer = plex.lex(module=self, **kwargs)

	def input(self, string):
		# define o texto de entrada
		self.lexer.input(string)

	def token(self):
		# determina o próximo token
		return self.lexer.token()

	def __iter__(self):
		return self.lexer.__iter__()