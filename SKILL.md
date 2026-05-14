---
name: log-visualization-reporter
description: Use when a user needs Python log parsing, metric extraction, CSV summaries, or lightweight visual reports from simulation logs, service logs, batch job output, benchmark logs, or timestamped key=value text files.
---

# Log Visualization Reporter

Use this skill to convert messy timestamped logs into normalized metric records, summary tables, and quick visual charts.

## Workflow

1. Inspect the sample log lines and identify timestamp format plus metric fields.
2. Adapt the parser to capture the required numeric metrics without treating unrelated text as data.
3. Run the pipeline to produce `records.csv`, `summary.csv`, and one chart per metric.
4. Validate with at least one fixture that covers the client's real log format.
5. Report the key trend, outliers, and any missing or malformed lines separately from the raw output.

## Local Starter

This repo includes a dependency-free implementation:

```bash
python -m log_visualization_starter examples/logs --out examples/output
```

Expected outputs:

- `records.csv` with `source`, `timestamp`, `metric`, and `value`
- `summary.csv` with count, min, max, and average per metric
- SVG line charts such as `residual.svg` and `pressure.svg`

## Adaptation Notes

- Preserve raw source filenames in output so every chart point can be traced back.
- Keep parser changes covered by tests before using the result for client work.
- Prefer CSV and SVG for first delivery because they are easy to inspect without notebook setup.
- If the client needs dashboards later, use these normalized records as the stable input layer.
