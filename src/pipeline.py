from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from src.converters.legacy_to_unicode import convert_legacy_to_unicode
from src.converters.mappings.krutidev import KRUTIDEV_MAPPING
from src.extractors.pdf_extractor import extract_text_by_page
from src.normalizers.hindi_normalizer import normalize_hindi_text
from src.storage.sqlite_store import SQLiteStore
from src.storage.pdf_exporter import export_transliteration_pdf
from src.transliterators.devanagari_to_latin import transliterate_devanagari_to_latin

logger = logging.getLogger(__name__)


def _ensure_parent(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    return str(target)


def _extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def run_pipeline(
    pdf_path: str,
    db_path: str,
    output_pdf_path: Optional[str] = None,
) -> None:
    db_path = _ensure_parent(db_path) or db_path
    output_pdf_path = _ensure_parent(output_pdf_path)

    store = SQLiteStore(db_path)

    for page_number, page_text in extract_text_by_page(pdf_path):
        if store.page_exists(page_number):
            logger.info("Skipping page %s (already processed)", page_number)
            continue

        try:
            unicode_text = convert_legacy_to_unicode(page_text, KRUTIDEV_MAPPING)
            unicode_text = normalize_hindi_text(unicode_text)

            title_hindi = _extract_title(unicode_text)
            translit_text = transliterate_devanagari_to_latin(unicode_text)
            title_translit = transliterate_devanagari_to_latin(title_hindi)

            store.save_page(
                page_number=page_number,
                title_hindi=title_hindi,
                title_translit=title_translit,
                hindi_text=unicode_text,
                translit_text=translit_text,
            )
            logger.info("Processed page %s", page_number)
        except Exception as exc:  # pragma: no cover - robust pipeline
            logger.exception("Error processing page %s: %s", page_number, exc)
            continue

    if output_pdf_path:
        export_transliteration_pdf(store.iter_pages(), output_pdf_path)

    store.close()
