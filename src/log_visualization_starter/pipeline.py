from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .parser import parse_line
from .svg import line_chart_svg


@dataclass(frozen=True)
class MetricRecord:
    source: str
    timestamp: str
    metric: str
    value: float


@dataclass(frozen=True)
class PipelineResult:
    out_dir: Path
    records: list[MetricRecord]
    metric_names: list[str]


def run_pipeline(source: Path, out_dir: Path) -> PipelineResult:
    out_dir.mkdir(parents=True, exist_ok=True)
    records = read_records(source)
    metric_names = sorted({record.metric for record in records})
    write_records_csv(records, out_dir / "records.csv")
    write_summary_csv(records, out_dir / "summary.csv")
    for metric in metric_names:
        series = [(record.timestamp, record.value) for record in records if record.metric == metric]
        (out_dir / f"{safe_name(metric)}.svg").write_text(
            line_chart_svg(metric, series),
            encoding="utf-8",
        )
    return PipelineResult(out_dir, records, metric_names)


def read_records(source: Path) -> list[MetricRecord]:
    files = sorted(source.glob("*.log")) + sorted(source.glob("*.txt")) if source.is_dir() else [source]
    records: list[MetricRecord] = []
    for path in files:
        for line in path.read_text("utf-8").splitlines():
            parsed = parse_line(line)
            if not parsed:
                continue
            for metric, value in parsed.metrics.items():
                records.append(MetricRecord(str(path), parsed.timestamp, metric, value))
    return records


def write_records_csv(records: list[MetricRecord], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "timestamp", "metric", "value"])
        writer.writeheader()
        for record in records:
            writer.writerow({
                "source": record.source,
                "timestamp": record.timestamp,
                "metric": record.metric,
                "value": f"{record.value:.8g}",
            })


def write_summary_csv(records: list[MetricRecord], path: Path) -> None:
    grouped: dict[str, list[float]] = {}
    for record in records:
        grouped.setdefault(record.metric, []).append(record.value)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "count", "min", "max", "avg"])
        writer.writeheader()
        for metric in sorted(grouped):
            values = grouped[metric]
            writer.writerow({
                "metric": metric,
                "count": len(values),
                "min": f"{min(values):.8g}",
                "max": f"{max(values):.8g}",
                "avg": f"{sum(values) / len(values):.8g}",
            })


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in value).strip("-") or "metric"

