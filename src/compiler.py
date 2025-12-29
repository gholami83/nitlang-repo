from .ast_nodes import *
from .vm import VMInstruction

class Compiler:
    def __init__(self):
        self.instructions = []

    def compile(self, node_or_nodes):
        if isinstance(node_or_nodes, list):
            for node in node_or_nodes:
                self.compile(node)
        else:
            self._compile_node(node_or_nodes)
        return self.instructions

    def _compile_node(self, node):
        if isinstance(node, NumberNode):
            self.instructions.append(VMInstruction('LOAD', node.value))
        elif isinstance(node, BinaryOpNode):
            self._compile_node(node.left)
            self._compile_node(node.right)
            if node.op == '+':
                self.instructions.append(VMInstruction('ADD'))
            elif node.op == '-':
                self.instructions.append(VMInstruction('SUB'))
            elif node.op == '*':
                self.instructions.append(VMInstruction('MUL'))
            elif node.op == '/':
                self.instructions.append(VMInstruction('DIV'))
        elif isinstance(node, VariableNode):
            self.instructions.append(VMInstruction('LOAD_VAR', node.name))
        elif isinstance(node, AssignNode):
            self._compile_node(node.value)
            self.instructions.append(VMInstruction('STORE', node.name))
        elif isinstance(node, LetNode):
            self._compile_node(node.value)
            self.instructions.append(VMInstruction('STORE', node.name))
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self._compile_node(stmt)
        elif isinstance(node, IfNode):
            self._compile_node(node.condition)
            self.instructions.append(VMInstruction('JZ', len(self.instructions) + 2))
            self._compile_node(node.then_branch)
            self.instructions.append(VMInstruction('JMP', len(self.instructions) + 1))
            self._compile_node(node.else_branch)
        elif isinstance(node, CallNode):
            pass
        elif isinstance(node, ArrayNode):
            for elem in node.elements:
                self._compile_node(elem)

        elif isinstance(node, LambdaNode):
            pass
        elif isinstance(node, IndexNode):
            pass
        else:
            raise TypeError(f"Cannot compile node: {node}")

    def reset(self):
        self.instructions = []