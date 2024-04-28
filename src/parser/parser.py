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

    def parse(self):
        """The entry point for parsing."""
        program = []
        while self.current_token.type != 'EOF':
            if self.current_token.type == 'NUMBER':  # Handle line numbers
                self.advance()
                statement = self.parse_statement()
                program.append(statement)
        return program

    def parse_statement(self):
        """Parse individual statements based on the first token after the line number."""
        if self.current_token.type == 'LET':
            return self.parse_assignment()
        elif self.current_token.type == 'PRINT':
            return self.parse_print_statement()
        else:
            raise Exception("Syntax Error: Unrecognized statement")

    def parse_print_statement(self):
        """Parse a PRINT statement."""
        self.expect('PRINT')  # Ensure the current token is PRINT and advance
        expr = self.parse_expression()
        return {'type': 'print', 'value': expr}

    def parse_assignment(self):
        """Parse a variable assignment statement."""
        self.expect('LET')
        if self.current_token.type != 'IDENTIFIER':
            raise Exception("Syntax Error: Expected identifier")
        var_name = self.current_token.value
        self.advance()
        self.expect('EQUALS')
        expr = self.parse_expression()
        return {'type': 'assignment', 'variable': var_name, 'value': expr}

    def parse_expression(self):
        """Parse an expression, including handling of basic arithmetic."""
        left = self.parse_term()
        while self.current_token.type in ['PLUS', 'MINUS']:
            op = self.current_token.type
            self.advance()
            right = self.parse_term()
            left = {'type': 'binary_expr', 'operator': op,
                    'left': left, 'right': right}
        return left

    def parse_term(self):
        """Parse a term, which is currently just a number or a variable."""
        if self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.advance()
            return {'type': 'number', 'value': value}
        elif self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.advance()
            return {'type': 'variable', 'name': name}
        else:
            raise Exception("Syntax Error: Expected a term")
