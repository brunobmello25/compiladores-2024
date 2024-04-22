
from typing import List
from src.dfa.dfa import DFA
from src.dfa.dfa_converter import DFAConverter
from src.dfa.dfa_merger import DFAMerger
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser
from src.scanner.token_priority import TokenPriority


class ScannerGenerator:
    def __init__(self):
        self.automatas: List[DFA] = []

    def add_token(self, expr: str, token_type: str, priority: TokenPriority) -> "ScannerGenerator":
        nfa = RegexParser(RegexLexer(expr)).parse()
        dfa = DFAConverter(nfa).get_dfa()

        dfa.associate_token(token_type, priority)

        self.automatas.append(dfa)

        return self

    def generate_scanner(self) -> DFA:
        if len(self.automatas) == 0:
            raise Exception("No tokens added to the scanner")

        automata = self.automatas[0]

        for dfa in self.automatas[1:]:
            automata = DFAMerger(automata, dfa).merge()

        return automata
