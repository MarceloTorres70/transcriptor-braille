from dataclasses import dataclass
from enum import Enum
from backend.domain.braille_cell import BrailleCell


class SymbolType(Enum):
    LETTER = "letter"
    ACCENTED_VOWEL = "accented_vowel"
    SPECIAL_LETTER = "special_letter"
    DIGIT = "digit"
    MATH_OPERATOR = "math_operator"
    PUNCTUATION = "punctuation"
    PREFIX = "prefix"
    SPACE = "space"


@dataclass(frozen=True)
class BrailleSymbol:
    """
    Símbolo Braille: mapeo entre texto original y su representación en Braille.
    
    Attributes:
        text: El carácter o secuencia original (ej: 'a', 'A', 'ñ')
        cell: La celda Braille que lo representa
        symbol_type: Clasificación del símbolo
    """
    text: str
    cell: BrailleCell
    symbol_type: SymbolType

    def __post_init__(self):
        if not self.text:
            raise ValueError("Symbol text cannot be empty")
        if not isinstance(self.cell, BrailleCell):
            raise TypeError("cell must be a BrailleCell instance")

    def to_unicode(self) -> str:
        """Retorna el carácter Unicode Braille."""
        return self.cell.unicode_character

    def __repr__(self) -> str:
        return f"BrailleSymbol('{self.text}' -> {self.cell})"
