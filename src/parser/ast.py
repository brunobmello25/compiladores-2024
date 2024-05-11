from dataclasses import dataclass
from typing import List, Tuple


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
class IfStatement(ASTNode):
    condition: Expression
    then_statement: ASTNode
    else_statement: ASTNode | None = None

    def __str__(self, level=0):
        then_str = self.then_statement.__str__(level + 1)
        if self.else_statement:
            else_str = self.else_statement.__str__(level + 1)
            return ("  " * level + "IfStatement:\n" +
                    "  " * (level + 1) + "Condition:\n" + self.condition.__str__(level + 2) + "\n" +
                    "  " * (level + 1) + "Then:\n" + then_str + "\n" +
                    "  " * (level + 1) + "Else:\n" + else_str)
        else:
            return ("  " * level + "IfStatement:\n" +
                    "  " * (level + 1) + "Condition:\n" + self.condition.__str__(level + 2) + "\n" +
                    "  " * (level + 1) + "Then:\n" + then_str)


@dataclass
class Program(ASTNode):
    statements: List[Tuple[ASTNode, int]]

    def __str__(self, level=0):
        def print_stmt(stmt: ASTNode, line: int):
            output = ""
            output += "  " * level + f"Line: {line}\n"
            output += stmt.__str__(level)
            return output

        return "\n\n".join(print_stmt(stmt[0], stmt[1]) for stmt in self.statements)
