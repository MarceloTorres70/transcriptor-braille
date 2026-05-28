# Guía Rápida: Diccionario Braille

## 🚀 Uso Rápido

### Traducir un texto
```python
from backend.application.braille_translator import BrailleTranslator

translator = BrailleTranslator()
braille = translator.translate_text("Hola")
print(braille)  # ⠠⠓⠕⠇⠁
```

### Traducir un carácter
```python
braille_a = translator.translate_character('a')  # ⠁
braille_A = translator.translate_character('A')  # ⠠⠁
```

### Detectar caracteres no soportados
```python
unsupported = translator.get_unsupported_characters("Hola123")
print(unsupported)  # {'1', '2', '3'}
```

### Verificar soporte de un carácter
```python
if translator.supports_character('ñ'):
    print("Soportado")  # ✓ Soportado
```

---

## 📚 API Completa

### BrailleDictionary
```python
from backend.domain.braille_dictionary import BrailleDictionary

dic = BrailleDictionary()

# Obtener símbolo
symbol = dic.get_symbol_for_text('a')
print(symbol.text)              # 'a'
print(symbol.symbol_type)       # SymbolType.LETTER
print(symbol.cell.dots)         # frozenset({1})
print(symbol.to_unicode())      # '⠁'

# Obtener secuencia (mayúsculas)
sequence = dic.get_symbol_sequence_for_text('A')
print(len(sequence))            # 2 (prefijo + letra)

# Verificar existencia
if dic.contains('ñ'):
    print("Existe")

# Explorar diccionario
lowercase = dic.get_all_lowercase_letters()      # 26 letras
uppercase = dic.get_all_uppercase_letters()      # 26 letras
special = dic.get_special_spanish_letters()      # {'ñ': ...}
```

### BrailleTranslator
```python
from backend.application.braille_translator import BrailleTranslator

tr = BrailleTranslator()

# Traducir
braille = tr.translate_text("Paz")
# → '⠠⠏⠁⠵'

# Analizar con metadata
metadata = tr.translate_with_metadata("Paz")
# → [('P', BrailleSymbol(...), '⠠⠏'),
#    ('a', BrailleSymbol(...), '⠁'),
#    ('z', BrailleSymbol(...), '⠵')]

for char, symbol, braille_char in metadata:
    if symbol:
        print(f"{char} → {braille_char} (tipo: {symbol.symbol_type.value})")
    else:
        print(f"{char} → {braille_char} (espacio)")

# Obtener caracteres no soportados
unsupported = tr.get_unsupported_characters("Hola@123")
# → {'@', '1', '2', '3'}

# Verificar carácter
if tr.supports_character('a'):
    print("Letra soportada")
```

---

## 🔢 Numeración Braille (Referencia)

### Celdas Braille (2×3)
```
1 4
2 5
3 6
```

### Ejemplos
| Carácter | Puntos | Unicode | Braille |
|----------|--------|---------|---------|
| a | 1 | U+2801 | ⠁ |
| b | 1,2 | U+2803 | ⠃ |
| c | 1,4 | U+2809 | ⠉ |
| ñ | 1,3,4,5,6 | U+283D | ⠽ |
| **A** | 6 (prefijo) | U+2820 | ⠠ |

---

## 🧪 Testing

```bash
# Todos los tests
python -m pytest tests/ -v

# Solo tests del dominio
python -m pytest tests/domain/ -v

# Solo tests de aplicación
python -m pytest tests/application/ -v

# Test específico
python -m pytest tests/domain/test_braille_rules.py::TestBrailleCell -v

# Con coverage
python -m pytest tests/ --cov=backend --cov-report=html
```

---

## 📝 Casos de Uso Comunes

### 1️⃣ Convertir un nombre
```python
translator = BrailleTranslator()
name = "María"
braille = translator.translate_text(name)
print(f"{name} → {braille}")
# María → ⠠⠍⠁⠗⠇⠁
```

### 2️⃣ Procesar una oración
```python
sentence = "El niño español"
braille = translator.translate_text(sentence)
# ⠠⠑⠇ ⠝⠊⠽⠕ ⠑⠎⠏⠁⠽⠕⠇
```

