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
        self.pos = 0
        self.last_accepting_position: int | None = None
        self.last_accepting_buffer: str | None = None

    def reset(self):
        self.buffer = ""
        self.dfa.reset()
        self.last_accepting_buffer = None
        self.last_accepting_position = None

    def next_token(self) -> ScannerResult:
        self.reset()
        while self.pos < len(self.input):
            char = self.input[self.pos]

            if char.isspace() and not self.dfa.is_valid_transition(char):
                if self.dfa.is_accepting() and self.buffer:
                    token = self.get_accepting_token()
                    self.reset()
                    return token
                self.pos += 1
                continue
            elif char.isspace():
                # FIXME: precisamos lidar com espaços em branco "válidos aqui"
                pass

            if self.dfa.is_valid_transition(char):
                self.buffer += char
                self.dfa.transition(char)

                if self.dfa.is_accepting():
                    self.last_accepting_buffer = self.buffer
                    self.last_accepting_position = self.pos

                elif self.last_accepting_buffer is not None:
                    self._backtrack()
                    token = self.get_accepting_token()
                    return token

                self.pos += 1
            else:
                if self.last_accepting_buffer is not None:
                    self._backtrack()
                    token = self.get_accepting_token()
                    return token

        if self.buffer and self.dfa.is_accepting():
            token = self.get_accepting_token()
            return token
        elif self.buffer:
            return LexicalError(f"Invalid token {self.buffer}", self.pos)
        else:
            return Token("EOF", "", TokenPriority.EOF)

    def _backtrack(self):
        if self.last_accepting_buffer is None or self.last_accepting_position is None:
            raise Exception(
                "Cannot backtrack to a position that was not accepting a token")
        amount = len(self.buffer) - len(self.last_accepting_buffer)
        self.dfa.backtrack(amount)
        self.buffer = self.last_accepting_buffer
        self.pos = self.last_accepting_position
        self.last_accepting_buffer = None

    def get_accepting_token(self) -> Token:
        type, priority = self.dfa.get_accepting_state_info()
        self.pos += 1
        return Token(type, self.buffer, priority)
