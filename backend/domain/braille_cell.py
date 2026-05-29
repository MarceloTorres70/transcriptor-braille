from dataclasses import dataclass
from typing import FrozenSet, Union


@dataclass(frozen=True)
class BrailleCell:
    """
    Representa una celda Braille (matriz 2x3 = 6 puntos).
    
    Numeración estándar de puntos:
        1 4
        2 5
        3 6
    
    Ejemplo: 'a' = punto 1 = (1,)
             'b' = puntos 1,2 = (1, 2)
    """
    dots: FrozenSet[int]

    def __init__(self, dots: Union[tuple[int, ...], set[int], list[int], None] = None):
        if dots is None:
            dots_set = frozenset()
        else:
            dots_set = frozenset(dots)
        
        # Validar que los puntos estén en rango 1-6
        if not all(1 <= dot <= 6 for dot in dots_set):
            raise ValueError("Braille dots must be in range 1-6")
        
        object.__setattr__(self, 'dots', dots_set)

    @property
    def unicode_character(self) -> str:
        """Retorna el carácter Unicode correspondiente a esta celda."""
        if not self.dots:
            return '\u2800'  # Braille blank
        
        # Construir el patrón binario de la celda
        # Unicode Braille: 0x2800 + suma de potencias de 2 para cada punto
        dot_map = {1: 0x01, 2: 0x02, 3: 0x04, 4: 0x08, 5: 0x10, 6: 0x20}
        value = sum(dot_map.get(dot, 0) for dot in self.dots)
        return chr(0x2800 + value)

    def __repr__(self) -> str:
        return f"BrailleCell({sorted(self.dots)})"

    def __bool__(self) -> bool:
        return bool(self.dots)
