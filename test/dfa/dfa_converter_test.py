from src.automata.state import State
from src.dfa.dfa_converter import DFAConverter
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


def test_dfa_acception():
    State.state_counter = 0
    nfa = RegexParser(RegexLexer("ab*c?d+e")).parse()
    dfa = DFAConverter(nfa).get_dfa()

    assert dfa.check("abdde")
    assert dfa.check("abde")
    assert dfa.check("acde")
    assert dfa.check("acdde")
    assert dfa.check("ade")
    assert dfa.check("abbde")
    assert dfa.check("abbbde")
    assert dfa.check("abcde")
    assert dfa.check("abcdde")
    assert dfa.check("abbcdddde")

    assert not dfa.check("abce")
    assert not dfa.check("abc")
    assert not dfa.check("abce")
    assert not dfa.check("bacde")
    assert not dfa.check("abdcde")
    assert not dfa.check("adebde")
    assert not dfa.check("abdede")
    assert not dfa.check("aed")
    assert not dfa.check("ab*cd+e")
    assert not dfa.check("")
    assert not dfa.check("ab")
    assert not dfa.check("abdd")
