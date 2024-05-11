from src.parser.ast import ASTNode, Assignment, BinaryExpression, Expression, IfStatement, NumberLiteral, PrintStatement, Program, StringLiteral, VariableReference
from src.scanner.scanner import Scanner, Token


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.advance()

    def advance(self):
        result = self.scanner.next_token()
        if isinstance(result, Token):
            self.current_token: Token = result

    def expect(self, token_type) -> str:
        if self.current_token.type == token_type:
            value = self.current_token.value
            self.advance()
            return value
        else:
            raise Exception(f"Syntax Error: Expected {
                            token_type}, found {self.current_token.type}")

    def parse(self) -> Program:
        statements = []
        while self.current_token.type != 'EOF':
            if self.current_token.type == 'NUMBER':
                line_number = int(self.current_token.value)
                self.advance()
                statement = self.parse_statement()
                statements.append(tuple([statement, line_number]))
        return Program(statements=statements)

    def parse_statement(self) -> ASTNode:
        if self.current_token.type == 'LET':
            return self.parse_assignment()
        elif self.current_token.type == 'PRINT':
            return self.parse_print_statement()
        elif self.current_token.type == "IF":
            return self.parse_if_statement()
        else:
            raise Exception("Syntax Error: Unrecognized statement")

    def parse_if_statement(self) -> IfStatement:
        self.expect('IF')
        condition = self.parse_expression()
        self.expect('THEN')
        then_statement = self.parse_statement()

        else_statement = None
        if self.current_token.type == 'ELSE':
            self.advance()
            else_statement = self.parse_statement()

        return IfStatement(
            condition=condition,
            then_statement=then_statement,
            else_statement=else_statement
        )

    def parse_print_statement(self) -> PrintStatement:
        self.expect('PRINT')
        expr = self.parse_expression()
        return PrintStatement(value=expr)

    def parse_assignment(self) -> Assignment:
        self.expect('LET')
        var_name = self.expect("IDENTIFIER")
        self.expect('ASSIGNMENT')
        expr = self.parse_expression()
        return Assignment(variable=var_name, value=expr)

    def parse_expression(self) -> Expression:
        return self.parse_relational()

    def parse_relational(self) -> Expression:
        expr = self.parse_additive()
        while self.current_token.type in ["EQUAL", "NE", "LTE", "GTE", "GT", "LT"]:
            operator = self.current_token.type
            self.advance()
            right = self.parse_additive()
            expr = BinaryExpression(left=expr, operator=operator, right=right)
        return expr

    def parse_additive(self) -> Expression:
        expr = self.parse_multiplicative()
        while self.current_token.type in ['ADDITION', 'SUBTRACTION']:
            operator = self.current_token.type
            self.advance()
            right = self.parse_multiplicative()
            expr = BinaryExpression(left=expr, operator=operator, right=right)
        return expr

    def parse_multiplicative(self) -> Expression:
        expr = self.parse_factor()
        while self.current_token.type in ['MULTIPLICATION', 'DIVISION']:
            operator = self.current_token.type
            self.advance()
            right = self.parse_factor()
            expr = BinaryExpression(left=expr, operator=operator, right=right)
        return expr

    def parse_factor(self) -> Expression:
        if self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.advance()
            return NumberLiteral(value=value)
        elif self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.advance()
            return VariableReference(name=name)
        elif self.current_token.type == 'LPAREN':
            self.advance()  # skip '('
            expr = self.parse_expression()
            self.expect('RPAREN')  # match ')'
            return expr
        elif self.current_token.is_string():
            value = self.current_token.value
            self.advance()
            return StringLiteral(value=value)
        else:
            raise Exception("Syntax Error: Expected a factor")

    def parse_term(self) -> Expression:
        if self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.advance()
            return NumberLiteral(value=value)
        elif self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.advance()
            return VariableReference(name=name)
        elif self.current_token.is_string():
            value = self.current_token.value
            self.advance()
            return StringLiteral(value=value)
        else:
            raise Exception("Syntax Error: Expected a term")
