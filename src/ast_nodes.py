from typing import Union

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value: Union[int, float]):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"StringNode({self.value})"

class BinaryOpNode(ASTNode):
    def __init__(self, left: 'ASTNode', op: str, right: 'ASTNode'):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.op}, {self.right})"

class FunctionNode(ASTNode):
    def __init__(self, name: str, params: list, body: ASTNode, closure_env=None):
        self.name = name
        self.params = params
        self.body = body
        self.closure_env = closure_env

    def __repr__(self):
        return f"FunctionNode({self.name}, {self.params}, {self.body})"

class CallNode(ASTNode):
    def __init__(self, name: str, args: list):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"CallNode({self.name}, {self.args})"

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_branch: ASTNode):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfNode({self.condition}, {self.then_branch}, {self.else_branch})"

class VariableNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"VariableNode({self.name})"

class TypeNode(ASTNode):
    def __init__(self, type_name: str):
        self.type_name = type_name

    def __repr__(self):
        return f"TypeNode({self.type_name})"

class LetNode(ASTNode):
    def __init__(self, name: str, value: ASTNode, type_node: TypeNode = None):
        self.name = name
        self.value = value
        self.type_node = type_node

    def __repr__(self):
        return f"LetNode({self.name}, {self.value}, {self.type_node})"

class BlockNode(ASTNode):
    def __init__(self, statements: list):
        self.statements = statements

    def __repr__(self):
        return f"BlockNode({self.statements})"

class RefNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"RefNode({self.name})"

class AssignRefNode(ASTNode):
    def __init__(self, ref: ASTNode, value: ASTNode):
        self.ref = ref
        self.value = value

    def __repr__(self):
        return f"AssignRefNode({self.ref}, {self.value})"