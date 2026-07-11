import json
from pathlib import Path
from typing import Any

from ocr_lain.models import ExtractedBlock, ExtractResult


def block_to_dict(block: ExtractedBlock) -> dict[str, Any]:

    return {
        "source_file": block.source_file,
        "source_type": block.source_type,
        "location": block.location,
        "method": block.method,
        "text": block.text,
        "metadata": block.metadata,
    }


def result_to_dict(result: ExtractResult) -> dict[str, Any]:

    return {
        "file_path": str(result.file_path),
        "file_name": result.file_path.name,
        "blocks_count": len(result.blocks),
        "errors_count": len(result.errors),
        "errors": result.errors,
        "full_text": result.full_text,
        "blocks": [
            block_to_dict(block)
            for block in result.blocks
        ],
    }


def save_json(result: ExtractResult, output_dir: Path) -> Path:

    output_dir.mkdir(parents=True, exist_ok=True)

    original_name = result.file_path.name
    output_file = output_dir / f"{original_name}.ocr.json"

    data = result_to_dict(result)

    output_file.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return output_file


def save_markdown(result: ExtractResult, output_dir: Path) -> Path:

    output_dir.mkdir(parents=True, exist_ok=True)

    original_name = result.file_path.name
    output_file = output_dir / f"{original_name}.ocr.md"

    lines: list[str] = []

    lines.append(f"# OCR-Lain — Resultado de `{original_name}`")
    lines.append("")
    lines.append(f"**Arquivo original:** `{result.file_path}`")
    lines.append("")
    lines.append(f"**Total de blocos extraídos:** `{len(result.blocks)}`")
    lines.append("")
    lines.append(f"**Total de erros:** `{len(result.errors)}`")
    lines.append("")
    lines.append("---")
    lines.append("")

    if result.errors:
        lines.append("## Erros")
        lines.append("")

        for error in result.errors:
            lines.append(f"- {error}")

        lines.append("")

    if not result.blocks:
        lines.append("## Resultado")
        lines.append("")
        lines.append("> Nenhum texto foi extraído.")
        lines.append("")

    for index, block in enumerate(result.blocks, start=1):
        lines.append(f"## Bloco {index}")
        lines.append("")
        lines.append(f"- **Tipo:** `{block.source_type}`")
        lines.append(f"- **Localização:** `{block.location}`")
        lines.append(f"- **Método:** `{block.method}`")
        lines.append("")
        lines.append("### Texto extraído")
        lines.append("")
        lines.append(block.text)
        lines.append("")
        lines.append("---")
        lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")

    return output_file