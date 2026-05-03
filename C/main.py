from parser import parser

print("LFun iniciado (Ctrl+C para sair)")

while True:
    try:
        s = input(">> ")
        if not s:
            continue
        parser.parse(s)
    except EOFError:
        break
    except KeyboardInterrupt:
        print("\nFim")
        break