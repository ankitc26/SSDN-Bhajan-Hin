from __future__ import annotations

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def transliterate_devanagari_to_latin(text: str) -> str:
    if not text:
        return ""

    # Preserve line breaks by transliterating line-by-line
    lines = text.splitlines(keepends=True)
    out_lines = []
    for line in lines:
        stripped = line.rstrip("\n")
        if stripped:
            converted = transliterate(stripped, sanscript.DEVANAGARI, sanscript.IAST)
        else:
            converted = ""
        out_lines.append(converted + ("\n" if line.endswith("\n") else ""))
    return "".join(out_lines)
