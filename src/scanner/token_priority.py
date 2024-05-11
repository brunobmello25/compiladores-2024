
from enum import Enum


class TokenPriority(Enum):
    EOF = 3
    HIGH = 2
    MEDIUM = 1
    LOW = 0

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __eq__(self, other):
        return self.value == other.value
