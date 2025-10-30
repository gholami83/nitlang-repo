from typing import Dict, Any
from .ast_nodes import ASTNode, NumberNode, BinaryOpNode, FunctionNode, CallNode, IfNode, VariableNode

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}

    def get(self, name: str) -> Any:
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Name '{name}' is not defined")

    def set(self, name: str, value: Any):
        self.vars[name] = value

def evaluate(node: ASTNode, env: Environment) -> Any:
    if isinstance(node, NumberNode):
        return node.value

    elif isinstance(node, BinaryOpNode):
        left_val = evaluate(node.left, env)
        right_val = evaluate(node.right, env)
        if node.op == 'PLUS':
            return left_val + right_val
        elif node.op == 'MINUS':
            return left_val - right_val
        elif node.op == 'MUL':
            return left_val * right_val
        elif node.op == 'DIV':
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val // right_val
        else:
            raise ValueError(f"Unknown operator: {node.op}")

    elif isinstance(node, IfNode):
        cond = evaluate(node.condition, env)
        if cond:
            return evaluate(node.then_branch, env)
        else:
            return evaluate(node.else_branch, env)

    elif isinstance(node, FunctionNode):
        env.set(node.name, node)
        return None

    elif isinstance(node, CallNode):
        func = env.get(node.name)
        if not isinstance(func, FunctionNode):
            raise TypeError(f"{node.name} is not a function")
        args = [evaluate(arg, env) for arg in node.args]
        if len(args) != len(func.params):
            raise TypeError(f"Function {node.name} expected {len(func.params)} args, got {len(args)}")
        local_env = Environment(env)
        for param, arg in zip(func.params, args):
            local_env.set(param, arg)
        return evaluate(func.body, local_env)

    elif isinstance(node, VariableNode):
        return env.get(node.name)

    else:
        raise TypeError(f"Unknown node type: {type(node)}")