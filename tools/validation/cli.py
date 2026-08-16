"""Command-line interface for repository validation."""

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from tools.context.repository import RepositoryView
from tools.repository_paths import contained_repository_path

from .models import ValidationMode
from .registry import VALIDATORS
from .runner import format_console_report, run_validators
from .targeting import AffectedScopePlanner, GitChangeDiscovery


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
        "--mode",
        choices=("full", "asset", "changed", "affected"),
        default="full",
        help="Validation mode; full remains the default and release-gate mode.",
    )
    parser.add_argument("--asset", action="append", default=[], help="Framework ID to validate.")
    parser.add_argument("--paths", nargs="*", default=[], help="Repository-relative paths to validate.")
    parser.add_argument("--base", help="Base Git revision for changed/affected modes.")
    parser.add_argument("--head", default="HEAD", help="Head Git revision (default: HEAD).")
    parser.add_argument(
        "--working-tree", action="store_true", help="Discover staged, unstaged, and untracked changes."
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
    try:
        report_path = contained_repository_path(
            repository_root, report_path, description="validation evidence path"
        )
    except ValueError as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 2

    view = RepositoryView(repository_root)
    index = view.build()
    requested_mode = {
        "full": ValidationMode.FULL,
        "asset": ValidationMode.TARGETED_ASSET,
        "changed": ValidationMode.CHANGED_FILES,
        "affected": ValidationMode.AFFECTED_CLOSURE,
    }[args.mode]
    paths = list(args.paths)
    ignored = []
    unresolved = []
    base_commit = None
    head_commit = index.source_commit
    if requested_mode in (ValidationMode.CHANGED_FILES, ValidationMode.AFFECTED_CLOSURE):
        if not args.working_tree and not args.base:
            build_parser().error("--base or --working-tree is required for changed/affected mode")
        changes = GitChangeDiscovery(repository_root).discover(
            base=args.base, head=args.head, working_tree=args.working_tree
        )
        paths.extend(changes.changed_paths)
        ignored.extend(changes.ignored_paths)
        unresolved.extend(changes.unresolved_paths)
        base_commit = changes.base
        head_commit = changes.head
    plan = AffectedScopePlanner(repository_root, index).plan(
        requested_mode, paths=paths, asset_ids=args.asset, base_commit=base_commit,
        head_commit=head_commit, ignored_paths=ignored, unresolved_paths=unresolved,
    )
    validation_run = run_validators(
        repository_root, VALIDATORS, plan=plan, repository_view=index
    )
    validation_run.write_json(report_path)
    print(format_console_report(validation_run))
    if plan.fallback_used:
        print("Full-validation fallback: {}".format("; ".join(plan.fallback_reasons)))
    print("JSON report: {}".format(report_path))
    return validation_run.exit_code
