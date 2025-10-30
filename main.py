
from src.lexer import tokenize
from src.parser import Parser
from src.evaluator import evaluate

def run(expression: str):
    print(f"Input: {expression}")
    tokens = tokenize(expression)
    print(f"Tokens: {tokens}")
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"AST: {ast}")
    result = evaluate(ast)
    print(f"Result: {result}")
    return result

if __name__ == "__main__":
    # تست‌های نمونه
    test_cases = [
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "10 - 2 / 2",
        "5 * (3 + 2) - 1"
    ]

    for expr in test_cases:
        try:
            run(expr)
            print("-" * 40)
        except Exception as e:
            print(f"Error: {e}")
            print("-" * 40)