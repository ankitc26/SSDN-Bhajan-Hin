from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException

from src.pipeline import run_pipeline
from src.storage.json_store import JsonStore

app = FastAPI(title="Bhajan API", version="1.0.0")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = PROJECT_ROOT / "PDF"
OUTPUT_DIR = PROJECT_ROOT / "output"
JSON_PATH = OUTPUT_DIR / "bhajans.json"
OUT_PDF_PATH = OUTPUT_DIR / "bhajans_translit.pdf"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/bhajans/{page_number}")
def get_bhajan(page_number: int):
    store = JsonStore(str(JSON_PATH))
    record = store.get_page(page_number)

    if not record:
        raise HTTPException(status_code=404, detail="Page not found")

    return record


@app.post("/process/{pdf_name}")
def process_pdf(pdf_name: str):
    pdf_path = (PDF_DIR / pdf_name).resolve()
    if PDF_DIR not in pdf_path.parents:
        raise HTTPException(status_code=400, detail="Invalid PDF path")
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found in PDF folder")

    run_pipeline(str(pdf_path), str(JSON_PATH), str(OUT_PDF_PATH))
    return {
        "status": "ok",
        "pdf": pdf_name,
        "json": str(JSON_PATH),
        "output_pdf": str(OUT_PDF_PATH),
    }
