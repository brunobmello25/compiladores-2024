from enum import Enum


class SymbolType(Enum):
    UPPER = "[A-Z]"
    LOWER = "[a-z]"
    TEXT = "[A-z]"
    NUMBER = "[0-9]"
    STAR = "*"
    PLUS = "+"
    OR = "|"
    OPTIONAL = "?"
    OPEN_PARENTHESIS = "("
    CLOSE_PARENTHESIS = ")"
    NUMERIC_DIGIT = "DIGIT"
    LETTER = "LETTER"
    EOF = "EOF"
    EQUAL = "="
    EXCLAMATION = "!"
    SEMICOLON = ";"
    PIPE = "|"
    ILLEGAL = "ILLEGAL"


class Symbol:
    def __init__(self, type: SymbolType, value: str):
        self.type = type
        self.value = value

    def is_content_symbol(self):
        return self.type in [
            SymbolType.NUMERIC_DIGIT,
            SymbolType.LETTER,
        ]

    def is_postfix_operator(self):
        return self.type in [
            SymbolType.STAR,
            SymbolType.PLUS,
            SymbolType.OPTIONAL,
        ]

    def is_shortcut_symbol(self):
        return self.type in [
            SymbolType.UPPER,
            SymbolType.LOWER,
            SymbolType.TEXT,
            SymbolType.NUMBER,
        ]

    def shortcut_to_list(self):
        if self.type == SymbolType.UPPER:
            return [chr(i) for i in range(65, 91)]
        elif self.type == SymbolType.LOWER:
            return [chr(i) for i in range(97, 123)]
        elif self.type == SymbolType.TEXT:
            return [chr(i) for i in range(65, 91)] + [
                chr(i) for i in range(97, 123)
            ]
        elif self.type == SymbolType.NUMBER:
            return [chr(i) for i in range(48, 58)]
        else:
            raise Exception("{} is not a shortcut symbol".format(self.type))
