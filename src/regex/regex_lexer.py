from src.utils.symbol import Symbol


class RegexLexer:
    def __init__(self, input: str):
        self.pos = 0
        self.input = input

    # TODO: deve retornar ILLEGAL pra caso de simbolo inválido
    def next_symbol(self) -> Symbol:
        if self.pos >= len(self.input):
            return Symbol.EOF

        if self.input[self.pos] == "[":
            return self._handle_regex_symbol()

        if self.input[self.pos] == Symbol.OPEN_PARENTHESIS.value:
            self.pos += 1
            return Symbol.OPEN_PARENTHESIS

        if self.input[self.pos] == Symbol.CLOSE_PARENTHESIS.value:
            self.pos += 1
            return Symbol.CLOSE_PARENTHESIS

        if self.input[self.pos] == Symbol.OR.value:
            self.pos += 1
            return Symbol.OR

        if self.input[self.pos] == Symbol.STAR.value:
            self.pos += 1
            return Symbol.STAR

        if self.input[self.pos] == Symbol.PLUS.value:
            self.pos += 1
            return Symbol.PLUS

    def _handle_regex_symbol(self) -> Symbol:
        inner_content = self.input[self.pos+1: self.pos+4]

        self.pos += 5

        if inner_content == "A-z":
            return Symbol.TEXT
        elif inner_content == "A-Z":
            return Symbol.UPPER
        elif inner_content == "a-z":
            return Symbol.LOWER
        elif inner_content == "0-9":
            return Symbol.NUMBER
