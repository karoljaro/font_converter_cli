"""Application layer exceptions"""


class ApplicationException(Exception):
    """Base exception for application layer"""

    pass


class InputFileNotFoundError(ApplicationException):
    """Raised when input file does not exist"""

    pass


class FontConversionFailedError(ApplicationException):
    """Raised when font conversion fails"""

    pass
