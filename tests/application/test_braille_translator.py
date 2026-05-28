import pytest
from backend.application.braille_translator import BrailleTranslator
from backend.domain.braille_dictionary import BrailleDictionary


class TestBrailleTranslator:
    """Tests para el servicio de traducción Braille."""
    
    @pytest.fixture
    def translator(self):
        return BrailleTranslator()
    
    def test_translator_initialization(self, translator):
        assert translator is not None
        assert translator.dictionary is not None
    
    # Tests de traducción de caracteres individuales
    def test_translate_lowercase_a(self, translator):
        result = translator.translate_character('a')
        assert result is not None
        assert result == '\u2801'  # Braille 'a'
    
    def test_translate_lowercase_b(self, translator):
        result = translator.translate_character('b')
        assert result is not None
        assert result == '\u2803'  # Braille 'b'
    
    def test_translate_uppercase_a(self, translator):
        result = translator.translate_character('A')
        assert result is not None
        # Debe tener dos caracteres: prefijo + letra
        assert len(result) == 2
        assert result[0] == '\u2820'  # Prefijo de mayúscula (punto 6)
        assert result[1] == '\u2801'  # Braille 'a'
    
    def test_translate_uppercase_b(self, translator):
        result = translator.translate_character('B')
        assert result is not None
        assert len(result) == 2
        assert result[0] == '\u2820'  # Prefijo
        assert result[1] == '\u2803'  # Braille 'b'
    
    def test_translate_spanish_enye(self, translator):
        result = translator.translate_character('ñ')
        assert result is not None
    
    def test_translate_unsupported_character(self, translator):
        result = translator.translate_character('@')
        assert result is None
    
    def test_translate_empty_string(self, translator):
        result = translator.translate_character('')
        assert result is None
    
    def test_translate_multi_char_string(self, translator):
        result = translator.translate_character('ab')
        assert result is None
    
    # Tests de traducción de texto
    def test_translate_text_simple_lowercase(self, translator):
        result = translator.translate_text('abc')
        assert result is not None
        assert len(result) > 0
        assert '\u2801' in result  # 'a'
    
    def test_translate_text_mixed_case(self, translator):
        result = translator.translate_text('Aa')
        assert result is not None
        # Debe contener prefijo de mayúscula
        assert '\u2820' in result
    
    def test_translate_text_with_spaces(self, translator):
        result = translator.translate_text('a b')
        assert result is not None
        assert ' ' in result  # Espacios se preservan
    
    def test_translate_text_empty(self, translator):
        result = translator.translate_text('')
        assert result == ''
    
    def test_translate_text_only_spaces(self, translator):
        result = translator.translate_text('   ')
        assert result == '   '
    
    def test_translate_text_with_unsupported_chars(self, translator):
        # Las palabras con caracteres no soportados saltan esos caracteres
        result = translator.translate_text('a@b')
        assert result is not None
        # Debe contener braille para 'a' y 'b'
        assert '\u2801' in result
        # '@' debe ser ignorado
    
    # Tests de metadata
    def test_translate_with_metadata_single_char(self, translator):
        result = translator.translate_with_metadata('a')
        assert len(result) == 1
        char, symbol, unicode_br = result[0]
        assert char == 'a'
        assert symbol is not None
        assert unicode_br is not None
    
    def test_translate_with_metadata_includes_spaces(self, translator):
        result = translator.translate_with_metadata('a b')
        assert len(result) == 3
        assert result[1] == (' ', None, ' ')  # Espacio en posición 1
        assert result[2][0] == 'b'  # Letra 'b' en posición 2
    
    # Tests de soporte de caracteres
    def test_supports_lowercase(self, translator):
        assert translator.supports_character('a')
        assert translator.supports_character('z')
    
    def test_supports_uppercase(self, translator):
        assert translator.supports_character('A')
        assert translator.supports_character('Z')
    
    def test_supports_space(self, translator):
        assert translator.supports_character(' ')
    
    def test_not_supports_digit(self, translator):
        assert not translator.supports_character('1')
    
    def test_not_supports_special_char(self, translator):
        assert not translator.supports_character('@')
    
    def test_supports_spanish_enye(self, translator):
        assert translator.supports_character('ñ')
    
    # Tests de caracteres no soportados
    def test_get_unsupported_characters_empty(self, translator):
        result = translator.get_unsupported_characters('abc')
        assert len(result) == 0
    
    def test_get_unsupported_characters_with_digits(self, translator):
        result = translator.get_unsupported_characters('a1b2')
        assert '1' in result
        assert '2' in result
        assert 'a' not in result
        assert 'b' not in result
    
    def test_get_unsupported_characters_ignores_spaces(self, translator):
        result = translator.get_unsupported_characters('a b')
        assert ' ' not in result
    
    def test_get_unsupported_characters_special_symbols(self, translator):
        result = translator.get_unsupported_characters('a@b#c')
        assert '@' in result
        assert '#' in result


class TestBrailleTranslatorIntegration:
    """Tests de integración para traducción Braille."""
    
    def test_translate_hello_world(self):
        translator = BrailleTranslator()
        result = translator.translate_text('Hola mundo')
        assert result is not None
        assert len(result) > 0
        # Debe contener el prefijo de mayúscula para 'H'
        assert '\u2820' in result
    
    def test_translate_all_lowercase_alphabet(self):
        translator = BrailleTranslator()
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        result = translator.translate_text(alphabet)
        assert result is not None
        assert len(result) == 26  # 26 caracteres únicos
    
    def test_translate_all_uppercase_alphabet(self):
        translator = BrailleTranslator()
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result = translator.translate_text(alphabet)
        assert result is not None
        # Cada mayúscula son 2 caracteres Braille: prefijo + letra
        assert len(result) == 52
    
    def test_translate_with_spanish_characters(self):
        translator = BrailleTranslator()
        result = translator.translate_text('niño')
        assert result is not None
        unsupported = translator.get_unsupported_characters('niño')
        assert len(unsupported) == 0
    
    def test_translate_spanish_sentence(self):
        translator = BrailleTranslator()
        result = translator.translate_text('El niño español')
        assert result is not None
        assert ' ' in result  # Espacios preservados
