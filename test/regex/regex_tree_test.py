from src.regex.regex_tree import RegexUnaryNode
from src.utils.symbol import Symbol, SymbolType


def test_add_child_unary_node():
    parent = RegexUnaryNode(Symbol(SymbolType.UPPER, SymbolType.UPPER.value))
    child = RegexUnaryNode(Symbol(SymbolType.LOWER, SymbolType.LOWER.value))

    parent.add_child(child)

    assert parent.child == child
    assert child.parent == parent
    assert parent.child is not None
    assert parent.child.symbol is not None
    assert parent.child.symbol.type == SymbolType.LOWER
    assert child.parent is not None
    assert child.parent.symbol is not None
    assert child.parent.symbol.type == SymbolType.UPPER
