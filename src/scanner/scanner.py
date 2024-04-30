from dataclasses import dataclass
from typing import List
from src.dfa.dfa import DFA
from src.scanner.token_priority import TokenPriority


class ScannerResult:
    pass


@dataclass
class Token(ScannerResult):
    type: str
    value: str
    priority: TokenPriority


@dataclass
class LexicalError(ScannerResult):
    message: str
    position: int


class Scanner:
    def __init__(self):
        self.automata: DFA | None = None
        self.input: str | None = None
        self.pos = 0
        self.errors: List[LexicalError] = []

    def with_input(self, input: str) -> "Scanner":
        self.input = input
        return self

    def with_automata(self, automata: DFA) -> "Scanner":
        self.automata = automata
        return self

    def next_token(self) -> Token | LexicalError:
        if self.input is None or self.automata is None:
            raise Exception(
                "Scanner not initialized. You must call '.with_automata' and '.with_input' first.")

        if self.pos >= len(self.input):
            return Token("EOF", "EOF", TokenPriority.HIGH)

        self.automata.reset()
        longest_accepting_length = 0
        last_accepting_info = None
        start_pos = self.pos
        while self.pos < len(self.input):
            char = self.input[self.pos]
            if not self.automata.transition(char):
                self.pos += 1  # Skip the problematic character
                self.automata.reset()  # Reset for next token
                continue
            accepting_info = self.automata.get_accepting_info()
            if accepting_info is not None:  # Token type is not None
                longest_accepting_length = self.pos - start_pos + 1
                last_accepting_info = accepting_info
            self.pos += 1

        if longest_accepting_length > 0 and last_accepting_info:
            token_type, token_priority = last_accepting_info
            token_value = self.input[start_pos:start_pos +
                                     longest_accepting_length]
            return Token(token_type, token_value, token_priority)

        if self.errors:
            return self.errors.pop(0)

        return LexicalError("No valid token found and no specific error identified", start_pos)
