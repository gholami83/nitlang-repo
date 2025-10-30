import re
from typing import List

TOKENS = [
    ('FUNC', r'func'),
    ('IF', r'if'),
    ('THEN', r'then'),
    ('ELSE', r'else'),
    ('NUMBER', r'\d+'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('EQUALS', r'=='),
    ('ASSIGN', r'='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('COMMA', r','),
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
            value = int(value)

        tokens.append(Token(kind, value))
    return tokens