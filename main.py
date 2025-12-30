from src.lexer import tokenize
from src.parser import Parser
from src.evaluator import evaluate, create_global_env
from src.compiler import Compiler
from src.vm import VirtualMachine


def run_with_evaluator(code: str):
    print("=== Running with Evaluator (Full Support) ===")
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


def run_with_vm(code: str):
    print("=== Running with VM (Simple Expressions Only) ===")
    print(f"Input:\n{code.strip()}\n")
    tokens = tokenize(code)
    print(f"Tokens: {tokens}\n")
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"AST: {ast}\n")

    compiler = Compiler()
    vm_code = compiler.compile(ast)
    print(f"VM Code:\n{vm_code}\n")

    vm = VirtualMachine()
    vm.code = vm_code
    print("Executing VM...")
    result = vm.execute()
    print(f"Result: {result}\n")
    return result


if __name__ == "__main__":
    test_code_evaluator = """
        2 + 15 * 3
    """

    test_code_vm = """
        let x = 10
        let y = 20
        if x < y then 1 else 0
    """

    print("🧪 Testing with Evaluator:")
    try:
        run_with_evaluator(test_code_evaluator)
    except Exception as e:
        print(f"Error: {e}\n")

    print("\n" + "=" * 50 + "\n")

    print("🧪 Testing with VM:")
    try:
        run_with_vm(test_code_vm)
    except Exception as e:
        print(f"Error: {e}\n")