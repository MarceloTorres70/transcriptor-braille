import pytest
from backend.domain.braille_cell import BrailleCell
from backend.domain.braille_symbol import BrailleSymbol, SymbolType
from backend.domain.braille_dictionary import BrailleDictionary


class TestBrailleCell:
    """Tests para la celda Braille."""
    
    def test_braille_cell_with_single_dot(self):
        cell = BrailleCell((1,))
        assert 1 in cell.dots
        assert len(cell.dots) == 1
    
    def test_braille_cell_with_multiple_dots(self):
        cell = BrailleCell((1, 2, 4))
        assert cell.dots == frozenset({1, 2, 4})
    
    def test_braille_cell_empty(self):
        cell = BrailleCell(())
        assert len(cell.dots) == 0
    
    def test_braille_cell_none(self):
        cell = BrailleCell(None)
        assert len(cell.dots) == 0
    
    def test_braille_cell_invalid_dot_number(self):
        with pytest.raises(ValueError, match="must be in range 1-6"):
            BrailleCell((1, 7))
    
    def test_braille_cell_unicode_character(self):
        # Celda vacía
        cell_empty = BrailleCell(())
        assert cell_empty.unicode_character == '\u2800'
        
        # Celda con punto 1
        cell_a = BrailleCell((1,))
        assert cell_a.unicode_character == '\u2801'
    
    def test_braille_cell_is_frozen(self):
        cell = BrailleCell((1, 2))
        with pytest.raises(AttributeError):
            cell.dots = frozenset({3, 4})
    
    def test_braille_cell_bool(self):
        assert bool(BrailleCell((1,)))
        assert not bool(BrailleCell(()))


class TestBrailleSymbol:
    """Tests para el símbolo Braille."""
    
    def test_symbol_creation(self):
        cell = BrailleCell((1,))
        symbol = BrailleSymbol('a', cell, SymbolType.LETTER)
        assert symbol.text == 'a'
        assert symbol.cell == cell
        assert symbol.symbol_type == SymbolType.LETTER
    
    def test_symbol_to_unicode(self):
        cell = BrailleCell((1,))
        symbol = BrailleSymbol('a', cell, SymbolType.LETTER)
        assert symbol.to_unicode() == '\u2801'
    
    def test_symbol_empty_text_raises_error(self):
        cell = BrailleCell((1,))
        with pytest.raises(ValueError, match="cannot be empty"):
            BrailleSymbol('', cell, SymbolType.LETTER)
    
    def test_symbol_invalid_cell_raises_error(self):
        with pytest.raises(TypeError):
            BrailleSymbol('a', "not_a_cell", SymbolType.LETTER)
    
    def test_symbol_is_frozen(self):
        cell = BrailleCell((1,))
        symbol = BrailleSymbol('a', cell, SymbolType.LETTER)
        with pytest.raises(AttributeError):
            symbol.text = 'b'


