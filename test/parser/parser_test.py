from src.parser.parser import Parser
from src.scanner.scanner import Scanner
from src.scanner.scanner_generator import ScannerGenerator
from src.scanner.token import Token
from src.scanner.token_priority import TokenPriority


def test_parse_basic_language():
    scanner = _build_basic_scanner()
    result = Parser(scanner).parse()

    print(result)


def _build_basic_scanner() -> Scanner:
    """
    scanner for the following basic program:

    10 LET A = 5
    20 LET B = 10
    30 LET C = A + B
    40 PRINT C
    50 PRINT "SUM OF A AND B IS"
    60 PRINT A + B
    """

    scanner = ScannerGenerator()\
        .add_token("x", "filler", TokenPriority.LOW)\
        .generate_scanner()

    scanner.DEBUG_tokens = [
        Token("10", "NUMBER", TokenPriority.LOW),
        Token("LET", "LET", TokenPriority.HIGH),
        Token("A", "IDENTIFIER", TokenPriority.LOW),
        Token("=", "EQUALS", TokenPriority.HIGH),
        Token("5", "NUMBER", TokenPriority.LOW),
        Token("+", "PLUS", TokenPriority.HIGH),
        Token("2", "NUMBER", TokenPriority.LOW),

        # Token("10", "NUMBER", TokenPriority.LOW),
        # Token("LET", "LET", TokenPriority.HIGH),
        # Token("A", "IDENTIFIER", TokenPriority.LOW),
        # Token("=", "EQUALS", TokenPriority.HIGH),
        # Token("5", "NUMBER", TokenPriority.LOW),
        #
        # Token("20", "NUMBER", TokenPriority.LOW),
        # Token("LET", "LET", TokenPriority.HIGH),
        # Token("B", "IDENTIFIER", TokenPriority.LOW),
        # Token("=", "EQUALS", TokenPriority.HIGH),
        # Token("10", "NUMBER", TokenPriority.LOW),
        #
        # Token("30", "NUMBER", TokenPriority.LOW),
        # Token("LET", "LET", TokenPriority.HIGH),
        # Token("C", "IDENTIFIER", TokenPriority.LOW),
        # Token("=", "EQUALS", TokenPriority.HIGH),
        # Token("A", "IDENTIFIER", TokenPriority.LOW),
        # Token("+", "PLUS", TokenPriority.HIGH),
        # Token("B", "IDENTIFIER", TokenPriority.LOW),
        #
        # Token("40", "NUMBER", TokenPriority.LOW),
        # Token("PRINT", "PRINT", TokenPriority.HIGH),
        # Token("C", "IDENTIFIER", TokenPriority.LOW),
        #
        # Token("50", "NUMBER", TokenPriority.LOW),
        # Token("PRINT", "PRINT", TokenPriority.HIGH),
        # Token("SUM OF A AND B IS", "STRING", TokenPriority.LOW),
        #
        # Token("60", "NUMBER", TokenPriority.LOW),
        # Token("PRINT", "PRINT", TokenPriority.HIGH),
        # Token("A", "IDENTIFIER", TokenPriority.LOW),
        # Token("+", "PLUS", TokenPriority.HIGH),
        # Token("B", "IDENTIFIER", TokenPriority.LOW),
    ]

    return scanner
