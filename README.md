# SSDN Bhajan Hin

Offline Indic text processing pipeline for legacy-font Hindi PDFs on macOS.

## Features
- Page-by-page PDF extraction with `pdfplumber`
- Legacy font (KrutiDev/Chanakya) to Unicode Devanagari conversion
- Unicode normalization (Indic NLP + regex)
- Devanagari to Latin transliteration (indic-transliteration)
- Resumable processing with SQLite
- Searchable PDF output of transliterated text
- FastAPI backend to fetch bhajans by page

## Setup
1. Run `./setup.sh`
2. Activate the venv:
   - `source .venv/bin/activate`

## Usage
Process a PDF into JSON and generate a transliterated PDF:
- Place your PDF in the `PDF/` folder and run:
   - `python -m src.cli --pdf your.pdf --json bhajans.json --out-pdf bhajans_translit.pdf`
- You can also pass an absolute path:
   - `python -m src.cli --pdf /full/path/to/input.pdf --json output/bhajans.json --out-pdf output/bhajans_translit.pdf`

Start the API:
- `uvicorn src.api.app:app --reload`

Process a PDF via API (reads from `PDF/`):
- `POST /process/{pdf_name}`

## Notes
- The KrutiDev/Chanakya mapping provided is a minimal starter. Extend `src/converters/mappings/krutidev.py` with a complete mapping for production use.
- For large PDFs (1000+ pages), the pipeline processes page-by-page and skips already processed pages.
