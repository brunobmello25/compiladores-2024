from src.parser.ast import Assignment, BinaryExpression, ForStatement, IfStatement, NumberLiteral, PrintStatement, StringLiteral, VariableReference
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
    input = '''
            10 LET A = 5
            20 LET B = 10
            30 LET C = A + B
            40 PRINT C
            50 PRINT "SUM OF A AND B IS"
            60 PRINT A + B
            70 IF A > B THEN IF C < D THEN PRINT "UM" ELSE PRINT "DOIS" ELSE PRINT "TRES"
            80 IF A THEN IF B THEN PRINT "X"
            90 IF A THEN IF B THEN PRINT "X" ELSE PRINT "Y"
            100 FOR I = 1 TO 10
            110 PRINT I
            120 NEXT I
            130 FOR I = 1 TO 9 STEP 2
            140 PRINT A + B
            150 NEXT I
            160 FOR I = 1 TO 10
            170 PRINT A + B
            180 A = A + 1
            190 NEXT I'''

    scanner = ScannerGenerator()\
        .add_token("[0-9]*", "NUMBER", TokenPriority.HIGH)\
        .add_token("[A-z]([A-z]|[0-9])*", "IDENTIFIER", TokenPriority.LOW)\
        .add_token('"([A-z]|[0-9]| )*"', "STRING", TokenPriority.HIGH)\
        .add_token("LET", "LET", TokenPriority.HIGH)\
        .add_token("PRINT", "PRINT", TokenPriority.HIGH)\
        .add_token("IF", "IF", TokenPriority.HIGH)\
        .add_token("THEN", "THEN", TokenPriority.HIGH)\
        .add_token("ELSE", "ELSE", TokenPriority.HIGH)\
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
        .add_token("\\>=", "GTE", TokenPriority.HIGH)\
        .add_token("\\<=", "LTE", TokenPriority.HIGH)\
        .add_token("FOR", "FOR", TokenPriority.HIGH)\
        .add_token("NEXT", "NEXT", TokenPriority.HIGH)\
        .add_token("TO", "TO", TokenPriority.HIGH)\
        .add_token("STEP", "STEP", TokenPriority.HIGH)\
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

    stmt = result.statements[4][0]
    assert isinstance(stmt, PrintStatement)
    assert stmt == PrintStatement(StringLiteral('"SUM OF A AND B IS"'))

    stmt = result.statements[5][0]
    assert isinstance(stmt, PrintStatement)
    assert stmt == PrintStatement(
        BinaryExpression(
            left=VariableReference("A"),
            operator="ADDITION",
            right=VariableReference("B"),
        )
    )

    stmt = result.statements[6][0]
    assert isinstance(stmt, IfStatement)
    assert stmt == IfStatement(
        condition=BinaryExpression(
            left=VariableReference("A"),
            operator="GT",
            right=VariableReference("B"),
        ),
        then_statement=IfStatement(
            condition=BinaryExpression(
                left=VariableReference("C"),
                right=VariableReference("D"),
                operator="LT",
            ),
            then_statement=PrintStatement(StringLiteral('"UM"')),
            else_statement=PrintStatement(StringLiteral('"DOIS"')),
        ),
        else_statement=PrintStatement(StringLiteral('"TRES"')),
    )

    stmt = result.statements[7][0]
    assert isinstance(stmt, IfStatement)
    assert stmt == IfStatement(
        condition=VariableReference("A"),
        then_statement=IfStatement(
            condition=VariableReference("B"),
            then_statement=PrintStatement(StringLiteral('"X"')),
            else_statement=None
        ),
        else_statement=None
    )

    stmt = result.statements[8][0]
    assert isinstance(stmt, IfStatement)
    assert stmt == IfStatement(
        condition=VariableReference("A"),
        then_statement=IfStatement(
            condition=VariableReference("B"),
            then_statement=PrintStatement(StringLiteral('"X"')),
            else_statement=PrintStatement(StringLiteral('"Y"'))
        ),
        else_statement=None
    )

    stmt = result.statements[9][0]
    assert isinstance(stmt, ForStatement)
    assert stmt == ForStatement(
        variable="I",
        start=NumberLiteral("1"),
        end=NumberLiteral("10"),
        step=None,
        body=[
            (PrintStatement(VariableReference("I")), '110'),
        ]

    )

    stmt = result.statements[10][0]
    assert isinstance(stmt, ForStatement)
    assert stmt == ForStatement(
        variable="I",
        start=NumberLiteral("1"),
        end=NumberLiteral("9"),
        step=NumberLiteral("2"),
        body=[
            (PrintStatement(BinaryExpression(
                left=VariableReference("A"),
                operator="ADDITION",
                right=VariableReference("B"),
            )), '140'),
        ]
    )

    stmt = result.statements[11][0]
    assert isinstance(stmt, ForStatement)
    assert stmt == ForStatement(
        variable="I",
        start=NumberLiteral("1"),
        end=NumberLiteral("10"),
        step=None,
        body=[
            (PrintStatement(BinaryExpression(
                left=VariableReference("A"),
                operator="ADDITION",
                right=VariableReference("B"),
            )), '170'),
            (Assignment("A", BinaryExpression(
                left=VariableReference("A"),
                operator="ADDITION",
                right=NumberLiteral("1"),
            )), '180'),
        ]
    )
