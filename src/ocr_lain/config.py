from dataclasses import dataclass


@dataclass
class OCRConfig:

    language: str = "por+eng"
    tesseract_config: str = "--psm 6"