from typing import Any
from .ast_nodes import ASTNode, NumberNode, StringNode, BinaryOpNode, FunctionNode, CallNode, IfNode, VariableNode, \
    LetNode, BlockNode, RefNode, AssignRefNode, AssignNode, ClassNode, NewNode, MethodCallNode, FieldAccessNode, \
    ArrayNode, LambdaNode, IndexNode


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


class ObjectInstance:
    def __init__(self, class_name: str, fields: dict, methods: dict):
        self.class_name = class_name
        self.fields = fields
        self.methods = methods


def evaluate(node_or_nodes, env: Environment) -> Any:
    if isinstance(node_or_nodes, list):
        result = None
        for node in node_or_nodes:
            result = evaluate(node, env)
        return result

    if isinstance(node_or_nodes, ArrayNode):
        return [evaluate(elem, env) for elem in node_or_nodes.elements]

    if isinstance(node_or_nodes, LambdaNode):
        def lambda_func(args):
            local_env = Environment(env)
            local_env.set(node_or_nodes.param, args[0])
            return evaluate(node_or_nodes.body, local_env)

        return lambda_func

    if isinstance(node_or_nodes, IndexNode):
        array_val = evaluate(node_or_nodes.array, env)
        index_val = evaluate(node_or_nodes.index, env)

        if not isinstance(array_val, list):
            raise TypeError("Indexing only supported on arrays")
        if not isinstance(index_val, int):
            raise TypeError("Array index must be an integer")
        if index_val < 0 or index_val >= len(array_val):
            raise IndexError(f"Array index {index_val} out of bounds")

        return array_val[index_val]

    if isinstance(node_or_nodes, NumberNode):
        return node_or_nodes.value

    elif isinstance(node_or_nodes, StringNode):
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
            if callable(func):
                args = [evaluate(arg, env) for arg in node_or_nodes.args]
                return func(args)
            raise TypeError(f"{node_or_nodes.name} is not a function")
        args = [evaluate(arg, env) for arg in node_or_nodes.args]
        if len(args) != len(func.params):
            raise TypeError(f"Function {node_or_nodes.name} expected {len(func.params)} args, got {len(args)}")

        local_env = Environment(func.closure_env)
        for param, arg in zip(func.params, args):
            local_env.set(param, arg)
        return evaluate(func.body, local_env)

    elif isinstance(node_or_nodes, ClassNode):
        env.set(node_or_nodes.name, node_or_nodes)
        return None

    elif isinstance(node_or_nodes, NewNode):
        class_def = env.get(node_or_nodes.class_name)
        if not isinstance(class_def, ClassNode):
            raise TypeError(f"{node_or_nodes.class_name} is not a class")

        field_env = Environment()

        for i, field_node in enumerate(class_def.fields):
            field_name = field_node.name
            if i < len(node_or_nodes.args):
                value = evaluate(node_or_nodes.args[i], env)
            else:
                if field_node.type_node and field_node.type_node.type_name == 'int':
                    value = 0
                elif field_node.type_node and field_node.type_node.type_name == 'string':
                    value = ""
                else:
                    value = 0

            field_env.set(field_name, value)

        fields = {}
        for field_name in field_env.vars:
            fields[field_name] = (field_env, field_name)

        class_env = Environment()

        for field_name, (field_env, actual_name) in fields.items():
            class_env.set(field_name, (field_env, actual_name))

        methods = {}
        for method_name, method_node in class_def.methods.items():
            method_with_env = FunctionNode(
                method_name,
                method_node.params,
                method_node.body,
                class_env
            )
            methods[method_name] = method_with_env
            class_env.set(method_name, method_with_env)

        return ObjectInstance(class_def.name, fields, methods)

    elif isinstance(node_or_nodes, MethodCallNode):
        obj = evaluate(node_or_nodes.obj, env)
        if not isinstance(obj, ObjectInstance):
            raise TypeError("Can only call methods on objects")

        method = obj.methods.get(node_or_nodes.method_name)
        if not method:
            raise AttributeError(f"Method {node_or_nodes.method_name} not found")

        method_env = Environment(env)

        for field_name, (field_env, actual_name) in obj.fields.items():
            method_env.set(field_name, (field_env, actual_name))

        for method_name, method_obj in obj.methods.items():
            method_env.set(method_name, method_obj)

        args = [evaluate(arg, env) for arg in node_or_nodes.args]
        for param, arg in zip(method.params, args):
            method_env.set(param, arg)

        result = evaluate(method.body, method_env)
        return result

    elif isinstance(node_or_nodes, FieldAccessNode):
        obj = evaluate(node_or_nodes.obj, env)
        if not isinstance(obj, ObjectInstance):
            raise TypeError("Can only access fields on objects")
        if node_or_nodes.field_name not in obj.fields:
            raise AttributeError(f"Field {node_or_nodes.field_name} not found")

        field_env, field_name = obj.fields[node_or_nodes.field_name]
        return field_env.get(field_name)

    elif isinstance(node_or_nodes, VariableNode):
        value = env.get(node_or_nodes.name)

        if isinstance(value, tuple) and len(value) == 2:
            field_env, field_name = value
            return field_env.get(field_name)

        return value

    elif isinstance(node_or_nodes, AssignNode):
        value = evaluate(node_or_nodes.value, env)

        current_env = env
        found = False
        while current_env is not None:
            if node_or_nodes.name in current_env.vars:
                found = True
                break
            current_env = current_env.parent

        if not found:
            raise NameError(f"Variable '{node_or_nodes.name}' is not defined. Use 'let' to declare variables.")

        try:
            current_value = env.get(node_or_nodes.name)
            if isinstance(current_value, tuple) and len(current_value) == 2:
                field_env, field_name = current_value
                field_env.set(field_name, value)
                return None
        except NameError:
            pass

        env.set(node_or_nodes.name, value)
        return None

    elif isinstance(node_or_nodes, LetNode):
        if node_or_nodes.value is None:
            return None

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


def builtin_map(args):
    func = args[0]
    arr = args[1]
    return [func([x]) for x in arr]


def create_global_env():
    env = Environment()
    env.set('map', builtin_map)
    return env