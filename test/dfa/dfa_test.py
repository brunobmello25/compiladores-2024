from src.automata.state import State
from src.dfa.dfa import DFA
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


def test_build_from_nfa():
    State.state_counter = 0
    nfa = RegexParser(RegexLexer("(a|b)")).parse()

    dfa = DFA(nfa)

    print()
    dfa.print()
