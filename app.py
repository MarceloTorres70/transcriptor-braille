from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from backend.application.dtos import TranslateTextRequestDTO
from backend.application.ml.predictor import BraillePredictor
from backend.application.use_cases import TranslateTextToBrailleUseCase
from backend.infrastructure.spanish_braille_dictionary import SpanishBrailleDictionary

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
CORS(app)

# Composition root: concrete infrastructure injected into application use case.
dictionary = SpanishBrailleDictionary()
translate_use_case = TranslateTextToBrailleUseCase(dictionary=dictionary)

# YOLOv8 Braille OCR — pesos cargados una sola vez al arrancar el servidor.
predictor = BraillePredictor.get_instance()


@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.post("/api/traducir")
def traducir():
    data = request.get_json(silent=True) or {}
    texto = data.get("texto", "")

    if not isinstance(texto, str):
        return jsonify({"ok": False, "error": "El campo 'texto' debe ser string."}), 400

    direction = data.get("direction", "es-br")
    dto = TranslateTextRequestDTO(text=texto, direction=direction, include_metadata=True)
    result = translate_use_case.execute(dto)

    response_body = {
        "ok": result.success,
        "texto": result.original_text,
        "braille": result.braille_output,
        "error": result.error,
        "metadata": result.metadata.__dict__ if result.metadata else None,
    }

    return jsonify(response_body), 200 if result.success else 422


@app.post("/api/ocr")
def ocr():
    data = request.get_json(silent=True) or {}
    imagen = data.get("imagen", "")

    if not isinstance(imagen, str) or not imagen:
        return jsonify({"ok": False, "error": "El campo 'imagen' debe ser un string Base64."}), 400

    try:
        image = BraillePredictor.image_from_base64(imagen)
        texto = predictor.predict(image)
        return jsonify({"ok": True, "texto": texto, "error": None}), 200
    except Exception as exc:
        return jsonify({"ok": False, "texto": "", "error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
