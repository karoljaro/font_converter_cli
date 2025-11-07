import pytest
from pathlib import Path
from unittest.mock import MagicMock

from domain.enums import FontFormat
from domain.entities import Font
from domain.ports import FontConverterPort, FileServicePort


@pytest.fixture
def ttf_font() -> Font:
    """Fixture: TTF font for tests"""
    return Font(original_format=FontFormat.TTF)


@pytest.fixture
def otf_font() -> Font:
    """Fixture: OTF font for tests"""
    return Font(original_format=FontFormat.OTF)


@pytest.fixture
def woff_font() -> Font:
    """Fixture: WOFF font for tests"""
    return Font(original_format=FontFormat.WOFF)


@pytest.fixture
def woff2_font() -> Font:
    """Fixture: WOFF2 font for tests"""
    return Font(original_format=FontFormat.WOFF2)


@pytest.fixture
def mock_font_converter() -> MagicMock:
    """Mock for FontConverterPort"""
    return MagicMock(spec=FontConverterPort)


@pytest.fixture
def mock_file_service() -> MagicMock:
    """Mock for FileServicePort"""
    mock = MagicMock(spec=FileServicePort)
    mock.get_parent_directory.return_value = Path("/output")
    mock.get_file_name_without_extension.return_value = "font"
    return mock
