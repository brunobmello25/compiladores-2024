from typing import List
from src.dfa.dfa import DFA
from src.scanner.token import Token
from src.scanner.token_priority import TokenPriority


class Scanner:
    def __init__(self):
        self.automata: DFA | None = None
        self.input: str | None = None

        self.DEBUG_tokens: List[Token] = []
        self.DEBUG_tokens_index = 0

    def with_input(self, input: str) -> "Scanner":
        self.input = input
        return self

    def with_automata(self, automata: DFA) -> "Scanner":
        self.automata = automata
        return self

    def next_token(self) -> Token:
        if self.input is None or self.automata is None:
            raise Exception(
                "Scanner not initialized. You have to call \".with_automata\" and \".with_input\" first")

        if self.DEBUG_tokens_index >= len(self.DEBUG_tokens):
            return Token("EOF", "EOF", TokenPriority.HIGH)

        token = self.DEBUG_tokens[self.DEBUG_tokens_index]
        self.DEBUG_tokens_index += 1
        return token
