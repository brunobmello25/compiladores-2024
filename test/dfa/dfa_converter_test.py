from src.automata.state import State
from src.dfa.dfa_converter import DFAConverter
from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


def test_dfa_acception():
    State.state_counter = 0

    def run(regex: str, expect: bool, input: str):
        nfa = RegexParser(RegexLexer(regex)).parse()
        dfa = DFAConverter(nfa).get_dfa()

        if expect:
            assert dfa.check(input)
        else:
            assert not dfa.check(input)

    reg = "ab*c?d+e"
    run(reg, True, "abdde")
    run(reg, True, "abde")
    run(reg, True, "acde")
    run(reg, True, "acdde")
    run(reg, True, "ade")
    run(reg, True, "abbde")
    run(reg, True, "abbbde")
    run(reg, True, "abcde")
    run(reg, True, "abcdde")
    run(reg, True, "abbcdddde")
    run(reg, False, "abce")
    run(reg, False, "abc")
    run(reg, False, "abce")
    run(reg, False, "bacde")
    run(reg, False, "abdcde")
    run(reg, False, "adebde")
    run(reg, False, "abdede")
    run(reg, False, "aed")
    run(reg, False, "ab*cd+e")
    run(reg, False, "")
    run(reg, False, "ab")
    run(reg, False, "abdd")

    # int test
    reg = "int"
    run(reg, True, "int")
    run(reg, False, "in")
    run(reg, False, "i")
    run(reg, False, "nt")
    run(reg, False, "t")
    run(reg, False, "n")

    # identifier
    reg = "[A-z]([A-z]|[0-9])*"
    run(reg, True, "a")
    run(reg, True, "abcd")
    run(reg, True, "ab1234fdsfasdhuisad")
    run(reg, False, "123")
    run(reg, False, "123abc")
