from src.utils.symbol import Symbol, SymbolType


class RegexLexer:
    def __init__(self, input: str):
        self.pos = 0
        self.input = input

    def next_symbol(self) -> Symbol:
        if self.pos >= len(self.input):
            return Symbol(SymbolType.EOF, SymbolType.EOF.value)

        if self.input[self.pos] == '_':
            self.pos += 1
            return Symbol(SymbolType.UNDERSCORE, SymbolType.UNDERSCORE.value)

        if self.input[self.pos] == "!":
            self.pos += 1
            return Symbol(SymbolType.EXCLAMATION, SymbolType.EXCLAMATION.value)

        if self.input[self.pos] == ";":
            self.pos += 1
            return Symbol(SymbolType.SEMICOLON, SymbolType.SEMICOLON.value)

        if self.input[self.pos] == "=":
            self.pos += 1
            return Symbol(SymbolType.EQUAL, SymbolType.EQUAL.value)

        if self.input[self.pos] == "[":
            return self._handle_regex_shortcut()

        if self.input[self.pos] == SymbolType.OPEN_PARENTHESIS.value:
            self.pos += 1
            return Symbol(
                SymbolType.OPEN_PARENTHESIS, SymbolType.OPEN_PARENTHESIS.value
            )

        if self.input[self.pos] == SymbolType.CLOSE_PARENTHESIS.value:
            self.pos += 1
            return Symbol(
                SymbolType.CLOSE_PARENTHESIS,
                SymbolType.CLOSE_PARENTHESIS.value,
            )

        if self.input[self.pos] == SymbolType.OR.value:
            self.pos += 1
            return Symbol(SymbolType.OR, SymbolType.OR.value)

        if self.input[self.pos] == SymbolType.STAR.value:
            self.pos += 1
            return Symbol(SymbolType.STAR, SymbolType.STAR.value)

        if self.input[self.pos] == SymbolType.OPTIONAL.value:
            self.pos += 1
            return Symbol(SymbolType.OPTIONAL, SymbolType.OPTIONAL.value)

        if self.is_alphabetic_digit(self.input[self.pos]):
            char = self.input[self.pos]
            self.pos += 1
            return Symbol(SymbolType.LETTER, char)

        if self.is_numeric_digit(self.input[self.pos]):
            digit = self.input[self.pos]
            self.pos += 1
            return Symbol(SymbolType.NUMERIC_DIGIT, digit)

        if self.input[self.pos] == SymbolType.PLUS.value:
            self.pos += 1
            return Symbol(SymbolType.PLUS, SymbolType.PLUS.value)

        return Symbol(SymbolType.ILLEGAL, self.input[self.pos])

    def is_alphabetic_digit(self, c: str) -> bool:
        return len(c) == 1 and c.isalpha()

    def is_numeric_digit(self, c: str) -> bool:
        return len(c) == 1 and c.isdigit()

    def _handle_regex_shortcut(self) -> Symbol:
        inner_content = self.input[self.pos + 1: self.pos + 4]

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
