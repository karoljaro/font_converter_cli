"""Port for resolving output file paths."""

from abc import ABC, abstractmethod
from pathlib import Path

from domain.enums import FontFormat


class OutputPathResolverPort(ABC):
    """Interface for resolving output paths for font conversion."""

    @abstractmethod
    def resolve(
        self,
        input_path: Path,
        target_format: FontFormat,
        output: str | None = None,
    ) -> Path:
        """
        Resolve the output file path based on input, format, and user preference.

        Args:
            input_path: Path to the input font file.
            target_format: Target font format.
            output: Optional user-provided output path or directory.

        Returns:
            Resolved output file path.
        """
