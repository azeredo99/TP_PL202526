# Processamento de Linguagens - Projeto LFun

Este repositório contém a resolução do trabalho prático da unidade curricular de **Processamento de Linguagens** (2º Ano, 2º Semestre) do curso de **LESI** (Licenciatura em Engenharia de Sistemas Informáticos).

O objetivo principal deste projeto é desenvolver um analisador léxico, sintático e um interpretador/avaliador para a linguagem especificada no enunciado (**LFun**).

## 🗂 Estrutura do Projeto

O projeto foi desenvolvido de forma incremental e está dividido em quatro pastas principais (A, B, C e D), correspondentes às fases da avaliação:

### 📁 [Parte A - Análise Léxica](./A/)
Foco na construção do analisador léxico (**Lexer**).
- Identificação e extração de tokens da linguagem (palavras reservadas, operadores, literais).
- Suporte a comentários de linha (`--`) e de bloco (`{- -}`).

### 📁 [Parte B - Análise Sintática](./B/)
Foco na construção da gramática e do analisador sintático (**Parser**).
- Definição da gramática da linguagem utilizando a ferramenta PLY (Python Lex-Yacc).
- Verificação sintática das expressões e validação estrutural.

### 📁 [Parte C - Avaliação Básica](./C/)
Integração do parser com um sistema inicial de avaliação.
- Interpretador capaz de analisar e avaliar as expressões de forma integrada.

### 📁 [Parte D - Representação Intermédia e Padrões](./D/)
A fase final e mais avançada do projeto. Introduz uma **Representação Intermédia (IR)** sob a forma de uma Árvore de Sintaxe Abstrata (AST) e suporte avançado a **Pattern Matching**.
- **Representação Intermédia Genérica:** Separa a fase de parsing da execução. As instruções são convertidas em nós AST (`ast_nodes.py`).
- **Pattern Matching Robusto:** Suporte completo a blocos `match`, permitindo validações por literais, alternativas, wildcards (`_`) e captura de variáveis.
- **Avaliador Desacoplado:** Avaliação das instruções (`eval.py`) operando exclusivamente sobre a AST.

## 🛠 Tecnologias Utilizadas
- **Python 3**
- **PLY (Python Lex-Yacc):** Utilizado para a construção do Lexer e Parser.

## 🚀 Como Executar

A versão mais completa e funcional do projeto encontra-se na **Parte D**. Para testar o interpretador de forma interativa (REPL), execute no diretório principal:

```bash
python D/main.py
```

### Executar os Testes

Para garantir que tudo funciona como esperado (com foco na Parte D), pode executar os ficheiros de testes disponibilizados:

```bash
# Testes básicos das expressões e funções base
python D/test_eval.py

# Testes extensivos (Pattern matching, captura de variáveis, múltiplos casos, etc.)
python D/test_eval_more.py

# Test Runner automatizado da Parte D
python D/run_tests.py
```

## ✨ Funcionalidades da Linguagem (LFun)
- **Tipos Básicos:** Inteiros numéricos e Booleanos (`true`, `false`).
- **Operações:** Aritméticas e relacionais completas.
- **Definições:** Declaração de funções e expressões usando `let`.
- **Condicionais:** Estruturas de decisão `if ... then ... else`.
- **Pattern Matching (`match`):**
  - Casos com valores literais.
  - Alternativas múltiplas.
  - Wildcards/omissão (`_`).
  - Captura e utilização de variáveis nos padrões.
