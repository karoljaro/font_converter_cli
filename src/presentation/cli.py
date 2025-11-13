"""Object-oriented CLI interface for font conversion using Typer.

This module exposes a class `FontConverterCLI` which encapsulates the Typer
application and depends on the use case. This makes it easier to construct the
CLI via dependency injection in `bootstrap.Container`.
"""

from pathlib import Path
from typing import Optional

import typer

from application.use_cases.convert_font_use_case import ConvertFontUseCase
from application.dto.convert_font_request import ConvertFontRequest
from application.dto.convert_font_result import ConvertFontResult
from domain.enums.font_format import FontFormat
from domain.ports import OutputPathResolverPort
from .exception_handlers import handle_exceptions


class FontConverterCLI:
    """Typer-based CLI wrapped in a class to enable constructor DI.

    The class exposes a `app` attribute (Typer instance) and a `run()` helper
    to start the CLI programmatically.
    """

    # ============================ CLI Initialization ============================

    def __init__(
        self,
        use_case: ConvertFontUseCase,
        output_path_resolver: OutputPathResolverPort,
    ) -> None:
        self.use_case = use_case
        self.output_path_resolver = output_path_resolver
        self.app = typer.Typer(
            help="Font conversion tool supporting TTF, OTF, WOFF, and WOFF2 formats."
        )

        # Register commands
        self.app.command(name="convert")(self._convert_command)
        self.app.callback()(self._main_callback)

    # ============================ CLI Commands ============================

    @handle_exceptions
    def _convert_command(
        self,
        input_file: Path = typer.Argument(
            ..., help="Path to input font file (TTF, OTF, WOFF, or WOFF2)", exists=True
        ),
        format: Optional[str] = typer.Option(
            None,
            "--format",
            "-f",
            help=(
                "Optional output file format (ttf, otf, woff, woff2)."
                "Defaults to woff2."
            ),
        ),
        output: Optional[str] = typer.Option(
            None,
            "--output",
            "-o",
            help=(
                "Optional output file path or directory."
                "Defaults to same directory as input."
            ),
        ),
    ) -> None:
        """Convert INPUT_FILE to another font format (orchestrator)."""
        input_path = input_file

        # Step 1: Parse and validate target format
        target_format = self.parse_target_format(format)

        # Step 2: Resolve output path
        output_path = self.resolve_output_path_with_warning(
            input_path, target_format, output
        )

        # Step 3: Execute conversion
        self.log_conversion_start(input_path, target_format)
        result = self.execute_conversion(input_path, target_format, output_path)

        # Step 4: Log success
        self.log_conversion_success(result)

    # ============================ Helper Methods ============================

    def parse_target_format(self, format_str: Optional[str]) -> FontFormat:
        """Parse and validate target font format.

        Defaults to WOFF2 if not provided.
        """
        if format_str is None:
            typer.secho(
                "ℹ️  No --format provided, defaulting to woff2.",
                fg=typer.colors.YELLOW,
            )
            return FontFormat.WOFF2

        try:
            return FontFormat(format_str.lower())
        except ValueError:
            typer.secho(
                f"❌ Invalid format: {format_str}", fg=typer.colors.RED, err=True
            )
            typer.secho(
                "Valid formats are: ttf, otf, woff, woff2",
                fg=typer.colors.YELLOW,
                err=True,
            )
            raise typer.Exit(code=1)

    def resolve_output_path_with_warning(
        self,
        input_path: Path,
        target_format: FontFormat,
        output: Optional[str],
    ) -> Path:
        """Resolve output path and warn if format adjustment is needed."""
        output_path = self.output_path_resolver.resolve(
            input_path, target_format, output
        )

        # Warn if user provided a file with wrong suffix
        if output is not None:
            output_candidate = Path(output)
            desired_suffix = f".{target_format.value}"
            if (
                output_candidate.suffix != ""
                and output_candidate.suffix.lower() != desired_suffix
            ):
                typer.secho(
                    "⚠️  Adjusting output filename to match target format "
                    f"({desired_suffix}).",
                    fg=typer.colors.YELLOW,
                )

        return output_path

    def log_conversion_start(self, input_path: Path, target_format: FontFormat) -> None:
        """Log conversion start."""
        typer.secho(
            f"🔄 Converting {input_path.name} → {target_format.value}...",
            fg=typer.colors.BLUE,
        )

    def execute_conversion(
        self,
        input_path: Path,
        target_format: FontFormat,
        output_path: Path,
    ) -> ConvertFontResult:
        """Execute font conversion via use case."""
        request = ConvertFontRequest(
            input_file_path=input_path,
            target_format=target_format,
            output_file_path=output_path,
        )
        return self.use_case.execute(request)

    def log_conversion_success(self, result: ConvertFontResult) -> None:
        """Log conversion success."""
        typer.secho("✅ Font converted successfully!", fg=typer.colors.GREEN)
        typer.secho(f"📁 Output file: {result.output_file_path}", fg=typer.colors.GREEN)

    def _main_callback(self) -> None:
        """Top-level callback for the CLI (currently a no-op)."""
        return None

    def run(self) -> None:
        """Run the Typer app (entry point)."""

        self.app()
