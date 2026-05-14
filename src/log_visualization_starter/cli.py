from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="log-visualization",
        description="Parse key=value metrics from logs and write CSV summaries plus SVG plots.",
    )
    parser.add_argument("source", help="Log file or directory containing .log/.txt files")
    parser.add_argument("--out", default="log-output", help="Output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_pipeline(Path(args.source), Path(args.out))
    print(f"records={len(result.records)}")
    print(f"metrics={len(result.metric_names)}")
    print(f"out={result.out_dir}")
    return 0

