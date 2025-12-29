from typing import List
from .lexer import Token
from .ast_nodes import ASTNode, NumberNode, StringNode, BinaryOpNode, FunctionNode, CallNode, IfNode, VariableNode, \
    LetNode, BlockNode, RefNode, AssignRefNode, TypeNode, ClassNode, NewNode, MethodCallNode, AssignNode, \
    FieldAccessNode, ArrayNode, LambdaNode


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

    def parse(self):
        return self.parse_program()

    def parse_program(self) -> list:
        statements = []
        while self.pos < len(self.tokens):
            if self.peek().type == 'CLASS':
                stmt = self.parse_class()
                statements.append(stmt)
            elif self.peek().type == 'FUNC':
                stmt = self.parse_function()
                statements.append(stmt)
            else:
                stmt = self.statement()
                statements.append(stmt)
        return statements

    def statement(self) -> ASTNode:
        pos_backup = self.pos

        if self.peek().type == 'IDENTIFIER':
            name_token = self.consume('IDENTIFIER')
            if self.peek().type == 'ASSIGN_REF':
                self.pos = pos_backup
                return self.assignment_ref()
            elif self.peek().type == 'ASSIGN':
                self.pos = pos_backup
                name = self.consume('IDENTIFIER').value
                self.consume('ASSIGN')
                value = self.comparison()
                return AssignNode(name, value)
            else:
                self.pos = pos_backup

        return self.comparison()

    def assignment_ref(self) -> ASTNode:
        node = self.factor()
        if self.peek().type == 'ASSIGN_REF':
            self.consume('ASSIGN_REF')
            right = self.comparison()
            if not isinstance(node, VariableNode):
                raise SyntaxError("Left side of ':=' must be a variable")
            return AssignRefNode(node, right)
        return node

    def comparison(self) -> ASTNode:
        node = self.expr()
        while self.peek().type in ('EQUALS', 'NOT_EQUALS', 'LESS', 'LESS_EQ', 'GREATER', 'GREATER_EQ'):
            op = self.consume().type
            right = self.expr()
            node = BinaryOpNode(node, op, right)
        return node

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
        elif token.type == 'STRING':
            self.consume('STRING')
            return StringNode(token.value)
        elif token.type == 'LBRACKET':
            return self.parse_array()
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            node = self.comparison()
            self.consume('RPAREN')
            return node
        elif token.type == 'NEW':
            return self.parse_new()
        elif token.type == 'LAMBDA':
            return self.parse_lambda()
        elif token.type == 'CLASS':
            return self.parse_class()
        elif token.type == 'LBRACE':
            return self.parse_block()
        elif token.type == 'IF':
            return self.parse_if()
        elif token.type == 'LET':
            return self.parse_let()
        elif token.type == 'REF':
            return self.parse_ref()
        elif token.type == 'IDENTIFIER':
            name = token.value
            self.consume('IDENTIFIER')
            if self.peek().type == 'LPAREN':
                return CallNode(name, self.parse_args())
            elif self.peek().type == 'DOT':
                self.consume('DOT')
                member_name = self.consume('IDENTIFIER').value
                if self.peek().type == 'LPAREN':
                    args = self.parse_args()
                    obj_node = VariableNode(name)
                    return MethodCallNode(obj_node, member_name, args)
                else:
                    obj_node = VariableNode(name)
                    return FieldAccessNode(obj_node, member_name)
            else:
                return VariableNode(name)
        else:
            raise SyntaxError(f"Unexpected token in factor: {token}")

    def parse_args(self) -> list:
        self.consume('LPAREN')
        args = []
        if self.peek().type != 'RPAREN':
            while True:
                args.append(self.comparison())
                if self.peek().type == 'COMMA':
                    self.consume('COMMA')
                else:
                    break
        self.consume('RPAREN')
        return args

    def parse_if(self) -> IfNode:
        self.consume('IF')
        condition = self.comparison()
        self.consume('THEN')
        then_branch = self.statement()
        self.consume('ELSE')
        else_branch = self.statement()
        return IfNode(condition, then_branch, else_branch)

    def parse_let(self) -> LetNode:
        self.consume('LET')
        name = self.consume('IDENTIFIER').value

        type_node = None
        if self.peek().type == 'COLON':
            self.consume('COLON')
            type_token = self.peek()
            if type_token.type in ('INT', 'BOOL', 'STRING_TYPE'):
                type_name = type_token.value
                self.consume(type_token.type)
                type_node = TypeNode(type_name)
            else:
                raise SyntaxError(f"Unknown type: {type_token.value}")

        in_class = hasattr(self, '_in_class') and self._in_class

        if self.peek().type == 'ASSIGN':
            self.consume('ASSIGN')
            value = self.comparison()
        else:
            if in_class:
                value = None
            else:
                if type_node and type_node.type_name == 'int':
                    value = NumberNode(0)
                elif type_node and type_node.type_name == 'string':
                    value = StringNode("")
                else:
                    value = NumberNode(0)

        return LetNode(name, value, type_node)

    def parse_block(self) -> BlockNode:
        self.consume('LBRACE')
        statements = []
        while self.peek().type != 'RBRACE' and self.peek().type != 'EOF':
            if self.peek().type == 'FUNC':
                stmt = self.parse_function()
            else:
                stmt = self.statement()
            statements.append(stmt)
        self.consume('RBRACE')
        return BlockNode(statements)

    def parse_function(self) -> FunctionNode:
        self.consume('FUNC')
        name = self.consume('IDENTIFIER').value

        params = []
        if self.peek().type == 'LPAREN':
            self.consume('LPAREN')
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
        if self.peek().type == 'LBRACE':
            body = self.parse_block()
        else:
            body = self.comparison()
        return FunctionNode(name, params, body)

    def parse_ref(self) -> RefNode:
        self.consume('REF')
        name = self.consume('IDENTIFIER').value
        return RefNode(name)

    def parse_class(self) -> ClassNode:
        self.consume('CLASS')
        name = self.consume('IDENTIFIER').value
        self.consume('LBRACE')

        old_in_class = getattr(self, '_in_class', False)
        self._in_class = True

        fields = []
        methods = {}
        while self.peek().type != 'RBRACE':
            if self.peek().type == 'LET':
                field = self.parse_let()
                fields.append(field)
            elif self.peek().type == 'FUNC':
                method = self.parse_function()
                methods[method.name] = method
            else:
                raise SyntaxError(f"Expected LET or FUNC in class, got {self.peek().type}")

        self._in_class = old_in_class
        self.consume('RBRACE')
        return ClassNode(name, fields, methods)

    def parse_new(self) -> NewNode:
        self.consume('NEW')
        class_name = self.consume('IDENTIFIER').value
        args = self.parse_args()
        return NewNode(class_name, args)

    def parse_array(self) -> ArrayNode:
        self.consume('LBRACKET')
        elements = []
        if self.peek().type != 'RBRACKET':
            while True:
                elements.append(self.comparison())
                if self.peek().type == 'COMMA':
                    self.consume('COMMA')
                else:
                    break
        self.consume('RBRACKET')
        return ArrayNode(elements)

    def parse_lambda(self) -> LambdaNode:
        self.consume('LAMBDA')
        param = self.consume('IDENTIFIER').value
        self.consume('ARROW')
        body = self.comparison()
        return LambdaNode(param, body)