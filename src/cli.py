from __future__ import annotations

import argparse
import logging
from pathlib import Path

from src.logging_config import setup_logging
from src.pipeline import run_pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = PROJECT_ROOT / "PDF"
OUTPUT_DIR = PROJECT_ROOT / "output"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Legacy Hindi PDF processor")
    parser.add_argument("--pdf", required=True, help="Path to input PDF")
    parser.add_argument("--json", required=True, help="Path to output JSON")
    parser.add_argument("--out-pdf", help="Path to output transliterated PDF")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(getattr(logging, args.log_level))

    pdf_path = Path(args.pdf).expanduser()
    if not pdf_path.is_absolute():
        if pdf_path.exists():
            pdf_path = pdf_path.resolve()
        else:
            pdf_path = (PDF_DIR / args.pdf).resolve()

    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    json_path = Path(args.json).expanduser()
    if not json_path.is_absolute():
        if json_path.parent == Path("."):
            json_path = OUTPUT_DIR / json_path.name
        else:
            json_path = PROJECT_ROOT / json_path

    out_pdf_path = None
    if args.out_pdf:
        out_pdf_path = Path(args.out_pdf).expanduser()
        if not out_pdf_path.is_absolute():
            if out_pdf_path.parent == Path("."):
                out_pdf_path = OUTPUT_DIR / out_pdf_path.name
            else:
                out_pdf_path = PROJECT_ROOT / out_pdf_path

    run_pipeline(str(pdf_path), str(json_path), str(out_pdf_path) if out_pdf_path else None)


if __name__ == "__main__":
    main()
