from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser
from src.regex.regex_tree import RegexBinaryNode, RegexUnaryNode
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


def test_parse_or_node():
    input = "ab|cd|ef"
    lexer = RegexLexer(input)

    result = RegexParser(lexer).parse()

    assert isinstance(result, RegexBinaryNode)
    assert result.symbol is not None
    assert result.symbol.type == SymbolType.OR
    assert result.symbol.value == SymbolType.OR.value

    assert isinstance(result.left, RegexUnaryNode)
    assert result.left.symbol is not None
    assert result.left.symbol.type == SymbolType.LETTER
    assert result.left.symbol.value == "a"

    assert isinstance(result.left.child, RegexUnaryNode)
    assert result.left.child.symbol is not None
    assert result.left.child.symbol.type == SymbolType.LETTER
    assert result.left.child.symbol.value == "b"

    assert isinstance(result.right, RegexBinaryNode)
    assert result.right.symbol is not None
    assert result.right.symbol.type == SymbolType.OR
    assert result.right.symbol.value == SymbolType.OR.value

    assert isinstance(result.right.left, RegexUnaryNode)
    assert result.right.left.symbol is not None
    assert result.right.left.symbol.type == SymbolType.LETTER
    assert result.right.left.symbol.value == "c"
    assert result.right.left.child is not None

    assert isinstance(result.right.left.child, RegexUnaryNode)
    assert result.right.left.child.symbol is not None
    assert result.right.left.child.symbol.type == SymbolType.LETTER
    assert result.right.left.child.symbol.value == "d"
    assert result.right.left.child.child is None

    assert isinstance(result.right.right, RegexUnaryNode)
    assert result.right.right.symbol is not None
    assert result.right.right.symbol.type == SymbolType.LETTER
    assert result.right.right.symbol.value == "e"
    assert result.right.right.child is not None

    assert isinstance(result.right.right.child, RegexUnaryNode)
    assert result.right.right.child.symbol is not None
    assert result.right.right.child.symbol.type == SymbolType.LETTER
    assert result.right.right.child.symbol.value == "f"
    assert result.right.right.child.child is None
