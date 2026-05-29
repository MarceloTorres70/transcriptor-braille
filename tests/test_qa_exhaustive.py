import pytest
import sys
import os

# Asegurar que el path incluya la raíz del proyecto para las importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.infrastructure.spanish_braille_dictionary import SpanishBrailleDictionary
from backend.application.use_cases import TranslateTextToBrailleUseCase
from backend.application.dtos import TranslateTextRequestDTO

@pytest.fixture
def translator():
    """Fixture que inicializa el caso de uso con el diccionario español."""
    return TranslateTextToBrailleUseCase(SpanishBrailleDictionary())

def test_lowercase_alphabet_coverage(translator):
    """Prueba exacta de mapeo Braille para cada letra minúscula (a-z)."""
    expected_map = {
        "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑",
        "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
        "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕",
        "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
        "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", "z": "⠵",
    }

    for letter, expected in expected_map.items():
        res = translator.execute(TranslateTextRequestDTO(letter, include_metadata=True))
        assert res.success, f"La traducción de '{letter}' falló"
        assert res.metadata.unsupported_chars == [], f"'{letter}' fue marcado como no soportado"
        assert res.braille_output == expected, (
            f"Error de mapeo para '{letter}': se esperaba '{expected}', se obtuvo '{res.braille_output}'"
        )

def test_special_spanish_characters(translator):
    """Prueba vocales tildadas (á, é, í, ó, ú), la 'ñ', la 'w' y la 'ü'."""
    special_chars = {
        "á": "⠷", # \u2837
        "é": "⠮", # \u282e
        "í": "⠔", # \u2814
        "ó": "⠬", # \u282c
        "ú": "⠾", # \u283e
        "ñ": "⠻", # \u283b
        "w": "⠺", # \u283a
        "ü": "⠳", # \u2833
    }
    
    for char, expected in special_chars.items():
        res = translator.execute(TranslateTextRequestDTO(char))
        assert res.braille_output == expected, f"Error traduciendo '{char}': se esperaba {expected}, se obtuvo {res.braille_output}"

def test_numbers_with_numeric_prefix(translator):
    """Prueba números (0-9) validando que el sistema agregue el prefijo numérico Braille (⠼)."""
    # El prefijo numérico en español es \u283c (⠼)
    numeric_prefix = "⠼"
    digits = {
        "1": "⠁", "2": "⠃", "3": "⠉", "4": "⠙", "5": "⠑",
        "6": "⠋", "7": "⠛", "8": "⠓", "9": "⠊", "0": "⠚"
    }
    
    for digit, braille in digits.items():
        res = translator.execute(TranslateTextRequestDTO(digit))
        expected = numeric_prefix + braille
        assert res.braille_output == expected, f"Error traduciendo número '{digit}': falta prefijo o carácter incorrecto"

def test_mathematical_signs_and_parentheses(translator):
    """Prueba signos matemáticos (+, -, *, /, =) y paréntesis."""
    math_symbols = {
        "+": "⠖", # \u2816
        "-": "⠤", # \u2824
        "*": "⠡", # \u2821
        "/": "⠌", # \u280c
        "=": "⠶", # \u2836
        "(": "⠦", # \u2826
        ")": "⠴", # \u2834
    }
    
    for symbol, expected in math_symbols.items():
        res = translator.execute(TranslateTextRequestDTO(symbol))
        assert res.braille_output == expected, f"Error traduciendo símbolo '{symbol}': se esperaba {expected}, se obtuvo {res.braille_output}"

def test_uppercase_failure_intentional(translator):
    """
    REQUISITO OBLIGATORIO: Debes programar intencionalmente un test que falle al evaluar las letras mayúsculas.
    
    Este test está diseñado para FALLAR.
    Supone erróneamente que las mayúsculas se traducen igual que las minúsculas sin prefijo.
    En realidad, el sistema agrega el prefijo de mayúscula '⠨' (\u2828).
    """
    char_upper = "A"
    # El sistema real producirá "⠨⠁" (\u2828\u2801)
    # Nosotros afirmamos incorrectamente que producirá solo "⠁" (\u2801)
    res = translator.execute(TranslateTextRequestDTO(char_upper))
    
    print(f"\n[DEBUG] Traduciendo '{char_upper}': Output real = '{res.braille_output}'")
    
    # Esta aserción FALLARÁ intencionalmente
    assert res.braille_output == "⠁", (
        f"TEST FALLIDO INTENCIONALMENTE: Se esperaba que '{char_upper}' no tuviera prefijo de mayúscula, "
        f"pero el sistema devolvió '{res.braille_output}'"
    )
