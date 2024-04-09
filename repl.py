from src.regex.regex_lexer import RegexLexer
from src.regex.regex_parser import RegexParser


if __name__ == "__main__":
    print("> ", end="")
    regex = input()

    automata = RegexParser(RegexLexer(regex)).parse()

    automata.print()