from src.regex.regex_lexer import RegexLexer
from src.utils.symbol import Symbol, SymbolType


def test_next_symbol():
    input = "/([A-z]|[A-Z])[0-9]?*[a-z]+?[xyz]aBCd12=!;_\\(\\)\\[\\]\\*\\+\"  "
    expected_symbols = [
        Symbol(SymbolType.SLASH, "/"),
        Symbol(SymbolType.OPEN_PARENTHESIS, SymbolType.OPEN_PARENTHESIS.value),
        Symbol(SymbolType.TEXT, SymbolType.TEXT.value),
        Symbol(SymbolType.OR, SymbolType.OR.value),
        Symbol(SymbolType.UPPER, SymbolType.UPPER.value),
        Symbol(
            SymbolType.CLOSE_PARENTHESIS, SymbolType.CLOSE_PARENTHESIS.value
        ),
        Symbol(SymbolType.NUMBER, SymbolType.NUMBER.value),
        Symbol(SymbolType.OPTIONAL, SymbolType.OPTIONAL.value),
        Symbol(SymbolType.STAR, SymbolType.STAR.value),
        Symbol(SymbolType.LOWER, SymbolType.LOWER.value),
        Symbol(SymbolType.PLUS, SymbolType.PLUS.value),
        Symbol(SymbolType.OPTIONAL, SymbolType.OPTIONAL.value),
        Symbol(SymbolType.ILLEGAL, "[xyz]"),
        Symbol(SymbolType.LETTER, "a"),
        Symbol(SymbolType.LETTER, "B"),
        Symbol(SymbolType.LETTER, "C"),
        Symbol(SymbolType.LETTER, "d"),
        Symbol(SymbolType.NUMERIC_DIGIT, "1"),
        Symbol(SymbolType.NUMERIC_DIGIT, "2"),
        Symbol(SymbolType.EQUAL, "="),
        Symbol(SymbolType.EXCLAMATION, "!"),
        Symbol(SymbolType.SEMICOLON, ";"),
        Symbol(SymbolType.UNDERSCORE, "_"),
        Symbol(SymbolType.ESCAPED, "("),
        Symbol(SymbolType.ESCAPED, ")"),
        Symbol(SymbolType.ESCAPED, "["),
        Symbol(SymbolType.ESCAPED, "]"),
        Symbol(SymbolType.ESCAPED, "*"),
        Symbol(SymbolType.ESCAPED, "+"),
        Symbol(SymbolType.QUOTE, '"'),
        Symbol(SymbolType.SPACE, ' '),
        Symbol(SymbolType.SPACE, ' '),
        Symbol(SymbolType.EOF, SymbolType.EOF.value),
        Symbol(SymbolType.EOF, SymbolType.EOF.value),
        Symbol(SymbolType.EOF, SymbolType.EOF.value),
    ]
    lexer = RegexLexer(input)

    for expected_symbol in expected_symbols:
        symbol = lexer.next_symbol()
        assert symbol.type == expected_symbol.type
        assert symbol.value == expected_symbol.value


def test_regex_shortcut():
    tests = [
        {
            "input": "[A-Z]",
            "expected": Symbol(SymbolType.UPPER, SymbolType.UPPER.value),
        },
        {
            "input": "[a-z]",
            "expected": Symbol(SymbolType.LOWER, SymbolType.LOWER.value),
        },
        {
            "input": "[A-z]",
            "expected": Symbol(SymbolType.TEXT, SymbolType.TEXT.value),
        },
        {
            "input": "[0-9]",
            "expected": Symbol(SymbolType.NUMBER, SymbolType.NUMBER.value),
        },
    ]

    for test in tests:
        lexer = RegexLexer(test["input"])
        symbol = lexer._handle_regex_shortcut()
        assert symbol.type == test["expected"].type
        assert symbol.value == test["expected"].value
