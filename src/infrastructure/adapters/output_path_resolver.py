"""Adapter for resolving output file paths."""

from pathlib import Path

from domain.enums import FontFormat
from domain.ports import OutputPathResolverPort


class OutputPathResolver(OutputPathResolverPort):
    """Resolves output paths for font conversion."""

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
        # Case 0: No output specified, use input directory with target format
        if output is None:
            return input_path.with_suffix(f".{target_format.value}")

        output_path_candidate = Path(output)

        # Case 1: Output points to existing directory
        if output_path_candidate.exists() and output_path_candidate.is_dir():
            return output_path_candidate / f"{input_path.stem}.{target_format.value}"

        # Case 2: Output is a path without suffix (treat as directory to create)
        if output_path_candidate.suffix == "":
            output_path_candidate.mkdir(parents=True, exist_ok=True)
            return output_path_candidate / f"{input_path.stem}.{target_format.value}"

        # Case 3: Output is a file path
        desired_suffix = f".{target_format.value}"
        if output_path_candidate.suffix.lower() != desired_suffix:
            # User provided wrong suffix, adjust it to match target format
            return output_path_candidate.with_suffix(desired_suffix)

        return output_path_candidate
