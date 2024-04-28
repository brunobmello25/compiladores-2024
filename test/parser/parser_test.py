from src.parser.ast import Assignment, BinaryExpression, NumberLiteral, PrintStatement, StringLiteral, VariableReference
from src.parser.parser import Parser
from src.scanner.scanner_generator import ScannerGenerator
from src.scanner.token import Token
from src.scanner.token_priority import TokenPriority


def test_complex_expression_parsing():
    """
    scanner for:

    10 LET RESULT = A + B * C / (B - A)
    """
    scanner = ScannerGenerator()\
        .add_token("x", "filler", TokenPriority.LOW)\
        .generate_scanner()

    scanner.DEBUG_tokens = [
        Token("10", "NUMBER", TokenPriority.LOW),
        Token("LET", "LET", TokenPriority.HIGH),
        Token("RESULT", "IDENTIFIER", TokenPriority.LOW),
        Token("=", "EQUALS", TokenPriority.HIGH),
        Token("A", "IDENTIFIER", TokenPriority.LOW),
        Token("+", "ADDITION", TokenPriority.HIGH),
        Token("B", "IDENTIFIER", TokenPriority.LOW),
        Token("*", "MULTIPLICATION", TokenPriority.HIGH),
        Token("C", "IDENTIFIER", TokenPriority.LOW),
        Token("/", "DIVISION", TokenPriority.HIGH),
        Token("(", "LPAREN", TokenPriority.HIGH),
        Token("B", "IDENTIFIER", TokenPriority.LOW),
        Token("-", "SUBTRACTION", TokenPriority.HIGH),
        Token("A", "IDENTIFIER", TokenPriority.LOW),
        Token(")", "RPAREN", TokenPriority.HIGH),
    ]

    result = Parser(scanner).parse()

    stmt = result.statements[0][0]
    assert isinstance(stmt, Assignment)
    assert stmt == Assignment("RESULT", BinaryExpression(
        left=VariableReference("A"),
        operator="ADDITION",
        right=BinaryExpression(
            left=BinaryExpression(
                left=VariableReference("B"),
                operator="MULTIPLICATION",
                right=VariableReference("C"),
            ),
            operator="DIVISION",
            right=BinaryExpression(
                left=VariableReference("B"),
                operator="SUBTRACTION",
                right=VariableReference("A"),
            ),
        )
    ))


def test_parse_basic_language():
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

        Token("20", "NUMBER", TokenPriority.LOW),
        Token("LET", "LET", TokenPriority.HIGH),
        Token("B", "IDENTIFIER", TokenPriority.LOW),
        Token("=", "EQUALS", TokenPriority.HIGH),
        Token("10", "NUMBER", TokenPriority.LOW),

        Token("30", "NUMBER", TokenPriority.LOW),
        Token("LET", "LET", TokenPriority.HIGH),
        Token("C", "IDENTIFIER", TokenPriority.LOW),
        Token("=", "EQUALS", TokenPriority.HIGH),
        Token("A", "IDENTIFIER", TokenPriority.LOW),
        Token("+", "ADDITION", TokenPriority.HIGH),
        Token("B", "IDENTIFIER", TokenPriority.LOW),

        Token("40", "NUMBER", TokenPriority.LOW),
        Token("PRINT", "PRINT", TokenPriority.HIGH),
        Token("C", "IDENTIFIER", TokenPriority.LOW),

        Token("50", "NUMBER", TokenPriority.LOW),
        Token("PRINT", "PRINT", TokenPriority.HIGH),
        Token("SUM OF A AND B IS", "STRING", TokenPriority.LOW),

        Token("60", "NUMBER", TokenPriority.LOW),
        Token("PRINT", "PRINT", TokenPriority.HIGH),
        Token("A", "IDENTIFIER", TokenPriority.LOW),
        Token("+", "ADDITION", TokenPriority.HIGH),
        Token("B", "IDENTIFIER", TokenPriority.LOW),
    ]

    result = Parser(scanner).parse()

    stmt = result.statements[0][0]
    assert isinstance(stmt, Assignment)
    assert stmt == Assignment("A", NumberLiteral("5"))

    stmt = result.statements[1][0]
    assert isinstance(stmt, Assignment)
    assert stmt == Assignment("B", NumberLiteral("10"))

    stmt = result.statements[2][0]
    assert isinstance(stmt, Assignment)
    assert stmt == Assignment("C", BinaryExpression(
        left=VariableReference("A"), right=VariableReference("B"), operator="ADDITION"))

    stmt = result.statements[3][0]
    assert isinstance(stmt, PrintStatement)
    assert stmt == PrintStatement(VariableReference("C"))

    stmt = result.statements[4][0]
    assert isinstance(stmt, PrintStatement)
    assert stmt == PrintStatement(StringLiteral("SUM OF A AND B IS"))

    stmt = result.statements[5][0]
    assert isinstance(stmt, PrintStatement)
    assert stmt == PrintStatement(
        BinaryExpression(
            left=VariableReference("A"),
            operator="ADDITION",
            right=VariableReference("B"),
        )
    )
