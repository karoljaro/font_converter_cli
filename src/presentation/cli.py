"""CLI interface for font conversion using Typer."""

from pathlib import Path
from typing import Optional

import typer
from dependency_injector.wiring import inject, Provide

from bootstrap import Container
from application.use_cases.convert_font_use_case import ConvertFontUseCase
from application.dto.convert_font_request import ConvertFontRequest
from domain.enums.font_format import FontFormat
from .exception_handlers import handle_exceptions

app = typer.Typer(
    help="Font conversion tool supporting TTF, OTF, WOFF, and WOFF2 formats."
)


@app.command(name="convert")
@handle_exceptions
def convert_font(
    input_file: Path = typer.Argument(
        ...,
        help="Path to input font file (TTF, OTF, WOFF, or WOFF2)",
        exists=True,
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help=(
            "Optional output file format (ttf, otf, woff, woff2). " "Defaults to woff2."
        ),
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Optional output file path or directory. "
            "Defaults to same directory as input."
        ),
    ),
) -> None:
    """Convert INPUT_FILE to another font format."""
    _convert_font_impl(input_file, format, output)


@inject
def _convert_font_impl(
    input_file: Path,
    format: Optional[str],
    output: Optional[str],
    use_case: ConvertFontUseCase = Provide[Container.convert_use_case],
) -> None:
    """Implementation function with dependency injection."""

    # Determine target format (default to woff2 when not provided)
    if format is None:
        typer.secho(
            "ℹ️  No --format provided, defaulting to woff2.", fg=typer.colors.YELLOW
        )
        target_format = FontFormat.WOFF2
    else:
        try:
            target_format = FontFormat(format.lower())
        except ValueError:
            typer.secho(f"❌ Invalid format: {format}", fg=typer.colors.RED, err=True)
            typer.secho(
                "Valid formats are: ttf, otf, woff, woff2",
                fg=typer.colors.YELLOW,
                err=True,
            )
            raise typer.Exit(code=1)

    input_path = input_file

    # Determine output path
    if output is None:
        output_path = input_path.with_suffix(f".{target_format.value}")
    else:
        output_path_candidate = Path(output)
        if output_path_candidate.exists() and output_path_candidate.is_dir():
            output_path = (
                output_path_candidate / f"{input_path.stem}.{target_format.value}"
            )
        elif output_path_candidate.suffix == "":
            output_path_candidate.mkdir(parents=True, exist_ok=True)
            output_path = (
                output_path_candidate / f"{input_path.stem}.{target_format.value}"
            )
        else:
            desired_suffix = f".{target_format.value}"
            if output_path_candidate.suffix.lower() != desired_suffix:
                typer.secho(
                    "⚠️  Adjusting output filename to match target format "
                    f"({desired_suffix}).",
                    fg=typer.colors.YELLOW,
                )
                output_path = output_path_candidate.with_suffix(desired_suffix)
            else:
                output_path = output_path_candidate

    typer.secho(
        f"🔄 Converting {input_path.name} → {target_format.value}...",
        fg=typer.colors.BLUE,
    )

    request = ConvertFontRequest(
        input_file_path=input_path,
        target_format=target_format,
        output_file_path=output_path,
    )

    result = use_case.execute(request)

    typer.secho("✅ Font converted successfully!", fg=typer.colors.GREEN)
    typer.secho(f"📁 Output file: {result.output_file_path}", fg=typer.colors.GREEN)


@app.callback()
def main_callback() -> None:
    """Font Converter CLI - Convert fonts between TTF, OTF, WOFF, and WOFF2 formats."""
    pass
