"""Editable, deterministic signals for provider-returned delegate reasoning."""
from __future__ import annotations

import json
from pathlib import Path
import re


PATTERN_FILE = Path(__file__).with_name("delegate_patterns.json")


def load_patterns(path: Path = PATTERN_FILE) -> dict[str, dict]:
    raw = json.loads(path.read_text())
    groups = raw.get("groups") or {}
    return {
        name: {
            "label": str(group.get("label") or name.replace("_", " ")),
            "patterns": [re.compile(pattern, re.IGNORECASE | re.DOTALL)
                         for pattern in group.get("patterns") or []],
        }
        for name, group in groups.items()
    }


PATTERNS = load_patterns()


def compact(text: str, start: int, end: int, radius: int = 90) -> str:
    return re.sub(r"\s+", " ", text[max(0, start - radius):min(len(text), end + radius)]).strip()


def find_delegate_signals(text: str, patterns: dict[str, dict] = PATTERNS) -> list[dict]:
    matches = []
    for group, definition in patterns.items():
        for pattern in definition["patterns"]:
            for match in pattern.finditer(text):
                matches.append({
                    "pattern": group,
                    "label": definition["label"],
                    "match": match.group(0),
                    "snippet": compact(text, match.start(), match.end()),
                })
    return matches
