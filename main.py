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

    if isinstance(result, bool):
        print_result = "true" if result else "false"
    else:
        print_result = result

    print(f"Result: {print_result}\n")
    return result


if __name__ == "__main__":
    test_code = """
class Point {
    let x:int
    let y:int
    let a:string 
    func move(dx, dy) = {
        x = x + dx
        y = y + dy
        a = "moved"
        a
    }
}

let p = new Point(2,3)
p.move(1,1)

    """

    try:
        run(test_code)
    except Exception as e:
        print(f"Error: {e}")