from enum import Enum


class Symbol(Enum):
    UPPER = "[A-Z]"
    LOWER = "[a-z]"
    TEXT = "[A-z]"
    NUMBER = "[0-9]"
    STAR = "*"
    PLUS = "+"
    OR = "|"
    OPEN_PARENTHESIS = "("
    CLOSE_PARENTHESIS = ")"
    EOF = "EOF"
