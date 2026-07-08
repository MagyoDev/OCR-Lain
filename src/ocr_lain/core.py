from pathlib import Path

from ocr_lain.config import OCRConfig
from ocr_lain.models import ExtractResult
from ocr_lain.router import SUPPORTED_EXTENSIONS, get_extractor


def collect_files(input_path: Path) -> list[Path]:

    if input_path.is_file():
        return [input_path]

    if input_path.is_dir():
        files: list[Path] = []

        for file_path in input_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(file_path)

        return files

    raise FileNotFoundError(f"Caminho não encontrado: {input_path}")


def extract_file(file_path: Path, config: OCRConfig) -> ExtractResult:

    extractor = get_extractor(file_path, config)
    return extractor.extract(file_path)


def extract_many(input_path: Path, config: OCRConfig) -> list[ExtractResult]:

    files = collect_files(input_path)

    results: list[ExtractResult] = []

    for file_path in files:
        result = extract_file(file_path, config)
        results.append(result)

    return results