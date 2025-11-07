"""Domain layer exceptions"""


class DomainException(Exception):
    """Base exception for domain layer"""

    pass


class InvalidFontFormatError(DomainException):
    """Raised when font format is invalid or not supported"""

    pass


class FontConversionError(DomainException):
    """Raised when font conversion is not allowed"""

    pass
