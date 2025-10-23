from src.interpreter import Interpreter

if __name__ == "__main__":
    interp = Interpreter()
    print("NITLang (Phase 1-3)")
    print("Example: let x = 10")
    print("Example: #x + 5")
    print("Type 'exit' to quit.")
    while True:
        code = input(">>> ")
        if code.strip() == "exit":
            break
        interp.run(code)
