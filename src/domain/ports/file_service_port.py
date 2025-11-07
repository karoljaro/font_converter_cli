"""Port (abstraction) for file operations"""

from abc import ABC, abstractmethod
from pathlib import Path


class FileServicePort(ABC):
    """Interface for file operations"""

    @abstractmethod
    def file_exists(self, file_path: Path) -> bool:
        """Check if file exists"""
        pass

    @abstractmethod
    def delete_file(self, file_path: Path) -> None:
        """Delete a file"""
        pass

    @abstractmethod
    def get_parent_directory(self, file_path: Path) -> Path:
        """Get parent directory of a file"""
        pass

    @abstractmethod
    def get_file_name_without_extension(self, file_path: Path) -> str:
        """Get file name without extension"""
        pass
