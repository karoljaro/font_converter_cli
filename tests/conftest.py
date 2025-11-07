import pytest

from domain.enums import FontFormat
from domain.entities import Font


@pytest.fixture
def ttf_font() -> Font:
    """Fixture: TTF czcionka do testów"""
    return Font(original_format=FontFormat.TTF)


@pytest.fixture
def otf_font() -> Font:
    """Fixture: OTF czcionka do testów"""
    return Font(original_format=FontFormat.OTF)


@pytest.fixture
def woff_font() -> Font:
    """Fixture: WOFF czcionka do testów"""
    return Font(original_format=FontFormat.WOFF)


@pytest.fixture
def woff2_font() -> Font:
    """Fixture: WOFF2 czcionka do testów"""
    return Font(original_format=FontFormat.WOFF2)
