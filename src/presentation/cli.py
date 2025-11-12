"""CLI interface for font conversion using Typer."""

from pathlib import Path
from typing import Optional

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
    input_file: Path = typer.Argument(
        ..., help="Path to input font file (TTF, OTF, WOFF, or WOFF2)", exists=True
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help=(
            "Optional output file format (ttf, otf, woff, woff2). "
            "When omitted the CLI defaults to woff2."
        ),
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Optional output file path or directory. If a directory is provided, "
            "the converted file will be written inside it. If omitted, the output "
            "is written next to the input file."
        ),
    ),
) -> None:
    """Convert INPUT_FILE to another font format.

    Example:
      convert test.ttf --format woff2 --output out_dir/
    """

    # Determine target format (default to woff2 when not provided)
    if format is None:
        typer.secho(
            "ℹ️  No --format provided, defaulting to woff2.",
            fg=typer.colors.YELLOW,
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

    # Input path is already a Path (typer validated exists)
    input_path = input_file

    # Resolve output path according to semantics:
    # - If --output omitted: place next to input, using input stem + target ext
    # - If --output provided and points to a directory (exists/is dir or has no suffix):
    #     place output inside that directory
    # - If --output provided and looks like a file: ensure extension matches
    if output is None:
        parent = input_path.parent
        output_path = parent / f"{input_path.stem}.{target_format.value}"
    else:
        output_path_candidate = Path(output)

        # If the path exists and is a directory -> use it
        if output_path_candidate.exists() and output_path_candidate.is_dir():
            output_path_candidate.mkdir(parents=True, exist_ok=True)
            filename = f"{input_path.stem}.{target_format.value}"
            output_path = output_path_candidate / filename
            typer.secho(
                f"ℹ️  Using directory as output: {output_path_candidate}",
                fg=typer.colors.BLUE,
            )
        else:
            # If the provided path has no suffix, treat it as a directory
            if output_path_candidate.suffix == "":
                output_path_candidate.mkdir(parents=True, exist_ok=True)
                filename = f"{input_path.stem}.{target_format.value}"
                output_path = output_path_candidate / filename
                typer.secho(
                    f"ℹ️  Using directory as output: {output_path_candidate}",
                    fg=typer.colors.BLUE,
                )
            else:
                # Treat as file path; ensure extension matches target
                desired_suffix = f".{target_format.value}"
                if output_path_candidate.suffix.lower() != desired_suffix:
                    typer.secho(
                        "⚠️  Output filename extension does not match the\n"
                        "target format; adjusting it to match.",
                        fg=typer.colors.YELLOW,
                    )
                    output_path = output_path_candidate.with_suffix(desired_suffix)
                else:
                    output_path = output_path_candidate

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
