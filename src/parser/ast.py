from dataclasses import dataclass
from typing import List, Tuple


spaces = "    "


@dataclass
class ASTNode:
    """ Base class for all AST nodes. """

    def __str__(self, level=0):
        return spaces * level + self.__class__.__name__


@dataclass
class Expression(ASTNode):
    """ Base class for expressions. """

    def __str__(self, level=0):
        return spaces * level + self.__class__.__name__


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression

    def __str__(self, level=0):
        return (spaces * level + "BinaryExpression:\n" +
                self.left.__str__(level + 1) + "\n" +
                spaces * (level + 1) + "Operator: " + self.operator + "\n" +
                self.right.__str__(level + 1))


@dataclass
class NumberLiteral(Expression):
    # TODO: use an int here
    value: str

    def __str__(self, level=0):
        return spaces * level + f"NumberLiteral: {self.value}"


@dataclass
class StringLiteral(Expression):
    value: str

    def __str__(self, level=0):
        return spaces * level + f"StringLiteral: {self.value}"


@dataclass
class VariableReference(Expression):
    name: str

    def __str__(self, level=0):
        return spaces * level + f"VariableReference: {self.name}"


@dataclass
class Assignment(ASTNode):
    variable: str
    value: Expression

    def __str__(self, level=0):
        return (spaces * level + "Assignment:\n" +
                spaces * (level + 1) + f"Variable: {self.variable}\n" +
                self.value.__str__(level + 1))


@dataclass
class PrintStatement(ASTNode):
    value: Expression

    def __str__(self, level=0):
        return spaces * level + "PrintStatement:\n" + self.value.__str__(level + 1)


@dataclass
class IfStatement(ASTNode):
    condition: Expression
    then_statement: ASTNode
    else_statement: ASTNode | None = None

    def __str__(self, level=0):
        then_str = self.then_statement.__str__(level + 2)
        if self.else_statement:
            else_str = self.else_statement.__str__(level + 2)
            return (spaces * level + "IfStatement:\n" +
                    spaces * (level + 1) + "Condition:\n" + self.condition.__str__(level + 2) + "\n" +
                    spaces * (level + 1) + "Then:\n" + then_str + "\n" +
                    spaces * (level + 1) + "Else:\n" + else_str)
        else:
            return (spaces * level + "IfStatement:\n" +
                    spaces * (level + 1) + "Condition:\n" + self.condition.__str__(level + 2) + "\n" +
                    spaces * (level + 1) + "Then:\n" + then_str)


@dataclass
class ForStatement(ASTNode):
    variable: str
    start: Expression
    end: Expression
    step: Expression | None
    # Including line numbers in body statements
    body: List[Tuple[ASTNode, str]]

    def __str__(self, level=0):
        # Default to step 1 if not provided
        step_str = f"Step: {self.step.__str__(
            level + 2)}" if self.step else "Step: 1"
        body_str = "\n".join(f"{stmt.__str__(
            level + 2)}" for stmt, _ in self.body)
        return (
            spaces * level + "ForStatement:\n" +
            spaces * (level + 1) + f"Variable: {self.variable}\n" +
            spaces * (level + 1) + "Start:\n" + self.start.__str__(level + 2) + "\n" +
            spaces * (level + 1) + "End:\n" + self.end.__str__(level + 2) + "\n" +
            spaces * (level + 1) + step_str + "\n" +
            spaces * (level + 1) + "Body:\n" + body_str
        )


@dataclass
class GoToStatement(ASTNode):
    label: str

    def __str__(self, level=0):
        return spaces * level + f"GoToStatement: {self.label}"


@dataclass
class Program(ASTNode):
    statements: List[Tuple[ASTNode, int]]

    def __str__(self, level=0):
        def print_stmt(stmt: ASTNode, line: int):
            output = ""
            output += spaces * level + f"Line: {line}\n"
            output += stmt.__str__(level)
            return output

        return "\n\n".join(print_stmt(stmt[0], stmt[1]) for stmt in self.statements)
