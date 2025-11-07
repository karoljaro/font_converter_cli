"""Adapter for file operations"""
from pathlib import Path

from domain.ports import FileServicePort


class FileService(FileServicePort):
    """Implementation of FileServicePort for real file operations"""

    def file_exists(self, file_path: Path) -> bool:
        """Check if file exists"""
        return file_path.exists() and file_path.is_file()

    def delete_file(self, file_path: Path) -> None:
        """Delete a file"""
        if file_path.exists():
            file_path.unlink()

    def get_parent_directory(self, file_path: Path) -> Path:
        """Get parent directory of a file"""
        return file_path.parent

    def get_file_name_without_extension(self, file_path: Path) -> str:
        """Get file name without extension"""
        return file_path.stem
