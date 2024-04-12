from src.automata.state import State
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


def test_shortcut_concatenation():
    State.state_counter = 0
    result = RegexParser(RegexLexer("1[a-z]2")).parse()

    result_state_names = {state.name for state in result.states}
    result_accept_state_names = {state.name for state in result.accept_states}

    assert result_state_names == {
        "q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7"}
    assert result_accept_state_names == {"q7"}
    assert result.start_state.name == "q0"

    assert result.check_transition_by_state_name("q0", "q1", None)
    assert result.check_transition_by_state_name("q1", "q2", "1")
    assert result.check_transition_by_state_name("q2", "q3", None)
    assert result.check_transition_by_state_name("q3", "q4", "a")
    assert result.check_transition_by_state_name("q3", "q4", "b")
    assert result.check_transition_by_state_name("q3", "q4", "c")
    assert result.check_transition_by_state_name("q3", "q4", "d")
    assert result.check_transition_by_state_name("q3", "q4", "e")
    assert result.check_transition_by_state_name("q3", "q4", "f")
    assert result.check_transition_by_state_name("q3", "q4", "g")
    assert result.check_transition_by_state_name("q3", "q4", "h")
    assert result.check_transition_by_state_name("q3", "q4", "i")
    assert result.check_transition_by_state_name("q3", "q4", "j")
    assert result.check_transition_by_state_name("q3", "q4", "k")
    assert result.check_transition_by_state_name("q3", "q4", "l")
    assert result.check_transition_by_state_name("q3", "q4", "m")
    assert result.check_transition_by_state_name("q3", "q4", "n")
    assert result.check_transition_by_state_name("q3", "q4", "o")
    assert result.check_transition_by_state_name("q3", "q4", "p")
    assert result.check_transition_by_state_name("q3", "q4", "q")
    assert result.check_transition_by_state_name("q3", "q4", "r")
    assert result.check_transition_by_state_name("q3", "q4", "s")
    assert result.check_transition_by_state_name("q3", "q4", "t")
    assert result.check_transition_by_state_name("q3", "q4", "u")
    assert result.check_transition_by_state_name("q3", "q4", "v")
    assert result.check_transition_by_state_name("q3", "q4", "w")
    assert result.check_transition_by_state_name("q3", "q4", "x")
    assert result.check_transition_by_state_name("q3", "q4", "y")
    assert result.check_transition_by_state_name("q3", "q4", "z")
    assert result.check_transition_by_state_name("q4", "q5", None)
    assert result.check_transition_by_state_name("q5", "q6", None)
    assert result.check_transition_by_state_name("q6", "q7", "2")
    assert len(result.transition_function.keys()) == 32


def test_optional():
    State.state_counter = 0
    result = RegexParser(RegexLexer("a?")).parse()

    result_state_names = {state.name for state in result.states}
    result_accept_state_names = {state.name for state in result.accept_states}

    assert result_state_names == {"q0", "q1", "q2"}
    assert result_accept_state_names == {"q0", "q2"}
    assert result.start_state.name == "q0"
    assert result.check_transition_by_state_name("q0", "q1", None)
    assert result.check_transition_by_state_name("q1", "q2", "a")
    assert len(result.transition_function.keys()) == 2


def test_plus():
    State.state_counter = 0
    result = RegexParser(RegexLexer("a+")).parse()

    result_state_names = {state.name for state in result.states}
    result_accept_state_names = {state.name for state in result.accept_states}

    assert result_state_names == {"q0", "q1", "q2"}
    assert result_accept_state_names == {"q2"}
    assert result.start_state.name == "q0"
    assert result.check_transition_by_state_name("q0", "q1", None)
    assert result.check_transition_by_state_name("q1", "q2", "a")
    assert result.check_transition_by_state_name("q2", "q0", None)
    assert len(result.transition_function.keys()) == 3


def test_star():
    State.state_counter = 0
    result = RegexParser(RegexLexer("a*")).parse()

    result_state_names = {state.name for state in result.states}
    result_accept_state_names = {state.name for state in result.accept_states}

    assert result_state_names == {"q0", "q1", "q2"}
    assert result_accept_state_names == {"q0", "q2"}
    assert result.start_state.name == "q0"
    assert result.check_transition_by_state_name("q0", "q1", None)
    assert result.check_transition_by_state_name("q1", "q2", "a")
    assert result.check_transition_by_state_name("q2", "q0", None)
    assert len(result.transition_function.keys()) == 3


