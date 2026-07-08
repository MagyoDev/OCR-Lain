from pathlib import Path

from PIL import Image

from ocr_lain.config import OCRConfig
from ocr_lain.extractors.base import BaseExtractor
from ocr_lain.models import ExtractedBlock, ExtractResult
from ocr_lain.ocr_engine import OCREngine


class ImageExtractor(BaseExtractor):
    """
    Formatos esperados:
    - png
    - jpg
    - jpeg
    - webp
    - bmp
    - tiff
    """

    def __init__(self, config: OCRConfig):
        self.config = config
        self.ocr_engine = OCREngine(config)

    def extract(self, file_path: Path) -> ExtractResult:
        """
        Abre a imagem, aplica OCR e retorna o resultado.
        """

        blocks: list[ExtractedBlock] = []
        errors: list[str] = []

        try:
            image = Image.open(file_path)

            text = self.ocr_engine.image_to_text(image)

            if text:
                block = ExtractedBlock(
                    source_file=str(file_path),
                    source_type="image",
                    location="image",
                    method="ocr_image",
                    text=text,
                    metadata={
                        "format": image.format,
                        "width": image.width,
                        "height": image.height,
                    },
                )

                blocks.append(block)

        except Exception as error:
            errors.append(f"Erro ao processar imagem {file_path}: {error}")

        return ExtractResult(
            file_path=file_path,
            blocks=blocks,
            errors=errors,
        )