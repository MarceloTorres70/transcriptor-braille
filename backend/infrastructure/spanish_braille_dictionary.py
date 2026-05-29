"""
Implementación Concreta del Diccionario Braille Español.
Capa: Infrastructure

REGLA ARQUITECTÓNICA:
  - Esta clase implementa BrailleDictionaryPort (dominio).
  - Los Use Cases NUNCA importan esta clase directamente.
  - La inyección ocurre en la capa de adaptadores/factory.

Diccionario completo:
  - Alfabeto a-z + ñ
  - Vocales tildadas: á, é, í, ó, ú, ü
  - Números 0-9 con prefijo numérico (⠼)
  - Signos matemáticos: +, -, *, /, =
  - Paréntesis: (, )
  - Puntuación general
  - Prefijos especiales: numérico y mayúscula
"""

from typing import Optional

from backend.domain.braille_cell import BrailleCell
from backend.domain.braille_symbol import BrailleSymbol, SymbolType
from backend.domain.braille_dictionary_port import BrailleDictionaryPort


def _cell(*dots: int) -> BrailleCell:
    """Helper para construir BrailleCell de forma legible."""
    return BrailleCell(dots)


class SpanishBrailleDictionary(BrailleDictionaryPort):
    """
    Diccionario Braille completo para el español.
    Estándar: Braille español (ONCE).
    """

    # Prefijos especiales
    _NUMERIC_PREFIX = BrailleSymbol(
        text="#", cell=_cell(3, 4, 5, 6), symbol_type=SymbolType.PREFIX
    )
    _CAPITAL_PREFIX = BrailleSymbol(
        text="^", cell=_cell(4, 6), symbol_type=SymbolType.PREFIX
    )

    _TABLE: dict[str, BrailleSymbol] = {
        # Letras minúsculas
        "a": BrailleSymbol("a", _cell(1),             SymbolType.LETTER),
        "b": BrailleSymbol("b", _cell(1, 2),          SymbolType.LETTER),
        "c": BrailleSymbol("c", _cell(1, 4),          SymbolType.LETTER),
        "d": BrailleSymbol("d", _cell(1, 4, 5),       SymbolType.LETTER),
        "e": BrailleSymbol("e", _cell(1, 5),          SymbolType.LETTER),
        "f": BrailleSymbol("f", _cell(1, 2, 4),       SymbolType.LETTER),
        "g": BrailleSymbol("g", _cell(1, 2, 4, 5),    SymbolType.LETTER),
        "h": BrailleSymbol("h", _cell(1, 2, 5),       SymbolType.LETTER),
        "i": BrailleSymbol("i", _cell(2, 4),          SymbolType.LETTER),
        "j": BrailleSymbol("j", _cell(2, 4, 5),       SymbolType.LETTER),
        "k": BrailleSymbol("k", _cell(1, 3),          SymbolType.LETTER),
        "l": BrailleSymbol("l", _cell(1, 2, 3),       SymbolType.LETTER),
        "m": BrailleSymbol("m", _cell(1, 3, 4),       SymbolType.LETTER),
        "n": BrailleSymbol("n", _cell(1, 3, 4, 5),    SymbolType.LETTER),
        "ñ": BrailleSymbol("ñ", _cell(1, 2, 4, 5, 6), SymbolType.SPECIAL_LETTER),
        "o": BrailleSymbol("o", _cell(1, 3, 5),       SymbolType.LETTER),
        "p": BrailleSymbol("p", _cell(1, 2, 3, 4),    SymbolType.LETTER),
        "q": BrailleSymbol("q", _cell(1, 2, 3, 4, 5), SymbolType.LETTER),
        "r": BrailleSymbol("r", _cell(1, 2, 3, 5),    SymbolType.LETTER),
        "s": BrailleSymbol("s", _cell(2, 3, 4),       SymbolType.LETTER),
        "t": BrailleSymbol("t", _cell(2, 3, 4, 5),    SymbolType.LETTER),
        "u": BrailleSymbol("u", _cell(1, 3, 6),       SymbolType.LETTER),
        "v": BrailleSymbol("v", _cell(1, 2, 3, 6),    SymbolType.LETTER),
        "w": BrailleSymbol("w", _cell(2, 4, 5, 6),    SymbolType.LETTER),
        "x": BrailleSymbol("x", _cell(1, 3, 4, 6),    SymbolType.LETTER),
        "y": BrailleSymbol("y", _cell(1, 3, 4, 5, 6), SymbolType.LETTER),
        "z": BrailleSymbol("z", _cell(1, 3, 5, 6),    SymbolType.LETTER),
        # Vocales tildadas
        "\u00e1": BrailleSymbol("á", _cell(1, 2, 3, 5, 6),  SymbolType.ACCENTED_VOWEL),
        "\u00e9": BrailleSymbol("é", _cell(2, 3, 4, 6),      SymbolType.ACCENTED_VOWEL),
        "\u00ed": BrailleSymbol("í", _cell(3, 5),            SymbolType.ACCENTED_VOWEL),
        "\u00f3": BrailleSymbol("ó", _cell(3, 4, 6),         SymbolType.ACCENTED_VOWEL),
        "\u00fa": BrailleSymbol("ú", _cell(2, 3, 4, 5, 6),   SymbolType.ACCENTED_VOWEL),
        "\u00fc": BrailleSymbol("ü", _cell(1, 2, 5, 6),      SymbolType.ACCENTED_VOWEL),
        # Números
        "1": BrailleSymbol("1", _cell(1),          SymbolType.DIGIT),
        "2": BrailleSymbol("2", _cell(1, 2),       SymbolType.DIGIT),
        "3": BrailleSymbol("3", _cell(1, 4),       SymbolType.DIGIT),
        "4": BrailleSymbol("4", _cell(1, 4, 5),    SymbolType.DIGIT),
        "5": BrailleSymbol("5", _cell(1, 5),       SymbolType.DIGIT),
        "6": BrailleSymbol("6", _cell(1, 2, 4),    SymbolType.DIGIT),
        "7": BrailleSymbol("7", _cell(1, 2, 4, 5), SymbolType.DIGIT),
        "8": BrailleSymbol("8", _cell(1, 2, 5),    SymbolType.DIGIT),
        "9": BrailleSymbol("9", _cell(2, 4),       SymbolType.DIGIT),
        "0": BrailleSymbol("0", _cell(2, 4, 5),    SymbolType.DIGIT),
        # Signos matemáticos
        "+": BrailleSymbol("+", _cell(2, 3, 5),    SymbolType.MATH_OPERATOR),
        "-": BrailleSymbol("-", _cell(3, 6),       SymbolType.MATH_OPERATOR),
        "*": BrailleSymbol("*", _cell(1, 6),       SymbolType.MATH_OPERATOR),
        "/": BrailleSymbol("/", _cell(3, 4),       SymbolType.MATH_OPERATOR),
        "=": BrailleSymbol("=", _cell(2, 3, 5, 6), SymbolType.MATH_OPERATOR),
        # Paréntesis
        "(": BrailleSymbol("(", _cell(2, 3, 6),   SymbolType.PUNCTUATION),
        ")": BrailleSymbol(")", _cell(3, 5, 6),   SymbolType.PUNCTUATION),
        # Puntuación
        ".":  BrailleSymbol(".",  _cell(2, 5, 6),  SymbolType.PUNCTUATION),
        ",":  BrailleSymbol(",",  _cell(2),         SymbolType.PUNCTUATION),
        ";":  BrailleSymbol(";",  _cell(2, 3),      SymbolType.PUNCTUATION),
        ":":  BrailleSymbol(":",  _cell(2, 5),      SymbolType.PUNCTUATION),
        "!":  BrailleSymbol("!",  _cell(2, 3, 5),   SymbolType.PUNCTUATION),
        "\u00a1": BrailleSymbol("¡", _cell(2, 3, 5), SymbolType.PUNCTUATION),
        "?":  BrailleSymbol("?",  _cell(2, 6),      SymbolType.PUNCTUATION),
        "\u00bf": BrailleSymbol("¿", _cell(2, 6),   SymbolType.PUNCTUATION),
        "'":  BrailleSymbol("'",  _cell(3),         SymbolType.PUNCTUATION),
        '"':  BrailleSymbol('"',  _cell(2, 3, 6),   SymbolType.PUNCTUATION),
        " ":  BrailleSymbol(" ",  _cell(),           SymbolType.SPACE),
    }

    def get_symbol_for_text(self, token: str) -> Optional[BrailleSymbol]:
        return self._TABLE.get(token) or self._TABLE.get(token.lower())

    def get_symbol_sequence_for_text(self, token: str) -> Optional[list[BrailleSymbol]]:
        """
        Retorna la secuencia de símbolos para un token.
        Mayúscula → [prefijo_mayúscula, símbolo_letra]
        Resto     → [símbolo]
        Nota: el prefijo numérico se gestiona por bloque en el Use Case.
        """
        symbol = self.get_symbol_for_text(token)
        if symbol is None:
            return None
        if token.isupper() and token.isalpha():
            return [self._CAPITAL_PREFIX, symbol]
        return [symbol]

    def contains(self, token: str) -> bool:
        return token in self._TABLE or token.lower() in self._TABLE

    @property
    def numeric_prefix(self) -> BrailleSymbol:
        return self._NUMERIC_PREFIX

    @property
    def capital_prefix(self) -> BrailleSymbol:
        return self._CAPITAL_PREFIX