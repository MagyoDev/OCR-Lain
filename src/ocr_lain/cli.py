from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ocr_lain.config import OCRConfig
from ocr_lain.core import extract_many
from ocr_lain.outputs import save_json, save_markdown
from ocr_lain.router import SUPPORTED_EXTENSIONS

app = typer.Typer(
    name="ocr-lain",
    help="OCR-Lain: extraia texto de imagens e documentos usando OCR.",
)

console = Console()


@app.command()
def run(
    input_path: Path = typer.Argument(
        ...,
        help="Arquivo ou pasta que será processado.",
    ),
    output_dir: Path = typer.Option(
        Path("outputs"),
        "--output",
        "-o",
        help="Pasta onde os resultados serão salvos.",
    ),
    lang: str = typer.Option(
        "por+eng",
        "--lang",
        help="Idioma do OCR. Exemplo: por, eng ou por+eng.",
    ),
    no_pdf_ocr: bool = typer.Option(
        False,
        "--no-pdf-ocr",
        help="Desativa OCR em páginas de PDF escaneadas.",
    ),
    no_embedded_images: bool = typer.Option(
        False,
        "--no-embedded-images",
        help="Desativa OCR em imagens internas de documentos.",
    ),
    dpi: int = typer.Option(
        200,
        "--dpi",
        help="Qualidade usada ao transformar páginas de PDF em imagem.",
    ),
    export_json: bool = typer.Option(
        False,
        "--json",
        help="Também salva o resultado em JSON.",
    ),
):

    config = OCRConfig(
        language=lang,
        dpi=dpi,
        ocr_pdf_pages=not no_pdf_ocr,
        ocr_embedded_images=not no_embedded_images,
    )

    console.print("[bold cyan]OCR-Lain iniciado[/bold cyan]")
    console.print(f"Entrada: [bold]{input_path}[/bold]")
    console.print(f"Saída: [bold]{output_dir}[/bold]")
    console.print(f"Idioma: [bold]{lang}[/bold]")
    console.print(f"DPI: [bold]{dpi}[/bold]")
    console.print(f"OCR em PDF: [bold]{not no_pdf_ocr}[/bold]")
    console.print(f"OCR em imagens internas: [bold]{not no_embedded_images}[/bold]")
    console.print(f"Exportar JSON: [bold]{export_json}[/bold]")
    console.print("")

    try:
        results = extract_many(input_path, config)

    except Exception as error:
        console.print(f"[bold red]Erro:[/bold red] {error}")
        raise typer.Exit(code=1)

    table = Table(title="Resultados do OCR-Lain")
    table.add_column("Arquivo")
    table.add_column("Blocos")
    table.add_column("Erros")
    table.add_column("Markdown")
    table.add_column("JSON")

    for result in results:
        markdown_file = save_markdown(result, output_dir)

        json_file_text = "Não gerado"

        if export_json:
            json_file = save_json(result, output_dir)
            json_file_text = str(json_file)

        table.add_row(
            result.file_path.name,
            str(len(result.blocks)),
            str(len(result.errors)),
            str(markdown_file),
            json_file_text,
        )

    console.print(table)

    console.print("")
    console.print("[bold green]Processamento finalizado.[/bold green]")


@app.command()
def formats():

    console.print("[bold cyan]Formatos suportados nesta versão:[/bold cyan]")

    for extension in sorted(SUPPORTED_EXTENSIONS):
        console.print(f"- {extension}")


if __name__ == "__main__":
    app()