from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser
from src.regex.regex_tree import RegexUnaryNode
from src.utils.symbol import SymbolType


def test_parse_concatenated_tokens():
    input = "abc"
    lexer = RegexLexer(input)

    result = RegexParser(lexer).parse()

    assert isinstance(result, RegexUnaryNode)
    assert result.symbol is not None
    assert result.symbol.type == SymbolType.LETTER
    assert result.symbol.value == "a"

    assert isinstance(result.child, RegexUnaryNode)
    assert result.child.symbol is not None
    assert result.child.symbol.type == SymbolType.LETTER
    assert result.child.symbol.value == "b"

    assert isinstance(result.child.child, RegexUnaryNode)
    assert result.child.child.symbol is not None
    assert result.child.child.symbol.type == SymbolType.LETTER
    assert result.child.child.symbol.value == "c"

    assert result.child.child.child is None

    assert result.child.child.parent is not None
    assert result.child.parent is not None
    assert result.parent is None
