from enum import Enum


class SymbolType(Enum):
    LETTER = "letter"
    ACCENTED_VOWEL = "accented_vowel"
    SPECIAL_LETTER = "special_letter"
    DIGIT = "digit"
    MATH_OPERATOR = "math_operator"
    PUNCTUATION = "punctuation"
    PREFIX = "prefix"
    SPACE = "space"


class BrailleSymbol:
    def __init__(self, text: str, cell: "BrailleCell", symbol_type: SymbolType):
        pass
