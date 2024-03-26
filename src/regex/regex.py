class RegexParser:
    def __init__(self, regex):
        self.regex = regex
        self.pos = 0

    def next_token(self):
        pass
        # if self.pos >= len(self.regex):
        #     return None
        # c = self.regex[self.pos]
        # self.pos += 1
        # return c
