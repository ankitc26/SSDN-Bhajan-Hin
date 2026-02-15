from __future__ import annotations

import regex as re

DEVANAGARI_RANGE = re.compile(r"[\u0900-\u097F]")


def validate_devanagari_text(text: str) -> None:
    """
    Raise ValueError if text does not contain any Devanagari characters.
    """
    if not text or not DEVANAGARI_RANGE.search(text):
        raise ValueError("No Devanagari Unicode characters found in converted text")
