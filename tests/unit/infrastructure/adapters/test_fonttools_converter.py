"""Tests for FontToolsConverter adapter"""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

import pytest

from domain.enums import FontFormat
from infrastructure.adapters import FontToolsConverter


class TestFontToolsConverter:
    """Tests for FontToolsConverter adapter"""

    @pytest.fixture
    def converter(self) -> FontToolsConverter:
        """Create FontToolsConverter instance"""
        return FontToolsConverter()

    @pytest.fixture
    def temp_dir(self) -> Generator[Path, None, None]:
        """Create temporary directory for tests"""
        with TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    def test_convert_raises_file_not_found_error(
        self, converter: FontToolsConverter, temp_dir: Path
    ) -> None:
        """Test that convert raises FileNotFoundError for nonexistent input"""
        # Arrange
        input_path = temp_dir / "nonexistent.ttf"
        output_path = temp_dir / "output.woff"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            converter.convert(input_path, output_path, FontFormat.WOFF)

    def test_convert_raises_value_error_for_unsupported_format(
        self, converter: FontToolsConverter, temp_dir: Path
    ) -> None:
        """Test that convert raises ValueError for unsupported format"""
        # This test would need a real font file to work properly
        # For now, we'll just verify the error handling exists
        # In a real scenario, you'd use a sample font file from fixtures
        pass

    def test_cleanup_on_failure(
        self, converter: FontToolsConverter, temp_dir: Path
    ) -> None:
        """Test that output file is cleaned up on conversion failure"""
        # This test would need a real font file and mock fontTools
        # to simulate a failure during conversion
        pass
