from eval import evaluate
from parser import parse


def main():
	print("LFun D iniciado (Ctrl+C para sair)")

	while True:
		try:
			source = input(">> ")
			if not source.strip():
				continue

			ast = parse(source)
			result = evaluate(ast)
			if result is not None:
				print(result)
		except EOFError:
			break
		except KeyboardInterrupt:
			print("\nFim")
			break


if __name__ == "__main__":
	main()
