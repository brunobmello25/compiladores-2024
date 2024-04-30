from src.scanner.scanner_generator import ScannerGenerator
from src.scanner.token_priority import TokenPriority


def test_scanner_generator_add_token():
    generator = ScannerGenerator()
    scanner = generator\
        .add_token("[A-z]([a-z]|([A-Z]|[0-9]))*", "identifier", TokenPriority.LOW)\
        .add_token("let", "let", TokenPriority.HIGH)\
        .add_token("[0-9]+", "number", TokenPriority.HIGH)\
        .with_input("")\
        .generate_scanner()

    assert scanner.automata is not None
    passes, state = scanner.automata.check_final_state("let")
    assert passes
    assert state.token_type == "let"
    assert state.token_priority == TokenPriority.HIGH

    passes, state = scanner.automata.check_final_state("banana")
    assert passes
    assert state.token_type == "identifier"
    assert state.token_priority == TokenPriority.LOW

    passes, state = scanner.automata.check_final_state("12345")
    assert passes
    assert state.token_type == "number"
    assert state.token_priority == TokenPriority.HIGH

    assert not scanner.automata.check("0invalid")
    assert not scanner.automata.check("(parenthesis)")
    assert not scanner.automata.check("")
