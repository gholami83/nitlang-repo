from .ast_nodes import *
from .vm import VMInstruction


class Compiler:
    def __init__(self):
        self.instructions = []

    def compile(self, node_or_nodes):
        if isinstance(node_or_nodes, list):
            for node in node_or_nodes:
                if self._is_expression(node):
                    self._compile_node(node)
                    self.instructions.append(VMInstruction('PRINT'))
                else:
                    self._compile_node(node)
        else:
            self._compile_node(node_or_nodes)
            if self._is_expression(node_or_nodes):
                self.instructions.append(VMInstruction('PRINT'))
        return self.instructions

    def _is_expression(self, node):
        return isinstance(node, (NumberNode, StringNode, BinaryOpNode, VariableNode, IfNode))  # ← IfNode اضافه شد

    def _compile_node(self, node):
        if isinstance(node, NumberNode):
            self.instructions.append(VMInstruction('LOAD', node.value))
        elif isinstance(node, StringNode):
            self.instructions.append(VMInstruction('LOAD', node.value))
        elif isinstance(node, BinaryOpNode):
            self._compile_node(node.left)
            self._compile_node(node.right)
            if node.op == 'PLUS':
                self.instructions.append(VMInstruction('ADD'))
            elif node.op == 'MINUS':
                self.instructions.append(VMInstruction('SUB'))
            elif node.op == 'MUL':
                self.instructions.append(VMInstruction('MUL'))
            elif node.op == 'DIV':
                self.instructions.append(VMInstruction('DIV'))
            elif node.op == 'EQUALS':
                self.instructions.append(VMInstruction('EQUALS'))
            elif node.op == 'NOT_EQUALS':
                self.instructions.append(VMInstruction('NOT_EQUALS'))
            elif node.op == 'LESS':
                self.instructions.append(VMInstruction('LESS'))
            elif node.op == 'LESS_EQ':
                self.instructions.append(VMInstruction('LESS_EQ'))
            elif node.op == 'GREATER':
                self.instructions.append(VMInstruction('GREATER'))
            elif node.op == 'GREATER_EQ':
                self.instructions.append(VMInstruction('GREATER_EQ'))
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

            current_pos = len(self.instructions)

            jz_pos = current_pos
            self.instructions.append(VMInstruction('JZ', 0))

            self._compile_node(node.then_branch)

            jmp_pos = len(self.instructions)
            self.instructions.append(VMInstruction('JMP', 0))

            else_start = len(self.instructions)

            self._compile_node(node.else_branch)

            end_pos = len(self.instructions)

            self.instructions[jz_pos].operand = else_start
            self.instructions[jmp_pos].operand = end_pos

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