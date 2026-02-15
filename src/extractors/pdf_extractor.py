from __future__ import annotations

import logging
from typing import Generator, Tuple

import pdfplumber

logger = logging.getLogger(__name__)


def extract_text_by_page(pdf_path: str) -> Generator[Tuple[int, str], None, None]:
    """
    Yields (page_number, text) without loading the entire PDF into memory.
    Page numbers are 1-based.
    """
    with pdfplumber.open(pdf_path) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:  # pragma: no cover - best-effort extraction
                logger.exception("Failed to extract page %s: %s", idx, exc)
                text = ""
            yield idx, text
