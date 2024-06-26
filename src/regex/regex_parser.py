from src.automata.automata import Automata
from src.regex.regex_lexer import RegexLexer
from src.utils.symbol import Symbol, SymbolType


class RegexParser:
    def __init__(self, regex_lexer: RegexLexer):
        self.regex_lexer = regex_lexer
        self.current_symbol = self.regex_lexer.next_symbol()
        self.peek_symbol = self.regex_lexer.next_symbol()
        self.current_level = 0

    def parse(self, return_to: int | None = None) -> Automata:
        automata = Automata()
        automata.return_to = return_to

        if self.current_symbol.type == SymbolType.EOF:
            self.current_level -= 1
            return automata

        while self.current_symbol.is_content_symbol():
            new_automata = Automata.make_symbol_automata(
                self.current_symbol.value
            )

            if self.peek_symbol.is_postfix_operator():
                self._process_postfix_symbol(new_automata, self.peek_symbol)
                self._consume()

            automata.concat(new_automata)
            self._consume()

        while self.current_symbol.is_shortcut_symbol():
            new_automata = Automata.make_shortcut_automata(self.current_symbol)

            if self.peek_symbol.is_postfix_operator():
                self._process_postfix_symbol(new_automata, self.peek_symbol)
                self._consume()

            automata.concat(new_automata)
            self._consume()

        if self.current_symbol.type == SymbolType.OR:
            self._consume()
            self.current_level += 1
            right = self.parse(automata.return_to)
            automata = Automata.union(automata, right)

        if self.current_symbol.type == SymbolType.OPEN_PARENTHESIS:
            self._consume()
            self.current_level += 1
            automata.concat(self.parse(self.current_level))

        if self.current_symbol.type == SymbolType.CLOSE_PARENTHESIS:
            if self.current_level == return_to:
                self._consume()

                if self.current_symbol.is_postfix_operator():
                    self._process_postfix_symbol(automata, self.current_symbol)
                    self._consume()

            self.current_level -= 1
            return automata

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

        self.current_level -= 1
        return automata

    def _process_postfix_symbol(self, automata: Automata, symbol: Symbol):
        if symbol.type == SymbolType.STAR:
            automata.star()
        elif symbol.type == SymbolType.PLUS:
            automata.plus()
        elif symbol.type == SymbolType.OPTIONAL:
            automata.optional()
        else:
            raise ValueError(
                "Invalid postfix symbol: {}".format(symbol)
            )

    def _consume(self):
        self.current_symbol = self.peek_symbol
        self.peek_symbol = self.regex_lexer.next_symbol()
