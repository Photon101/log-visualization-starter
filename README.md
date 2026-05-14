# Log Visualization Starter

No-dependency Python starter for extracting metrics from simulation or service logs and producing decision-ready summaries.

It is designed as proof-of-work for data visualization jobs where the raw input is "weeks of logs" rather than a tidy dataset.

## What It Does

- Parses timestamped lines with `key=value` metrics.
- Accepts mixed text around the metrics.
- Writes a normalized `records.csv`.
- Writes a `summary.csv` with min, max, average, and sample count per metric.
- Generates simple SVG line plots without matplotlib or notebook setup.
- Includes tests that run without external data.

## Quick Start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest
python -m log_visualization_starter examples/logs --out examples/output
```

Generated files:

- `records.csv`
- `summary.csv`
- one SVG per metric, for example `residual.svg`

## Example Log Line

```text
2026-05-01T10:00:00Z step=120 pressure=0.83 velocity=1.41 residual=0.008
```

## Production Next Steps

For client work, the next step is adapting the parser to the exact log format, defining the important plots, and adding a short interpretation report around the charts.

