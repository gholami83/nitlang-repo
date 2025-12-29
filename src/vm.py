class VMInstruction:
    def __init__(self, op: str, operand=None):
        self.op = op
        self.operand = operand

    def __repr__(self):
        if self.operand is not None:
            return f"{self.op} {self.operand}"
        return self.op

class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.env = {}
        self.code = []

    def load(self, value):
        self.stack.append(value)

    def add(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    def sub(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)

    def mul(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a * b)

    def div(self):
        b = self.stack.pop()
        a = self.stack.pop()
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        self.stack.append(a / b)

    def print(self):
        result = self.stack.pop()
        print(result)
        return result

    def store(self, name):
        self.env[name] = self.stack.pop()

    def load_var(self, name):
        self.stack.append(self.env[name])

    def execute(self):
        for inst in self.code:
            if inst.op == 'LOAD':
                self.load(inst.operand)
            elif inst.op == 'ADD':
                self.add()
            elif inst.op == 'SUB':
                self.sub()
            elif inst.op == 'MUL':
                self.mul()
            elif inst.op == 'DIV':
                self.div()
            elif inst.op == 'PRINT':
                self.print()
            elif inst.op == 'STORE':
                self.store(inst.operand)
            elif inst.op == 'LOAD_VAR':
                self.load_var(inst.operand)
            else:
                raise ValueError(f"Unknown instruction: {inst}")