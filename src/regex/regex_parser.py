from src.regex.regex_lexer import RegexLexer
from src.regex.regex_tree import Node


# Uma regex pode ser composta de alguns módulos:
# - expressões -> por exemplo, regex [A-Z][a-z] é composta pelas expressões [A-Z] e [a-z]
# - termos -> são vistos como a concatenação de fatores: Por exemplo, o termo "ab" é a concatenação do fator a com o fator b
# - fatores -> são atomicos sucedidos de um quantificador (* ou +). Por ex.: a* ou (ab)+
# - atomicos -> pode ser um único simbolo, ou uma subexpressão dentro de parenteses
class RegexParser:
    def __init__(self, regex_lexer: RegexLexer):
        self.regex_lexer = regex_lexer
        self.current_symbol = self.regex_lexer.next_symbol()

    def parse(self) -> Node:
        return self._parse_expression()

    def _parse_expression(self) -> Node:
        return Node()
