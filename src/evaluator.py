
from typing import Any
from .ast_nodes import ASTNode, NumberNode, BinaryOpNode, FunctionNode, CallNode, IfNode, VariableNode, LetNode, \
    BlockNode, RefNode, AssignRefNode


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

    def get_var_ref(self, name: str):
        if name in self.vars:
            return (self, name)
        if self.parent:
            return self.parent.get_var_ref(name)
        raise NameError(f"Name '{name}' is not defined")


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
        has_float = isinstance(left_val, float) or isinstance(right_val, float)

        if node_or_nodes.op == 'PLUS':
            result = left_val + right_val
            return float(result) if has_float else result
        elif node_or_nodes.op == 'MINUS':
            result = left_val - right_val
            return float(result) if has_float else result
        elif node_or_nodes.op == 'MUL':
            result = left_val * right_val
            return float(result) if has_float else result
        elif node_or_nodes.op == 'DIV':
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val / right_val
        elif node_or_nodes.op == 'EQUALS':
            return 1 if left_val == right_val else 0
        elif node_or_nodes.op == 'NOT_EQUALS':
            return 1 if left_val != right_val else 0
        elif node_or_nodes.op == 'LESS':
            return 1 if left_val < right_val else 0
        elif node_or_nodes.op == 'LESS_EQ':
            return 1 if left_val <= right_val else 0
        elif node_or_nodes.op == 'GREATER':
            return 1 if left_val > right_val else 0
        elif node_or_nodes.op == 'GREATER_EQ':
            return 1 if left_val >= right_val else 0
        else:
            raise ValueError(f"Unknown operator: {node_or_nodes.op}")

    elif isinstance(node_or_nodes, IfNode):
        cond = evaluate(node_or_nodes.condition, env)
        if cond != 0:
            return evaluate(node_or_nodes.then_branch, env)
        else:
            return evaluate(node_or_nodes.else_branch, env)

    elif isinstance(node_or_nodes, FunctionNode):
        func_with_env = FunctionNode(
            node_or_nodes.name,
            node_or_nodes.params,
            node_or_nodes.body,
            env
        )
        env.set(node_or_nodes.name, func_with_env)
        return None

    elif isinstance(node_or_nodes, CallNode):
        func = env.get(node_or_nodes.name)
        if not isinstance(func, FunctionNode):
            raise TypeError(f"{node_or_nodes.name} is not a function")
        args = [evaluate(arg, env) for arg in node_or_nodes.args]
        if len(args) != len(func.params):
            raise TypeError(f"Function {node_or_nodes.name} expected {len(func.params)} args, got {len(args)}")

        local_env = Environment(func.closure_env)
        for param, arg in zip(func.params, args):
            local_env.set(param, arg)
        return evaluate(func.body, local_env)

    elif isinstance(node_or_nodes, VariableNode):
        value = env.get(node_or_nodes.name)

        def resolve_value(val, depth=0):
            if depth > 10:
                raise RuntimeError("Reference chain too deep")
            if isinstance(val, tuple) and len(val) == 2:
                target_env, target_name = val
                actual_value = target_env.get(target_name)
                return resolve_value(actual_value, depth + 1)
            return val

        return resolve_value(value)

    elif isinstance(node_or_nodes, LetNode):
        value = evaluate(node_or_nodes.value, env)

        if node_or_nodes.type_node:
            expected_type = node_or_nodes.type_node.type_name
            if expected_type == 'int':
                if not isinstance(value, int):
                    raise TypeError(f"Expected int, got {type(value).__name__}")
            elif expected_type == 'bool':
                if not isinstance(value, int):
                    raise TypeError(f"Expected bool (as int), got {type(value).__name__}")
            elif expected_type == 'string':
                if not isinstance(value, str):
                    raise TypeError(f"Expected string, got {type(value).__name__}")

        env.set(node_or_nodes.name, value)
        return None

    elif isinstance(node_or_nodes, BlockNode):
        local_env = Environment(env)
        result = None
        for stmt in node_or_nodes.statements:
            result = evaluate(stmt, local_env)
        return result

    elif isinstance(node_or_nodes, RefNode):
        return env.get_var_ref(node_or_nodes.name)

    elif isinstance(node_or_nodes, AssignRefNode):
        left_node = node_or_nodes.ref
        if not isinstance(left_node, VariableNode):
            raise TypeError("Left side of ':=' must be a variable")

        ref_value = env.get(left_node.name)
        if not isinstance(ref_value, tuple) or len(ref_value) != 2:
            raise TypeError(f"'{left_node.name}' is not a reference")

        target_env, target_name = ref_value
        new_value = evaluate(node_or_nodes.value, env)
        target_env.set(target_name, new_value)
        return None

    else:
        raise TypeError(f"Unknown node type: {type(node_or_nodes)}")