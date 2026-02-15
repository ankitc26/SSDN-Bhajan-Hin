from __future__ import annotations

from typing import Dict

import regex as re

DEVANAGARI_CONSONANTS = "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"


def _reorder_matra_i(text: str) -> str:
    """
    Fix ordering where legacy encodings place 'ि' before the consonant.
    Convert 'िक' -> 'कि'.
    """
    pattern = rf"ि([{DEVANAGARI_CONSONANTS}])"
    return re.sub(pattern, r"\1ि", text)


def convert_legacy_to_unicode(text: str, mapping: Dict[str, str]) -> str:
    """
    Convert legacy font-encoded Hindi text to Unicode using a mapping dictionary.
    Uses longest-first replacement to support multi-character glyphs.
    Applies reordering of 'ि' matra after conversion.
    """
    if not text:
        return ""

    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    for key in sorted_keys:
        text = text.replace(key, mapping[key])

    return _reorder_matra_i(text)


def contains_devanagari(text: str) -> bool:
    return bool(re.search(r"[\u0900-\u097F]", text or ""))
