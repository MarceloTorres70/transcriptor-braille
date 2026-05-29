"""
Data Transfer Objects (DTOs).
Capa: Application

Contratos de entrada/salida que coinciden con el JSON que espera el Frontend.
Sin lógica de negocio; solo estructura y validación de borde.
"""

from dataclasses import dataclass, field


@dataclass
class TranslateTextRequestDTO:
    """
    POST /api/translate
    { "text": "Hola 123", "include_metadata": true }
    """
    text: str
    include_metadata: bool = False

    def is_valid(self) -> tuple[bool, str]:
        if not self.text or not self.text.strip():
            return False, "El texto no puede estar vacío."
        if len(self.text) > 5000:
            return False, "El texto no puede superar los 5000 caracteres."
        return True, ""


@dataclass
class TranslationMetadataDTO:
    total_chars: int
    translated_chars: int
    unsupported_chars: list[str] = field(default_factory=list)

    @property
    def coverage_percentage(self) -> float:
        if self.total_chars == 0:
            return 0.0
        return round((self.translated_chars / self.total_chars) * 100, 2)


from typing import Optional


@dataclass
class TranslateTextResponseDTO:
    """
    Respuesta de POST /api/translate
    {
        "success": true,
        "original_text": "Hola 123",
        "braille_output": "...",
        "metadata": { ... },
        "error": null
    }
    """
    success: bool
    original_text: str
    braille_output: str
    metadata: Optional[TranslationMetadataDTO] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        result = {
            "success": self.success,
            "original_text": self.original_text,
            "braille_output": self.braille_output,
            "error": self.error,
        }
        if self.metadata:
            result["metadata"] = {
                "total_chars": self.metadata.total_chars,
                "translated_chars": self.metadata.translated_chars,
                "unsupported_chars": self.metadata.unsupported_chars,
                "coverage_percentage": self.metadata.coverage_percentage,
            }
        return result


@dataclass
class ErrorResponseDTO:
    error: str
    code: str
    success: bool = False

    def to_dict(self) -> dict:
        return {"success": self.success, "error": self.error, "code": self.code}