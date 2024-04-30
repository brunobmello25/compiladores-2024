from src.scanner.token_priority import TokenPriority


class Token:
    def __init__(self, value: str, type: str, priority: TokenPriority):
        self.type = type
        self.priority = priority
        self.value = value
