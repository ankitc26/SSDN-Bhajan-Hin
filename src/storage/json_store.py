from __future__ import annotations

import json
from typing import Iterable, Dict, Any


def export_to_json(records: Iterable[Dict[str, Any]], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(list(records), f, ensure_ascii=False, indent=2)
