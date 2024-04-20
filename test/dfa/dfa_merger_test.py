from src.automata.state import State
from src.dfa.dfa_converter import DFAConverter
from src.dfa.dfa_merger import DFAMerger
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser
from src.scanner.token_priority import TokenPriority


def test_merge_int_and_identifier():
    State.state_counter = 0

    int_automata = DFAConverter(RegexParser(
        RegexLexer("int")).parse()).get_dfa()
    int_automata.associate_token("int", TokenPriority.HIGH)

    identifier_automata = DFAConverter(RegexParser(
        RegexLexer("[A-z]([A-z]|[0-9])*")).parse()).get_dfa()
    identifier_automata.associate_token("identifier", TokenPriority.LOW)

    merged = DFAMerger(int_automata, identifier_automata).merge()

    assert merged.check("int")
    assert merged.check_final_state("int")[1].token_type == "int"
    assert merged.check_final_state(
        "int")[1].token_priority == TokenPriority.HIGH
    assert merged.check("inte")
    assert merged.check_final_state("inte")[1].token_type == "identifier"
    assert merged.check_final_state(
        "inte")[1].token_priority == TokenPriority.LOW


def test_merge():
    State.state_counter = 0

    A = DFAConverter(RegexParser(RegexLexer("a")).parse()).get_dfa()
    B = DFAConverter(RegexParser(RegexLexer("b")).parse()).get_dfa()
    A.associate_token("a", TokenPriority.HIGH)
    B.associate_token("b", TokenPriority.LOW)

    merged = DFAMerger(A, B).merge()

    assert merged.check("a")
    assert merged.check("b")
    assert not merged.check("aa")
    assert not merged.check("ab")
    assert not merged.check("ba")
    assert not merged.check("bb")

    assert merged.check_final_state("a")[1].token_type == "a"
    assert merged.check_final_state(
        "a")[1].token_priority == TokenPriority.HIGH
    assert merged.check_final_state("b")[1].token_type == "b"
    assert merged.check_final_state(
        "b")[1].token_priority == TokenPriority.LOW
    assert merged.check_final_state("aa")[1].token_type is None
    assert merged.check_final_state("bb")[1].token_type is None
    assert merged.check_final_state("aa")[1].token_priority is None
    assert merged.check_final_state("bb")[1].token_priority is None
