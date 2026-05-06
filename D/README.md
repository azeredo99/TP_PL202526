# Número D: Avaliação com Representação Intermédia e Suporte a Padrões

## Resumo da Solução

Este trabalho implementa a linguagem LFun com suporte robusto para:
- **Representação Intermédia (IR):** Todas as expressões e padrões são convertidos em instâncias de classes AST (`ast_nodes.py`) 
- **Padrões (Pattern Matching):** Suporte completo a padrões literais, alternativas, wildcard (`_`) e captura de variáveis.
- **Avaliação Genérica:** O evaluador (`eval.py`) opera exclusivamente sobre objetos AST, permitindo futuras transformações e gerações de código.

## Estrutura Implementada

### Ficheiros Principais

#### 1. `ast_nodes.py` (Representação Intermédia)
Classes para representar todas as construções da linguagem:
- **Literais:** `NumberLiteral`, `BoolLiteral`
- **Expressões:** `VarExpr`, `IfExpr`, `MatchExpr`, `BinOp`, `UnaryOp`, `CallExpr`
- **Padrões:** `IntPattern`, `WildcardPattern`, `VarPattern`
- **Definições:** `LetStmt`, `FunDef`, `Signature`
- **Casos de Match:** `Case`

#### 2. `parser.py` (Parser → AST)
- Converte texto em AST de forma genérica
- Suporta toda a gramática LFun (expressões, padrões, `when`/`if`, funções)
- Produz instâncias de `ast_nodes` (não dicionários)

#### 3. `eval.py` (Avaliador)
- Avalia AST de forma recursiva
- **Match Genérico:** padrões literais, alternativas, wildcard e captura de variáveis
- **Suporte a Funções:** definições `let name arg = expr`, chamadas `name(arg)`, assinaturas `fun name : type -> type`
- **Sem compatibilidade com dicionários:** código limpo e preparado para transformações futuras

#### 4. `lexer.py` (Análise Léxica)
- Tokeniza entrada conforme reservadas, operadores e literais
- Suporta comentários de linha (`--`) e blocos (`{- -}`)

#### 5. `main.py` (REPL)
- Interface interativa para testar a linguagem

### Ficheiros de Teste

#### `test_eval.py` (Testes Básicos)
Exemplos da documentação do trabalho (absoluto, eZero, avalia).

#### `test_eval_more.py` (Testes Extensivos)
Cobertura variada:
- Valores negativos, zero, positivos
- Padrões simples, alternativas múltiplas, wildcard
- Captura de variáveis e aritmética com padrões
- Nested match
- Casos não-exaustivos (com erro esperado)

#### `tests/test_eval_pytest.py` (Testes Automatizados)
Suite de testes pytest-style (compatível com runner manual).

#### `run_tests.py` (Test Runner)
Executor de testes sem dependência de pytest instalado.

## Conformidade com Requisitos

### ✅ Tópico D Completado

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Padrões (literal, alternativas, wildcard, captura) | ✅ Completo | `test_eval_more.py`: todos os tipos de padrão funcionam |
| Representação intermédia genérica | ✅ Completo | `ast_nodes.py`: classes para todas as construções |
| Avaliação sobre IR | ✅ Completo | `eval.py`: opera apenas em nós AST |
| Adaptabilidade (não apenas exemplos) | ✅ Completo | Suporte a casos genéricos além dos exemplos |
| Remoção de código duplicado | ✅ Completo | Sem fallback de dicionários em `eval.py` |

### Exemplos de Execução

```python
# Padrões simples
absoluto(-5) -> 5
eZero(0) -> True, eZero(1) -> False

# Alternativas
avalia(-1) -> True, avalia(0) -> False, avalia(2) -> True

# Captura de variável
id(123) -> 123, addOne(41) -> 42

# Wildcard
always42(999) -> 42

# Nested match
sign(-5) -> -1, sign(0) -> 0, sign(7) -> 1

# Padrões booleanos
boolToInt(true) -> 1, boolToInt(false) -> 0

# Erro não-exaustivo
onlyZero(1) -> ERROR: Non-exhaustive match and no case matched
```

## Como Testar

### Modo Interativo
```powershell
python -u D\main.py
```

### Testes Manuais
```powershell
python -u D\test_eval.py
python -u D\test_eval_more.py
```

### Testes Automatizados (sem pytest)
```powershell
python -u D\run_tests.py
```

## Pontos Fortes

1. **IR Genérica:** Representação limpa e sem mistura de tipos (AST classes only).
2. **Padrões Flexíveis:** Suporta todas as variações (literais, alternativas, wildcard, captura).
3. **Avaliação Robusta:** Trata corretamente scope, captura de variáveis e match não-exaustivo.
4. **Código Limpo:** Sem código duplicado ou fallbacks obsoletos.
5. **Testes Abrangentes:** Cobertura manual e automatizada de casos normais e edge-cases.

## Oportunidades Futuras

- Adicionar mais tipos de padrões (estruturas, listas)
- Implementar compilação para bytecode ou Python
- Otimizações baseadas em IR (inlining, dead code elimination)
- Type-checking estático baseado em assinaturas

## Conclusão

O trabalho cumpre totalmente o requisito D de "análise com representação intermédia genérica e geração de código preparada". A solução é extensível, testável e pronta para adaptação a novos requisitos.
