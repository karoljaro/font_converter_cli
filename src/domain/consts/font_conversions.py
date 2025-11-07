from domain.enums.font_format import FontFormat

UNSUPPORTED_CONVERSIONS: dict[FontFormat, frozenset[FontFormat]] = {
    FontFormat.WOFF: frozenset([FontFormat.TTF, FontFormat.OTF]),
    FontFormat.WOFF2: frozenset([FontFormat.TTF, FontFormat.OTF]),
}
