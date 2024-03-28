from enum import Enum


class SymbolType(Enum):
    UPPER = "[A-Z]"
    LOWER = "[a-z]"
    TEXT = "[A-z]"
    NUMBER = "[0-9]"
    STAR = "*"
    PLUS = "+"
    OR = "|"
    OPEN_PARENTHESIS = "("
    CLOSE_PARENTHESIS = ")"
    DIGIT = "DIGIT"
    LETTER = "LETTER"
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"


class Symbol:
    def __init__(self, type: SymbolType, value: str):
        self.type = type
        self.value = value
