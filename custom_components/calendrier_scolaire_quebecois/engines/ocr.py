"""Moteur OCR pour l'extraction de texte à partir d'images et de PDF."""
from __future__ import annotations

import logging
from typing import Any, Dict, List

_LOGGER = logging.getLogger(__name__)


class OCREngine:
    """Extrait le texte des PDF et images en utilisant OCR."""

    def __init__(self, manager: Any) -> None:
        """Initialise le moteur OCR."""
        self.manager = manager
        self.tesseract_available = False
        self._check_tesseract()

    def _check_tesseract(self) -> None:
        """Vérifie si tesseract est disponible."""
        try:
            import pytesseract

            self.tesseract_available = True
            _LOGGER.debug("Tesseract OCR engine available")
        except ImportError:
            _LOGGER.warning("pytesseract not available, OCR features disabled")

    async def extract_from_pdf(
        self, pdf_data: bytes, source: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract text and events from PDF using OCR."""
        _LOGGER.debug("Extracting text from PDF using OCR: %s", source.get("name"))

        events = []

        if not self.tesseract_available:
            _LOGGER.warning("Tesseract not available, skipping OCR")
            return events

        try:
            from pdf2image import convert_from_bytes
            import pytesseract
            from PIL import Image

            # Convert PDF to images
            images = convert_from_bytes(pdf_data)

            # Extract text from each image
            full_text = ""
            for image in images:
                text = pytesseract.image_to_string(image, lang="fra+eng")
                full_text += text + "\n"

            # Extract events from the combined text
            if hasattr(self.manager, "parser_engine"):
                events = await self.manager.parser_engine._extract_events_from_text(
                    full_text, source
                )

        except ImportError as err:
            _LOGGER.warning("Missing dependencies for OCR: %s", err)
        except Exception as err:
            _LOGGER.error("Error extracting from PDF with OCR: %s", err)

        return events

    async def extract_from_image(
        self, image_data: bytes, source: Dict[str, Any]
    ) -> str:
        """Extract text from an image using OCR."""
        _LOGGER.debug("Extracting text from image using OCR")

        if not self.tesseract_available:
            _LOGGER.warning("Tesseract not available")
            return ""

        try:
            import pytesseract
            from PIL import Image
            import io

            # Load image
            image = Image.open(io.BytesIO(image_data))

            # Extract text
            text = pytesseract.image_to_string(image, lang="fra+eng")
            return text

        except Exception as err:
            _LOGGER.error("Error extracting text from image: %s", err)
            return ""

    async def preprocess_image(self, image_data: bytes) -> bytes:
        """Preprocess image to improve OCR accuracy."""
        try:
            from PIL import Image, ImageEnhance, ImageFilter
            import io

            image = Image.open(io.BytesIO(image_data))

            # Convert to grayscale
            image = image.convert("L")

            # Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2)

            # Apply threshold
            image = image.point(lambda x: 0 if x < 128 else 255, "1")

            # Save to bytes
            output = io.BytesIO()
            image.save(output, format="PNG")
            return output.getvalue()

        except Exception as err:
            _LOGGER.error("Error preprocessing image: %s", err)
            return image_data
