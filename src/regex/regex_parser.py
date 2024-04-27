from src.automata.automata import Automata
from src.regex.regex_lexer import RegexLexer
from src.utils.symbol import SymbolType


class RegexParser:
    def __init__(self, regex_lexer: RegexLexer):
        self.regex_lexer = regex_lexer
        self.current_symbol = self.regex_lexer.next_symbol()
        self.peek_symbol = self.regex_lexer.next_symbol()

    def DEBUG_print_automata(self, automata: Automata, title: str | None):
        if title:
            print("---------- {} ----------".format(title))
        else:
            print("---------- Automata ----------")
        print(automata)
        print("---------- End Automata ----------")

    def parse(self) -> Automata:
        automata = Automata()
        # self.DEBUG_print_automata(automata, "Initial automata")

        if self.current_symbol.type == SymbolType.EOF:
            return automata

        while self.current_symbol.is_content_symbol():
            new_automata = Automata.make_symbol_automata(
                self.current_symbol.value
            )

            if self.peek_symbol.is_postfix_operator():
                self._process_postfix_symbol(new_automata)
                self._consume()

            automata.concat(new_automata)
            self._consume()

        while self.current_symbol.is_shortcut_symbol():
            new_automata = Automata.make_shortcut_automata(self.current_symbol)
            automata.concat(new_automata)
            self._consume()

        if self.current_symbol.type == SymbolType.OPEN_PARENTHESIS:
            self._consume()
            automata.concat(self.parse())

        if self.current_symbol.type == SymbolType.CLOSE_PARENTHESIS:
            self._consume()
            return automata

        if self.current_symbol.type == SymbolType.OR:
            self._consume()
            right = self.parse()
            automata = Automata.union(automata, right)

        if self.current_symbol.type == SymbolType.STAR:
            automata.star()
            self._consume()

        if self.current_symbol.type == SymbolType.OPTIONAL:
            automata.optional()
            self._consume()

        if self.current_symbol.type == SymbolType.PLUS:
            automata.plus()
            self._consume()

        if self.current_symbol.type != SymbolType.EOF:
            automata.concat(self.parse())

        return automata

    def _process_postfix_symbol(self, automata: Automata):
        if self.peek_symbol.type == SymbolType.STAR:
            automata.star()
        elif self.peek_symbol.type == SymbolType.PLUS:
            automata.plus()
        elif self.peek_symbol.type == SymbolType.OPTIONAL:
            automata.optional()
        else:
            raise ValueError(
                "Invalid postfix symbol: {}".format(self.peek_symbol)
            )

    def _consume(self):
        self.current_symbol = self.peek_symbol
        self.peek_symbol = self.regex_lexer.next_symbol()
