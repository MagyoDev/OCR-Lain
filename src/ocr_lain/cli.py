from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ocr_lain.config import OCRConfig
from ocr_lain.core import extract_many
from ocr_lain.outputs import save_markdown
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
):

    config = OCRConfig(language=lang)

    console.print("[bold cyan]OCR-Lain iniciado[/bold cyan]")
    console.print(f"Entrada: [bold]{input_path}[/bold]")
    console.print(f"Saída: [bold]{output_dir}[/bold]")
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
    table.add_column("Saída")

    for result in results:
        output_file = save_markdown(result, output_dir)

        table.add_row(
            result.file_path.name,
            str(len(result.blocks)),
            str(len(result.errors)),
            str(output_file),
        )

    console.print(table)

    console.print("")
    console.print("[bold green]Processamento finalizado.[/bold green]")


@app.command()
def formats():
    """
    Lista os formatos suportados.
    """

    console.print("[bold cyan]Formatos suportados nesta versão:[/bold cyan]")

    for extension in sorted(SUPPORTED_EXTENSIONS):
        console.print(f"- {extension}")


if __name__ == "__main__":
    app()