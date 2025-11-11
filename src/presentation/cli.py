"""CLI interface for font conversion using Typer."""

from pathlib import Path

import typer
from infrastructure.adapters.file_service import FileService
from infrastructure.adapters.fonttools_converter import FontToolsConverter
from application.use_cases.convert_font_use_case import ConvertFontUseCase
from application.dto.convert_font_request import ConvertFontRequest
from domain.enums.font_format import FontFormat
from .exception_handlers import handle_exceptions

app = typer.Typer(
    help="Font conversion tool supporting TTF, OTF, WOFF, and WOFF2 formats."
)

# Initialize infrastructure and application layers
_file_service = FileService()
_converter = FontToolsConverter()
_use_case = ConvertFontUseCase(
    converter=_converter,
    file_service=_file_service,
)


@app.command(name="convert")
@handle_exceptions
def convert_font(
    input_file: str = typer.Argument(
        ...,
        help="Path to input font file (TTF, OTF, WOFF, or WOFF2)",
        exists=True,
    ),
    output_format: str = typer.Argument(
        ...,
        help="Target font format (TTF, OTF, WOFF, or WOFF2)",
        exists=True
    ),
    output_file: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Optional output file path. If not specified, "
            "will be generated in the same directory."
        ),
    ),
) -> None:
    try:
        target_format = FontFormat(output_format.lower())
    except ValueError:
        typer.secho(
            f"❌ Invalid output format: {output_format}",
            fg=typer.colors.RED,
            err=True,
        )
        typer.secho(
            "Valid formats are: TTF, OTF, WOFF, WOFF2",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(code=1)

    # Prepare input and output paths
    input_path = Path(input_file)
    # If user provided output path, use it; otherwise let the use case auto-generate
    output_path = Path(output_file) if output_file else None

    typer.secho(
        f"🔄 Converting {input_path.name} to {target_format.value}...",
        fg=typer.colors.BLUE,
    )

    # Create request and execute conversion using use case
    request = ConvertFontRequest(
        input_file_path=input_path,
        target_format=target_format,
        output_file_path=output_path,
    )
    result = _use_case.execute(request)

    # Display success message
    typer.secho("✅ Font converted successfully!", fg=typer.colors.GREEN)
    typer.secho(f"📁 Output file: {result.output_file_path}", fg=typer.colors.GREEN)


@app.callback()
def main_callback() -> None:
    """Font Converter CLI - Convert fonts between TTF, OTF, WOFF, and WOFF2 formats."""
    pass
