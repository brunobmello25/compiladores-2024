from src.regex.regex_lexer import RegexLexer
from src.utils.symbol import Symbol


def test_next_symbol():
    input = "([A-z]|[A-Z])[0-9]*[a-z]+"
    expected_symbols = [
        Symbol.OPEN_PARENTHESIS,
        Symbol.TEXT,
        Symbol.OR,
        Symbol.UPPER,
        Symbol.CLOSE_PARENTHESIS,
        Symbol.NUMBER,
        Symbol.STAR,
        Symbol.LOWER,
        Symbol.PLUS,
        Symbol.EOF,
        Symbol.EOF,
        Symbol.EOF,
    ]
    lexer = RegexLexer(input)

    for expected_symbol in expected_symbols:
        symbol = lexer.next_symbol()
        assert symbol == expected_symbol


def test_regex_shortcut():
    tests = [
        {
            "input": "[A-Z]",
            "expected": Symbol.UPPER
        },
        {
            "input": "[a-z]",
            "expected": Symbol.LOWER
        },
        {
            "input": "[A-z]",
            "expected": Symbol.TEXT
        },
        {
            "input": "[0-9]",
            "expected": Symbol.NUMBER
        }
    ]

    for test in tests:
        lexer = RegexLexer(test["input"])
        symbol = lexer._handle_regex_shortcut()
        assert symbol == test["expected"]
