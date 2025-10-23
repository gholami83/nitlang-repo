import re

class Parser:
    def parse(self, expr):
        tokens = re.findall(r'\d+|[+\-*/()]', expr)
        return self._parse_expr(tokens)

    def _parse_expr(self, tokens):
        # سادگی: فعلاً از eval استفاده می‌کنیم
        return eval(''.join(tokens))
