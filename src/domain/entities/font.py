from dataclasses import dataclass

from domain.consts import UNSUPPORTED_CONVERSIONS
from domain.enums import FontFormat


@dataclass
class Font:
    original_format: FontFormat

    def can_convert_to(self, target_format: FontFormat) -> bool:
        blocked = UNSUPPORTED_CONVERSIONS.get(self.original_format, frozenset())
        return target_format not in blocked