class TestBrailleDictionary:
    """Tests para el diccionario Braille."""
    
    @pytest.fixture
    def dictionary(self):
        return BrailleDictionary()
    
    def test_dictionary_initialization(self, dictionary):
        assert dictionary is not None
    
    # Tests de letras minúsculas
    def test_lowercase_letter_a(self, dictionary):
        symbol = dictionary.get_symbol_for_text('a')
        assert symbol is not None
        assert symbol.text == 'a'
        assert 1 in symbol.cell.dots
        assert symbol.symbol_type == SymbolType.LETTER
    
    def test_lowercase_letter_b(self, dictionary):
        symbol = dictionary.get_symbol_for_text('b')
        assert symbol is not None
        assert 1 in symbol.cell.dots
        assert 2 in symbol.cell.dots
    
    def test_all_lowercase_letters_exist(self, dictionary):
        lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
        for letter in lowercase_letters:
            assert dictionary.contains(letter), f"Letter '{letter}' not found"
            symbol = dictionary.get_symbol_for_text(letter)
            assert symbol is not None
    
    # Tests de letras mayúsculas
    def test_uppercase_letter_returns_prefix(self, dictionary):
        symbol = dictionary.get_symbol_for_text('A')
        assert symbol is not None
        assert symbol.symbol_type == SymbolType.PREFIX
        assert 6 in symbol.cell.dots  # Prefijo de mayúscula es punto 6
    
    def test_all_uppercase_letters_exist(self, dictionary):
        uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in uppercase_letters:
            assert dictionary.contains(letter), f"Letter '{letter}' not found"
            symbol = dictionary.get_symbol_for_text(letter)
            assert symbol is not None
            assert symbol.symbol_type == SymbolType.PREFIX
    
    def test_uppercase_sequence(self, dictionary):
        sequence = dictionary.get_symbol_sequence_for_text('A')
        assert sequence is not None
        assert len(sequence) == 2
        
        prefix_symbol, letter_symbol = sequence
        assert prefix_symbol.symbol_type == SymbolType.PREFIX
        assert 6 in prefix_symbol.cell.dots
        
        assert letter_symbol.symbol_type == SymbolType.LETTER
        assert 1 in letter_symbol.cell.dots  # Letra 'a'
    
    def test_uppercase_b_sequence(self, dictionary):
        sequence = dictionary.get_symbol_sequence_for_text('B')
        assert sequence is not None
        assert len(sequence) == 2
        
        prefix_symbol, letter_symbol = sequence
        assert 6 in prefix_symbol.cell.dots
        assert 1 in letter_symbol.cell.dots
        assert 2 in letter_symbol.cell.dots
    
    # Tests de letras españolas especiales
    def test_spanish_letter_enye(self, dictionary):
        symbol = dictionary.get_symbol_for_text('ñ')
        assert symbol is not None
        assert symbol.text == 'ñ'
        assert symbol.symbol_type == SymbolType.SPECIAL_LETTER
        assert symbol.cell.dots == frozenset({1, 3, 4, 5, 6})
    
    # Tests de contains
    def test_contains_lowercase(self, dictionary):
        assert dictionary.contains('a')
        assert dictionary.contains('z')
    
    def test_contains_uppercase(self, dictionary):
        assert dictionary.contains('A')
        assert dictionary.contains('Z')
    
    def test_contains_special(self, dictionary):
        assert dictionary.contains('ñ')
    
    def test_not_contains_invalid(self, dictionary):
        assert not dictionary.contains('@')
        assert not dictionary.contains('1')
        assert not dictionary.contains('')
    
    # Tests de diccionarios
    def test_get_all_lowercase_letters(self, dictionary):
        lowercase_dict = dictionary.get_all_lowercase_letters()
        assert len(lowercase_dict) == 26
        assert 'a' in lowercase_dict
        assert 'z' in lowercase_dict
    
    def test_get_all_uppercase_letters(self, dictionary):
        uppercase_dict = dictionary.get_all_uppercase_letters()
        assert len(uppercase_dict) == 26
        assert 'A' in uppercase_dict
        assert 'Z' in uppercase_dict
    
    def test_get_special_spanish_letters(self, dictionary):
        special_dict = dictionary.get_special_spanish_letters()
        assert 'ñ' in special_dict
        assert special_dict['ñ'].symbol_type == SymbolType.SPECIAL_LETTER


class TestBrailleRules:
    """Tests para las reglas de conversión Braille."""
    
    def test_lowercase_a_to_z_conversion(self):
        """Prueba que todas las letras minúsculas se convierten correctamente."""
        dictionary = BrailleDictionary()
        lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
        
        for letter in lowercase_letters:
            symbol = dictionary.get_symbol_for_text(letter)
            assert symbol is not None, f"No symbol found for '{letter}'"
            assert symbol.to_unicode() != '\u2800', f"Symbol for '{letter}' is blank"
    
    def test_uppercase_translation_requires_prefix(self):
        """Prueba que las mayúsculas incluyen prefijo (punto 6)."""
        dictionary = BrailleDictionary()
        uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        for letter in uppercase_letters:
            symbol = dictionary.get_symbol_for_text(letter)
            assert symbol is not None, f"No symbol found for '{letter}'"
            assert 6 in symbol.cell.dots, f"Uppercase '{letter}' missing prefix (dot 6)"
    
    def test_uppercase_sequence_has_two_cells(self):
        """Prueba que mayúsculas generan dos celdas: prefijo + letra."""
        dictionary = BrailleDictionary()
        uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        for letter in uppercase_letters:
            sequence = dictionary.get_symbol_sequence_for_text(letter)
            assert sequence is not None, f"No sequence found for '{letter}'"
            assert len(sequence) == 2, f"Uppercase '{letter}' should have 2 symbols"
            
            prefix, letter_symbol = sequence
            assert prefix.symbol_type == SymbolType.PREFIX
            assert letter_symbol.symbol_type == SymbolType.LETTER
    
    def test_spanish_enye_distinct_from_n(self):
        """Prueba que ñ es distinto de n."""
        dictionary = BrailleDictionary()
        
        symbol_n = dictionary.get_symbol_for_text('n')
        symbol_enye = dictionary.get_symbol_for_text('ñ')
        
        assert symbol_n is not None
        assert symbol_enye is not None
        assert symbol_n.cell.dots != symbol_enye.cell.dots
    
    def test_numeric_prefix_for_0_to_9(self):
        # TODO: Implementar test para prefijo numérico (puntos 3, 4, 5, 6)
        pass

