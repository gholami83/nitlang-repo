from src.lexer import tokenize
from src.parser import Parser
from src.evaluator import evaluate, Environment

def run(code: str):
    print(f"Input:\n{code.strip()}\n")
    tokens = tokenize(code)
    print(f"Tokens: {tokens}\n")
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"AST: {ast}\n")

    env = Environment()
    result = evaluate(ast, env)
    print(f"Result: {result}\n")
    return result

if __name__ == "__main__":
    test_code = """
let base = 2

func power(exp) = {
    if exp == 0 then 1 else {
        let current = base
        current * power(exp - 1)
    }
}

func wrapper() = {
    let base = 3  
    power(2)  
}

wrapper()

    """

    try:
        run(test_code)
    except Exception as e:
        print(f"Error: {e}")