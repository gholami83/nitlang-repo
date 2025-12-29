import re
from typing import List

TOKENS = [
    ('CLASS', r'class\b'),
    ('NEW', r'new\b'),
    ('FUNC', r'func\b'),
    ('IF', r'if\b'),
    ('THEN', r'then\b'),
    ('ELSE', r'else\b'),
    ('LET', r'let\b'),
    ('REF', r'ref\b'),
    ('LAMBDA', r'lambda\b'),
    ('INT', r'int\b'),
    ('BOOL', r'bool\b'),
    ('STRING_TYPE', r'string\b'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('NUMBER', r'\d*\.\d+|\d+\.|\d+'),
    ('STRING', r'"[^"]*"'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('LESS_EQ', r'<='),
    ('LESS', r'<'),
    ('GREATER_EQ', r'>='),
    ('GREATER', r'>'),
    ('NOT_EQUALS', r'!='),
    ('EQUALS', r'=='),
    ('ASSIGN_REF', r':='),
    ('ASSIGN', r'='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('COMMA', r','),
    ('DOT', r'\.'),
    ('ARROW', r'->'),        
    ('COLON', r':'),
    ('WHITESPACE', r'\s+'),
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS)

class Token:
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def tokenize(text: str) -> List[Token]:
    tokens = []
    for match in re.finditer(TOKEN_REGEX, text):
        kind = match.lastgroup
        value = match.group()
        if kind == 'WHITESPACE':
            continue
        elif kind == 'NUMBER':
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        elif kind == 'STRING':
            value = value[1:-1]
        tokens.append(Token(kind, value))
    return tokens