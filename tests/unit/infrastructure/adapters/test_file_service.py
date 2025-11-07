"""Tests for FileService adapter"""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

import pytest

from infrastructure.adapters import FileService


class TestFileService:
    """Tests for FileService adapter"""

    @pytest.fixture
    def file_service(self) -> FileService:
        """Create FileService instance"""
        return FileService()

    @pytest.fixture
    def temp_dir(self) -> Generator[Path, None, None]:
        """Create temporary directory for tests"""
        with TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    def test_file_exists_returns_true_for_existing_file(
        self, file_service: FileService, temp_dir: Path
    ) -> None:
        """Test that file_exists returns True for existing file"""
        # Arrange
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Act
        result = file_service.file_exists(test_file)

        # Assert
        assert result is True

    def test_file_exists_returns_false_for_nonexistent_file(
        self, file_service: FileService, temp_dir: Path
    ) -> None:
        """Test that file_exists returns False for nonexistent file"""
        # Arrange
        test_file = temp_dir / "nonexistent.txt"

        # Act
        result = file_service.file_exists(test_file)

        # Assert
        assert result is False

    def test_file_exists_returns_false_for_directory(
        self, file_service: FileService, temp_dir: Path
    ) -> None:
        """Test that file_exists returns False for directory"""
        # Act
        result = file_service.file_exists(temp_dir)

        # Assert
        assert result is False

    def test_delete_file_removes_file(
        self, file_service: FileService, temp_dir: Path
    ) -> None:
        """Test that delete_file removes a file"""
        # Arrange
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()

        # Act
        file_service.delete_file(test_file)

        # Assert
        assert not test_file.exists()

    def test_delete_file_handles_nonexistent_file(
        self, file_service: FileService, temp_dir: Path
    ) -> None:
        """Test that delete_file handles nonexistent file gracefully"""
        # Arrange
        test_file = temp_dir / "nonexistent.txt"

        # Act & Assert - should not raise
        file_service.delete_file(test_file)

    def test_get_parent_directory_returns_parent(
        self, file_service: FileService, temp_dir: Path
    ) -> None:
        """Test that get_parent_directory returns parent directory"""
        # Arrange
        test_file = temp_dir / "subdir" / "test.txt"

        # Act
        result = file_service.get_parent_directory(test_file)

        # Assert
        assert result == temp_dir / "subdir"

    def test_get_file_name_without_extension(self, file_service: FileService) -> None:
        """Test that get_file_name_without_extension returns correct name"""
        # Arrange
        test_file = Path("/path/to/font.ttf")

        # Act
        result = file_service.get_file_name_without_extension(test_file)

        # Assert
        assert result == "font"

    def test_get_file_name_without_extension_with_multiple_dots(
        self, file_service: FileService
    ) -> None:
        """Test file name without extension when name has multiple dots"""
        # Arrange
        test_file = Path("/path/to/my.font.file.ttf")

        # Act
        result = file_service.get_file_name_without_extension(test_file)

        # Assert
        assert result == "my.font.file"
