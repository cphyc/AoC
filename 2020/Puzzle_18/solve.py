TOKENS = {"+": "PLUS", "*": "TIMES", "(": "LPAREN", ")": "RPAREN", " ": None}


def parse(char):
    if char in TOKENS:
        return TOKENS[char]
    else:
        return int(char)


def parse_line(line):
    tokens = []
    for char in line:
        token = parse(char)
        if token:
            tokens.append(token)

    return iter(tokens)


def build_ast(tokens):
    ast = []
    for token in tokens:
        if token == "LPAREN":
            ast.append(build_ast(tokens))
        elif token == "RPAREN":
            return ["PLUS"] + ast + [None]
        else:
            ast.append(token)
    return ["PLUS"] + ast + [None]


def eval_ast(ast, acc=0):
    op = next(ast)
    if op is None:
        return acc

    rhs = next(ast)

    if isinstance(rhs, list):
        rhs = eval_ast(iter(rhs))

    if op == "PLUS":
        acc += rhs
    elif op == "TIMES":
        acc *= rhs
    return eval_ast(ast, acc)


def eval_ast2(ast, acc=0):
    for i, token, next_token in enumerate(ast):
        if token == "PLUS":
            pass


test_lines = (
    ("2 * 3 + (4 * 5)", 26),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
)

for line, expected, _ in test_lines:
    tokens = parse_line(line)
    ast = iter(build_ast(tokens))
    print(eval_ast(ast), expected)

total = 0
for line in open("input").readlines():
    line = line.strip()
    tokens = parse_line(line)
    ast = iter(build_ast(tokens))
    total += eval_ast(ast)

print(f"Total: {total}")
