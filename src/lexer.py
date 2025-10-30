import re
from typing import List, Tuple

TOKENS = [
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
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