"""Port (abstraction) for font conversion"""

from abc import ABC, abstractmethod
from pathlib import Path

from domain.enums import FontFormat


class FontConverterPort(ABC):
    """Interface for converting fonts to various formats"""

    @abstractmethod
    def convert(
        self,
        input_path: Path,
        output_path: Path,
        target_format: FontFormat,
    ) -> None:
        """
        Converts a font from input_path to target_format and saves to output_path

        Args:
            input_path: Path to the source font file
            output_path: Path to the destination font file
            target_format: Target format (WOFF, WOFF2, TTF, OTF)

        Raises:
            FileNotFoundError: If input file does not exist
            ValueError: If format is not supported
        """
        pass
