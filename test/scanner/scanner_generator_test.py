import pytest
from src.scanner.scanner_generator import ScannerGenerator
from src.scanner.token_priority import TokenPriority


@pytest.mark.skip("should fix the problem that happens with star and or operator when parsing this regex: \"(a|(b|c))*\"")
def test_scanner_generator_add_token():
    generator = ScannerGenerator()
    scanner = generator\
        .add_token("[A-z]([a-z]|([A-Z]|[0-9]))*", "identifier", TokenPriority.LOW)\
        .add_token("let", "let", TokenPriority.HIGH)\
        .generate_scanner()

    assert scanner.automata.check_final_state("let")[0]
    assert scanner.automata.check_final_state("let")[1].token_type == "let"
    assert scanner.automata.check_final_state(
        "let")[1].token_priority == TokenPriority.HIGH

    assert scanner.automata.check_final_state("banana")[0]
    assert scanner.automata.check_final_state(
        "banana")[1].token_type == "identifier"
    assert scanner.automata.check_final_state(
        "let")[1].token_priority == TokenPriority.LOW
