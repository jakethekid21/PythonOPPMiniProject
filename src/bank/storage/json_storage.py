from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JSONStorage:
    """Simple json storage a list of dict records per file"""

    def __init__(self, filepath: str) -> None:
        self.path = Path(filepath)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[dict[str, Any]]:
        """Load records from json Returns [] if file missing or empty"""
        if not self.path.exists():
            return []

        text = self.path.read_text(encoding="utf-8").strip()
        if not text:
            return []

        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError(f"Invalid json format in {self.path}; expected list")
        return data

    def save(self, records: list[dict[str, Any]]) -> None:
        """Save records to json using  safe tempfile swap"""
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(records, indent=2), encoding="utf-8")
        tmp.replace(self.path)