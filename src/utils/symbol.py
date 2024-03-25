from enum import Enum


class Symbol(Enum):
    MAIUSCULA = "[A-Z]"
    MINUSCULA = "[a-z]"
    TEXTO = "[A-z]"
    NUMERICO = "[0-9]"
    ESTRELA = "*"
    MAIS = "+"
    OU = "|"
    ABRE_PARENTESES = "("
    FECHA_PARENTESES = ")"
