from src.dfa.dfa import DFA


class Scanner:
    def __init__(self, automata: DFA):
        self.automata = automata
        self.input = ""

    def load_input(self, input: str):
        self.input = input
