from __future__ import annotations

import sqlite3
from typing import Optional


class SQLiteStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bhajans (
                page_number INTEGER PRIMARY KEY,
                bhajan_title_hindi TEXT,
                bhajan_title_transliterated TEXT,
                hindi_unicode_text TEXT,
                transliterated_text TEXT
            )
            """
        )
        self._conn.commit()

    def page_exists(self, page_number: int) -> bool:
        cur = self._conn.execute(
            "SELECT 1 FROM bhajans WHERE page_number = ?", (page_number,)
        )
        return cur.fetchone() is not None

    def save_page(
        self,
        page_number: int,
        title_hindi: str,
        title_translit: str,
        hindi_text: str,
        translit_text: str,
    ) -> None:
        self._conn.execute(
            """
            INSERT OR REPLACE INTO bhajans
                (page_number, bhajan_title_hindi, bhajan_title_transliterated, hindi_unicode_text, transliterated_text)
            VALUES (?, ?, ?, ?, ?)
            """,
            (page_number, title_hindi, title_translit, hindi_text, translit_text),
        )
        self._conn.commit()

    def get_page(self, page_number: int) -> Optional[dict]:
        cur = self._conn.execute(
            "SELECT * FROM bhajans WHERE page_number = ?", (page_number,)
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def iter_pages(self):
        cur = self._conn.execute(
            "SELECT * FROM bhajans ORDER BY page_number ASC"
        )
        for row in cur.fetchall():
            yield dict(row)

    def close(self) -> None:
        self._conn.close()
