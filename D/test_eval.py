from D.grammar import parse
from eval import evaluate


def run(src):
    try:
        ast = parse(src)
        result = evaluate(ast)
        print(f"{src.strip()} -> {result}")
    except Exception as e:
        print(f"{src.strip()} -> ERROR: {e}")

print('\n=== Tests: absoluto with varied values ===')
run("let absoluto n = if n < 0 then 0 - n else n;")
run("absoluto(-10);")
run("absoluto(0);")
run("absoluto(5);")

print('\n=== Tests: eZero with negatives/zero/positive ===')
run("let eZero n = when (n) is\n  0 -> true;\n  _ -> false;\nend;")
run("eZero(-1);")
run("eZero(0);")
run("eZero(1);")

print('\n=== Tests: avalia alternatives (more alternates) ===')
run("let avalia x = when (x) is\n  -2, -1, 1, 2 -> true;\n  0 -> false;\n  _ -> true;\nend;")
run("avalia(-2);")
run("avalia(-1);")
run("avalia(0);")
run("avalia(2);")

print('\n=== Tests: boolean patterns and bool->int ===')
run("let boolToInt b = when (b) is\n  true -> 1;\n  false -> 0;\nend;")
run("boolToInt(true);")
run("boolToInt(false);")

print('\n=== Tests: variable-pattern capture and arithmetic ===')
run("let addOne n = when (n) is\n  m -> m + 1;\nend;")
run("addOne(41);")

print('\n=== Tests: id via capture (returns same value) ===')
run("let id x = when (x) is\n  y -> y;\nend;")
run("id(123);")
run("id(true);")

print('\n=== Tests: wildcard-only match ===')
run("let always42 x = when (x) is\n  _ -> 42;\nend;")
run("always42(999);")

print('\n=== Tests: nested match example ===')
run("let sign n = when (n) is\n  0 -> 0;\n  _ -> when (n) is\n    m -> (if m < 0 then -1 else 1);\n  end;\nend;")
run("sign(-5);")
run("sign(0);")
run("sign(7);")

print('\n=== Tests: edge cases (large number, zero division check avoided) ===')
run("absoluto(1000000);")
run("absoluto(-1000000);")

print('\n=== Tests: non-exhaustive match (shows error) ===')
run("let onlyZero n = when (n) is\n  0 -> true;\nend;")
run("onlyZero(1);")