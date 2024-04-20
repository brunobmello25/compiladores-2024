from src.automata.state import State
from src.dfa.dfa_converter import DFAConverter
from src.dfa.dfa_merger import DFAMerger
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


def test_merge():
    State.state_counter = 0

    A = DFAConverter(RegexParser(RegexLexer("a")).parse()).get_dfa()
    B = DFAConverter(RegexParser(RegexLexer("b")).parse()).get_dfa()
    A.associate_token("a")
    B.associate_token("b")

    merged = DFAMerger(A, B).merge()

    assert merged.check("a")
    assert merged.check("b")
    assert not merged.check("aa")
    assert not merged.check("ab")
    assert not merged.check("ba")
    assert not merged.check("bb")

    # TODO: fazer esta porra funcionar
    # assert merged.check_final_state("a")[1].token_type == "a"
    # assert merged.check_final_state("b")[1].token_type == "b"
