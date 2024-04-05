from src.automata.automata import Automata
from src.regex.regex_lexer import RegexLexer
from src.utils.symbol import Symbol, SymbolType


class RegexParser:
    def __init__(self, regex_lexer: RegexLexer):
        self.regex_lexer = regex_lexer
        self.current_symbol = self.regex_lexer.next_symbol()
        self.peek_symbol = self.regex_lexer.next_symbol()

    def parse(self) -> Automata:
        automata = self._make_empty_word_automata()

        if self.current_symbol.type == SymbolType.EOF:
            return automata

        while self.current_symbol.is_content_symbol():
            new_automata = self._make_symbol_automata(self.current_symbol)
            automata.concat(new_automata)
            self._consume()

        if self.current_symbol.type == SymbolType.OPEN_PARENTHESIS:
            self._consume()
            automata.concat(self.parse())

        if self.current_symbol.type == SymbolType.CLOSE_PARENTHESIS:
            self._consume()
            automata.concat(self.parse())

        return automata

    def _make_empty_word_automata(self) -> Automata:
        a = Automata()
        s = a.add_state(True)
        a.set_start(s)
        return a

    def _make_symbol_automata(self, symbol: Symbol) -> Automata:
        automata = Automata()
        q0 = automata.add_state(False)
        q1 = automata.add_state(True)
        automata.add_transition(q0, q1, symbol.value)
        automata.set_start(q0)
        return automata

    def _consume(self):
        self.current_symbol = self.peek_symbol
        self.peek_symbol = self.regex_lexer.next_symbol()
