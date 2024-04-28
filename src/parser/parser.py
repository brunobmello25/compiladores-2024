from src.parser.ast import ASTNode, Assignment, BinaryExpression, Expression, NumberLiteral, PrintStatement, Program, StringLiteral, VariableReference
from src.scanner.scanner import Scanner
from src.scanner.token import Token


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.advance()  # Initialize the first token

    def advance(self):
        """Move to the next token."""
        self.current_token: Token = self.scanner.next_token()

    def expect(self, token_type):
        """Ensure the current token matches the expected type and advance."""
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Syntax Error: Expected {
                            token_type}, found {self.current_token.type}")

    def parse(self) -> Program:
        """The entry point for parsing."""
        statements = []
        while self.current_token.type != 'EOF':
            if self.current_token.type == 'NUMBER':  # Handle line numbers
                line_number = int(self.current_token.value)
                self.advance()
                statement = self.parse_statement()
                statements.append(tuple([statement, line_number]))
        return Program(statements=statements)

    def parse_statement(self) -> ASTNode:
        """Parse individual statements based on the first token after the line number."""
        if self.current_token.type == 'LET':
            return self.parse_assignment()
        elif self.current_token.type == 'PRINT':
            return self.parse_print_statement()
        else:
            raise Exception("Syntax Error: Unrecognized statement")

    def parse_print_statement(self) -> PrintStatement:
        """Parse a PRINT statement."""
        self.expect('PRINT')  # Ensure the current token is PRINT and advance
        expr = self.parse_expression()
        return PrintStatement(value=expr)

    def parse_assignment(self) -> Assignment:
        """Parse a variable assignment statement."""
        self.expect('LET')
        if self.current_token.type != 'IDENTIFIER':
            raise Exception("Syntax Error: Expected identifier")
        var_name = self.current_token.value
        self.advance()
        self.expect('EQUALS')
        expr = self.parse_expression()
        return Assignment(variable=var_name, value=expr)

    def parse_expression(self) -> Expression:
        """Parse an expression, including handling of basic arithmetic."""
        left = self.parse_term()
        while self.current_token.type in ['PLUS', 'MINUS']:
            op = self.current_token.type
            self.advance()
            right = self.parse_term()
            left = BinaryExpression(left=left, right=right, operator=op)
        return left

    def parse_term(self) -> Expression:
        """Parse a term, which is currently just a number or a variable."""
        if self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.advance()
            return NumberLiteral(value=value)
        elif self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.advance()
            return VariableReference(name=name)
        elif self.current_token.type == 'STRING':
            value = self.current_token.value
            self.advance()
            return StringLiteral(value=value)
        else:
            raise Exception("Syntax Error: Expected a term")
