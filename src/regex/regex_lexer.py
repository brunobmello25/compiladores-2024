from src.utils.symbol import Symbol, SymbolType


class RegexLexer:
    def __init__(self, input: str):
        self.pos = 0
        self.input = input

    # TODO: deve retornar ILLEGAL pra caso de simbolo inválido
    def next_symbol(self) -> Symbol:
        if self.pos >= len(self.input):
            return Symbol(SymbolType.EOF, SymbolType.EOF.value)

        if self.input[self.pos] == "[":
            return self._handle_regex_shortcut()

        if self.input[self.pos] == SymbolType.OPEN_PARENTHESIS.value:
            self.pos += 1
            return Symbol(SymbolType.OPEN_PARENTHESIS,
                          SymbolType.OPEN_PARENTHESIS.value)

        if self.input[self.pos] == SymbolType.CLOSE_PARENTHESIS.value:
            self.pos += 1
            return Symbol(SymbolType.CLOSE_PARENTHESIS,
                          SymbolType.CLOSE_PARENTHESIS.value)

        if self.input[self.pos] == SymbolType.OR.value:
            self.pos += 1
            return Symbol(SymbolType.OR, SymbolType.OR.value)

        if self.input[self.pos] == SymbolType.STAR.value:
            self.pos += 1
            return Symbol(SymbolType.STAR, SymbolType.STAR.value)

        if self.input[self.pos] == SymbolType.PLUS.value:
            self.pos += 1
            return Symbol(SymbolType.PLUS, SymbolType.PLUS.value)

        return Symbol(SymbolType.ILLEGAL, self.input[self.pos])

    def _handle_regex_shortcut(self) -> Symbol:
        inner_content = self.input[self.pos+1: self.pos+4]

        self.pos += 5

        content = f"[{inner_content}]"

        if content == "[A-z]":
            return Symbol(SymbolType.TEXT, content)
        elif content == "[A-Z]":
            return Symbol(SymbolType.UPPER, content)
        elif content == "[a-z]":
            return Symbol(SymbolType.LOWER, content)
        elif content == "[0-9]":
            return Symbol(SymbolType.NUMBER, content)
        return Symbol(SymbolType.ILLEGAL, content)
