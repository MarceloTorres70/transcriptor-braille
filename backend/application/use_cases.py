"""
Casos de Uso del Transcriptor Braille.
Capa: Application

REGLA CRÍTICA: Solo se importa el Puerto (BrailleDictionaryPort).
NUNCA se importa SpanishBrailleDictionary ni ninguna clase de infrastructure.
La implementación concreta llega por inyección de dependencias.
"""

from typing import Optional

from backend.domain.braille_dictionary_port import BrailleDictionaryPort
from backend.domain.braille_symbol import BrailleSymbol, SymbolType
from backend.application.dtos import (
    TranslateTextRequestDTO,
    TranslateTextResponseDTO,
    TranslationMetadataDTO,
)

_CAPITAL_PREFIX_UNICODE = "\u2828"  # ⠨ puntos (4, 6)
_NUMERIC_PREFIX_UNICODE = "\u283c"  # ⠼ puntos (3, 4, 5, 6)
_BRAILLE_SPACE = "\u2800"


class TranslateTextToBrailleUseCase:
    """
    Caso de Uso: Traduce texto español ↔ Braille según request.direction.

    Direcciones:
      - "es-br" (default): español → Braille Unicode
      - "br-es": Braille Unicode → español
    """

    def __init__(self, dictionary: BrailleDictionaryPort) -> None:
        # Depende SOLO del puerto; agnóstico a la implementación concreta
        self._dict = dictionary

    def execute(self, request: TranslateTextRequestDTO) -> TranslateTextResponseDTO:
        is_valid, error_msg = request.is_valid()
        if not is_valid:
            return TranslateTextResponseDTO(
                success=False,
                original_text=request.text,
                braille_output="",
                error=error_msg,
            )

        if request.direction == "br-es":
            output, unsupported = self._translate_braille_to_text(request.text)
        else:
            symbols, unsupported = self._translate(request.text)
            output = "".join(s.to_unicode() for s in symbols)

        metadata = None
        if request.include_metadata:
            metadata = TranslationMetadataDTO(
                total_chars=len(request.text),
                translated_chars=len(request.text) - len(unsupported),
                unsupported_chars=list(set(unsupported)),
            )

        return TranslateTextResponseDTO(
            success=bool(output),
            original_text=request.text,
            braille_output=output,
            metadata=metadata,
        )

    # ──────────────────────────────────────────────────────
    # Español → Braille
    # ──────────────────────────────────────────────────────

    def _translate(
        self, text: str
    ) -> tuple[list[BrailleSymbol], list[str]]:
        result: list[BrailleSymbol] = []
        unsupported: list[str] = []
        in_number_block = False

        i = 0
        while i < len(text):
            char = text[i]
            is_digit = char.isdigit()

            # Regla de palabra en mayúsculas: secuencias continuas (len >= 2)
            # se traducen con prefijo doble al inicio y letras sin prefijo individual.
            if char.isalpha() and char.isupper():
                j = i
                while j < len(text) and text[j].isalpha() and text[j].isupper():
                    j += 1

                uppercase_run = text[i:j]
                if len(uppercase_run) >= 2:
                    in_number_block = False
                    capital_prefix = self._get_capital_prefix()
                    if capital_prefix:
                        result.extend([capital_prefix, capital_prefix])

                    for upper_char in uppercase_run:
                        sequence = self._dict.get_symbol_sequence_for_text(upper_char.lower())
                        if sequence:
                            result.extend(sequence)
                        else:
                            unsupported.append(upper_char)

                    i = j
                    continue

            # Gestión del bloque numérico
            if is_digit and not in_number_block:
                numeric_prefix = self._get_numeric_prefix()
                if numeric_prefix:
                    result.append(numeric_prefix)
                in_number_block = True
            elif not is_digit:
                in_number_block = False

            sequence = self._dict.get_symbol_sequence_for_text(char)

            if sequence:
                result.extend(sequence)
            else:
                unsupported.append(char)

            i += 1

        return result, unsupported

    # ──────────────────────────────────────────────────────
    # Braille → Español
    # ──────────────────────────────────────────────────────

    def _translate_braille_to_text(
        self, braille: str
    ) -> tuple[str, list[str]]:
        result: list[str] = []
        unsupported: list[str] = []
        capitalized_next = False
        all_caps_word = False
        number_mode = False

        i = 0
        while i < len(braille):
            char = braille[i]

            if char == _CAPITAL_PREFIX_UNICODE:
                if i + 1 < len(braille) and braille[i + 1] == _CAPITAL_PREFIX_UNICODE:
                    all_caps_word = True
                    i += 2
                    continue
                capitalized_next = True
                i += 1
                continue

            if char == _NUMERIC_PREFIX_UNICODE:
                number_mode = True
                i += 1
                continue

            if char in (" ", _BRAILLE_SPACE, "\n"):
                result.append(" " if char != "\n" else "\n")
                all_caps_word = False
                number_mode = False
                i += 1
                continue

            symbol_type = SymbolType.DIGIT if number_mode else None
            symbol = self._lookup_by_unicode(char, symbol_type)

            if symbol is not None:
                text = symbol.text
                if all_caps_word or capitalized_next:
                    text = text.upper()
                    capitalized_next = False
                result.append(text)
            else:
                unsupported.append(char)

            i += 1

        return "".join(result), unsupported

    def _lookup_by_unicode(
        self, unicode_char: str, symbol_type: Optional[SymbolType]
    ) -> Optional[BrailleSymbol]:
        if hasattr(self._dict, "get_symbol_by_unicode"):
            return self._dict.get_symbol_by_unicode(  # type: ignore[attr-defined]
                unicode_char, symbol_type
            )
        return None

    def _get_numeric_prefix(self) -> Optional[BrailleSymbol]:
        if hasattr(self._dict, "numeric_prefix"):
            return self._dict.numeric_prefix  # type: ignore[attr-defined]
        return self._dict.get_symbol_for_text("#")

    def _get_capital_prefix(self) -> Optional[BrailleSymbol]:
        if hasattr(self._dict, "capital_prefix"):
            return self._dict.capital_prefix  # type: ignore[attr-defined]
        return self._dict.get_symbol_for_text("^")


class GetSupportedCharsUseCase:
    """Retorna los grupos de caracteres soportados (para validación en Frontend)."""

    def __init__(self, dictionary: BrailleDictionaryPort) -> None:
        self._dict = dictionary

    def execute(self) -> dict:
        groups = {
            "letras":            list("abcdefghijklmnñopqrstuvwxyz"),
            "vocales_tildadas":  list("áéíóúü"),
            "numeros":           list("0123456789"),
            "signos_matematicos": list("+-*/="),
            "parentesis":        list("()"),
            "puntuacion":        list(".,;:!¡?¿'\" "),
        }
        return {
            group: [c for c in chars if self._dict.contains(c)]
            for group, chars in groups.items()
        }
