"""
	Processamento de Linguagens
	Licenciatura em Engenharia de Sistemas Informáticos
	2025/2026
"""
# lfun_grammar_test.py
from lfun_grammar import LFunGrammar
from pprint import PrettyPrinter

pp = PrettyPrinter(sort_dicts=False)

lg = LFunGrammar()
lg.build()

exemplos = [
	# expressões aritméticas
	"3 + 4;",
	"10 - 2 * 3;",
	"(8 + 2) * 5;",
	# expressões booleanas
	"3 < 5;",
	"10 == 7;",
	"(4 + 1) == 5;",
	# definições let
	"let base : Int = 10;",
	"let ativo : Bool = true;",
	"let area : Int = 4 * 5;",
	# variáveis em expressões
	"let largura : Int = 8; let altura : Int = 5; let area : Int = largura * altura;",
]

for frase in exemplos:
	print(f"----------------------")
	print(f"--- frase '{frase.strip()}'")
	res = lg.parse(frase)
	print("resultado: ")
	pp.pprint(res)