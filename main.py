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
let call_count = 0
let count_ref = ref call_count

func max(a, b) = 
    if a >= b then a else b

func factorial_with_tracking(n) = {
    count_ref := count_ref + 1
    if n <= 1 then 1 else {
        n * factorial_with_tracking(n - 1)
    }
}

let global_x = 100

func scope_demo() = {
    let local_y = 200
    let global_x = 300  
    if global_x > 250 then {
        let temp_ref = ref global_x
        temp_ref := temp_ref + local_y
        global_x
    } else 0
}

let fact_result = factorial_with_tracking(5)
let scope_result = scope_demo()
let max_result = max(75, 90)
let count_final = call_count

let final = (fact_result * 100) + (scope_result * 10) + max_result + count_final
final

    """

    try:
        run(test_code)
    except Exception as e:
        print(f"Error: {e}")