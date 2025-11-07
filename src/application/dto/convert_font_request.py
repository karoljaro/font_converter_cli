"""Request DTO for font conversion"""

from dataclasses import dataclass
from pathlib import Path

from domain.enums import FontFormat


@dataclass
class ConvertFontRequest:
    """Data transfer object for font conversion request"""

    input_file_path: Path
    target_format: FontFormat
    output_file_path: Path | None = None
