from pathlib import Path

from ocr_lain.models import ExtractResult


class BaseExtractor:

    def extract(self, file_path: Path) -> ExtractResult:
        raise NotImplementedError("Método extract().")