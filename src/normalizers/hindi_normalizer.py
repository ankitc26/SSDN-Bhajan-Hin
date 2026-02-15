from __future__ import annotations

import logging

import regex as re
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory

logger = logging.getLogger(__name__)


def normalize_hindi_text(text: str) -> str:
    if not text:
        return ""

    # Normalize with Indic NLP
    try:
        factory = IndicNormalizerFactory()
        normalizer = factory.get_normalizer("hi", remove_nuktas=False)
        text = normalizer.normalize(text)
    except Exception as exc:  # pragma: no cover - best-effort normalization
        logger.warning("Indic normalization failed: %s", exc)

    # Clean whitespace and preserve line breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    text = text.strip()
    return text
