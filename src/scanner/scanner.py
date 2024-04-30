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
        self.errors: List[str] = []

    def with_input(self, input: str) -> "Scanner":
        self.input = input
        return self

    def with_automata(self, automata: DFA) -> "Scanner":
        self.automata = automata
        return self

    def next_token(self) -> Token:
        if self.input is None or self.automata is None:
            raise Exception(
                "Scanner not initialized. You must call '.with_automata' and '.with_input' first.")

        if self.pos >= len(self.input):
            return Token("EOF", "EOF", TokenPriority.HIGH)

        self.automata.reset()  # Start at the initial state of the DFA

        longest_accepting_length = 0
        start_pos = self.pos
        while self.pos < len(self.input):
            char = self.input[self.pos]
            if not self.automata.transition(char):
                # Record the error and attempt to continue scanning
                error_message = f"Invalid character {
                    char} at position {self.pos}"
                self.errors.append(error_message)
                self.pos += 1  # Skip the problematic character
                self.automata.reset()  # Reset the DFA to start state for a new token
                continue  # Skip to the next character in the input
            if self.automata.is_accepting():
                longest_accepting_length = self.pos - start_pos + 1
            self.pos += 1

        if longest_accepting_length > 0:
            # Return the longest valid token found
            token_value = self.input[start_pos:start_pos +
                                     longest_accepting_length]
            return Token("VALID_TOKEN_TYPE", token_value, TokenPriority.NORMAL)
        else:
            # No valid token found, return an error token (if not already reported)
            if not self.errors:
                self.errors.append(
                    f"No valid token found starting from position {start_pos}")
            return Token("ERROR", self.input[start_pos:self.pos], TokenPriority.LOW)
