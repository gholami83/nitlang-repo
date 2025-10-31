# src/ast_nodes.py

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"

class BinaryOpNode(ASTNode):
    def __init__(self, left: 'ASTNode', op: str, right: 'ASTNode'):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.op}, {self.right})"

class FunctionNode(ASTNode):
    def __init__(self, name: str, params: list, body: ASTNode):
        self.name = name
        self.params = params
        self.body = body

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

class LetNode(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"LetNode({self.name}, {self.value})"