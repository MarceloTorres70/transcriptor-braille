from typing import Optional
from backend.domain.braille_cell import BrailleCell
from backend.domain.braille_symbol import BrailleSymbol, SymbolType
from backend.domain.braille_dictionary_port import BrailleDictionaryPort


class BrailleDictionary(BrailleDictionaryPort):
    """
    Implementación del diccionario Braille.
    
    Mapea caracteres españoles (letras mayúsculas/minúsculas) a sus 
    representaciones en Braille usando el estándar grado 1.
    
    Estructura:
    - Letras minúsculas: se representan directamente (ej: a=1, b=1,2, etc.)
    - Letras mayúsculas: se usa prefijo de mayúscula (punto 6) + letra minúscula
    """
    
    # Diccionario base: letras minúsculas españolas (estándar Braille grado 1)
    # Basado en el estándar de Braille español
    _LOWERCASE_LETTERS = {
        'a': (1,),
        'b': (1, 2),
        'c': (1, 4),
        'd': (1, 4, 5),
        'e': (1, 5),
        'f': (1, 2, 4),
        'g': (1, 2, 4, 5),
        'h': (1, 2, 5),
        'i': (2, 4),
        'j': (2, 4, 5),
        'k': (1, 3),
        'l': (1, 2, 3),
        'm': (1, 3, 4),
        'n': (1, 3, 4, 5),
        'o': (1, 3, 5),
        'p': (1, 2, 3, 4),
        'q': (1, 2, 3, 4, 5),
        'r': (1, 2, 3, 5),
        's': (2, 3, 4),
        't': (2, 3, 4, 5),
        'u': (1, 3, 6),
        'v': (1, 2, 3, 6),
        'w': (2, 4, 5, 6),
        'x': (1, 3, 4, 6),
        'y': (1, 3, 4, 5, 6),
        'z': (1, 3, 5, 6),
    }
    
    # Letra española: ñ
    _SPECIAL_SPANISH = {
        'ñ': (1, 3, 4, 5, 6),
    }
    
    # Prefijo para mayúsculas: punto 6
    _UPPERCASE_PREFIX = (6,)
    
    def __init__(self):
        """Inicializa el diccionario con todos los símbolos precargados."""
        self._symbols = {}
        self._build_dictionary()
    
    def _build_dictionary(self) -> None:
        """Construye el diccionario con todas las letras y prefijos."""
        # Letras minúsculas
        for char, dots in self._LOWERCASE_LETTERS.items():
            cell = BrailleCell(dots)
            symbol = BrailleSymbol(char, cell, SymbolType.LETTER)
            self._symbols[char] = symbol
        
        # Letra española ñ
        for char, dots in self._SPECIAL_SPANISH.items():
            cell = BrailleCell(dots)
            symbol = BrailleSymbol(char, cell, SymbolType.SPECIAL_LETTER)
            self._symbols[char] = symbol
        
        # Letras mayúsculas: combinación de prefijo + minúscula
        for char in self._LOWERCASE_LETTERS:
            uppercase_char = char.upper()
            dots_prefix = self._UPPERCASE_PREFIX
            dots_letter = self._LOWERCASE_LETTERS[char]
            
            # Crear dos celdas: primero prefijo de mayúscula, luego la letra
            cell_prefix = BrailleCell(dots_prefix)
            symbol_prefix = BrailleSymbol(uppercase_char, cell_prefix, SymbolType.PREFIX)
            
            # Almacenar como clave única (puede ser expandida para multicelda)
            prefix_key = f"_prefix_{uppercase_char}"
            self._symbols[prefix_key] = symbol_prefix
            
            # Almacenar también la letra minúscula del par mayúscula
            cell_letter = BrailleCell(dots_letter)
            symbol_letter = BrailleSymbol(uppercase_char, cell_letter, SymbolType.LETTER)
            letter_key = f"_letter_{uppercase_char}"
            self._symbols[letter_key] = symbol_letter
        
        # Almacenar mapa directo de mayúsculas para búsqueda rápida
        self._uppercase_map = {}
        for char in self._LOWERCASE_LETTERS:
            uppercase_char = char.upper()
            prefix_symbol = self._symbols[f"_prefix_{uppercase_char}"]
            letter_symbol = self._symbols[f"_letter_{uppercase_char}"]
            self._uppercase_map[uppercase_char] = (prefix_symbol, letter_symbol)
    
    def get_symbol_for_text(self, token: str) -> Optional[BrailleSymbol]:
        """
        Obtiene el símbolo Braille para un token.
        
        Para minúsculas: retorna directamente la celda.
        Para mayúsculas: retorna el prefijo (punto 6) como símbolo.
        
        Args:
            token: Carácter a traducir
        
        Returns:
            BrailleSymbol o None si no existe
        """
        if not token:
            return None
        
        # Búsqueda directa para minúsculas y caracteres especiales
        if token in self._symbols:
            return self._symbols[token]
        
        # Para mayúsculas, retornar el prefijo primero
        if token.isupper() and token in self._uppercase_map:
            prefix_symbol, _ = self._uppercase_map[token]
            return prefix_symbol
        
        return None
    
    def get_symbol_sequence_for_text(self, token: str) -> Optional[list[BrailleSymbol]]:
        """
        Obtiene la secuencia de símbolos para un token (útil para mayúsculas).
        
        Ejemplo:
            'A' -> [BrailleSymbol(prefijo_mayúscula), BrailleSymbol(letra_a)]
        
        Args:
            token: Carácter a traducir
        
        Returns:
            Lista de símbolos o None
        """
        if not token:
            return None
        
        # Minúsculas: una sola celda
        if token in self._symbols and not token.isupper():
            return [self._symbols[token]]
        
        # Mayúsculas: prefijo + letra
        if token.isupper() and token in self._uppercase_map:
            prefix_symbol, letter_symbol = self._uppercase_map[token]
            return [prefix_symbol, letter_symbol]
        
        return None
    
    def contains(self, token: str) -> bool:
        """Verifica si un token existe en el diccionario."""
        if not token:
            return False
        
        if token in self._symbols:
            return True
        
        if token.isupper() and token in self._uppercase_map:
            return True
        
        return False
    
    def get_all_lowercase_letters(self) -> dict[str, BrailleSymbol]:
        """Retorna todas las letras minúsculas del diccionario."""
        return {
            char: self._symbols[char]
            for char in self._LOWERCASE_LETTERS
        }
    
    def get_all_uppercase_letters(self) -> dict[str, tuple[BrailleSymbol, BrailleSymbol]]:
        """Retorna todas las letras mayúsculas del diccionario."""
        return self._uppercase_map.copy()
    
    def get_special_spanish_letters(self) -> dict[str, BrailleSymbol]:
        """Retorna las letras españolas especiales (ñ, etc.)."""
        return {
            char: self._symbols[char]
            for char in self._SPECIAL_SPANISH
        }
