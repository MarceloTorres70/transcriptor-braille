from typing import Optional
from backend.domain.braille_dictionary_port import BrailleDictionaryPort
from backend.domain.braille_symbol import BrailleSymbol


class BrailleTranslator:
    """
    Servicio de aplicación para traducir texto a Braille.

    Utiliza el puerto del diccionario Braille (abstracción) para convertir
    caracteres individuales a sus representaciones en Braille.
    """

    def __init__(self, dictionary_port: BrailleDictionaryPort):
        """
        Inicializa el traductor con una implementación del puerto.

        Args:
            dictionary_port: Instancia que implementa BrailleDictionaryPort
        """
        if not isinstance(dictionary_port, BrailleDictionaryPort):
            raise TypeError("dictionary_port must implement BrailleDictionaryPort")
        self.dictionary = dictionary_port

    def translate_character(self, char: str) -> Optional[str]:
        """
        Traduce un carácter individual a Braille Unicode.

        Args:
            char: Carácter a traducir (ej: 'a', 'A', 'ñ', '5')

        Returns:
            String con carácter(es) Unicode Braille o None si no está en el diccionario

        Ejemplo:
            'a' -> '\u2801' (Braille para 'a')
            'A' -> '\u2820\u2801' (prefijo mayúscula + Braille para 'a')
            '5' -> '\u283c\u2815' (prefijo numérico + Braille para '5')
        """
        if not char or len(char) != 1:
            return None

        sequence = self.dictionary.get_symbol_sequence_for_text(char)
        if sequence:
            return ''.join(symbol.to_unicode() for symbol in sequence)

        symbol = self.dictionary.get_symbol_for_text(char)
        if symbol:
            return symbol.to_unicode()

        return None

    def translate_text(self, text: str) -> str:
        """
        Traduce un texto completo a Braille Unicode.

        Salta caracteres no reconocidos (excepto espacios que mantiene).

        Args:
            text: Texto a traducir (ej: 'Hola 123')

        Returns:
            String con caracteres Unicode Braille correspondientes
        """
        if not text:
            return ""

        result = []
        for char in text:
            if char == ' ':
                result.append(' ')
            else:
                braille = self.translate_character(char)
                if braille:
                    result.append(braille)

        return ''.join(result)

    def translate_with_metadata(self, text: str) -> list[tuple[str, Optional[BrailleSymbol], Optional[str]]]:
        """
        Traduce un texto manteniendo metadata sobre cada símbolo.

        Útil para debugging y análisis.

        Args:
            text: Texto a traducir

        Returns:
            Lista de tuplas (carácter_original, símbolo_braille, unicode_braille)
        """
        result = []
        for char in text:
            if char == ' ':
                result.append((char, None, ' '))
            else:
                symbol = self.dictionary.get_symbol_for_text(char)
                unicode_braille = self.translate_character(char)
                result.append((char, symbol, unicode_braille))

        return result

    def supports_character(self, char: str) -> bool:
        """Verifica si un carácter está soportado en el diccionario."""
        if char == ' ':
            return True
        return self.dictionary.contains(char)

    def get_unsupported_characters(self, text: str) -> set[str]:
        """Retorna el conjunto de caracteres no soportados en un texto."""
        unsupported = set()
        for char in text:
            if char != ' ' and not self.supports_character(char):
                unsupported.add(char)
        return unsupported

