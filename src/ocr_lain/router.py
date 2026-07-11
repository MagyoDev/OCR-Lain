from pathlib import Path

from ocr_lain.config import OCRConfig
from ocr_lain.extractors.docx_extractor import DOCXExtractor
from ocr_lain.extractors.image_extractor import ImageExtractor
from ocr_lain.extractors.pdf_extractor import PDFExtractor
from ocr_lain.extractors.pptx_extractor import PPTXExtractor


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

SUPPORTED_DOCX_EXTENSIONS = {
    ".docx",
}

SUPPORTED_PPTX_EXTENSIONS = {
    ".pptx",
}

SUPPORTED_EXTENSIONS = (
    SUPPORTED_IMAGE_EXTENSIONS
    | SUPPORTED_PDF_EXTENSIONS
    | SUPPORTED_DOCX_EXTENSIONS
    | SUPPORTED_PPTX_EXTENSIONS
)


def get_extractor(file_path: Path, config: OCRConfig):

    extension = file_path.suffix.lower()

    if extension in SUPPORTED_IMAGE_EXTENSIONS:
        return ImageExtractor(config)

    if extension in SUPPORTED_PDF_EXTENSIONS:
        return PDFExtractor(config)

    if extension in SUPPORTED_DOCX_EXTENSIONS:
        return DOCXExtractor(config)

    if extension in SUPPORTED_PPTX_EXTENSIONS:
        return PPTXExtractor(config)

    raise ValueError(f"Formato não suportado ainda: {extension}")