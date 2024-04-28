from src.scanner.token_priority import TokenPriority


class Token:
    def __init__(self, type: str, priority: TokenPriority):
        self.type = type
        self.priority = priority
