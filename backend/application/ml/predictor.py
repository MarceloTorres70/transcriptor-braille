"""
Motor de inferencia Braille (YOLOv8).
Adaptado desde DotNeuralNet/src/inference.py para uso vía API Flask.
"""

from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import Optional, Union

import PIL.Image
from ultralytics import YOLO

from backend.application.ml.convert import convert_to_braille_unicode, parse_xywh_and_class

_ML_DIR = Path(__file__).resolve().parent
_DEFAULT_WEIGHTS = _ML_DIR / "yolov8_braille.pt"
_DEFAULT_MAP = _ML_DIR / "braille_map.json"
_DEFAULT_CONF = 0.15


class BraillePredictor:
    """Singleton que carga los pesos YOLOv8 una sola vez en memoria."""

    _instance: Optional["BraillePredictor"] = None

    def __init__(
        self,
        weights_path: Union[str, Path] = _DEFAULT_WEIGHTS,
        map_path: Union[str, Path] = _DEFAULT_MAP,
        conf: float = _DEFAULT_CONF,
    ) -> None:
        self.weights_path = Path(weights_path)
        self.map_path = Path(map_path)
        self.conf = conf

        if not self.weights_path.is_file():
            raise FileNotFoundError(f"Pesos YOLO no encontrados: {self.weights_path}")
        if not self.map_path.is_file():
            raise FileNotFoundError(f"Mapa Braille no encontrado: {self.map_path}")

        self.model = YOLO(str(self.weights_path))

    @classmethod
    def get_instance(
        cls,
        weights_path: Union[str, Path] = _DEFAULT_WEIGHTS,
        map_path: Union[str, Path] = _DEFAULT_MAP,
        conf: float = _DEFAULT_CONF,
    ) -> "BraillePredictor":
        if cls._instance is None:
            cls._instance = cls(
                weights_path=weights_path,
                map_path=map_path,
                conf=conf,
            )
        return cls._instance

    @staticmethod
    def image_from_base64(imagen: str) -> PIL.Image.Image:
        """Decodifica un string Base64 (con o sin prefijo data-URI) a PIL.Image."""
        payload = imagen.split(",", 1)[1] if "," in imagen else imagen
        raw = base64.b64decode(payload)
        image = PIL.Image.open(io.BytesIO(raw))
        return image.convert("RGB")

    def predict(self, image: PIL.Image.Image) -> str:
        """Ejecuta inferencia YOLOv8 y retorna texto Braille Unicode."""
        results = self.model.predict(
            image,
            conf=self.conf,
            verbose=False,
        )
        boxes = results[0].boxes
        if boxes is None or len(boxes) == 0:
            return ""

        list_boxes = parse_xywh_and_class(boxes)
        lines: list[str] = []
        for box_line in list_boxes:
            chars = ""
            for each_class in box_line[:, -1]:
                class_name = self.model.names[int(each_class)]
                chars += convert_to_braille_unicode(
                    class_name, path=str(self.map_path)
                )
            lines.append(chars)
        return "\n".join(lines)
