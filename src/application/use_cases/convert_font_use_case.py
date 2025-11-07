"""Use case for converting fonts"""

from pathlib import Path

from application.dto import ConvertFontRequest, ConvertFontResult
from domain.entities import Font
from domain.enums import FontFormat
from domain.ports import FileServicePort, FontConverterPort


class ConvertFontUseCase:
    """Use case for converting fonts to different formats"""

    def __init__(
        self,
        converter: FontConverterPort,
        file_service: FileServicePort,
    ) -> None:
        self.converter = converter
        self.file_service = file_service

    def execute(self, request: ConvertFontRequest) -> ConvertFontResult:
        """
        Execute font conversion

        Args:
            request: Conversion request with input file, target format, etc.

        Returns:
            ConvertFontResult with output file path and success status

        Raises:
            FileNotFoundError: If input file does not exist
            ValueError: If target format conversion is not allowed
        """
        # 1. Validate input file exists
        if not self.file_service.file_exists(request.input_file_path):
            raise FileNotFoundError(f"Input file not found: {request.input_file_path}")

        # 2. Determine output file path
        output_path = self._determine_output_path(request)

        # 3. Create Font entity and validate conversion is possible
        font = Font(original_format=self._detect_font_format(request.input_file_path))
        if not font.can_convert_to(request.target_format):
            raise ValueError(
                f"Cannot convert from {font.original_format.value} to "
                f"{request.target_format.value}"
            )

        # 4. Perform conversion
        try:
            self.converter.convert(
                request.input_file_path,
                output_path,
                request.target_format,
            )
        except Exception:
            # Cleanup on failure
            if self.file_service.file_exists(output_path):
                self.file_service.delete_file(output_path)
            raise

        # 5. Return result
        return ConvertFontResult(
            output_file_path=output_path,
            target_format=request.target_format,
            success=True,
        )

    def _determine_output_path(self, request: ConvertFontRequest) -> Path:
        """Determine output file path"""
        if request.output_file_path:
            return request.output_file_path

        parent_dir = self.file_service.get_parent_directory(request.input_file_path)
        file_name = self.file_service.get_file_name_without_extension(
            request.input_file_path
        )
        return parent_dir / f"{file_name}.{request.target_format.value}"

    def _detect_font_format(self, file_path: Path) -> FontFormat:
        """Detect font format from file extension"""
        extension = file_path.suffix.lower().lstrip(".")
        try:
            return FontFormat(extension)
        except ValueError:
            raise ValueError(f"Unknown font format: {extension}")
