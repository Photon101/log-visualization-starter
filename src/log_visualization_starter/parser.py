from __future__ import annotations

import re
from dataclasses import dataclass


TIMESTAMP_RE = re.compile(r"(?P<timestamp>\d{4}-\d{2}-\d{2}[T ][0-9:.+-]+Z?)")
METRIC_RE = re.compile(r"\b(?P<key>[A-Za-z_][A-Za-z0-9_.-]*)=(?P<value>-?\d+(?:\.\d+)?)\b")


@dataclass(frozen=True)
class ParsedLine:
    timestamp: str
    metrics: dict[str, float]


def parse_line(line: str) -> ParsedLine | None:
    timestamp_match = TIMESTAMP_RE.search(line)
    metrics = {
        match.group("key"): float(match.group("value"))
        for match in METRIC_RE.finditer(line)
    }
    if not timestamp_match or not metrics:
        return None
    return ParsedLine(timestamp_match.group("timestamp"), metrics)

