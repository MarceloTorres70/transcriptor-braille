from abc import ABC, abstractmethod
from typing import Optional
from backend.domain.braille_symbol import BrailleSymbol


class BrailleDictionaryPort(ABC):
    """
    Puerto (abstracción) para acceder al diccionario Braille.
    Permite traducir texto a símbolos Braille.
    """
    
    @abstractmethod
    def get_symbol_for_text(self, token: str) -> Optional[BrailleSymbol]:
        """
        Busca el símbolo Braille para un token de texto.
        
        Args:
            token: Carácter o secuencia a traducir (ej: 'a', 'A', 'ñ')
        
        Returns:
            BrailleSymbol si existe, None si no está en el diccionario
        """
        pass
    
    @abstractmethod
    def contains(self, token: str) -> bool:
        """Verifica si un token existe en el diccionario."""
        pass
