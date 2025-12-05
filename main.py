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
let global_counter = 0
let str_global = "global"

let counter_ref = ref global_counter

func factorial(n) = {
    counter_ref := counter_ref + 1
    if n <= 1 then 1 else n * factorial(n - 1)
}

class BankAccount {
    let balance:int
    let owner:string
    let transaction_count:int
    
    func deposit(amount) = {
        balance = balance + amount
        transaction_count = transaction_count + 1
        
        counter_ref := counter_ref + 1
        balance
    }
    
    func withdraw(amount) = {
        if balance >= amount then {
            balance = balance - amount
            transaction_count = transaction_count + 1
            balance
        } else {
            let msg:string = "error"
            msg
        }
    }
    
    func get_balance() = balance
    func get_owner() = owner
    func get_transactions() = transaction_count
}

let account1 = new BankAccount(1000, "Alice", 0)
let account2 = new BankAccount(500, "Bob", 0)

account1.deposit(200)
account1.withdraw(100)
account2.deposit(300)

let total_balance = account1.get_balance() + account2.get_balance()
let total_transactions = account1.get_transactions() + account2.get_transactions()

let fact_result = factorial(4)  

let final_result = (total_balance * 10) + (total_transactions * 100) + fact_result + global_counter
final_result
    """

    try:
        run(test_code)
    except Exception as e:
        print(f"Error: {e}")