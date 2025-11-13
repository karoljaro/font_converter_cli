import pytest
from pathlib import Path
from unittest.mock import MagicMock

from domain.enums import FontFormat
from domain.entities import Font
from domain.ports import FontConverterPort, FileServicePort, OutputPathResolverPort
from application.use_cases import ConvertFontUseCase
from presentation.cli import FontConverterCLI


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


@pytest.fixture
def mock_use_case() -> MagicMock:
    """Mock for ConvertFontUseCase (for CLI tests)."""
    return MagicMock(spec=ConvertFontUseCase)


@pytest.fixture
def mock_output_path_resolver() -> MagicMock:
    """Mock for OutputPathResolverPort (for CLI tests)."""
    return MagicMock(spec=OutputPathResolverPort)


@pytest.fixture
def cli(
    mock_use_case: MagicMock,
    mock_output_path_resolver: MagicMock,
) -> FontConverterCLI:
    """Fixture: FontConverterCLI instance with mocked dependencies."""
    return FontConverterCLI(
        use_case=mock_use_case,
        output_path_resolver=mock_output_path_resolver,
    )
