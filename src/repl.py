from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


if __name__ == "__main__":
    print("> ", end="")
    regex = input()

    while regex != "":
        automata = RegexParser(RegexLexer(regex)).parse()

        automata.print()

        print("> ", end="")
        regex = input()
