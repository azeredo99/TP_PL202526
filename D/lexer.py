"""
    Processamento de Linguagens
    Licenciatura em Engenharia de Sistemas Informáticos
    2025/2026

    LFunLexer - Analisador Léxico para a linguagem LFun
"""
# lexer.py
import ply.lex as plex


class LFunLexer:

    # ─────────────────────────────────────────────
    #  PALAVRAS RESERVADAS
    #  Se um identificador for uma destas palavras,
    #  o seu tipo muda automaticamente
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
    #  Ordenadas da mais específica para a mais geral
    # ─────────────────────────────────────────────

    def t_COMMENT_BLOCK(self, t):
        r'\{-(.|\n)*?-\}'
        # Comentários multi-linha {- ... -}
        t.lexer.lineno += t.value.count('\n')
        # não retorna → token ignorado

    def t_COMMENT_LINE(self, t):
        r'--[^\n]*'
        pass  # não retorna → token ignorado

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        # não retorna → newlines ignoradas

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*'
        # Verifica se é palavra reservada; se não for, fica como ID
        t.type = LFunLexer.reserved.get(t.value, 'ID')
        return t

    # Tokens com múltiplos caracteres (têm de estar antes dos literais simples)
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
        print(f"[Erro Léxico] Caractere desconhecido '{t.value[0]}' na linha {t.lexer.lineno}")
        t.lexer.skip(1)

    # ─────────────────────────────────────────────
    #  BUILD e interface 
    # ─────────────────────────────────────────────

    def __init__(self):
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)

    def input(self, string):
        self.lexer.input(string)

    def token(self):
        return self.lexer.token()

    def __iter__(self):
        return self.lexer.__iter__()


# ─────────────────────────────────────────────
#  TESTE 
# ─────────────────────────────────────────────
if __name__ == '__main__':

    def testar(codigo):
        print(f"\n{'='*50}")
        print(f"Código: {codigo.strip()}")
        print(f"{'='*50}")
        lexer = LFunLexer()
        lexer.build()
        lexer.input(codigo)
        for tok in lexer:
            print(f"  {tok.type:<12} → {tok.value!r}")

    testar("3 + 4;")
    testar("let base : Int = 10;")
    testar("let ativo : Bool = true;")
    testar("fun dobro : Int -> Int;")
    testar("let dobro n = n * 2;")
    testar("if n < 0 then 0 - n else n;")
    testar("-- comentário de linha\nlet x : Int = 1;")
    testar("{- comentário\n   multi-linha -}\nlet y : Bool = false;")
    testar("3 == 3;")
    testar("3 != 4;")
    testar("3 <= 5;")
    testar("true && false;")
    testar("true || false;")
    testar("when (n) is\n  0 -> true;\n  _ -> false;\nend;")