"""Adapter for font conversion using fonttools library"""

from pathlib import Path

from fontTools.ttLib import TTFont  # type: ignore

from domain.enums import FontFormat
from domain.ports import FontConverterPort


class FontToolsConverter(FontConverterPort):
    """Implementation of FontConverterPort using fonttools library"""

    def convert(
        self,
        input_path: Path,
        output_path: Path,
        target_format: FontFormat,
    ) -> None:
        """
        Convert font to target format using fonttools

        Args:
            input_path: Path to source font file
            output_path: Path to destination font file
            target_format: Target format (WOFF, WOFF2, TTF, OTF)

        Raises:
            FileNotFoundError: If input file does not exist
            ValueError: If format is not supported
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Font file not found: {input_path}")

        try:
            # Load the font
            font = TTFont(str(input_path))

            # Convert based on target format
            if target_format == FontFormat.WOFF:
                font.flavor = "woff"
            elif target_format == FontFormat.WOFF2:
                font.flavor = "woff2"
            elif target_format == FontFormat.TTF:
                font.flavor = None
            elif target_format == FontFormat.OTF:
                font.flavor = None
            else:
                raise ValueError(f"Unsupported format: {target_format.value}")

            # Save to file (TTFont.save() handles file opening)
            font.save(str(output_path))  # type: ignore

        except Exception:
            # Clean up output file if it was created
            if output_path.exists():
                output_path.unlink()
            raise
