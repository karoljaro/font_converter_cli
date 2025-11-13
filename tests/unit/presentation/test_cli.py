"""Tests for FontConverterCLI presentation layer."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from application.dto import ConvertFontRequest, ConvertFontResult
from domain.enums import FontFormat
from presentation.cli import FontConverterCLI


class TestFontConverterCLI:
    """Tests for FontConverterCLI class."""

    # ======================== parse_target_format Tests ========================

    def test_parse_target_format_with_ttf(self, cli: FontConverterCLI) -> None:
        """Test parsing TTF format."""
        result = cli.parse_target_format("ttf")
        assert result == FontFormat.TTF

    def test_parse_target_format_with_otf(self, cli: FontConverterCLI) -> None:
        """Test parsing OTF format."""
        result = cli.parse_target_format("otf")
        assert result == FontFormat.OTF

    def test_parse_target_format_with_woff(self, cli: FontConverterCLI) -> None:
        """Test parsing WOFF format."""
        result = cli.parse_target_format("woff")
        assert result == FontFormat.WOFF

    def test_parse_target_format_with_woff2(self, cli: FontConverterCLI) -> None:
        """Test parsing WOFF2 format."""
        result = cli.parse_target_format("woff2")
        assert result == FontFormat.WOFF2

    def test_parse_target_format_case_insensitive(self, cli: FontConverterCLI) -> None:
        """Test that format parsing is case-insensitive."""
        result = cli.parse_target_format("WOFF2")
        assert result == FontFormat.WOFF2

    @patch("typer.secho")
    def test_parse_target_format_defaults_to_woff2_when_none(
        self, mock_secho: MagicMock, cli: FontConverterCLI
    ) -> None:
        """Test that None format defaults to WOFF2 with info message."""
        result = cli.parse_target_format(None)
        assert result == FontFormat.WOFF2
        mock_secho.assert_called_once()
        args, kwargs = mock_secho.call_args
        assert "defaulting to woff2" in args[0].lower()
        assert kwargs.get("fg") == typer.colors.YELLOW

    @patch("typer.secho")
    def test_parse_target_format_invalid_raises_exit(
        self, mock_secho: MagicMock, cli: FontConverterCLI
    ) -> None:
        """Test that invalid format raises typer.Exit."""
        with pytest.raises(typer.Exit) as exc_info:
            cli.parse_target_format("invalid")
        assert exc_info.value.exit_code == 1
        # Should have called secho twice (error + valid formats list)
        assert mock_secho.call_count == 2

    # ==================== resolve_output_path_with_warning Tests ====================

    def test_resolve_output_path_uses_resolver_service(
        self,
        cli: FontConverterCLI,
        mock_output_path_resolver: MagicMock,
    ) -> None:
        """Test that output path resolution delegates to the service."""
        input_path = Path("font.ttf")
        expected_output = Path("font.woff2")
        mock_output_path_resolver.resolve.return_value = expected_output

        result = cli.resolve_output_path_with_warning(
            input_path, FontFormat.WOFF2, None
        )

        assert result == expected_output
        mock_output_path_resolver.resolve.assert_called_once_with(
            input_path, FontFormat.WOFF2, None
        )

    @patch("typer.secho")
    def test_resolve_output_path_warns_on_suffix_mismatch(
        self,
        mock_secho: MagicMock,
        cli: FontConverterCLI,
        mock_output_path_resolver: MagicMock,
    ) -> None:
        """Test that warning is shown when user provides wrong suffix."""
        input_path = Path("font.ttf")
        output_path = Path("output.ttf")
        mock_output_path_resolver.resolve.return_value = output_path

        cli.resolve_output_path_with_warning(input_path, FontFormat.WOFF2, "output.ttf")

        # Should have called secho with warning
        mock_secho.assert_called_once()
        args, kwargs = mock_secho.call_args
        assert "Adjusting output filename" in args[0]
        assert ".woff2" in args[0]
        assert kwargs.get("fg") == typer.colors.YELLOW

    @patch("typer.secho")
    def test_resolve_output_path_no_warning_when_suffix_matches(
        self,
        mock_secho: MagicMock,
        cli: FontConverterCLI,
        mock_output_path_resolver: MagicMock,
    ) -> None:
        """Test that no warning is shown when suffix matches."""
        input_path = Path("font.ttf")
        output_path = Path("output.woff2")
        mock_output_path_resolver.resolve.return_value = output_path

        cli.resolve_output_path_with_warning(
            input_path, FontFormat.WOFF2, "output.woff2"
        )

        # Should NOT call secho (no warning)
        mock_secho.assert_not_called()

    @patch("typer.secho")
    def test_resolve_output_path_no_warning_when_output_is_none(
        self,
        mock_secho: MagicMock,
        cli: FontConverterCLI,
        mock_output_path_resolver: MagicMock,
    ) -> None:
        """Test that no warning is shown when output is None."""
        input_path = Path("font.ttf")
        output_path = Path("font.woff2")
        mock_output_path_resolver.resolve.return_value = output_path

        cli.resolve_output_path_with_warning(input_path, FontFormat.WOFF2, None)

        # Should NOT call secho (no warning)
        mock_secho.assert_not_called()

    # ======================= log_conversion_start Tests =======================

    @patch("typer.secho")
    def test_log_conversion_start(
        self, mock_secho: MagicMock, cli: FontConverterCLI
    ) -> None:
        """Test that conversion start is logged correctly."""
        input_path = Path("font.ttf")
        cli.log_conversion_start(input_path, FontFormat.WOFF2)

        mock_secho.assert_called_once()
        args, kwargs = mock_secho.call_args
        assert "Converting font.ttf → woff2" in args[0]
        assert kwargs.get("fg") == typer.colors.BLUE

    # ======================== execute_conversion Tests ========================

    def test_execute_conversion_calls_use_case(
        self,
        cli: FontConverterCLI,
        mock_use_case: MagicMock,
    ) -> None:
        """Test that execute_conversion calls the use case."""
        input_path = Path("font.ttf")
        output_path = Path("font.woff2")
        expected_result = ConvertFontResult(
            output_file_path=output_path,
            target_format=FontFormat.WOFF2,
            success=True,
        )
        mock_use_case.execute.return_value = expected_result

        result = cli.execute_conversion(input_path, FontFormat.WOFF2, output_path)

        assert result == expected_result
        mock_use_case.execute.assert_called_once()
        call_args = mock_use_case.execute.call_args[0][0]
        assert isinstance(call_args, ConvertFontRequest)
        assert call_args.input_file_path == input_path
        assert call_args.target_format == FontFormat.WOFF2
        assert call_args.output_file_path == output_path

    # ======================= log_conversion_success Tests =======================

    @patch("typer.secho")
    def test_log_conversion_success(
        self, mock_secho: MagicMock, cli: FontConverterCLI
    ) -> None:
        """Test that conversion success is logged correctly."""
        output_path = Path("font.woff2")
        result = ConvertFontResult(
            output_file_path=output_path,
            target_format=FontFormat.WOFF2,
            success=True,
        )

        cli.log_conversion_success(result)

        # Should have called secho twice (success + file path)
        assert mock_secho.call_count == 2
        calls = mock_secho.call_args_list

        # First call: success message
        assert "successfully" in calls[0][0][0].lower()
        assert calls[0][1]["fg"] == typer.colors.GREEN

        # Second call: file path
        assert str(output_path) in calls[1][0][0]
        assert calls[1][1]["fg"] == typer.colors.GREEN

    # ========================== Integration Tests ==========================

    def test_cli_initialization(
        self,
        mock_use_case: MagicMock,
        mock_output_path_resolver: MagicMock,
    ) -> None:
        """Test that CLI initializes correctly with dependencies."""
        cli = FontConverterCLI(
            use_case=mock_use_case,
            output_path_resolver=mock_output_path_resolver,
        )

        assert cli.use_case is mock_use_case
        assert cli.output_path_resolver is mock_output_path_resolver
        assert cli.app is not None
        assert isinstance(cli.app, typer.Typer)
