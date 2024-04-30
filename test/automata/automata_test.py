import string
from typing import Tuple
from src.automata.automata import Automata
from src.automata.state import State
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser
from src.utils.symbol import Symbol, SymbolType


def test_special_symbols():
    State.state_counter = 0

    a = RegexParser(RegexLexer("!=;!;=_=_")).parse()

    state_names = {state.name for state in a.states}
    accept_state_names = {state.name for state in a.accept_states}

    assert state_names == {"q0", "q1", "q2", "q3", "q4", "q5",
                           "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18"}
    assert accept_state_names == {"q18"}
    assert a.start_state.name == "q0"
    assert a.check_transition_by_state_name("q0", "q1", None)
    assert a.check_transition_by_state_name("q1", "q2", "!")
    assert a.check_transition_by_state_name("q2", "q3", None)
    assert a.check_transition_by_state_name("q3", "q4", "=")
    assert a.check_transition_by_state_name("q4", "q5", None)
    assert a.check_transition_by_state_name("q5", "q6", ";")
    assert a.check_transition_by_state_name("q6", "q7", None)
    assert a.check_transition_by_state_name("q7", "q8", "!")
    assert a.check_transition_by_state_name("q8", "q9", None)
    assert a.check_transition_by_state_name("q9", "q10", ";")
    assert a.check_transition_by_state_name("q10", "q11", None)
    assert a.check_transition_by_state_name("q11", "q12", "=")
    assert a.check_transition_by_state_name("q12", "q13", None)
    assert a.check_transition_by_state_name("q13", "q14", "_")
    assert a.check_transition_by_state_name("q14", "q15", None)
    assert a.check_transition_by_state_name("q15", "q16", "=")
    assert a.check_transition_by_state_name("q16", "q17", None)
    assert a.check_transition_by_state_name("q17", "q18", "_")


def test_symbol_set():
    State.state_counter = 0
    a = RegexParser(RegexLexer("a|b?c+d*")).parse()

    assert a.symbol_set() == {"a", "b", "c", "d"}


def test_epsilon_closure():
    State.state_counter = 0
    a = RegexParser(RegexLexer("(a|b)")).parse()

    def closure(name: str):
        state = [state for state in a.states if state.name == name][0]
        closure = {state.name for state in a.epsilon_closure(state)}
        return closure

    assert closure("q0") == {"q0", "q1", "q2", "q4", "q5", "q7"}
    assert closure("q7") == {"q7", "q1", "q2", "q4", "q5"}
    assert closure("q1") == {"q1", "q2"}
    assert closure("q4") == {"q4", "q5"}
    assert closure("q2") == {"q2"}
    assert closure("q5") == {"q5"}


def test_make_shortcut_lower():
    State.state_counter = 0

    symbol = Symbol(SymbolType.LOWER, SymbolType.LOWER.value)
    a = Automata.make_shortcut_automata(symbol)

    q0 = a.start_state
    q1 = a.accept_states.pop()

    for letter in string.ascii_lowercase:
        assert a.transition_function[(q0, letter)] == {q1}

    assert len(a.transition_function.keys()) == 26


def test_make_shortcut_upper():
    State.state_counter = 0

    symbol = Symbol(SymbolType.UPPER, SymbolType.UPPER.value)
    a = Automata.make_shortcut_automata(symbol)

    q0 = a.start_state
    q1 = a.accept_states.pop()

    for letter in string.ascii_uppercase:
        assert a.transition_function[(q0, letter)] == {q1}

    assert len(a.transition_function.keys()) == 26


def test_make_shortcut_upper_and_lower():
    State.state_counter = 0

    symbol = Symbol(SymbolType.TEXT, SymbolType.TEXT.value)
    a = Automata.make_shortcut_automata(symbol)

    q0 = a.start_state
    q1 = a.accept_states.pop()

    for letter in string.ascii_uppercase:
        assert a.transition_function[(q0, letter)] == {q1}

    for letter in string.ascii_lowercase:
        assert a.transition_function[(q0, letter)] == {q1}

    assert len(a.transition_function.keys()) == 52


def test_init_automata():
    State.state_counter = 0
    a = Automata()
    q0 = a.start_state

    assert q0.name == "q0"

    assert a.states == {q0}
    assert a.transition_function == {}
    assert a.accept_states == {q0}


