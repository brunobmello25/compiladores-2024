from src.automata.automata import Automata
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


def test_parse_concat_regex():
    Automata.state_counter = 0
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
