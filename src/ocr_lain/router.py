from pathlib import Path

from ocr_lain.config import OCRConfig
from ocr_lain.extractors.image_extractor import ImageExtractor


SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
}


SUPPORTED_EXTENSIONS = SUPPORTED_IMAGE_EXTENSIONS


def get_extractor(file_path: Path, config: OCRConfig):

    extension = file_path.suffix.lower()

    if extension in SUPPORTED_IMAGE_EXTENSIONS:
        return ImageExtractor(config)

    raise ValueError(f"Formato não suportado ainda: {extension}")