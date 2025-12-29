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
let global_factor = 2
let call_count = 0
let call_ref = ref call_count

let process = lambda x -> {
    call_ref := call_ref + 1
    x * global_factor
}

let numbers = [1, 2, 3, 4, 5]
let processed = map(process, numbers)

processed[0] + processed[1] + call_count
    """

    try:
        run(test_code)
    except Exception as e:
        print(f"Error: {e}")