### 3️⃣ Validar entrada antes de convertir
```python
text = "Hola123"
unsupported = translator.get_unsupported_characters(text)

if unsupported:
    print(f"⚠️ Caracteres no soportados: {unsupported}")
else:
    print(f"✓ Puede ser convertido: {translator.translate_text(text)}")
```

### 4️⃣ Obtener metadata para debugging
```python
text = "Paz"
metadata = translator.translate_with_metadata(text)

for i, (original, symbol, braille) in enumerate(metadata, 1):
    if symbol:
        print(f"{i}. '{original}' → {braille} (puntos: {sorted(symbol.cell.dots)})")
```

### 5️⃣ Iterar sobre el diccionario
```python
dictionary = BrailleDictionary()

# Todas las minúsculas
for char, symbol in dictionary.get_all_lowercase_letters().items():
    print(f"{char} → {symbol.to_unicode()}")

# Todas las mayúsculas
for char, (prefix, letter) in dictionary.get_all_uppercase_letters().items():
    braille = prefix.to_unicode() + letter.to_unicode()
    print(f"{char} → {braille}")
```

---

## ⚙️ Configuración

No hay configuración requerida. El diccionario está **precargado en memoria**.

Para usar una implementación diferente (DB, API, etc.):

```python
from backend.domain.braille_dictionary_port import BrailleDictionaryPort

class CustomDictionary(BrailleDictionaryPort):
    def get_symbol_for_text(self, token):
        # Tu implementación
        pass
    
    def contains(self, token):
        # Tu implementación
        pass

# Usar con el traductor
translator = BrailleTranslator(dictionary=CustomDictionary())
```

---

## 🐛 Troubleshooting

### Carácter devuelve None
```python
translator = BrailleTranslator()
result = translator.translate_character('1')  # None

# Solución: Verificar si está soportado
if translator.supports_character('1'):
    result = translator.translate_character('1')
else:
    print(f"No soportado. Soportados: {translator.supports_character('a')}")
```

### Unicode Braille no se ve correctamente
- Asegurate de usar una **fuente que soporte Braille Unicode**
- Opciones: DejaVu Sans, Code2000, ADFX Braille
- En navegadores: Unicode Braille Unicode font

### Mayúsculas generan dos caracteres
```python
# Correcto: Braille estándar requiere 2 celdas
braille = translator.translate_character('A')
print(len(braille))  # 2 (prefijo + letra)
print(braille[0])    # ⠠ (prefijo)
print(braille[1])    # ⠁ (letra a)
```

---

## 📦 Dependencias

- **Python 3.10+**
- **pytest** (solo para tests)
- Sin dependencias externas

```bash
pip install pytest  # Para ejecutar tests
```

---

## 📖 Documentación Completa

Ver `docs/BRAILLE_ARCHITECTURE.md` para:
- Decisiones de arquitectura
- Extensibilidad
- Próximos pasos
- Estándar Braille

---

## 💡 Tips & Tricks

```python
# 1. Reutiliza la misma instancia de BrailleTranslator
translator = BrailleTranslator()  # Constructor una sola vez
for text in texts:
    braille = translator.translate_text(text)

# 2. Acceso directo a diccionario si necesitas performance
from backend.domain.braille_dictionary import BrailleDictionary
dic = BrailleDictionary()  # O(1) lookup
symbol = dic.get_symbol_for_text('a')  # Muy rápido

# 3. Verificar soporte antes de convertir
texts = ["Hola", "Hola123", "El niño"]
for text in texts:
    unsupported = translator.get_unsupported_characters(text)
    if not unsupported:
        print(f"✓ {text} → {translator.translate_text(text)}")
    else:
        print(f"✗ {text} tiene: {unsupported}")

# 4. Extraer solo caracteres soportados
def clean_text(text, translator):
    return ''.join(
        c for c in text 
        if c == ' ' or translator.supports_character(c)
    )

clean = clean_text("Hola123", translator)  # "Hola"
braille = translator.translate_text(clean)
```

---

**Última actualización:** 2025-05-27
