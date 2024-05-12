import argparse
import os
import sys
from typing import List, Tuple

from src.parser.parser import Parser
from src.scanner.scanner import Scanner
from src.scanner.scanner_generator import ScannerGenerator
from src.scanner.token_priority import TokenPriority


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Scanner e parser da linguagem BASIC'
    )

    parser.add_argument('--input-file', required=True,
                        help='Caminho para o arquivo de código para a entrada')
    parser.add_argument('--token-file', required=True,
                        help='Caminho para o arquivo contendo as especificações de tokens')

    args = parser.parse_args()

    return args


def check_if_file_exists(file_path: str):
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado")
        sys.exit(1)


def parse_tokens_file(file_path) -> List[Tuple[str, str, TokenPriority]]:
    with open(file_path, 'r') as file:
        content = file.read().strip()

    blocks = content.split('\n\n')

    tokens = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) == 3:
            priority = TokenPriority.from_string(lines[2])
            regex_dict = (
                lines[0],
                lines[1],
                priority
            )
            tokens.append(regex_dict)
        else:
            print(f"Warning: Skipping malformed block:\n{block}")

    return tokens


def parse_input_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read().strip()


def make_scanner(tokens: List[Tuple[str, str, TokenPriority]], input: str) -> Scanner:
    scanner_generator = ScannerGenerator()
    for token in tokens:
        scanner_generator = scanner_generator.add_token(
            token[0],  token[1], token[2])

    scanner_generator = scanner_generator.with_input(input)

    scanner = scanner_generator.generate_scanner()

    return scanner


def main():
    args = parse_arguments()

    check_if_file_exists(args.input_file)
    check_if_file_exists(args.token_file)

    tokens = parse_tokens_file(args.token_file)
    input = parse_input_file(args.input_file)

    scanner = make_scanner(tokens, input)
    parser = Parser(scanner)
    program = parser.parse()

    if parser.has_errors():
        print("Erros léxicos ou sintáticos encontrados:")
        for error in parser.lexical_errors:
            print(f"Erro léxico: {error.message}")
        for error in parser.syntatical_errors:
            print(f"Erro sintático: {error}")
        sys.exit(1)

    print(program)


if __name__ == "__main__":
    main()
