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
func outer() = {
    let z = 30
    func inner() = {
        z * 2
    }
    inner()
}
outer()
   
    """

    try:
        run(test_code)
    except Exception as e:
        print(f"Error: {e}")