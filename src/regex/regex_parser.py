from src.automata.automata import Automata
from src.regex.regex_lexer import RegexLexer
from src.utils.symbol import Symbol, SymbolType


def _make_symbol_automata(symbol: str) -> Automata:
    a = Automata()

    q0 = a.accept_states.pop()

    q1 = a.add_state(True)
    a.add_transition(q0, q1, symbol)
    return a


class RegexParser:
    def __init__(self, regex_lexer: RegexLexer):
        self.regex_lexer = regex_lexer
        self.current_symbol = self.regex_lexer.next_symbol()
        self.peek_symbol = self.regex_lexer.next_symbol()

    def parse(self) -> Automata:
        automata = Automata()

        if self.current_symbol.type == SymbolType.EOF:
            return automata

        while self.current_symbol.is_content_symbol():
            new_automata = _make_symbol_automata(self.current_symbol.value)
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

        if self.current_symbol.type == SymbolType.PLUS:
            automata.plus()
            self._consume()

        if self.current_symbol.type != SymbolType.EOF:
            automata.concat(self.parse())

        return automata

    def _consume(self):
        self.current_symbol = self.peek_symbol
        self.peek_symbol = self.regex_lexer.next_symbol()
