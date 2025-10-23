from .parser import Parser
from .environment import Environment

class Interpreter:
    def __init__(self):
        self.parser = Parser()
        self.env = Environment()

    def eval_expr(self, expr):
        return self.parser.parse(expr)

    def eval_stmt(self, stmt):
        if stmt.startswith("let"):
            _, name, _, expr = stmt.split(" ", 3)
            value = self.eval_expr(expr)
            self.env.set(name, value)
            return value
        else:
            return self.eval_expr(stmt)

    def run(self, code):
        lines = [l.strip() for l in code.split('\n') if l.strip()]
        for line in lines:
            if line.startswith("#"):
                expr = line[1:].strip()
                print(self.eval_expr(expr))
            else:
                self.eval_stmt(line)
