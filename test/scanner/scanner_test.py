from src.scanner.scanner_generator import ScannerGenerator
from src.scanner.token import Token
from src.scanner.token_priority import TokenPriority


def test_DEBUG_next_token():
    scanner = ScannerGenerator()\
        .add_token("let", "let", TokenPriority.HIGH)\
        .generate_scanner()

    scanner.DEBUG_tokens = [
        Token("type1", TokenPriority.LOW),
        Token("type2", TokenPriority.LOW)
    ]

    token = scanner.next_token()
    assert token.type == "type1"
    assert token.priority == TokenPriority.LOW

    token = scanner.next_token()
    assert token.type == "type2"
    assert token.priority == TokenPriority.LOW

    assert scanner.next_token().type == "EOF"
    assert scanner.next_token().type == "EOF"
    assert scanner.next_token().type == "EOF"
    assert scanner.next_token().type == "EOF"
    assert scanner.next_token().type == "EOF"
