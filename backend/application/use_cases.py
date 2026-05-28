"""
Casos de Uso del Transcriptor Braille.
Capa: Application

REGLA CRÍTICA: Solo se importa el Puerto (BrailleDictionaryPort).
NUNCA se importa SpanishBrailleDictionary ni ninguna clase de infrastructure.
La implementación concreta llega por inyección de dependencias.
"""

from backend.domain.braille_dictionary_port import BrailleDictionaryPort
from backend.domain.braille_symbol import BrailleSymbol, SymbolType
from backend.application.dtos import (
    TranslateTextRequestDTO,
    TranslateTextResponseDTO,
    TranslationMetadataDTO,
)


class TranslateTextToBrailleUseCase:
    """
    Caso de Uso: Traduce texto español → Braille.

    Reglas de negocio:
    1. Mayúsculas    → get_symbol_sequence_for_text ya antepone el prefijo (^)
    2. Bloque numérico → prefijo ⠼ se inserta al abrir el bloque;
                         se cierra con cualquier carácter no-dígito
    3. Caracteres sin soporte → omitidos, registrados en metadatos
    4. Espacio → celda vacía Braille
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

        symbols, unsupported = self._translate(request.text)
        braille_output = "".join(s.to_unicode() for s in symbols)

        metadata = None
        if request.include_metadata:
            metadata = TranslationMetadataDTO(
                total_chars=len(request.text),
                translated_chars=len(request.text) - len(unsupported),
                unsupported_chars=list(set(unsupported)),
            )

        return TranslateTextResponseDTO(
            success=bool(braille_output),
            original_text=request.text,
            braille_output=braille_output,
            metadata=metadata,
        )

    # ──────────────────────────────────────────────────────
    # Algoritmo de traducción
    # ──────────────────────────────────────────────────────

    def _translate(
        self, text: str
    ) -> tuple[list[BrailleSymbol], list[str]]:
        result: list[BrailleSymbol] = []
        unsupported: list[str] = []
        in_number_block = False

        for char in text:
            is_digit = char.isdigit()

            # Gestión del bloque numérico
            if is_digit and not in_number_block:
                # Accedemos al prefijo numérico a través del puerto
                # (el puerto concreto lo expone; si no lo expone usamos contains)
                numeric_prefix = self._get_numeric_prefix()
                if numeric_prefix:
                    result.append(numeric_prefix)
                in_number_block = True
            elif not is_digit:
                in_number_block = False

            # Obtener secuencia de símbolos (maneja mayúsculas internamente)
            sequence = self._dict.get_symbol_sequence_for_text(char)

            if sequence:
                result.extend(sequence)
            else:
                unsupported.append(char)

        return result, unsupported

    def _get_numeric_prefix(self) -> BrailleSymbol | None:
        """
        Obtiene el prefijo numérico del diccionario si lo expone,
        de lo contrario lo busca por su token convencional '#'.
        """
        # Muchas implementaciones de BrailleDictionaryPort exponen
        # numeric_prefix como property; lo intentamos con duck typing
        if hasattr(self._dict, "numeric_prefix"):
            return self._dict.numeric_prefix  # type: ignore[attr-defined]
        # Fallback: buscar por token '#'
        return self._dict.get_symbol_for_text("#")


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