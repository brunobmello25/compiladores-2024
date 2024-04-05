from src.automata.automata import Automata
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


def test_parse_concat_regex():
    Automata.state_counter = 0
    lexer = RegexLexer("abc")

    result = RegexParser(lexer).parse()

    assert len(result.states) == 7

    assert result.states == ["q0", "q3", "q4", "q7", "q8", "q11", "q12"]
    assert result.start_state == "q0"
    assert result.accept_states == ["q12"]
    assert result.transition_function[("q0", None)] == {"q3"}
    assert result.transition_function[("q3", "a")] == {"q4"}
    assert result.transition_function[("q4", None)] == {"q7"}
    assert result.transition_function[("q7", "b")] == {"q8"}
    assert result.transition_function[("q8", None)] == {"q11"}
    assert result.transition_function[("q11", "c")] == {"q12"}
    assert len(result.transition_function.keys()) == 6
