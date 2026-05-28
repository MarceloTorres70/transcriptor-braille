"""
Controlador API REST — Braille Transcriptor.
Capa: Adapters

Aquí ocurre el wiring completo de dependencias:
  SpanishBrailleDictionary (Infrastructure)
    └── BrailleDictionaryPort (Domain interface)
        └── TranslateTextToBrailleUseCase (Application)
            └── BrailleController (Adapters)
"""

from backend.application.dtos import TranslateTextRequestDTO, ErrorResponseDTO
from backend.application.use_cases import TranslateTextToBrailleUseCase, GetSupportedCharsUseCase
from backend.infrastructure.spanish_braille_dictionary import SpanishBrailleDictionary


def build_dependencies() -> dict:
    dictionary = SpanishBrailleDictionary()
    return {
        "translate": TranslateTextToBrailleUseCase(dictionary=dictionary),
        "supported_chars": GetSupportedCharsUseCase(dictionary=dictionary),
    }


class BrailleController:
    def __init__(self, deps: dict | None = None) -> None:
        if deps is None:
            deps = build_dependencies()
        self._translate_uc: TranslateTextToBrailleUseCase = deps["translate"]
        self._supported_uc: GetSupportedCharsUseCase = deps["supported_chars"]

    def translate(self, body: dict) -> tuple[dict, int]:
        """POST /api/translate"""
        text = body.get("text", "")
        if not isinstance(text, str):
            return ErrorResponseDTO("El campo 'text' debe ser string.", "INVALID_TYPE").to_dict(), 400

        dto = TranslateTextRequestDTO(text=text, include_metadata=body.get("include_metadata", False))
        response = self._translate_uc.execute(dto)
        return response.to_dict(), 200 if response.success else 422

    def get_supported_chars(self) -> tuple[dict, int]:
        """GET /api/supported-chars"""
        return self._supported_uc.execute(), 200