def test_union_2():
    State.state_counter = 0
    result = RegexParser(RegexLexer("(a|b)c")).parse()

    result_state_names = {state.name for state in result.states}
    result_accept_state_names = {state.name for state in result.accept_states}

    assert result_state_names == {"q0", "q1", "q2",
                                  "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"}
    assert result_accept_state_names == {"q10"}
    assert result.start_state.name == "q0"
    assert result.check_transition_by_state_name("q0", "q7", None)
    assert result.check_transition_by_state_name("q7", "q1", None)
    assert result.check_transition_by_state_name("q7", "q4", None)
    assert result.check_transition_by_state_name("q1", "q2", None)
    assert result.check_transition_by_state_name("q4", "q5", None)
    assert result.check_transition_by_state_name("q2", "q3", "a")
    assert result.check_transition_by_state_name("q5", "q6", "b")
    assert result.check_transition_by_state_name("q3", "q8", None)
    assert result.check_transition_by_state_name("q6", "q8", None)
    assert result.check_transition_by_state_name("q8", "q9", None)
    assert result.check_transition_by_state_name("q9", "q10", "c")
    assert len(result.transition_function.keys()) == 10


def test_union_1():
    State.state_counter = 0
    result = RegexParser(RegexLexer("ab|cd")).parse()
    result_states_names = {state.name for state in result.states}
    result_accept_state_names = {state.name for state in result.accept_states}

    assert result_states_names == {
        "q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"}
    assert result_accept_state_names == {"q4", "q9"}
    assert result.start_state.name == "q10"

    assert result.check_transition_by_state_name("q0", "q1", None)
    assert result.check_transition_by_state_name("q1", "q2", "a")
    assert result.check_transition_by_state_name("q2", "q3", None)
    assert result.check_transition_by_state_name("q3", "q4", "b")
    assert result.check_transition_by_state_name("q5", "q6", None)
    assert result.check_transition_by_state_name("q6", "q7", "c")
    assert result.check_transition_by_state_name("q7", "q8", None)
    assert result.check_transition_by_state_name("q8", "q9", "d")
    assert result.check_transition_by_state_name("q10", "q0", None)
    assert result.check_transition_by_state_name("q10", "q5", None)
    assert len(result.transition_function) == 9


def test_parse_concat_regex():
    State.state_counter = 0
    lexer = RegexLexer("abc")

    result = RegexParser(lexer).parse()

    result_states_names = {state.name for state in result.states}
    result_accept_states_names = {state.name for state in result.accept_states}

    assert len(result.states) == 7
    assert result_states_names == {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
    assert result.start_state.name == "q0"
    assert result_accept_states_names == {"q6"}
    assert result.check_transition_by_state_name("q0", "q1", None)
    assert result.check_transition_by_state_name("q1", "q2", "a")
    assert result.check_transition_by_state_name("q2", "q3", None)
    assert result.check_transition_by_state_name("q3", "q4", "b")
    assert result.check_transition_by_state_name("q4", "q5", None)
    assert result.check_transition_by_state_name("q5", "q6", "c")
    assert len(result.transition_function.keys()) == 6


def test_parse_parenthesis_regex():
    State.state_counter = 0
    lexer = RegexLexer("((a)b)")

    result = RegexParser(lexer).parse()

    result_states_names = {state.name for state in result.states}
    result_accept_states_names = {state.name for state in result.accept_states}

    assert len(result.states) == 8
    assert result_states_names == {
        "q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7"}
    assert result.start_state.name == "q0"
    assert result_accept_states_names == {"q7"}
    assert result.check_transition_by_state_name("q0", "q1", None)
    assert result.check_transition_by_state_name("q1", "q2", None)
    assert result.check_transition_by_state_name("q2", "q3", None)
    assert result.check_transition_by_state_name("q3", "q4", "a")
    assert result.check_transition_by_state_name("q4", "q5", None)
    assert result.check_transition_by_state_name("q5", "q6", None)
    assert result.check_transition_by_state_name("q6", "q7", "b")
    assert len(result.transition_function.keys()) == 7
