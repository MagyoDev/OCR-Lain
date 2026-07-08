import pytesseract
from PIL import Image

from ocr_lain.config import OCRConfig
from ocr_lain.preprocess import preprocess_image


class OCREngine:

    def __init__(self, config: OCRConfig):
        self.config = config

    def image_to_text(self, image: Image.Image) -> str:

        prepared_image = preprocess_image(image)

        text = pytesseract.image_to_string(
            prepared_image,
            lang=self.config.language,
            config=self.config.tesseract_config,
        )

        return text.strip()