from parser import parser
from lexer import lexer

print("LFun iniciado (Ctrl+C para sair)")

while True:
    try:
        s = input(">> ")
        if not s:
            continue
        parser.parse(s, lexer=lexer)
    except EOFError:
        break
    except KeyboardInterrupt:
        print("\nFim")
        break