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

    def is_eof(self):
        return self.type == "EOF"


@dataclass
class LexicalError(ScannerResult):
    message: str
    position: int


class Scanner:
    def __init__(self, dfa: DFA, input: str = ""):
        self.dfa = dfa
        self.input = input
        self.reset()
        self.errors: List[LexicalError] = []
        self.position = 0
        self.last_accepting_position: int | None = None
        self.last_accepting_buffer: str | None = None

    def reset(self):
        self.buffer = ""
        self.dfa.reset()
        self.last_accepting_buffer = None
        self.last_accepting_position = None

    def next_token(self) -> ScannerResult:
        while self.position < len(self.input):
            char = self.input[self.position]
            if char.isspace() and not self.dfa.is_valid_transition(char):
                # if self.current_state in self.dfa.accepting_states and self.buffer:
                if self.dfa.is_accepting() and self.buffer:
                    type, priority = self.dfa.get_accepting_state_info()
                    token = Token(type, self.buffer, priority)
                    self.reset()
                    return token
                # Skip whitespace and continue
                self.position += 1
                continue

            self.buffer += char
            if self.dfa.is_valid_transition(char):
                self.dfa.transition(char)
                if self.position == len(self.input) - 1 or not self.dfa.is_valid_transition(self.input[self.position + 1]):
                    if self.dfa.is_accepting():
                        type, priority = self.dfa.get_accepting_state_info()
                        token = Token(type, self.buffer, priority)
                        self.reset()
                        self.position += 1
                        return token
            else:
                self.reset()
            self.position += 1

        # Check if the last token needs to be returned
        if self.dfa.is_accepting() and self.buffer:
            type, priority = self.dfa.get_accepting_state_info()
            token = Token(type, self.buffer, priority)
            self.reset()
            return token
        elif self.buffer:
            return LexicalError("Invalid token", self.position - len(self.buffer))

        return Token("EOF", "", TokenPriority.EOF)
