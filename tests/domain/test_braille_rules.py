import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.infrastructure.spanish_braille_dictionary import SpanishBrailleDictionary
from backend.application.use_cases import TranslateTextToBrailleUseCase
from backend.application.dtos import TranslateTextRequestDTO

class TestBrailleRules:
    def test_numeric_prefix_for_0_to_9(self):
        dic = SpanishBrailleDictionary()
        uc = TranslateTextToBrailleUseCase(dic)
        res = uc.execute(TranslateTextRequestDTO("1"))
        assert res.braille_output.startswith("⠼")

    def test_uppercase_translation_fails_intentionally(self):
        # Alejo: Implementando el test que falla intencionalmente
        dic = SpanishBrailleDictionary()
        uc = TranslateTextToBrailleUseCase(dic)
        res = uc.execute(TranslateTextRequestDTO("B"))
        
        # El sistema real devuelve '⠨⠃', pero nosotros esperamos erróneamente '⠃'
        assert res.braille_output == "⠃", "FALLO INTENCIONAL: Se esperaba '⠃' (sin prefijo) pero el sistema usa prefijos"

