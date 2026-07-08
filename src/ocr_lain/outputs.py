from pathlib import Path

from ocr_lain.models import ExtractResult


def save_markdown(result: ExtractResult, output_dir: Path) -> Path:

    output_dir.mkdir(parents=True, exist_ok=True)

    original_name = result.file_path.name
    output_file = output_dir / f"{original_name}.ocr.md"

    lines: list[str] = []

    lines.append(f"# OCR-Lain — Resultado de `{original_name}`")
    lines.append("")
    lines.append(f"**Arquivo original:** `{result.file_path}`")
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