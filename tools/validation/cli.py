"""Command-line interface for repository validation."""

import argparse
from pathlib import Path
from typing import Optional, Sequence

from .registry import VALIDATORS
from .runner import format_console_report, run_validators


DEFAULT_REPORT = Path(".validation-reports/validation-report.json")


def find_repository_root(start: Optional[Path] = None) -> Path:
    """Find the nearest parent containing the repository instruction file."""

    candidate = (start or Path.cwd()).resolve()
    for path in (candidate,) + tuple(candidate.parents):
        if (path / "AGENTS.md").is_file() and (path / ".git").exists():
            return path
    return candidate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run registered Enterprise Agentic SDLC validation checks."
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Repository root (auto-detected by default).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="JSON report path relative to the repository root.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    repository_root = (args.root or find_repository_root()).resolve()
    report_path = args.report or DEFAULT_REPORT
    if not report_path.is_absolute():
        report_path = repository_root / report_path

    validation_run = run_validators(repository_root, VALIDATORS)
    validation_run.write_json(report_path)
    print(format_console_report(validation_run))
    print("JSON report: {}".format(report_path))
    return validation_run.exit_code
