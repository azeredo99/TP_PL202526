import sys

from eval import evaluate
from grammar import parse


def main():
	if len(sys.argv) > 1:
		file_path = sys.argv[1]
		with open(file_path, "r", encoding="utf-8") as handle:
			source = handle.read().lstrip("\ufeff")

		try:
			ast = parse(source)
			result = evaluate(ast)
			if result is not None:
				print(result)
		except Exception as exc:
			print(f"Error: {exc}")
			raise SystemExit(1)
		return

	print("LFun D iniciado (Ctrl+C para sair)")

	while True:
		try:
			source = input(">> ")
			if not source.strip():
				continue

			try:
				ast = parse(source)
				result = evaluate(ast)
				if result is not None:
					print(result)
			except Exception as exc:
				print(f"Error: {exc}")
		except EOFError:
			break
		except KeyboardInterrupt:
			print("\nFim")
			break


if __name__ == "__main__":
	main()
