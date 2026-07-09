from io import BytesIO
from pathlib import Path

import fitz
from PIL import Image

from ocr_lain.config import OCRConfig
from ocr_lain.extractors.base import BaseExtractor
from ocr_lain.models import ExtractedBlock, ExtractResult
from ocr_lain.ocr_engine import OCREngine


class PDFExtractor(BaseExtractor):

    def __init__(self, config: OCRConfig):
        self.config = config
        self.ocr_engine = OCREngine(config)

    def extract(self, file_path: Path) -> ExtractResult:

        blocks: list[ExtractedBlock] = []
        errors: list[str] = []

        try:
            document = fitz.open(file_path)

            for page_index, page in enumerate(document, start=1):
                native_text = self._extract_native_text(page)

                if native_text:
                    blocks.append(
                        ExtractedBlock(
                            source_file=str(file_path),
                            source_type="pdf",
                            location=f"page:{page_index}",
                            method="native_text",
                            text=native_text,
                            metadata={
                                "page": page_index,
                            },
                        )
                    )

                should_apply_ocr = (
                    self.config.ocr_pdf_pages
                    and len(native_text.strip()) < self.config.min_native_chars
                )

                if should_apply_ocr:
                    try:
                        image = self._render_page_to_image(page)
                        ocr_text = self.ocr_engine.image_to_text(image)

                        if ocr_text:
                            blocks.append(
                                ExtractedBlock(
                                    source_file=str(file_path),
                                    source_type="pdf",
                                    location=f"page:{page_index}",
                                    method="ocr_pdf_page",
                                    text=ocr_text,
                                    metadata={
                                        "page": page_index,
                                        "dpi": self.config.dpi,
                                    },
                                )
                            )

                    except Exception as error:
                        errors.append(
                            f"Erro ao aplicar OCR na página {page_index} de {file_path}: {error}"
                        )

            document.close()

        except Exception as error:
            errors.append(f"Erro ao processar PDF {file_path}: {error}")

        return ExtractResult(
            file_path=file_path,
            blocks=blocks,
            errors=errors,
        )

    def _extract_native_text(self, page) -> str:

        text = page.get_text("text")
        return text.strip()

    def _render_page_to_image(self, page) -> Image.Image:

        zoom = self.config.dpi / 72
        matrix = fitz.Matrix(zoom, zoom)

        pixmap = page.get_pixmap(matrix=matrix, alpha=False)

        image_bytes = pixmap.tobytes("png")
        image = Image.open(BytesIO(image_bytes))

        return image.copy()