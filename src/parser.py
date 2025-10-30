# parser.py

from typing import List
from lexer import Token
from ast_nodes import ASTNode, NumberNode, BinaryOpNode

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token('EOF', '')

    def consume(self, expected_type: str = None) -> Token:
        token = self.peek()
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token.type}")
        self.pos += 1
        return token

    def parse(self) -> ASTNode:
        return self.expr()

    # expr   : term ((PLUS | MINUS) term)*
    def expr(self) -> ASTNode:
        node = self.term()
        while self.peek().type in ('PLUS', 'MINUS'):
            op = self.consume().type
            right = self.term()
            node = BinaryOpNode(node, op, right)
        return node

    # term   : factor ((MUL | DIV) factor)*
    def term(self) -> ASTNode:
        node = self.factor()
        while self.peek().type in ('MUL', 'DIV'):
            op = self.consume().type
            right = self.factor()
            node = BinaryOpNode(node, op, right)
        return node

    # factor : NUMBER | LPAREN expr RPAREN
    def factor(self) -> ASTNode:
        token = self.peek()
        if token.type == 'NUMBER':
            self.consume('NUMBER')
            return NumberNode(token.value)
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            node = self.expr()
            self.consume('RPAREN')
            return node
        else:
            raise SyntaxError(f"Unexpected token: {token}")