from src.lexer import tokenize
from src.parser import Parser
from src.compiler import Compiler
from src.vm import VirtualMachine


def run(code: str):
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
    test_code = """
    let x = 5
    let y = 10
    x + y
    """

    try:
        run(test_code)
    except Exception as e:
        print(f"Error: {e}")