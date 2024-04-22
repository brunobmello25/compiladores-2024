

# TODO: Implement test_scanner_generator
# def test_scanner_generator():
#     scanner = ScannerGenerator()\
#         .add_token("int", "int", TokenPriority.HIGH)\
#         .add_token("[A-z]([a-z]|[A-Z]|[0-9])*", "identifier", TokenPriority.LOW)\
#         .add_token("=", "assign", TokenPriority.LOW)\
#         .add_token(";", "semicolon", TokenPriority.LOW)\
#         .add_token("[0-9]*", "intnumber", TokenPriority.LOW)\
#         .generate_scanner()
#
#     assert scanner.check_final_state("int")[0]
#     assert scanner.check_final_state("int")[1].token_type == "int"
#     assert scanner.check_final_state(
#         "int")[1].token_priority == TokenPriority.HIGH
#
#     assert scanner.check_final_state("somevariable")[0]
#     assert scanner.check_final_state("somevariable")[
#         1].token_type == "identifier"
#     assert scanner.check_final_state("somevariable")[
#         1].token_priority == TokenPriority.LOW
