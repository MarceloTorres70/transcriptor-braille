# Arquitectura del Diccionario y Traductor Braille

## 📋 Índice
1. [Visión General](#visión-general)
2. [Componentes](#componentes)
3. [Modelo de Datos](#modelo-de-datos)
4. [Estándar Braille Implementado](#estándar-braille-implementado)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Extensibilidad](#extensibilidad)

---

## Visión General

El sistema de diccionario Braille es una arquitectura **limpia, modular y escalable** para traducir texto español a su representación en Braille. 

**Principios:**
- ✅ **Separación de responsabilidades**: Domain Model ← Application Service ← Port/Adapter Pattern
- ✅ **Inmutabilidad**: Todas las clases de dominio son `frozen` (dataclasses)
- ✅ **Testabilidad**: 100% testeable, sin dependencias externas
- ✅ **Extensibilidad**: Fácil agregar números, símbolos, vocales acentuadas, etc.

---

## Componentes

### 1. **BrailleCell** (`backend/domain/braille_cell.py`)
Representa una **celda Braille** (matriz 2×3 = 6 puntos).

**Características:**
- Almacena puntos como `frozenset` (inmutable, hashable)
- Convierte automáticamente a Unicode Braille
- Valida que puntos estén en rango 1-6
- Impagable para usar en diccionarios

```python
from backend.domain.braille_cell import BrailleCell

# Letra 'a': punto 1
cell_a = BrailleCell((1,))
print(cell_a.unicode_character)  # → '⠁'

# Letra 'b': puntos 1 y 2
cell_b = BrailleCell((1, 2))
print(cell_b.unicode_character)  # → '⠃'
```

**Numeración estándar de puntos:**
```
1 4
2 5
3 6
```

---

### 2. **BrailleSymbol** (`backend/domain/braille_symbol.py`)
Representa un **símbolo Braille completo** (carácter + celda + metadata).

**Características:**
- Mapea un carácter original a su celda Braille
- Clasifica el símbolo (`letter`, `uppercase_prefix`, `special_letter`, etc.)
- Dataclass frozen para inmutabilidad

```python
from backend.domain.braille_symbol import BrailleSymbol, SymbolType

symbol_a = BrailleSymbol(
    text='a',
    cell=BrailleCell((1,)),
    symbol_type=SymbolType.LETTER
)

print(symbol_a.to_unicode())  # → '⠁'
```

**Tipos de símbolos:**
- `LETTER`: Letra minúscula
- `SPECIAL_LETTER`: Letras españolas especiales (ñ)
- `PREFIX`: Prefijo de mayúscula (punto 6)
- `ACCENTED_VOWEL`: Para extensión futura
- `DIGIT`, `PUNCTUATION`, etc.: Para extensión futura

---

### 3. **BrailleDictionaryPort** (`backend/domain/braille_dictionary_port.py`)
**Interfaz (Puerto)** que define el contrato del diccionario.

```python
from abc import ABC, abstractmethod

class BrailleDictionaryPort(ABC):
    @abstractmethod
    def get_symbol_for_text(self, token: str) -> Optional[BrailleSymbol]:
        """Obtiene el símbolo Braille para un token."""
        pass
    
    @abstractmethod
    def contains(self, token: str) -> bool:
        """Verifica si un token existe."""
        pass
```

Permite **múltiples implementaciones** (base de datos, archivo, en memoria, etc.).

---

### 4. **BrailleDictionary** (`backend/domain/braille_dictionary.py`)
**Implementación concreta** del puerto.

**Características:**
- Diccionario precargado con 26 letras minúsculas españolas
- Soporte para mayúsculas usando prefijo (punto 6)
- Letra española 'ñ'
- Búsqueda O(1) con diccionarios internos
- Métodos de utilidad para exploración

```python
from backend.domain.braille_dictionary import BrailleDictionary

dictionary = BrailleDictionary()

# Minúscula
symbol = dictionary.get_symbol_for_text('a')
# → BrailleSymbol('a', BrailleCell((1,)), SymbolType.LETTER)

# Mayúscula retorna prefijo
prefix = dictionary.get_symbol_for_text('A')
# → BrailleSymbol('A', BrailleCell((6,)), SymbolType.PREFIX)

# Secuencia completa de mayúscula
sequence = dictionary.get_symbol_sequence_for_text('A')
# → [BrailleSymbol('A', (6,), PREFIX), BrailleSymbol('A', (1,), LETTER)]
```

---

### 5. **BrailleTranslator** (`backend/application/braille_translator.py`)
**Servicio de aplicación** que usa el diccionario para traducir texto.

**Características:**
- Traduce caracteres individuales o textos completos
- Genera Unicode Braille directo
- Detecta caracteres no soportados
- Proporciona metadata sobre conversión (debugging)

```python
from backend.application.braille_translator import BrailleTranslator

translator = BrailleTranslator()

# Carácter individual
braille = translator.translate_character('a')
# → '⠁'

# Texto completo
text = translator.translate_text('Hola')
# → '⠠⠓⠕⠇⠁'

# Con espacios preservados
text = translator.translate_text('El niño')
# → '⠠⠑⠇ ⠝⠊⠽⠕'

# Análisis detallado
metadata = translator.translate_with_metadata('Paz')
# → [('P', BrailleSymbol(...), '⠠⠏'),
#    ('a', BrailleSymbol(...), '⠁'),
#    ('z', BrailleSymbol(...), '⠵')]
```

---

## Modelo de Datos

### Estructura del Diccionario

El **BrailleDictionary** mantiene internamente:

1. **`_LOWERCASE_LETTERS`**: Mapeo base
   ```python
   {
       'a': (1,),
       'b': (1, 2),
       ...
       'z': (1, 3, 5, 6)
   }
   ```

2. **`_SPECIAL_SPANISH`**: Letras españolas
   ```python
   {
       'ñ': (1, 3, 4, 5, 6)
   }
   ```

3. **`_UPPERCASE_PREFIX`**: Prefijo para mayúsculas
   ```python
   (6,)  # Punto 6
   ```

4. **`_symbols`**: Diccionario interno de símbolos
   ```python
   {
       'a': BrailleSymbol(...),
       'A': BrailleSymbol(...),  # Prefijo
       ...
   }
   ```

---

## Estándar Braille Implementado

### Grado 1 Español
El sistema implementa **Braille Grado 1** (uno a uno, sin contracciones):

| Carácter | Puntos | Unicode | Braille |
|----------|--------|---------|---------|
| a        | 1      | U+2801  | ⠁       |
| b        | 1,2    | U+2803  | ⠃       |
| c        | 1,4    | U+2809  | ⠉       |
| d        | 1,4,5  | U+2819  | ⠙       |
| ñ        | 1,3,4,5,6 | U+283D | ⠽       |
| **A** (prefijo) | 6 | U+2820 | ⠠ |
| **A** (letra a) | 1 | U+2801 | ⠁ |
| **A** (combinado) | — | — | ⠠⠁ |

**Nota:** Las mayúsculas se representan como **secuencia de dos celdas**:
- Celda 1: Prefijo de mayúscula (punto 6)
- Celda 2: Letra minúscula correspondiente

---

## Ejemplos de Uso

### Ejemplo 1: Traducción simple
```python
from backend.application.braille_translator import BrailleTranslator

translator = BrailleTranslator()

texto = "Hola mundo"
braille = translator.translate_text(texto)
print(braille)  # ⠠⠓⠕⠇⠁ ⠍⠥⠝⠙⠕
```

### Ejemplo 2: Validación de caracteres
```python
translator = BrailleTranslator()

# ¿Qué caracteres no son soportados?
unsupported = translator.get_unsupported_characters("Hola123!")
print(unsupported)  # {'1', '2', '3', '!'}
```

### Ejemplo 3: Análisis con metadata
```python
translator = BrailleTranslator()

metadata = translator.translate_with_metadata("Paz")
for char, symbol, braille in metadata:
    if symbol:
        print(f"'{char}' → Tipo: {symbol.symbol_type.value} → {braille}")
    else:
        print(f"'{char}' → Espacio")

# Salida:
# 'P' → Tipo: prefix → ⠠⠏
# 'a' → Tipo: letter → ⠁
# 'z' → Tipo: letter → ⠵
```

---

## Extensibilidad

### Agregando números (Grado 1 español)

```python
# En BrailleDictionary._LOWERCASE_LETTERS, agregar:
_DIGIT_PREFIX = (3, 4, 5, 6)  # Números usan este prefijo

_DIGIT_LETTERS = {
    '1': (1,),      # Mismo patrón que 'a'
    '2': (1, 2),    # Mismo patrón que 'b'
    ...
    '0': (3, 4, 5, 6)  # Cero es especial
}

# Agregar en _build_dictionary():
for digit, dots in self._DIGIT_LETTERS.items():
    cell = BrailleCell(dots)
    prefix = BrailleCell(self._DIGIT_PREFIX)
    symbol = BrailleSymbol(digit, cell, SymbolType.DIGIT)
    prefix_symbol = BrailleSymbol(f'_{digit}', prefix, SymbolType.PREFIX)
    self._symbols[digit] = (prefix_symbol, symbol)
```

### Agregando vocales acentuadas

```python
_ACCENTED_VOWELS = {
    'á': (3, 4, 5, 6, 1),
    'é': (3, 4, 5, 6, 1, 5),
    'í': (3, 4, 5, 6, 2, 4),
    'ó': (3, 4, 5, 6, 1, 3, 5),
    'ú': (3, 4, 5, 6, 1, 3, 6),
}

# Agregar en _build_dictionary():
for char, dots in self._ACCENTED_VOWELS.items():
    cell = BrailleCell(dots)
    symbol = BrailleSymbol(char, cell, SymbolType.ACCENTED_VOWEL)
    self._symbols[char] = symbol
```

### Agregando puntuación

```python
_PUNCTUATION = {
    '.': (2, 3, 4, 5, 6),  # Punto
    ',': (2,),             # Coma
    '!': (2, 3, 5),        # Exclamación
    '?': (2, 3, 4, 6),     # Interrogación
    ...
}
```

---

## Pruebas

El proyecto incluye **66 tests** que verifican:

### Domain Layer (34 tests)
- ✅ Creación de celdas Braille
- ✅ Validación de puntos
- ✅ Conversión a Unicode
- ✅ Diccionario completo (26 minúsculas + 26 mayúsculas + ñ)
- ✅ Prefijo de mayúsculas
- ✅ Secuencias de mayúsculas

### Application Layer (32 tests)
- ✅ Traducción de caracteres individuales
- ✅ Traducción de textos completos
- ✅ Preservación de espacios
- ✅ Detección de caracteres no soportados
- ✅ Metadata y análisis detallado
- ✅ Integración (frases completas)

Ejecutar tests:
```bash
python -m pytest tests/ -v
# → 66 passed in 0.22s ✓
```

---

## Arquitectura de Carpetas

```
backend/
├── domain/                          # Domain Layer (Modelos)
│   ├── braille_cell.py             # Celda Braille
│   ├── braille_symbol.py           # Símbolo Braille
│   ├── braille_dictionary_port.py  # Puerto (interfaz)
│   └── braille_dictionary.py       # Diccionario (implementación)
│
└── application/                     # Application Layer (Servicios)
    └── braille_translator.py       # Traductor (orquestador)

tests/
├── domain/                          # Tests del dominio
│   └── test_braille_rules.py       # 34 tests
│
└── application/                     # Tests de aplicación
    └── test_braille_translator.py  # 32 tests

demo.py                             # Script de demostración
```

---

## Decisiones de Arquitectura

### 1. **Frozen Dataclasses**
- **Por qué:** Garantizan inmutabilidad, previenen bugs, son hashables
- **Beneficio:** Seguridad, paralelismo, caché

### 2. **Port/Adapter Pattern**
- **Por qué:** Permite múltiples implementaciones (DB, archivo, API, etc.)
- **Beneficio:** Testeable, desacoplado, flexible

### 3. **Separación Domain/Application**
- **Por qué:** Domain = lógica pura, Application = orquestación
- **Beneficio:** Reutilizable, testeable independientemente

### 4. **Diccionario precargado**
- **Por qué:** O(1) lookup, sin I/O
- **Beneficio:** Performance, simplicidad, ideal para MVP

### 5. **Secuencias para mayúsculas**
- **Por qué:** Braille estándar requiere 2 celdas (prefijo + letra)
- **Beneficio:** Correcto según estándar, escalable para otros prefijos

---

## Próximos Pasos

Para expandir el sistema:

1. ✅ **Números** (prefijo específico)
2. ✅ **Vocales acentuadas** (español)
3. ✅ **Puntuación** (. , ! ? ; :)
4. ✅ **Símbolos matemáticos** (+, −, =, ÷, ×)
5. ✅ **Braille Grado 2** (con contracciones, para optimización)
6. ✅ **Persistencia** (almacenar en BD, permitir múltiples idiomas)
7. ✅ **API REST** (exponer como servicio)

---

**Documentación generada por:** Backend Senior Developer  
**Fecha:** 2025-05-27  
**Versión:** 1.0 (MVP)
