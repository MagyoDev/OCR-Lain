from dataclasses import dataclass


@dataclass
class OCRConfig:
 
    language: str = "por+eng"
    tesseract_config: str = "--psm 6"

    # PDF settings
    dpi: int = 200
    min_native_chars: int = 30
    ocr_pdf_pages: bool = True

    ocr_embedded_images: bool = True