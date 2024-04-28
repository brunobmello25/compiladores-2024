from dataclasses import dataclass
from typing import List


@dataclass
class ASTNode:
    """ Base class for all AST nodes. """

    def __str__(self, level=0):
        return "  " * level + self.__class__.__name__


@dataclass
class Expression(ASTNode):
    """ Base class for expressions. """

    def __str__(self, level=0):
        return "  " * level + self.__class__.__name__


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression

    def __str__(self, level=0):
        return ("  " * level + "BinaryExpression:\n" +
                self.left.__str__(level + 1) + "\n" +
                "  " * (level + 1) + "Operator: " + self.operator + "\n" +
                self.right.__str__(level + 1))


@dataclass
class NumberLiteral(Expression):
    # TODO: use an int here
    value: str

    def __str__(self, level=0):
        return "  " * level + f"NumberLiteral: {self.value}"


@dataclass
class StringLiteral(Expression):
    value: str

    def __str__(self, level=0):
        return "  " * level + f"StringLiteral: {self.value}"


@dataclass
class VariableReference(Expression):
    name: str

    def __str__(self, level=0):
        return "  " * level + f"VariableReference: {self.name}"


@dataclass
class Assignment(ASTNode):
    variable: str
    value: Expression

    def __str__(self, level=0):
        return ("  " * level + "Assignment:\n" +
                "  " * (level + 1) + f"Variable: {self.variable}\n" +
                self.value.__str__(level + 1))


@dataclass
class PrintStatement(ASTNode):
    value: Expression

    def __str__(self, level=0):
        return "  " * level + "PrintStatement:\n" + self.value.__str__(level + 1)


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

    def __str__(self, level=0):
        return "\n\n".join(stmt.__str__(level) for stmt in self.statements)
