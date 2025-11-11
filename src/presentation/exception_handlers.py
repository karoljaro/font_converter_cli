"""Helper utilities to handle CLI exceptions and keep command handlers small.

This module provides a decorator that catches domain/application
exceptions and prints user-friendly messages instead of repeating boilerplate
in each command function.
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, Dict, ParamSpec, Tuple, Type, TypeVar

import typer

from domain.exceptions.application_exceptions import (
    InputFileNotFoundError,
    FontConversionFailedError,
)
from domain.exceptions.domain_exceptions import (
    InvalidFontFormatError,
    FontConversionError,
)


EXCEPTION_MAP: Dict[Type[BaseException], Tuple[str, int]] = {
    InputFileNotFoundError: ("❌ Input file not found: {details}", 1),
    InvalidFontFormatError: (
        "❌ Invalid font format or unsupported conversion\nDetails: {details}",
        2,
    ),
    FontConversionError: ("❌ Font conversion failed\nDetails: {details}", 2),
    FontConversionFailedError: (
        "❌ Font conversion failed with error\nDetails: {details}",
        2,
    ),
}


P = ParamSpec("P")
R = TypeVar("R")


def handle_exceptions(fn: Callable[P, R]) -> Callable[P, R]:
    """Decorator to centralize CLI exception handling.

    Catches known domain/application exceptions and exits with a user
    friendly message and an appropriate exit code. Unexpected exceptions
    are reported and exit with code 3.
    """

    exceptions_tuple: Tuple[Type[BaseException], ...] = tuple(EXCEPTION_MAP.keys())

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return fn(*args, **kwargs)
        except exceptions_tuple as e:
            cls = type(e)
            template, code = EXCEPTION_MAP.get(cls, ("❌ Error\nDetails: {details}", 2))
            details = str(e)
            typer.secho(template.format(details=details), fg=typer.colors.RED, err=True)
            raise typer.Exit(code=code)
        except Exception as e:  # unexpected
            typer.secho("❌ Unexpected error occurred", fg=typer.colors.RED, err=True)
            typer.secho(f"Details: {str(e)}", fg=typer.colors.YELLOW, err=True)
            raise typer.Exit(code=3)

    return wrapper