def test_add_state():
    State.state_counter = 0
    a1 = Automata()
    a2 = Automata()

    q0 = a1.start_state
    q2 = a1.add_state(False)
    q3 = a1.add_state(False)
    q4 = a1.add_state(True)

    q1 = a2.start_state
    q5 = a2.add_state(True)
    q6 = a2.add_state(False)

    assert q0.name == "q0"
    assert q1.name == "q1"
    assert q2.name == "q2"
    assert q3.name == "q3"
    assert q4.name == "q4"
    assert q5.name == "q5"
    assert q6.name == "q6"

    assert a1.states == {q0, q2, q3, q4}
    assert a2.states == {q1, q5, q6}

    assert a1.accept_states == {q0, q4}
    assert a2.accept_states == {q1, q5}


def test_add_transition():
    State.state_counter = 0
    a = Automata()

    q0 = a.start_state
    q1 = a.add_state(False)
    q2 = a.add_state(True)

    a.add_transition(q0, q1, "a")
    a.add_transition(q1, q2, "1")
    a.add_transition(q1, q0, "1")
    a.add_transition(q2, q0, "[A-Z]")

    assert a.transition_function[(q0, "a")] == {q1}
    assert a.transition_function[(q1, "1")] == {q2, q0}
    assert a.transition_function[(q2, "[A-Z]")] == {q0}


def test_union():
    State.state_counter = 0
    a1, q0, q1 = make_basic_char_automata()
    a2, q2, q3 = make_basic_char_automata("b")

    result = Automata.union(a1, a2)
    q4 = result.start_state

    assert result.states == {q0, q1, q2, q3, q4}
    assert result.accept_states == {q1, q3}
    assert result.transition_function[(q4, None)] == {q0, q2}
    assert result.transition_function[(q0, "a")] == {q1}
    assert result.transition_function[(q2, "b")] == {q3}
    assert len(result.transition_function.keys()) == 3


def test_optional():
    State.state_counter = 0
    a, q0, q1 = make_basic_char_automata()

    a.optional()

    assert a.states == {q0, q1}
    assert a.accept_states == {q0, q1}
    assert a.start_state == q0
    assert a.transition_function[(q0, "a")] == {q1}


def test_concat_empty_with_symbol():
    State.state_counter = 0
    start = Automata()
    q0 = start.start_state

    symbol_automata, q1, q2 = make_basic_char_automata()

    start.concat(symbol_automata)

    assert start.states == {q0, q1, q2}
    assert start.accept_states == {q2}
    assert start.start_state == q0
    assert start.transition_function[(q0, None)] == {q1}
    assert start.transition_function[(q1, "a")] == {q2}
    assert len(start.transition_function.keys()) == 2


def test_concat():
    State.state_counter = 0
    a1 = Automata()
    q0 = a1.accept_states.pop()
    q1 = a1.add_state(False)
    q2 = a1.add_state(True)
    q3 = a1.add_state(False)
    q4 = a1.add_state(True)
    a1.add_transition(q0, q1, None)
    a1.add_transition(q1, q2, "a")
    a1.add_transition(q0, q3, None)
    a1.add_transition(q3, q4, "b")

    a2 = Automata()
    q5 = a2.accept_states.pop()
    q6 = a2.add_state(True)
    a2.add_transition(q5, q6, "c")

    a1.concat(a2)

    assert a1.states == {q0, q1, q2, q3, q4, q5, q6}
    assert a1.start_state == q0
    assert a1.accept_states == {q6}

    assert a1.transition_function[(q0, None)] == {q1, q3}
    assert a1.transition_function[(q1, "a")] == {q2}
    assert a1.transition_function[(q3, "b")] == {q4}
    assert a1.transition_function[(q2, None)] == {q5}
    assert a1.transition_function[(q4, None)] == {q5}
    assert a1.transition_function[(q5, "c")] == {q6}
    assert len(a1.transition_function.keys()) == 6


def test_plus():
    State.state_counter = 0
    a, q0, q1 = make_basic_char_automata()

    a.plus()

    assert a.states == {q0, q1}
    assert a.start_state == q0
    assert a.accept_states == {q1}
    assert a.transition_function[(q0, "a")] == {q1}
    assert a.transition_function[(q1, None)] == {q0}
    assert len(a.transition_function.keys()) == 2


def test_star():
    State.state_counter = 0
    a, q0, q1 = make_basic_char_automata()

    a.star()

    assert a.states == {q0, q1}
    assert a.start_state == q0
    assert a.accept_states == {q0, q1}
    assert a.transition_function[(q0, "a")] == {q1}
    assert a.transition_function[(q1, None)] == {q0}
    assert len(a.transition_function.keys()) == 2


def make_basic_char_automata(symbol="a") -> Tuple[Automata, State, State]:
    a = Automata()

    q0 = a.accept_states.pop()

    q1 = a.add_state(True)
    a.add_transition(q0, q1, symbol)

    return a, q0, q1
