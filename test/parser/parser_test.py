from src.parser.ast import Assignment, BinaryExpression, NumberLiteral, PrintStatement, StringLiteral, VariableReference
from src.parser.parser import Parser
from src.scanner.scanner_generator import ScannerGenerator
from src.scanner.token_priority import TokenPriority


def test_multiple_paren_levels():
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

    result = Parser(scanner).parse()

    print()
    print(result)

    stmt = result.statements[0][0]
    assert isinstance(stmt, Assignment)
    assert stmt == Assignment("RESULT", BinaryExpression(
        left=BinaryExpression(
            left=VariableReference("A"),
            operator="ADDITION",
            right=VariableReference("B"),
        ),
        operator="MULTIPLICATION",
        right=BinaryExpression(
            left=BinaryExpression(
                left=VariableReference("C"),
                operator="DIVISION",
                right=BinaryExpression(
                    left=VariableReference("D"),
                    operator="SUBTRACTION",
                    right=VariableReference("E"),
                ),
            ),
            operator="ADDITION",
            right=VariableReference("F")
        ),
    ))


def test_complex_expression_parsing():
    input = "10 LET RESULT = A + B * C / (B - A)"
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
    # TODO: tirar isso quando resolver o problema das strings no scanner
    # input = '10 LET A = 5\n20 LET B = 10\n30 LET C = A + B\n40 PRINT C\n50 PRINT "SUM OF A AND B IS"\n60 PRINT A + B'
    input = '10 LET A = 5\n20 LET B = 10\n30 LET C = A + B\n40 PRINT C\n60 PRINT A + B'

    scanner = ScannerGenerator()\
        .add_token("[0-9]*", "NUMBER", TokenPriority.HIGH)\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .add_token('"([A-z]|[0-9])*"', "STRING", TokenPriority.HIGH)\
        .add_token("LET", "LET", TokenPriority.HIGH)\
        .add_token("PRINT", "PRINT", TokenPriority.HIGH)\
        .add_token("\\(", "LPAREN", TokenPriority.HIGH)\
        .add_token("\\)", "RPAREN", TokenPriority.HIGH)\
        .add_token("\\+", "ADDITION", TokenPriority.HIGH)\
        .add_token("\\*", "MULTIPLICATION", TokenPriority.HIGH)\
        .add_token("/", "DIVISION", TokenPriority.HIGH)\
        .add_token("-", "SUBTRACTION", TokenPriority.HIGH)\
        .add_token("=", "ASSIGNMENT", TokenPriority.HIGH)\
        .with_input(input)\
        .generate_scanner()

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

    # stmt = result.statements[4][0]
    # assert isinstance(stmt, PrintStatement)
    # assert stmt == PrintStatement(StringLiteral("SUM OF A AND B IS"))

    stmt = result.statements[4][0]
    assert isinstance(stmt, PrintStatement)
    assert stmt == PrintStatement(
        BinaryExpression(
            left=VariableReference("A"),
            operator="ADDITION",
            right=VariableReference("B"),
        )
    )
