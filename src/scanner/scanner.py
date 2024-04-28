from typing import List
from src.dfa.dfa import DFA
from src.scanner.token import Token
from src.scanner.token_priority import TokenPriority


class Scanner:
    def __init__(self, automata: DFA):
        self.automata = automata
        self.input = ""

        self.DEBUG_tokens: List[Token] = []
        self.DEBUG_tokens_index = 0

    def load_input(self, input: str):
        self.input = input

    def next_token(self) -> Token:
        if self.DEBUG_tokens_index >= len(self.DEBUG_tokens):
            return Token("EOF", "EOF", TokenPriority.HIGH)

        token = self.DEBUG_tokens[self.DEBUG_tokens_index]
        self.DEBUG_tokens_index += 1
        return token
