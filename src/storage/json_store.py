from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, Optional


class JsonStore:
    def __init__(self, json_path: str) -> None:
        self.json_path = Path(json_path)
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[int, dict] = {}
        self._load()

    def _load(self) -> None:
        if not self.json_path.exists():
            return
        with self.json_path.open("r", encoding="utf-8") as f:
            try:
                items = json.load(f)
            except json.JSONDecodeError:
                items = []
        for item in items:
            if "page_number" in item:
                self._data[int(item["page_number"])] = item

    def page_exists(self, page_number: int) -> bool:
        return page_number in self._data

    def save_page(self, record: dict) -> None:
        page_number = int(record["page_number"])
        self._data[page_number] = record
        self._flush()

    def get_page(self, page_number: int) -> Optional[dict]:
        return self._data.get(page_number)

    def iter_pages(self) -> Iterable[dict]:
        for key in sorted(self._data.keys()):
            yield self._data[key]

    def _flush(self) -> None:
        items = [self._data[key] for key in sorted(self._data.keys())]
        with self.json_path.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
