from typing import List
from .lexer import Token
from .ast_nodes import ASTNode, NumberNode, BinaryOpNode, FunctionNode, CallNode, IfNode, VariableNode

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
            raise SyntaxError(f"Expected {expected_type}, got {token.type} ({token.value})")
        self.pos += 1
        return token

    def parse(self) -> ASTNode:
        if self.peek().type == 'FUNC':
            return self.parse_function()
        else:
            return self.expr()

    def parse_function(self) -> FunctionNode:
        self.consume('FUNC')
        name = self.consume('IDENTIFIER').value
        self.consume('LPAREN')
        params = []
        if self.peek().type != 'RPAREN':
            while True:
                param = self.consume('IDENTIFIER').value
                params.append(param)
                if self.peek().type == 'COMMA':
                    self.consume('COMMA')
                else:
                    break
        self.consume('RPAREN')
        self.consume('ASSIGN')
        body = self.expr()
        return FunctionNode(name, params, body)

    def expr(self) -> ASTNode:
        node = self.term()
        while self.peek().type in ('PLUS', 'MINUS'):
            op = self.consume().type
            right = self.term()
            node = BinaryOpNode(node, op, right)
        return node

    def term(self) -> ASTNode:
        node = self.factor()
        while self.peek().type in ('MUL', 'DIV'):
            op = self.consume().type
            right = self.factor()
            node = BinaryOpNode(node, op, right)
        return node

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
        elif token.type == 'IF':
            return self.parse_if()
        elif token.type == 'IDENTIFIER':
            name = token.value
            self.consume('IDENTIFIER')
            if self.peek().type == 'LPAREN':
                self.consume('LPAREN')
                args = []
                if self.peek().type != 'RPAREN':
                    while True:
                        args.append(self.expr())
                        if self.peek().type == 'COMMA':
                            self.consume('COMMA')
                        else:
                            break
                self.consume('RPAREN')
                return CallNode(name, args)
            else:
                return VariableNode(name)
        else:
            raise SyntaxError(f"Unexpected token in factor: {token}")

    def parse_if(self) -> IfNode:
        self.consume('IF')
        condition = self.expr()
        self.consume('THEN')
        then_branch = self.expr()
        self.consume('ELSE')
        else_branch = self.expr()
        return IfNode(condition, then_branch, else_branch)