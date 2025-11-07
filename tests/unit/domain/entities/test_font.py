"""Testy dla Font entity"""

from domain.entities import Font
from domain.enums import FontFormat


class TestCanConvertTo:
    """Testy metody can_convert_to"""

    def test_ttf_can_convert_to_woff(self, ttf_font: Font) -> None:
        """TTF powinno móc konwertować na WOFF"""
        assert ttf_font.can_convert_to(FontFormat.WOFF) is True

    def test_ttf_can_convert_to_woff2(self, ttf_font: Font) -> None:
        """TTF powinno móc konwertować na WOFF2"""
        assert ttf_font.can_convert_to(FontFormat.WOFF2) is True

    def test_ttf_can_convert_to_otf(self, ttf_font: Font) -> None:
        """TTF powinno móc konwertować na OTF"""
        assert ttf_font.can_convert_to(FontFormat.OTF) is True

    def test_otf_can_convert_to_woff(self, otf_font: Font) -> None:
        """OTF powinno móc konwertować na WOFF"""
        assert otf_font.can_convert_to(FontFormat.WOFF) is True

    def test_otf_can_convert_to_woff2(self, otf_font: Font) -> None:
        """OTF powinno móc konwertować na WOFF2"""
        assert otf_font.can_convert_to(FontFormat.WOFF2) is True

    def test_otf_can_convert_to_ttf(self, otf_font: Font) -> None:
        """OTF powinno móc konwertować na TTF"""
        assert otf_font.can_convert_to(FontFormat.TTF) is True

    def test_woff_cannot_convert_to_ttf(self, woff_font: Font) -> None:
        """WOFF nie powinno móc konwertować na TTF"""
        assert woff_font.can_convert_to(FontFormat.TTF) is False

    def test_woff_cannot_convert_to_otf(self, woff_font: Font) -> None:
        """WOFF nie powinno móc konwertować na OTF"""
        assert woff_font.can_convert_to(FontFormat.OTF) is False

    def test_woff_can_convert_to_woff2(self, woff_font: Font) -> None:
        """WOFF powinno móc konwertować na WOFF2"""
        assert woff_font.can_convert_to(FontFormat.WOFF2) is True

    def test_woff2_cannot_convert_to_ttf(self, woff2_font: Font) -> None:
        """WOFF2 nie powinno móc konwertować na TTF"""
        assert woff2_font.can_convert_to(FontFormat.TTF) is False

    def test_woff2_cannot_convert_to_otf(self, woff2_font: Font) -> None:
        """WOFF2 nie powinno móc konwertować na OTF"""
        assert woff2_font.can_convert_to(FontFormat.OTF) is False

    def test_woff2_can_convert_to_woff(self, woff2_font: Font) -> None:
        """WOFF2 powinno móc konwertować na WOFF"""
        assert woff2_font.can_convert_to(FontFormat.WOFF) is True


class TestFontInstantiation:
    """Testy tworzenia instancji Font"""

    def test_create_ttf_font(self) -> None:
        """Można stworzyć czcionkę TTF"""
        font = Font(original_format=FontFormat.TTF)
        assert font.original_format == FontFormat.TTF

    def test_create_otf_font(self) -> None:
        """Można stworzyć czcionkę OTF"""
        font = Font(original_format=FontFormat.OTF)
        assert font.original_format == FontFormat.OTF

    def test_create_woff_font(self) -> None:
        """Można stworzyć czcionkę WOFF"""
        font = Font(original_format=FontFormat.WOFF)
        assert font.original_format == FontFormat.WOFF

    def test_create_woff2_font(self) -> None:
        """Można stworzyć czcionkę WOFF2"""
        font = Font(original_format=FontFormat.WOFF2)
        assert font.original_format == FontFormat.WOFF2


class TestIsSameFormat:
    """Testy metody is_same_format"""

    def test_ttf_is_same_as_ttf(self, ttf_font: Font) -> None:
        """TTF powinno być tym samym formatem co TTF"""
        assert ttf_font.is_same_format(FontFormat.TTF) is True

    def test_ttf_is_not_same_as_otf(self, ttf_font: Font) -> None:
        """TTF nie powinno być tym samym formatem co OTF"""
        assert ttf_font.is_same_format(FontFormat.OTF) is False

    def test_ttf_is_not_same_as_woff(self, ttf_font: Font) -> None:
        """TTF nie powinno być tym samym formatem co WOFF"""
        assert ttf_font.is_same_format(FontFormat.WOFF) is False

    def test_ttf_is_not_same_as_woff2(self, ttf_font: Font) -> None:
        """TTF nie powinno być tym samym formatem co WOFF2"""
        assert ttf_font.is_same_format(FontFormat.WOFF2) is False

    def test_otf_is_same_as_otf(self, otf_font: Font) -> None:
        """OTF powinno być tym samym formatem co OTF"""
        assert otf_font.is_same_format(FontFormat.OTF) is True

    def test_otf_is_not_same_as_ttf(self, otf_font: Font) -> None:
        """OTF nie powinno być tym samym formatem co TTF"""
        assert otf_font.is_same_format(FontFormat.TTF) is False

    def test_woff_is_same_as_woff(self, woff_font: Font) -> None:
        """WOFF powinno być tym samym formatem co WOFF"""
        assert woff_font.is_same_format(FontFormat.WOFF) is True

    def test_woff_is_not_same_as_woff2(self, woff_font: Font) -> None:
        """WOFF nie powinno być tym samym formatem co WOFF2"""
        assert woff_font.is_same_format(FontFormat.WOFF2) is False

    def test_woff2_is_same_as_woff2(self, woff2_font: Font) -> None:
        """WOFF2 powinno być tym samym formatem co WOFF2"""
        assert woff2_font.is_same_format(FontFormat.WOFF2) is True

    def test_woff2_is_not_same_as_woff(self, woff2_font: Font) -> None:
        """WOFF2 nie powinno być tym samym formatem co WOFF"""
        assert woff2_font.is_same_format(FontFormat.WOFF) is False
