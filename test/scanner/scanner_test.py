from src.scanner.scanner import LexicalError, Token
from src.scanner.scanner_generator import ScannerGenerator
from src.scanner.token_priority import TokenPriority


def test_scan_with_skipable_only_spaces():
    scanner = ScannerGenerator()\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .with_input('A BC  D')\
        .generate_scanner()

    expected_tokens = [
        ("A", "IDENTIFIER", TokenPriority.LOW),
        ("BC", "IDENTIFIER", TokenPriority.LOW),
        ("D", "IDENTIFIER", TokenPriority.LOW),
        ("", "EOF", TokenPriority.EOF),
        ("", "EOF", TokenPriority.EOF),
    ]

    for expected_token in expected_tokens:
        result = scanner.next_token()
        assert isinstance(result, Token)
        assert result.value == expected_token[0]
        assert result.type == expected_token[1]
        assert result.priority == expected_token[2]


def test_scan_with_whitespace():
    input = 'A  B  "uma  string  longa"'

    scanner = ScannerGenerator()\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .add_token('\\"([A-z]|[0-9]| )*\\"', "STRING", TokenPriority.HIGH)\
        .with_input(input)\
        .generate_scanner()

    expected_tokens = [
        ("A", "IDENTIFIER", TokenPriority.LOW),
        ("B", "IDENTIFIER", TokenPriority.LOW),
        ('"uma  string  longa"', "STRING", TokenPriority.HIGH),
        ("", "EOF", TokenPriority.EOF),
        ("", "EOF", TokenPriority.EOF),
        ("", "EOF", TokenPriority.EOF),
    ]

    for expected_token in expected_tokens:
        result = scanner.next_token()
        assert isinstance(result, Token)
        assert result.value == expected_token[0]
        assert result.type == expected_token[1]
        assert result.priority == expected_token[2]


def test_scan_with_backtrack():
    scanner = ScannerGenerator()\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .add_token("\\(", "LPAREN", TokenPriority.HIGH)\
        .with_input("(ABC")\
        .generate_scanner()

    expected_tokens = [
        ("(", "LPAREN", TokenPriority.HIGH),
        ("ABC", "IDENTIFIER", TokenPriority.LOW),
        ("", "EOF", TokenPriority.EOF),
    ]

    for expected_token in expected_tokens:
        result = scanner.next_token()
        assert isinstance(result, Token)
        assert result.value == expected_token[0]
        assert result.type == expected_token[1]
        assert result.priority == expected_token[2]


def test_scan_string_and_symbols():
    scanner = ScannerGenerator()\
        .add_token("\"([A-z]|[0-9]| )*\"", "STRING", TokenPriority.HIGH)\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .with_input('A BC "um dois tres" D')\
        .generate_scanner()

    expected_tokens = [
        ("A", "IDENTIFIER", TokenPriority.LOW),
        ("BC", "IDENTIFIER", TokenPriority.LOW),
        ('"um dois tres"', "STRING", TokenPriority.HIGH),
        ("D", "IDENTIFIER", TokenPriority.LOW),
    ]

    for expected_token in expected_tokens:
        token = scanner.next_token()
        assert isinstance(token, Token)
        assert token.value == expected_token[0]
        assert token.type == expected_token[1]
        assert token.priority == expected_token[2]


def test_parse_string():
    input = '"A 10 20 B 30"'
    scanner = ScannerGenerator()\
        .add_token('\\"([A-z]|[0-9]| )*\\"', "STRING", TokenPriority.HIGH)\
        .with_input(input)\
        .generate_scanner()

    result = scanner.next_token()
    assert isinstance(result, Token)
    assert result.type == "STRING"
    assert result.value == '"A 10 20 B 30"'


def test_invalid_token():
    input = "10"

    scanner = ScannerGenerator()\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .with_input(input)\
        .generate_scanner()

    result = scanner.next_token()
    assert isinstance(result, LexicalError)


def test_next_token():
    input = "10 LET RESULT = (A + B) * ((C / (D - E)) + F)"

    scanner = ScannerGenerator()\
        .add_token("[0-9]*", "NUMBER", TokenPriority.HIGH)\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .add_token("LET", "LET", TokenPriority.HIGH)\
        .add_token("\\(", "LPAREN", TokenPriority.HIGH)\
        .add_token("\\)", "RPAREN", TokenPriority.HIGH)\
        .add_token("\\+", "ADDITION", TokenPriority.HIGH)\
        .add_token("\\*", "MULTIPLICATION", TokenPriority.HIGH)\
        .add_token("/", "DIVISION", TokenPriority.HIGH)\
        .add_token("-", "SUBTRACTION", TokenPriority.HIGH)\
        .add_token("=", "ASSIGNMENT", TokenPriority.HIGH)\
        .with_input(input)\
        .generate_scanner()

    expected_tokens = [
        ("10", "NUMBER", TokenPriority.HIGH),
        ("LET", "LET", TokenPriority.HIGH),
        ("RESULT", "IDENTIFIER", TokenPriority.LOW),
        ("=", "ASSIGNMENT", TokenPriority.HIGH),
        ("(", "LPAREN", TokenPriority.HIGH),
        ("A", "IDENTIFIER", TokenPriority.LOW),
        ("+", "ADDITION", TokenPriority.HIGH),
        ("B", "IDENTIFIER", TokenPriority.LOW),
        (")", "RPAREN", TokenPriority.HIGH),
        ("*", "MULTIPLICATION", TokenPriority.HIGH),
        ("(", "LPAREN", TokenPriority.HIGH),
        ("(", "LPAREN", TokenPriority.HIGH),
        ("C", "IDENTIFIER", TokenPriority.LOW),
        ("/", "DIVISION", TokenPriority.HIGH),
        ("(", "LPAREN", TokenPriority.HIGH),
        ("D", "IDENTIFIER", TokenPriority.LOW),
        ("-", "SUBTRACTION", TokenPriority.HIGH),
        ("E", "IDENTIFIER", TokenPriority.LOW),
        (")", "RPAREN", TokenPriority.HIGH),
        (")", "RPAREN", TokenPriority.HIGH),
        ("+", "ADDITION", TokenPriority.HIGH),
        ("F", "IDENTIFIER", TokenPriority.LOW),
        (")", "RPAREN", TokenPriority.HIGH),
        ("", "EOF", TokenPriority.EOF),
        ("", "EOF", TokenPriority.EOF),
        ("", "EOF", TokenPriority.EOF),
        ("", "EOF", TokenPriority.EOF),
    ]

    for expected_token in expected_tokens:
        token = scanner.next_token()
        assert isinstance(token, Token)
        assert token.value == expected_token[0]
        assert token.type == expected_token[1]
        assert token.priority == expected_token[2]
