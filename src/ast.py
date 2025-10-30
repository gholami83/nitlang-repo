
class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"

class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.op}, {self.right})"