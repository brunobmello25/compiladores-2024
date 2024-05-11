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
    input = 'A  B  "uma  string  longa" \'outra string\''

    scanner = ScannerGenerator()\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .add_token('\\"([A-z]|[0-9]| )*\\"', "STRING_DOUBLE", TokenPriority.HIGH)\
        .add_token("\\'([A-z]|[0-9]| )*\\'", "STRING_SINGLE", TokenPriority.HIGH)\
        .with_input(input)\
        .generate_scanner()

    expected_tokens = [
        ("A", "IDENTIFIER", TokenPriority.LOW),
        ("B", "IDENTIFIER", TokenPriority.LOW),
        ('"uma  string  longa"', "STRING_DOUBLE", TokenPriority.HIGH),
        ("'outra string'", "STRING_SINGLE", TokenPriority.HIGH),
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


def test_scan_basic_language():
    input = '''10 LET A = 5
               20 PRINT C
               30 PRINT "SUM OF A AND B IS"
               40 PRINT A + B
               50 IF A > B THEN IF C > D THEN PRINT "UM" ELSE PRINT "DOIS" ELSE PRINT "TRES"
               60 IF A <= B THEN IF C == D THEN PRINT "UM" ELSE PRINT "DOIS" ELSE PRINT "TRES"
               70 IF A != B THEN PRINT A'''

    scanner = ScannerGenerator()\
        .add_token("[0-9]*", "NUMBER", TokenPriority.HIGH)\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .add_token('"([A-z]|[0-9]| )*"', "STRING", TokenPriority.HIGH)\
        .add_token("LET", "LET", TokenPriority.HIGH)\
        .add_token("IF", "IF", TokenPriority.HIGH)\
        .add_token("THEN", "THEN", TokenPriority.HIGH)\
        .add_token("ELSE", "ELSE", TokenPriority.HIGH)\
        .add_token("PRINT", "PRINT", TokenPriority.HIGH)\
        .add_token("\\(", "LPAREN", TokenPriority.HIGH)\
        .add_token("\\)", "RPAREN", TokenPriority.HIGH)\
        .add_token("\\+", "ADDITION", TokenPriority.HIGH)\
        .add_token("\\*", "MULTIPLICATION", TokenPriority.HIGH)\
        .add_token("\\/", "DIVISION", TokenPriority.HIGH)\
        .add_token("\\-", "SUBTRACTION", TokenPriority.HIGH)\
        .add_token("\\=", "ASSIGNMENT", TokenPriority.HIGH)\
        .add_token("\\==", "EQUAL", TokenPriority.HIGH)\
        .add_token("\\!=", "NE", TokenPriority.HIGH)\
        .add_token("\\>", "GT", TokenPriority.HIGH)\
        .add_token("\\<", "LT", TokenPriority.HIGH)\
        .add_token("\\<=", "LTE", TokenPriority.HIGH)\
        .add_token("\\>=", "GTE", TokenPriority.HIGH)\
        .with_input(input)\
        .generate_scanner()

    expected_tokens = [
        ("10", "NUMBER", TokenPriority.HIGH),
        ("LET", "LET", TokenPriority.HIGH),
        ("A", "IDENTIFIER", TokenPriority.LOW),
        ("=", "ASSIGNMENT", TokenPriority.HIGH),
        ("5", "NUMBER", TokenPriority.HIGH),

        ("20", "NUMBER", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ("C", "IDENTIFIER", TokenPriority.LOW),

        ("30", "NUMBER", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ('"SUM OF A AND B IS"', "STRING", TokenPriority.HIGH),

        ("40", "NUMBER", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ("A", "IDENTIFIER", TokenPriority.LOW),
        ("+", "ADDITION", TokenPriority.HIGH),
        ("B", "IDENTIFIER", TokenPriority.LOW),

        ("50", "NUMBER", TokenPriority.HIGH),
        ("IF", "IF", TokenPriority.HIGH),
        ("A", "IDENTIFIER", TokenPriority.LOW),
        (">", "GT", TokenPriority.HIGH),
        ("B", "IDENTIFIER", TokenPriority.LOW),
        ("THEN", "THEN", TokenPriority.HIGH),
        ("IF", "IF", TokenPriority.HIGH),
        ("C", "IDENTIFIER", TokenPriority.LOW),
        (">", "GT", TokenPriority.HIGH),
        ("D", "IDENTIFIER", TokenPriority.LOW),
        ("THEN", "THEN", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ('"UM"', "STRING", TokenPriority.HIGH),
        ("ELSE", "ELSE", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ('"DOIS"', "STRING", TokenPriority.HIGH),
        ("ELSE", "ELSE", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ('"TRES"', "STRING", TokenPriority.HIGH),

        ("60", "NUMBER", TokenPriority.HIGH),
        ("IF", "IF", TokenPriority.HIGH),
        ("A", "IDENTIFIER", TokenPriority.LOW),
        ("<=", "LTE", TokenPriority.HIGH),
        ("B", "IDENTIFIER", TokenPriority.LOW),
        ("THEN", "THEN", TokenPriority.HIGH),
        ("IF", "IF", TokenPriority.HIGH),
        ("C", "IDENTIFIER", TokenPriority.LOW),
        ("==", "EQUAL", TokenPriority.HIGH),
        ("D", "IDENTIFIER", TokenPriority.LOW),
        ("THEN", "THEN", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ('"UM"', "STRING", TokenPriority.HIGH),
        ("ELSE", "ELSE", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ('"DOIS"', "STRING", TokenPriority.HIGH),
        ("ELSE", "ELSE", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ('"TRES"', "STRING", TokenPriority.HIGH),

        ("70", "NUMBER", TokenPriority.HIGH),
        ("IF", "IF", TokenPriority.HIGH),
        ("A", "IDENTIFIER", TokenPriority.LOW),
        ("!=", "NE", TokenPriority.HIGH),
        ("B", "IDENTIFIER", TokenPriority.LOW),
        ("THEN", "THEN", TokenPriority.HIGH),
        ("PRINT", "PRINT", TokenPriority.HIGH),
        ("A", "IDENTIFIER", TokenPriority.LOW),
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
