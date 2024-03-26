from src.regex.regex_lexer import RegexLexer


class RegexParser:
    def __init__(self, regex_lexer: RegexLexer):
        self.regex_lexer = regex_lexer
        self.current_symbol = self.regex_lexer.next_symbol()

    def next_symbol(self):
        pass
        # if self.pos >= len(self.regex):
        #     return None
        # c = self.regex[self.pos]
        # self.pos += 1
        # return c
