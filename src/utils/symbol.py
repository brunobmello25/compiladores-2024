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

    def is_shortcut_symbol(self):
        return self.type in [
            SymbolType.UPPER,
            SymbolType.LOWER,
            SymbolType.TEXT,
            SymbolType.NUMBER,
        ]
