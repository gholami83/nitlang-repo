from src.lexer import tokenize
from src.parser import Parser
from src.evaluator import evaluate, create_global_env


def run(code: str):
    print(f"Input:\n{code.strip()}\n")
    tokens = tokenize(code)
    print(f"Tokens: {tokens}\n")
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"AST: {ast}\n")

    env = create_global_env()
    result = evaluate(ast, env)
    print(f"Result: {result}\n")
    return result


if __name__ == "__main__":
    test_code = """
    let nums = [1,2,3,4,5]
    map (lambda x -> x*2) nums
    """

    try:
        run(test_code)
    except Exception as e:
        print(f"Error: {e}")