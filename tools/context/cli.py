"""Developer-facing entry point for indexing and context selection."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from tools.repository_paths import contained_repository_path

from .repository import RepositoryView
from .selector import ContextSelector


DEFAULT_INDEX = ".context-reports/repository-index.json"
DEFAULT_MANIFEST = ".context-reports/context-manifest.json"


def repository_root(start: Optional[Path] = None) -> Path:
    candidate = (start or Path.cwd()).resolve()
    for path in (candidate,) + tuple(candidate.parents):
        if (path / ".git").exists() and (path / "tools").is_dir():
            return path
    raise RuntimeError("repository root could not be resolved")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        prog="python3 -m tools.context",
        description="Build derived repository intelligence and select explainable context.",
    )
    value.add_argument("--root", type=Path, help="repository root; defaults to discovery")
    subcommands = value.add_subparsers(dest="command", required=True)

    index = subcommands.add_parser("index", help="build the derived repository asset index")
    index.add_argument("--output", default=DEFAULT_INDEX)

    select = subcommands.add_parser("select", help="select Minimum Sufficient Context")
    select.add_argument("--story", help="story tracking ID, with or without STORY- prefix")
    select.add_argument("--asset", help="governed framework asset ID")
    select.add_argument("--target", action="append", default=[], help="explicit target path")
    select.add_argument("--index", default=DEFAULT_INDEX, help="index evidence path")
    select.add_argument("--output", default=DEFAULT_MANIFEST)
    select.add_argument("--expand-to", type=int, default=4, choices=range(0, 6))
    select.add_argument("--full-fallback", action="store_true")
    select.add_argument(
        "--restricted-path",
        action="append",
        default=[],
        help="restricted path or glob; selection records but does not authorize it",
    )
    return value


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        root = repository_root(arguments.root)
    except RuntimeError as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 2
    view = RepositoryView(root)

    if arguments.command == "index":
        try:
            output = contained_repository_path(
                root, arguments.output, description="context evidence path"
            )
        except ValueError as error:
            print("ERROR: {}".format(error), file=sys.stderr)
            return 2
        index = view.build()
        view.write(index, output)
        print(
            "Indexed {} assets and {} relationships from {} source reads in {} ms.".format(
                index.metrics.assets_produced,
                index.metrics.relationships_produced,
                index.metrics.source_reads,
                index.metrics.generation_duration_ms,
            )
        )
        print("Index evidence: {}".format(output))
        if index.duplicates:
            print("ERROR: duplicate framework IDs prevent authoritative lookup.", file=sys.stderr)
            return 1
        return 0

    task_reference = arguments.story or arguments.asset
    if arguments.story and arguments.asset:
        print("ERROR: choose either --story or --asset.", file=sys.stderr)
        return 2
    if not task_reference and not arguments.target:
        print("ERROR: select requires --story, --asset, or --target.", file=sys.stderr)
        return 2

    try:
        index_path = contained_repository_path(
            root, arguments.index, description="context evidence path"
        )
        output = contained_repository_path(
            root, arguments.output, description="context evidence path"
        )
    except ValueError as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 2
    regenerated = False
    if index_path.exists():
        index = view.read(index_path)
        fresh, reasons = view.freshness(index)
        if not fresh:
            index = view.build()
            view.write(index, index_path)
            regenerated = True
            fresh, reasons = view.freshness(index)
    else:
        index = view.build()
        view.write(index, index_path)
        regenerated = True
        fresh, reasons = view.freshness(index)

    selector = ContextSelector(
        root,
        index,
        restricted_patterns=arguments.restricted_path,
        index_fresh=fresh,
        freshness_reasons=reasons,
    )
    manifest = selector.select(
        task_reference=task_reference,
        target_paths=arguments.target,
        expansion_level=arguments.expand_to,
        full_fallback=arguments.full_fallback,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "Selected {} files; {} restricted; {} unresolved; fallback required: {}.".format(
            manifest.metrics.files_selected,
            manifest.metrics.files_restricted,
            manifest.metrics.unresolved_references,
            str(manifest.fallback_required).lower(),
        )
    )
    if regenerated:
        print("Repository index was generated or refreshed before selection.")
    print("Context manifest: {}".format(output))
    return 0 if not manifest.unresolved and not manifest.restricted else 1
