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

    def equals(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(1 if a == b else 0)

    def not_equals(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(1 if a != b else 0)

    def less(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(1 if a < b else 0)

    def less_eq(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(1 if a <= b else 0)

    def greater(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(1 if a > b else 0)

    def greater_eq(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(1 if a >= b else 0)

    def print(self):
        result = self.stack.pop()
        print(result)
        return result

    def store(self, name):
        self.env[name] = self.stack.pop()

    def load_var(self, name):
        self.stack.append(self.env[name])

    def jump(self, target):
        return target

    def jump_if_zero(self, target):
        condition = self.stack.pop()
        if condition == 0:
            return target
        return None

    def jump_if_not_zero(self, target):
        condition = self.stack.pop()
        if condition != 0:
            return target
        return None

    def execute(self):
        ip = 0
        last_result = None

        while ip < len(self.code):
            inst = self.code[ip]

            if inst.op == 'LOAD':
                self.load(inst.operand)
                ip += 1
            elif inst.op == 'ADD':
                self.add()
                ip += 1
            elif inst.op == 'SUB':
                self.sub()
                ip += 1
            elif inst.op == 'MUL':
                self.mul()
                ip += 1
            elif inst.op == 'DIV':
                self.div()
                ip += 1
            elif inst.op == 'EQUALS':
                self.equals()
                ip += 1
            elif inst.op == 'NOT_EQUALS':
                self.not_equals()
                ip += 1
            elif inst.op == 'LESS':
                self.less()
                ip += 1
            elif inst.op == 'LESS_EQ':
                self.less_eq()
                ip += 1
            elif inst.op == 'GREATER':
                self.greater()
                ip += 1
            elif inst.op == 'GREATER_EQ':
                self.greater_eq()
                ip += 1
            elif inst.op == 'PRINT':
                last_result = self.print()
                ip += 1
            elif inst.op == 'STORE':
                self.store(inst.operand)
                ip += 1
            elif inst.op == 'LOAD_VAR':
                self.load_var(inst.operand)
                ip += 1
            elif inst.op == 'JMP':
                ip = inst.operand
            elif inst.op == 'JZ':
                target = self.jump_if_zero(inst.operand)
                if target is not None:
                    ip = target
                else:
                    ip += 1
            elif inst.op == 'JNZ':
                target = self.jump_if_not_zero(inst.operand)
                if target is not None:
                    ip = target
                else:
                    ip += 1
            else:
                raise ValueError(f"Unknown instruction: {inst}")

        return last_result