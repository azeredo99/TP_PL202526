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
	# ── Fase B (ainda funciona)─────
	"3 + 4;",
	"10 - 2 * 3;",
	"(8 + 2) * 5;",
	"3 < 5;",
	"let base : Int = 10;",
	"let ativo : Bool = true;",
	# ── assinatura de função ─────────────
	"fun dobro : Int -> Int;",
	# ── definição de função ──────────────
	"let dobro n = n * 2;",
	# ── chamada de função ─────────────────
	"dobro(7);",
	# ── função com Bool ───────────────────
	"fun ePositivo : Int -> Bool;",
	"let ePositivo n = n > 0;",
	"ePositivo(3);",
	"ePositivo(-2);",
	# ── função com if ─────────────────────
	"fun absoluto : Int -> Int;",
	"let absoluto n = if n < 0 then 0 - n else n;",
	"absoluto(-5);",
	"absoluto(8);",
	# ── programa completo ─────────────────
	"""
	fun dobro : Int -> Int;
	let dobro n = n * 2;
	dobro(7);
	""",
]

for frase in exemplos:
	print(f"----------------------")
	print(f"--- frase '{frase.strip()}'")
	res = lg.parse(frase)
	print("resultado: ")
	pp.pprint(res)