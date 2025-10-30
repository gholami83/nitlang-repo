# evaluator.py

from .ast_nodes import ASTNode, NumberNode, BinaryOpNode

def evaluate(node: ASTNode) -> int:
    if isinstance(node, NumberNode):
        return node.value
    elif isinstance(node, BinaryOpNode):
        left_val = evaluate(node.left)
        right_val = evaluate(node.right)
        if node.op == 'PLUS':
            return left_val + right_val
        elif node.op == 'MINUS':
            return left_val - right_val
        elif node.op == 'MUL':
            return left_val * right_val
        elif node.op == 'DIV':
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val // right_val  # تقسیم صحیح
        else:
            raise ValueError(f"Unknown operator: {node.op}")
    else:
        raise TypeError(f"Unknown node type: {type(node)}")