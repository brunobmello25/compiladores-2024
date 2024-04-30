from typing import Dict, Tuple
from src.automata.state import State
from src.dfa.dfa import DFA
from src.dfa.dfa_converter import DFAConverter
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


def test_accept_escaped_characters():
    State.state_counter = 0

    nfa = RegexParser(RegexLexer("\\+\\[\\]\\(\\)\\*")).parse()
    dfa = DFAConverter(nfa).get_dfa()

    assert dfa.check("+[]()*")


def test_associate_token():
    State.state_counter = 0

    nfa = RegexParser(RegexLexer("int")).parse()
    dfa = DFAConverter(nfa).get_dfa()
    dfa.associate_token("int")

    for state in dfa.accept_states:
        assert state.token_type == "int"
    for state in {state for state in dfa.states if state not in dfa.accept_states}:
        assert state.token_type is None


def test_extend_alphabet():
    State.state_counter = 0

    q0 = State()
    q1 = State()
    q2 = State()
    transition_function: Dict[Tuple[State, str], State] = {
        (q0, "a"): q1,
        (q1, "a"): q2,
        (q2, "a"): q2,
    }
    dfa = DFA(
        start_state=q0,
        states={q0, q1, q2},
        transition_function=transition_function,
        accept_states={q1},
        alphabet={"a"},
    )

    dfa.extend_alphabet({"b"})

    assert dfa.check("a")
    assert not dfa.check("b")
    assert not dfa.check("ab")
    assert not dfa.check("ba")
    assert not dfa.check("aba")
    assert not dfa.check("bab")
    assert not dfa.check("aaa")
    assert not dfa.check("bbb")
    assert dfa.alphabet == {"a", "b"}
    assert len(dfa.states) == 4
    assert len(dfa.transition_function) == 8
    assert all(
        (state, symbol) in dfa.transition_function
        for state in dfa.states
        for symbol in dfa.alphabet
    )
