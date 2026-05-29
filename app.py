from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.application.dtos import TranslateTextRequestDTO
from backend.application.use_cases import TranslateTextToBrailleUseCase
from backend.infrastructure.spanish_braille_dictionary import SpanishBrailleDictionary

app = Flask(__name__)
CORS(app)

# Composition root: concrete infrastructure injected into application use case.
dictionary = SpanishBrailleDictionary()
translate_use_case = TranslateTextToBrailleUseCase(dictionary=dictionary)


@app.post("/api/traducir")
def traducir():
    data = request.get_json(silent=True) or {}
    texto = data.get("texto", "")

    if not isinstance(texto, str):
        return jsonify({"ok": False, "error": "El campo 'texto' debe ser string."}), 400

    dto = TranslateTextRequestDTO(text=texto, include_metadata=True)
    result = translate_use_case.execute(dto)

    response_body = {
        "ok": result.success,
        "texto": result.original_text,
        "braille": result.braille_output,
        "error": result.error,
        "metadata": result.metadata.__dict__ if result.metadata else None,
    }

    return jsonify(response_body), 200 if result.success else 422


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
