# Processamento de Linguagens - Projeto LFun

Este repositório contém a resolução do trabalho prático da unidade curricular de **Processamento de Linguagens** (2º Ano, 2º Semestre) do curso de **LESI** (Licenciatura em Engenharia de Sistemas Informáticos).

O objetivo principal deste projeto é desenvolver um analisador léxico, sintático e um interpretador/avaliador para a linguagem especificada no enunciado (**LFun**).

## Estrutura do Projeto

O projeto foi desenvolvido de forma incremental e está dividido em quatro pastas principais (A, B, C e D), correspondentes às fases da avaliação:

### [Parte A - Análise Léxica](./A/)
Construção do analisador léxico (**Lexer**).
- Identificação e extração de tokens da linguagem (palavras reservadas, operadores, literais).
- Suporte a comentários de linha (`--`) e de bloco (`{- -}`).
- Ficheiros: `lfun_lexer.py`, `lfun_lexer_test.py`

### [Parte B - Gramática Básica + AST Nodes](./B/)
Introdução da gramática e da representação intermédia básica.
- Gramática para expressões aritméticas, booleanas e definições `let`.
- Primeiros nós AST: `NumberLiteral`, `BoolLiteral`, `VarExpr`, `BinOp`, `UnaryOp`, `LetStmt`.
- Ficheiros: `lfun_lexer.py`, `ast_nodes.py`, `lfun_grammar.py`, `lfun_grammar_test.py`

### [Parte C - Gramática Completa](./C/)
Extensão da gramática com funções, condicionais e chamadas.
- Adicionadas regras para assinatura de função (`fun f : T -> T`), definição de função (`let f x = E`), condicional (`if ... then ... else`) e chamada (`f(E)`).
- Novos nós AST: `IfExpr`, `CallExpr`, `FunSig`, `FunDef`.
- Ficheiros: `lfun_lexer.py`, `ast_nodes.py`, `lfun_grammar.py`, `lfun_grammar_test.py`

### [Parte D - Avaliador Completo](./D/)
Fase final com avaliador e suporte a **Pattern Matching** (`when`).
- **AST completa:** todos os nós, incluindo `MatchExpr`, `Case`, `IntPattern`, `WildcardPattern`, `VarPattern`, `LetExpr`, `FunExpr`.
- **Pattern Matching:** blocos `when (expr) is ... end` com literais, alternativas múltiplas (`,`), wildcard (`_`) e captura de variáveis.
- **Avaliador desacoplado** (`eval.py`) que opera exclusivamente sobre a AST.
- **Ponto de entrada** (`main.py`) com modo interativo (REPL) e execução de ficheiros `.lfun`.
- Ficheiros: `lexer.py`, `ast_nodes.py`, `grammar.py`, `eval.py`, `main.py`, `test_eval.py`, `ex1.lfun`–`ex5.lfun`

## Tecnologias Utilizadas
- **Python 3**
- **PLY (Python Lex-Yacc):** Utilizado para a construção do Lexer e Parser.

## Como Executar

### Parte A — testar o lexer
```bash
cd A
python lfun_lexer_test.py
```

### Parte B — testar o parser básico
```bash
cd B
python lfun_grammar_test.py
```

### Parte C — testar o parser completo
```bash
cd C
python lfun_grammar_test.py
```

### Parte D — interpretador interativo (REPL)
```bash
cd D
python main.py
```

### Parte D — executar um ficheiro `.lfun`
```bash
cd D
python main.py ex1.lfun
```

### Parte D — executar os testes
```bash
cd D
python test_eval.py
```

## Funcionalidades da Linguagem (LFun)
- **Tipos Básicos:** Inteiros e Booleanos (`true`, `false`).
- **Operações:** Aritméticas (`+`, `-`, `*`, `/`), relacionais (`<`, `>`, `<=`, `>=`, `==`, `!=`) e lógicas (`&&`, `||`).
- **Definições:** Declaração de variáveis (`let x : Int = E`) e funções (`let f x = E`).
- **Assinaturas de tipo:** `fun f : Int -> Bool`
- **Condicionais:** `if E then E else E`
- **Pattern Matching (`when`):**
  - Casos com valores literais inteiros e booleanos.
  - Alternativas múltiplas no mesmo caso (`0, 1 -> ...`).
  - Wildcard (`_`) para captura de qualquer valor.
  - Captura de variáveis nos padrões.
