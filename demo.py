"""
Script de demostración del diccionario y traductor Braille.

Muestra la funcionalidad básica: conversión de letras españolas a Braille.
"""
from backend.infrastructure.spanish_braille_dictionary import SpanishBrailleDictionary
from backend.application.braille_translator import BrailleTranslator


def demo_basic_letters():
    """Demuestra la conversión de letras individuales."""
    print("=" * 70)
    print("DEMO 1: Conversión de letras individuales")
    print("=" * 70)

    dictionary = SpanishBrailleDictionary()

    # Minúsculas
    print("\n▸ Letras minúsculas (a-f):")
    for char in 'abcdef':
        symbol = dictionary.get_symbol_for_text(char)
        unicode_br = symbol.to_unicode()
        dots = sorted(symbol.cell.dots)
        print(f"  '{char}' → Puntos {dots} → Unicode: {repr(unicode_br)} → Braille: {unicode_br}")

    # Mayúsculas
    print("\n▸ Letras mayúsculas (A-C):")
    for char in 'ABC':
        sequence = dictionary.get_symbol_sequence_for_text(char)
        braille_text = ''.join(s.to_unicode() for s in sequence)
        prefix_dots = sorted(sequence[0].cell.dots)
        letter_dots = sorted(sequence[1].cell.dots)
        print(f"  '{char}' → Prefijo {prefix_dots} + Letra {letter_dots} → {braille_text}")

    # Letra española
    print("\n▸ Letra española especial:")
    symbol = dictionary.get_symbol_for_text('ñ')
    dots = sorted(symbol.cell.dots)
    unicode_br = symbol.to_unicode()
    print(f"  'ñ' → Puntos {dots} → Unicode: {repr(unicode_br)} → Braille: {unicode_br}")

    # Vocales acentuadas
    print("\n▸ Vocales acentuadas:")
    for char in 'áéíóú':
        if dictionary.contains(char):
            symbol = dictionary.get_symbol_for_text(char)
            unicode_br = symbol.to_unicode()
            dots = sorted(symbol.cell.dots)
            print(f"  '{char}' → Puntos {dots} → Braille: {unicode_br}")

    # Números
    print("\n▸ Números (0-3):")
    for char in '0123':
        if dictionary.contains(char):
            sequence = dictionary.get_symbol_sequence_for_text(char)
            braille_text = ''.join(s.to_unicode() for s in sequence)
            print(f"  '{char}' → {braille_text}")

    # Operadores matemáticos
    print("\n▸ Operadores matemáticos:")
    for char in '+-*':
        if dictionary.contains(char):
            symbol = dictionary.get_symbol_for_text(char)
            unicode_br = symbol.to_unicode()
            print(f"  '{char}' → {unicode_br}")


def demo_text_translation():
    """Demuestra la traducción de textos completos."""
    print("\n" + "=" * 70)
    print("DEMO 2: Traducción de textos")
    print("=" * 70)

    translator = BrailleTranslator(SpanishBrailleDictionary())

    test_texts = [
        "hola",
        "Hola",
        "El niño español",
        "ABC abc",
        "Año 2024",
    ]

    for text in test_texts:
        braille = translator.translate_text(text)
        unsupported = translator.get_unsupported_characters(text)
        unsupported_str = f" [No soportado: {unsupported}]" if unsupported else ""
        print(f"\n  Entrada:  '{text}'")
        print(f"  Braille:  {braille}{unsupported_str}")


def demo_detailed_analysis():
    """Demuestra análisis detallado de conversión."""
    print("\n" + "=" * 70)
    print("DEMO 3: Análisis detallado")
    print("=" * 70)

    translator = BrailleTranslator(SpanishBrailleDictionary())
    text = "Paz"

    print(f"\nAnálisis de '{text}':")
    metadata = translator.translate_with_metadata(text)

    for i, (original_char, symbol, braille) in enumerate(metadata, 1):
        if symbol:
            dots = sorted(symbol.cell.dots)
            symbol_type = symbol.symbol_type.value
            print(f"  {i}. Carácter: '{original_char}'")
            print(f"     Tipo: {symbol_type}")
            print(f"     Puntos Braille: {dots}")
            print(f"     Unicode: {repr(braille)} → {braille}")
        else:
            print(f"  {i}. Carácter: '{original_char}' (espacio)")


def demo_dictionary_stats():
    """Muestra estadísticas del diccionario."""
    print("\n" + "=" * 70)
    print("DEMO 4: Estadísticas del diccionario")
    print("=" * 70)

    dictionary = SpanishBrailleDictionary()

    lowercase = dictionary.get_all_lowercase_letters()
    accented = dictionary.get_all_accented_vowels()
    uppercase = dictionary.get_all_uppercase_letters()
    digits = dictionary.get_digits()
    math_ops = dictionary.get_math_operators()
    special = dictionary.get_special_spanish_letters()

    print(f"\n  ▸ Letras minúsculas: {len(lowercase)}")
    print(f"  ▸ Vocales acentuadas: {len(accented)}")
    print(f"  ▸ Letras mayúsculas: {len(uppercase)}")
    print(f"  ▸ Dígitos: {len(digits)}")
    print(f"  ▸ Operadores matemáticos: {len(math_ops)}")
    print(f"  ▸ Letras españolas especiales: {len(special)}")

    all_lowercase = ''.join(sorted(lowercase.keys()))
    print(f"\n  Minúsculas soportadas: {all_lowercase}")

    all_accented = ''.join(sorted(accented.keys()))
    print(f"  Acentuadas soportadas: {all_accented}")

    all_uppercase = ''.join(sorted(uppercase.keys()))
    print(f"  Mayúsculas soportadas: {all_uppercase}")

    all_digits = ''.join(sorted(digits.keys()))
    print(f"  Dígitos soportados: {all_digits}")

    all_special = ''.join(sorted(special.keys()))
    print(f"  Especiales soportadas: {all_special}")


def demo_validation():
    """Demuestra validación de caracteres."""
    print("\n" + "=" * 70)
    print("DEMO 5: Validación de caracteres")
    print("=" * 70)

    translator = BrailleTranslator(SpanishBrailleDictionary())

    test_chars = ['a', 'A', 'ñ', '1', '@', ' ', 'á', '+']

    print("\nVerificación de caracteres soportados:")
    for char in test_chars:
        supported = translator.supports_character(char)
        status = "✓" if supported else "✗"
        print(f"  {status} '{char}' → {'Soportado' if supported else 'No soportado'}")


if __name__ == "__main__":
    print("\n")
    print("=" * 70)
    print("DEMOSTRACIÓN: Diccionario y Traductor Braille Español".center(70))
    print("=" * 70)

    demo_basic_letters()
    demo_text_translation()
    demo_detailed_analysis()
    demo_dictionary_stats()
    demo_validation()

    print("\n" + "=" * 70)
    print("Demo completada exitosamente".center(70))
    print("=" * 70 + "\n")

