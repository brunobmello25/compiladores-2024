from src.automata.state import State
from src.dfa.dfa_converter import DFAConverter
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


def test_dfa_acception():
    State.state_counter = 0
    nfa = RegexParser(RegexLexer("ab*c?d+e")).parse()
    dfa = DFAConverter(nfa).get_dfa()

    # TODO: add more assertions here
    assert dfa.check("abdde")
    assert dfa.check("abde")
    assert dfa.check("acde")
    assert dfa.check("acdde")
    assert not dfa.check("")
    assert not dfa.check("ab")
    assert not dfa.check("abdd")
