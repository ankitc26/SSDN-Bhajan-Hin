from __future__ import annotations

from typing import Dict

import unicodedata
import regex as re

DEVANAGARI_CONSONANTS = "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"


def _reorder_matra_i(text: str) -> str:
    """
    Fix ordering where legacy encodings place 'ि' before the consonant cluster.
    Convert 'िक' -> 'कि', 'िक्त' -> 'क्ति'.
    """
    pattern = rf"ि((?:[{DEVANAGARI_CONSONANTS}](?:्[{DEVANAGARI_CONSONANTS}])?)+)"
    return re.sub(pattern, r"\1ि", text)


def _reorder_reph(text: str) -> str:
    """
    Move trailing 'र्' to the start of the consonant cluster.
    Convert 'क्रर्' (cluster + र्) -> 'र्क्र'.
    """
    pattern = rf"((?:[{DEVANAGARI_CONSONANTS}](?:्[{DEVANAGARI_CONSONANTS}])?)+)र्"
    return re.sub(pattern, r"र्\1", text)


def convert_legacy_to_unicode(text: str, mapping: Dict[str, str]) -> str:
    """
    Convert legacy font-encoded Hindi text to Unicode using a mapping dictionary.
    Uses longest-first replacement to support multi-character glyphs.
    Applies reordering of 'ि' matra after conversion.
    """
    if not text:
        return ""

    # Normalize glyph output for consistency
    text = unicodedata.normalize("NFKC", text)

    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    for key in sorted_keys:
        text = text.replace(key, mapping[key])

    text = _reorder_reph(text)
    return _reorder_matra_i(text)


