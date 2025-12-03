from typing import Any
from .ast_nodes import ASTNode, NumberNode, StringNode, BoolNode, BinaryOpNode, AssignNode, FunctionNode, CallNode, \
    IfNode, VariableNode, LetNode, BlockNode, RefNode, AssignRefNode, ClassNode, NewNode, MethodCallNode


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}
        self.objects = {}

    def get(self, name: str) -> Any:
        if name in self.vars:
            return self.vars[name]
        if name in self.objects:
            return self.objects[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Name '{name}' is not defined")

    def set(self, name: str, value: Any):
        self.vars[name] = value

    def set_object(self, name: str, obj: Any):
        self.objects[name] = obj

    def get_var_ref(self, name: str):
        if name in self.vars:
            return (self, name)
        if name in self.objects:
            return (self, name)
        if self.parent:
            return self.parent.get_var_ref(name)
        raise NameError(f"Name '{name}' is not defined")


class ClassInstance:
    def __init__(self, class_name: str, env: Environment):
        self.class_name = class_name
        self.env = env


def evaluate(node_or_nodes, env: Environment) -> Any:
    if isinstance(node_or_nodes, list):
        result = None
        for node in node_or_nodes:
            result = evaluate(node, env)
        return result

    if isinstance(node_or_nodes, NumberNode):
        return node_or_nodes.value

    elif isinstance(node_or_nodes, StringNode):
        return node_or_nodes.value

    elif isinstance(node_or_nodes, BoolNode):
        return node_or_nodes.value

    elif isinstance(node_or_nodes, AssignNode):
        value = evaluate(node_or_nodes.value, env)
        env.set(node_or_nodes.name, value)
        return value

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

    elif isinstance(node_or_nodes, ClassNode):
        env.set_object(node_or_nodes.name, node_or_nodes)
        return None

    elif isinstance(node_or_nodes, NewNode):
        cls = env.get(node_or_nodes.class_name)
        if not isinstance(cls, ClassNode):
            raise TypeError(f"{node_or_nodes.class_name} is not a class")

        obj_env = Environment(env)
        for i, field in enumerate(cls.fields):
            if i < len(node_or_nodes.args):
                obj_env.set(field.name, evaluate(node_or_nodes.args[i], env))
            else:
                obj_env.set(field.name, 0)

        instance = ClassInstance(cls.name, obj_env)
        return instance

    elif isinstance(node_or_nodes, MethodCallNode):
        obj = evaluate(node_or_nodes.obj, env)
        if not isinstance(obj, ClassInstance):
            raise TypeError("Object must be an instance of a class")

        cls = env.get(obj.class_name)
        if not isinstance(cls, ClassNode):
            raise TypeError(f"Class {obj.class_name} not found")

        method = cls.methods.get(node_or_nodes.method_name)
        if not method:
            raise AttributeError(f"Method '{node_or_nodes.method_name}' not found")

        local_env = Environment(obj.env)
        args = [evaluate(arg, env) for arg in node_or_nodes.args]
        for param, arg in zip(method.params, args):
            local_env.set(param, arg)

        return evaluate(method.body, local_env)

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
                if not isinstance(value, bool):
                    raise TypeError(f"Expected bool (true/false), got {type(value).__name__}")
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

        def resolve_ref(current_env, name):
            try:
                value = current_env.get(name)
                if isinstance(value, tuple) and len(value) == 2:
                    target_env, target_name = value
                    try:
                        next_value = target_env.get(target_name)
                        if isinstance(next_value, tuple) and len(next_value) == 2:
                            return resolve_ref(target_env, target_name)
                        else:
                            return (target_env, target_name)
                    except:
                        return (target_env, target_name)
                else:
                    return (current_env, name)
            except:
                return (current_env, name)

        try:
            target_env, target_name = resolve_ref(env, left_node.name)
            new_value = evaluate(node_or_nodes.value, env)
            target_env.set(target_name, new_value)
        except Exception as e:
            raise TypeError(f"Cannot assign to reference '{left_node.name}': {e}")

        return None

    else:
        raise TypeError(f"Unknown node type: {type(node_or_nodes)}")