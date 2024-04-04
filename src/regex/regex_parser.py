from src.regex.regex_lexer import RegexLexer
from src.regex.regex_tree import RegexBinaryNode, RegexNode, RegexUnaryNode
from src.utils.symbol import Symbol, SymbolType


# Uma regex pode ser composta de alguns módulos:
# - expressões -> por exemplo, regex [A-Z][a-z] é composta pelas expressões [A-Z] e [a-z]
# - termos -> são vistos como a concatenação de fatores: Por exemplo, o termo "ab" é a concatenação do fator a com o fator b
# - fatores -> são atomicos sucedidos de um quantificador (* ou +). Por ex.: a* ou (ab)+
# - atomicos -> pode ser um único simbolo, ou uma subexpressão dentro de parenteses
class RegexParser:
    def __init__(self, regex_lexer: RegexLexer):
        self.regex_lexer = regex_lexer
        self.current_symbol = self.regex_lexer.next_symbol()
        self.last_inserted: RegexNode | None = None
        self.root: RegexNode | None = None

    def parse(self):
        while self._is_content_symbol(self.current_symbol):
            node = RegexUnaryNode(self.current_symbol)

            if self.root is None or self.last_inserted is None:
                self.root = node
            else:
                self.last_inserted.add_child(node)
            self.last_inserted = node

            self._consume()

        if self.current_symbol.type == SymbolType.OR:
            or_node = RegexBinaryNode(self.current_symbol)

            or_node.left = self.root
            or_node.right = RegexParser(self.regex_lexer).parse()
            self.root = or_node

        return self.root

    def _is_content_symbol(self, symbol: Symbol):
        return symbol.type in [
            SymbolType.UPPER,
            SymbolType.LOWER,
            SymbolType.TEXT,
            SymbolType.NUMBER,
            SymbolType.NUMERIC_DIGIT,
            SymbolType.LETTER,
        ]

    def _consume(self):
        self.current_symbol = self.regex_lexer.next_symbol()
