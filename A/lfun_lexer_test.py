"""
	Processamento de Linguagens
	Licenciatura em Engenharia de Sistemas Informáticos
	2025/2026
"""
# lfun_lexer_test.py
from lfun_lexer import LFunLexer

exemplos = [
	# expressões aritméticas
	"3 + 4;",
	"let base : Int = 10;",
	"let ativo : Bool = true;",
	# funções
	"fun dobro : Int -> Int;",
	"let dobro n = n * 2;",
	# condicional
	"if n < 0 then 0 - n else n;",
	# comentários (devem ser ignorados pelo lexer)
	"-- comentário de linha\nlet x : Int = 1;",
	"{- comentário\n   multi-linha -}\nlet y : Bool = false;",
	# operadores de comparação e lógicos
	"3 == 3;",
	"3 != 4;",
	"3 <= 5;",
	"true && false;",
	"true || false;",
	# when
	"when (n) is\n  0 -> true;\n  _ -> false;\nend;",
]

for frase in exemplos:
	print(f"----------------------")
	print(f"frase: '{frase.strip()}'")
	al = LFunLexer()
	al.build()
	al.input(frase)
	print('tokens: ', end="")
	while True:
		tk = al.token()
		if not tk:
			break
		print(tk.type, end=" ")
	print()