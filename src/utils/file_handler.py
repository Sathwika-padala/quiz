"""File I/O utilities for JSON data."""

import json
from pathlib import Path
from typing import Any, List, Dict


def load_json(path: Path) -> Any:
    """Load JSON from file."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any, indent: int = 2) -> None:
    """Save data to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_lines(path: Path) -> List[str]:
    """Load lines from text file."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def append_to_json_list(path: Path, item: Dict) -> None:
    """Append a dict to JSON array; create file if not exists."""
    data = load_json(path)
    if not isinstance(data, list):
        data = []
    data.append(item)
    save_json(path, data)
