from pathlib import Path

from ocr_lain.config import OCRConfig
from ocr_lain.extractors.image_extractor import ImageExtractor
from ocr_lain.extractors.pdf_extractor import PDFExtractor


SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
}

SUPPORTED_PDF_EXTENSIONS = {
    ".pdf",
}

SUPPORTED_EXTENSIONS = SUPPORTED_IMAGE_EXTENSIONS | SUPPORTED_PDF_EXTENSIONS


def get_extractor(file_path: Path, config: OCRConfig):

    extension = file_path.suffix.lower()

    if extension in SUPPORTED_IMAGE_EXTENSIONS:
        return ImageExtractor(config)

    if extension in SUPPORTED_PDF_EXTENSIONS:
        return PDFExtractor(config)

    raise ValueError(f"Formato não suportado ainda: {extension}")