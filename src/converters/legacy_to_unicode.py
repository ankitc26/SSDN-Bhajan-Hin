from __future__ import annotations

from typing import Dict


def convert_legacy_to_unicode(text: str, mapping: Dict[str, str]) -> str:
    """
    Convert legacy font-encoded Hindi text to Unicode using a mapping dictionary.
    Uses longest-first replacement to support multi-character glyphs.
    """
    if not text:
        return ""

    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    for key in sorted_keys:
        text = text.replace(key, mapping[key])
    return text
