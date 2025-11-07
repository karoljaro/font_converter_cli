"""Tests for ConvertFontUseCase"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from application.dto import ConvertFontRequest
from application.use_cases import ConvertFontUseCase
from domain.enums import FontFormat
from domain.exceptions import (
    FontConversionError,
    FontConversionFailedError,
    InputFileNotFoundError,
)


class TestConvertFontUseCase:
    """Tests for ConvertFontUseCase"""

    @pytest.fixture
    def use_case(
        self, mock_font_converter: MagicMock, mock_file_service: MagicMock
    ) -> ConvertFontUseCase:
        """Create ConvertFontUseCase with mocks"""
        return ConvertFontUseCase(
            converter=mock_font_converter,
            file_service=mock_file_service,
        )

    def test_successful_conversion(
        self,
        use_case: ConvertFontUseCase,
        mock_file_service: MagicMock,
    ) -> None:
        """Test successful font conversion"""
        # Arrange
        mock_file_service.file_exists.return_value = True
        input_path = Path("font.ttf")
        request = ConvertFontRequest(
            input_file_path=input_path,
            target_format=FontFormat.WOFF,
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert result.success is True
        assert result.target_format == FontFormat.WOFF
        assert result.output_file_path == Path("/output/font.woff")
        mock_file_service.file_exists.assert_called_with(input_path)

    def test_input_file_not_found(
        self,
        use_case: ConvertFontUseCase,
        mock_file_service: MagicMock,
    ) -> None:
        """Test error when input file does not exist"""
        # Arrange
        mock_file_service.file_exists.return_value = False
        request = ConvertFontRequest(
            input_file_path=Path("nonexistent.ttf"),
            target_format=FontFormat.WOFF,
        )

        # Act & Assert
        with pytest.raises(InputFileNotFoundError):
            use_case.execute(request)

    def test_invalid_font_format(
        self,
        use_case: ConvertFontUseCase,
        mock_file_service: MagicMock,
    ) -> None:
        """Test error when input file has unknown font format"""
        # Arrange
        mock_file_service.file_exists.return_value = True
        request = ConvertFontRequest(
            input_file_path=Path("font.xyz"),
            target_format=FontFormat.WOFF,
        )

        # Act & Assert
        with pytest.raises(FontConversionError):
            use_case.execute(request)

    def test_unsupported_conversion(
        self,
        use_case: ConvertFontUseCase,
        mock_file_service: MagicMock,
    ) -> None:
        """Test error when conversion is not allowed (WOFF to TTF)"""
        # Arrange
        mock_file_service.file_exists.return_value = True
        request = ConvertFontRequest(
            input_file_path=Path("font.woff"),
            target_format=FontFormat.TTF,
        )

        # Act & Assert
        with pytest.raises(FontConversionError) as exc_info:
            use_case.execute(request)
        assert "cannot convert from woff to ttf" in str(exc_info.value).lower()

    def test_conversion_failure(
        self,
        use_case: ConvertFontUseCase,
        mock_font_converter: MagicMock,
        mock_file_service: MagicMock,
    ) -> None:
        """Test error when conversion process fails"""
        # Arrange
        mock_file_service.file_exists.return_value = True
        mock_font_converter.convert.side_effect = Exception("Conversion failed")
        request = ConvertFontRequest(
            input_file_path=Path("font.ttf"),
            target_format=FontFormat.WOFF,
        )

        # Act & Assert
        with pytest.raises(FontConversionFailedError):
            use_case.execute(request)

        # Verify cleanup was called
        mock_file_service.delete_file.assert_called()

    def test_cleanup_on_failure(
        self,
        use_case: ConvertFontUseCase,
        mock_font_converter: MagicMock,
        mock_file_service: MagicMock,
    ) -> None:
        """Test that output file is deleted on conversion failure"""
        # Arrange
        mock_file_service.file_exists.side_effect = [True, True]  # file exists checks
        mock_font_converter.convert.side_effect = Exception("Conversion failed")
        request = ConvertFontRequest(
            input_file_path=Path("font.ttf"),
            target_format=FontFormat.WOFF,
        )

        # Act & Assert
        with pytest.raises(FontConversionFailedError):
            use_case.execute(request)

        # Verify output file was deleted
        delete_calls = mock_file_service.delete_file.call_args_list
        assert len(delete_calls) > 0

    def test_custom_output_path(
        self,
        use_case: ConvertFontUseCase,
        mock_file_service: MagicMock,
    ) -> None:
        """Test conversion with custom output path"""
        # Arrange
        mock_file_service.file_exists.return_value = True
        output_path = Path("/custom/output.woff")
        request = ConvertFontRequest(
            input_file_path=Path("font.ttf"),
            target_format=FontFormat.WOFF,
            output_file_path=output_path,
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert result.output_file_path == output_path
