from typing import Any
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

def evaluate(node_or_nodes, env: Environment) -> Any:
    if isinstance(node_or_nodes, list):
        result = None
        for node in node_or_nodes:
            result = evaluate(node, env)
        return result

    if isinstance(node_or_nodes, NumberNode):
        return node_or_nodes.value

    elif isinstance(node_or_nodes, BinaryOpNode):
        left_val = evaluate(node_or_nodes.left, env)
        right_val = evaluate(node_or_nodes.right, env)
        if node_or_nodes.op == 'PLUS':
            return left_val + right_val
        elif node_or_nodes.op == 'MINUS':
            return left_val - right_val
        elif node_or_nodes.op == 'MUL':
            return left_val * right_val
        elif node_or_nodes.op == 'DIV':
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val // right_val
        elif node_or_nodes.op == 'EQUALS':
            return 1 if left_val == right_val else 0
        else:
            raise ValueError(f"Unknown operator: {node_or_nodes.op}")

    elif isinstance(node_or_nodes, IfNode):
        cond = evaluate(node_or_nodes.condition, env)
        if cond != 0:
            return evaluate(node_or_nodes.then_branch, env)
        else:
            return evaluate(node_or_nodes.else_branch, env)

    elif isinstance(node_or_nodes, FunctionNode):
        env.set(node_or_nodes.name, node_or_nodes)
        return None

    elif isinstance(node_or_nodes, CallNode):
        func = env.get(node_or_nodes.name)
        if not isinstance(func, FunctionNode):
            raise TypeError(f"{node_or_nodes.name} is not a function")
        args = [evaluate(arg, env) for arg in node_or_nodes.args]
        if len(args) != len(func.params):
            raise TypeError(f"Function {node_or_nodes.name} expected {len(func.params)} args, got {len(args)}")
        local_env = Environment(env)
        for param, arg in zip(func.params, args):
            local_env.set(param, arg)
        return evaluate(func.body, local_env)

    elif isinstance(node_or_nodes, VariableNode):
        return env.get(node_or_nodes.name)

    else:
        raise TypeError(f"Unknown node type: {type(node_or_nodes)}")