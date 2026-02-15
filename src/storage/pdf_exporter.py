from __future__ import annotations

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def export_transliteration_pdf(records, output_path: str) -> None:
    """
    Generate a lightweight searchable PDF containing transliterated text.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    margin = 40
    y = height - margin

    c.setFont("Helvetica", 10)

    for record in records:
        header = f"Page {record['page_number']}: {record.get('bhajan_title_transliterated') or ''}"
        lines = [header, ""] + (record.get("transliterated_text") or "").splitlines()

        for line in lines:
            if y < margin:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - margin
            c.drawString(margin, y, line)
            y -= 14
        y -= 10

    c.save()
