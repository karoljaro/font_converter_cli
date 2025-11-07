"""Response DTO for font conversion"""

from dataclasses import dataclass
from pathlib import Path

from domain.enums import FontFormat


@dataclass
class ConvertFontResult:
    """Data transfer object for font conversion result"""

    output_file_path: Path
    target_format: FontFormat
    success: bool
