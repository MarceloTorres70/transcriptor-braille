import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from backend.infrastructure.spanish_braille_dictionary import SpanishBrailleDictionary
from backend.application.use_cases import TranslateTextToBrailleUseCase
from backend.application.dtos import TranslateTextRequestDTO
from backend.domain.braille_dictionary_port import BrailleDictionaryPort
from backend.domain.braille_cell import BrailleCell
from backend.domain.braille_symbol import BrailleSymbol
from backend.domain.braille_symbol import SymbolType


@pytest.fixture
def dic():
    return SpanishBrailleDictionary()

@pytest.fixture
def uc(dic):
    return TranslateTextToBrailleUseCase(dictionary=dic)


class TestDictionary:
    def test_basic_letters(self, dic):
        for ch in "abcdefghijklmnopqrstuvwxyz":
            assert dic.contains(ch), f"Falta letra: {ch}"

    def test_enie(self, dic):
        assert dic.contains("ñ")

    def test_vocales_tildadas(self, dic):
        for ch in "áéíóúü":
            assert dic.contains(ch), f"Falta tildada: {ch}"

    def test_digits(self, dic):
        for d in "0123456789":
            assert dic.contains(d), f"Falta dígito: {d}"

    def test_math_signs(self, dic):
        for s in "+-*/=":
            assert dic.contains(s), f"Falta signo: {s}"

    def test_parentheses(self, dic):
        assert dic.contains("(")
        assert dic.contains(")")

    def test_numeric_prefix_exists(self, dic):
        assert dic.numeric_prefix is not None
        assert dic.numeric_prefix.symbol_type == SymbolType.PREFIX

    def test_capital_prefix_exists(self, dic):
        assert dic.capital_prefix is not None
        assert dic.capital_prefix.symbol_type == SymbolType.PREFIX

    def test_uppercase_sequence_has_prefix(self, dic):
        seq = dic.get_symbol_sequence_for_text("A")
        assert len(seq) == 2
        assert seq[0].symbol_type == SymbolType.PREFIX  # capital prefix
        assert seq[1].symbol_type == SymbolType.LETTER

    def test_lowercase_sequence_no_prefix(self, dic):
        seq = dic.get_symbol_sequence_for_text("a")
        assert len(seq) == 1


class TestUseCase:
    def test_simple_word(self, uc):
        res = uc.execute(TranslateTextRequestDTO("hola"))
        assert res.success
        assert res.braille_output != ""

    def test_uppercase_prefix_in_output(self, uc):
        res = uc.execute(TranslateTextRequestDTO("A"))
        # Prefijo mayúscula (puntos 4,6) → U+2828 (⠨)
        assert "⠨" in res.braille_output

    def test_number_block_single_prefix(self, uc):
        res = uc.execute(TranslateTextRequestDTO("123"))
        numeric_prefix_unicode = "\u283c"  # puntos 3,4,5,6
        assert res.braille_output.count(numeric_prefix_unicode) == 1

    def test_two_number_blocks_two_prefixes(self, uc):
        res = uc.execute(TranslateTextRequestDTO("1a2"))
        numeric_prefix_unicode = "\u283c"
        assert res.braille_output.count(numeric_prefix_unicode) == 2

    def test_empty_text_fails(self, uc):
        res = uc.execute(TranslateTextRequestDTO(""))
        assert not res.success
        assert res.error

    def test_metadata_coverage(self, uc):
        res = uc.execute(TranslateTextRequestDTO("hola", include_metadata=True))
        assert res.metadata.total_chars == 4
        assert res.metadata.coverage_percentage == 100.0

    def test_unsupported_char_tracked(self, uc):
        res = uc.execute(TranslateTextRequestDTO("a€b", include_metadata=True))
        assert "€" in res.metadata.unsupported_chars

    def test_tilde_vowels(self, uc):
        res = uc.execute(TranslateTextRequestDTO("áéíóú"))
        assert res.success

    def test_math_expression(self, uc):
        res = uc.execute(TranslateTextRequestDTO("2+2=4"))
        assert res.success

    def test_to_dict_structure(self, uc):
        res = uc.execute(TranslateTextRequestDTO("ok", include_metadata=True))
        d = res.to_dict()
        assert all(k in d for k in ["success", "original_text", "braille_output", "error", "metadata"])
        assert "coverage_percentage" in d["metadata"]

    def test_use_case_with_port_stub_isolated(self):
        class StubBrailleDictionary(BrailleDictionaryPort):
            def __init__(self):
                self._table = {
                    "a": BrailleSymbol("a", BrailleCell((1,)), SymbolType.LETTER),
                    "b": BrailleSymbol("b", BrailleCell((1, 2)), SymbolType.LETTER),
                    "#": BrailleSymbol("#", BrailleCell((3, 4, 5, 6)), SymbolType.PREFIX),
                }

            def get_symbol_for_text(self, token: str):
                return self._table.get(token)

            def get_symbol_sequence_for_text(self, token: str):
                symbol = self.get_symbol_for_text(token)
                return [symbol] if symbol else None

            def contains(self, token: str) -> bool:
                return token in self._table

        uc_stub = TranslateTextToBrailleUseCase(dictionary=StubBrailleDictionary())
        res = uc_stub.execute(TranslateTextRequestDTO("abx", include_metadata=True))

        assert res.braille_output == "⠁⠃"
        assert res.metadata is not None
        assert "x" in res.metadata.unsupported_chars