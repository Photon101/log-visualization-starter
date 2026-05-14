from __future__ import annotations

import csv

from log_visualization_starter.parser import parse_line
from log_visualization_starter.pipeline import run_pipeline, safe_name
from log_visualization_starter.svg import line_chart_svg


def test_parse_line_extracts_timestamp_and_metrics() -> None:
    parsed = parse_line("info 2026-05-01T10:00:00Z step=120 pressure=0.83 residual=0.008")
    assert parsed is not None
    assert parsed.timestamp == "2026-05-01T10:00:00Z"
    assert parsed.metrics == {"step": 120.0, "pressure": 0.83, "residual": 0.008}


def test_parse_line_ignores_non_metric_text() -> None:
    assert parse_line("warning no numeric metrics here") is None


def test_pipeline_writes_records_summary_and_svg(tmp_path) -> None:
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "run.log").write_text(
        "\n".join([
            "2026-05-01T10:00:00Z step=1 pressure=0.50 residual=0.100",
            "2026-05-01T10:01:00Z step=2 pressure=0.75 residual=0.050",
        ]),
        encoding="utf-8",
    )

    result = run_pipeline(logs, tmp_path / "out")

    assert len(result.records) == 6
    assert set(result.metric_names) == {"pressure", "residual", "step"}
    rows = list(csv.DictReader((tmp_path / "out" / "summary.csv").open()))
    pressure = next(row for row in rows if row["metric"] == "pressure")
    assert pressure["count"] == "2"
    assert pressure["avg"] == "0.625"
    assert (tmp_path / "out" / "residual.svg").read_text("utf-8").startswith("<svg")


def test_svg_escapes_title_and_labels() -> None:
    svg = line_chart_svg("<residual>", [("<t0>", 1.0), ("t1", 2.0)])
    assert "&lt;residual&gt;" in svg
    assert "&lt;t0&gt;" in svg


def test_safe_name() -> None:
    assert safe_name("pressure.avg") == "pressure-avg"
    assert safe_name("$$$") == "metric"

