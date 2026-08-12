"""Minimal local interface for deterministic execution governance."""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from tools.context.cli import repository_root
from tools.context.repository import RepositoryView

from .budget import BudgetEvaluator
from .checkpoint import CheckpointStore
from .evidence import read_json, write_json
from .loop import LoopDetector
from .models import (
    EVIDENCE_FORMAT_VERSION,
    BudgetAction,
    BudgetLimit,
    BudgetProfile,
    BudgetState,
    CapabilityTier,
    ExecutionCheckpoint,
    ExecutionEvidence,
    FactorLevel,
    FailureEvent,
    LoopResponse,
    RoutingFactors,
)
from .routing import Router, RoutingPolicy


DEFAULT_DIRECTORY = ".execution-reports"


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        prog="python3 -m tools.execution",
        description="Evaluate execution budgets, loops, checkpoints, and routing policy.",
    )
    value.add_argument("--root", type=Path, help="repository root; defaults to discovery")
    commands = value.add_subparsers(dest="command", required=True)

    budget = commands.add_parser("budget", help="evaluate measured state against a profile")
    budget.add_argument("--profile", required=True)
    budget.add_argument("--state", required=True)
    budget.add_argument("--context-manifest")
    budget.add_argument("--execution-id", required=True)
    budget.add_argument("--output", default=DEFAULT_DIRECTORY + "/budget-evidence.json")

    checkpoint = commands.add_parser("checkpoint", help="write or inspect a checkpoint")
    checkpoint_commands = checkpoint.add_subparsers(dest="checkpoint_command", required=True)
    create = checkpoint_commands.add_parser("create")
    create.add_argument("--input", required=True)
    create.add_argument("--output", default=DEFAULT_DIRECTORY + "/checkpoint.json")
    inspect = checkpoint_commands.add_parser("inspect")
    inspect.add_argument("--checkpoint", required=True)

    loop = commands.add_parser("loop", help="evaluate normalized failure events")
    loop.add_argument("--events", required=True)
    loop.add_argument("--threshold", required=True, type=int)
    loop.add_argument("--response", required=True, choices=[item.value for item in LoopResponse])
    loop.add_argument("--output", default=DEFAULT_DIRECTORY + "/loop-evidence.json")

    route = commands.add_parser("route", help="produce a vendor-neutral tier recommendation")
    route.add_argument("--factors", required=True)
    route.add_argument("--current-tier", required=True, type=int, choices=range(1, 6))
    route.add_argument("--output", default=DEFAULT_DIRECTORY + "/routing-evidence.json")
    return value


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        root = repository_root(arguments.root)
    except RuntimeError as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 2
    try:
        for name in (
            "profile",
            "state",
            "context_manifest",
            "input",
            "checkpoint",
            "events",
            "factors",
            "output",
        ):
            raw_path = getattr(arguments, name, None)
            if raw_path:
                setattr(arguments, name, _repository_path(root, raw_path))
    except ValueError as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 2
    commit = RepositoryView(root).current_commit()

    if arguments.command == "budget":
        profile = _profile(read_json(arguments.profile))
        state_value = read_json(arguments.state)
        state = BudgetState(
            values=state_value.get("values", {}),
            triggering_event=state_value.get("triggering_event", "state_loaded"),
            measured_at=state_value.get("measured_at"),
        )
        restricted = False
        fallback = False
        expansions = int(state.values.get("context_expansions") or 0)
        if arguments.context_manifest:
            manifest = read_json(arguments.context_manifest)
            state = BudgetEvaluator.from_context_manifest(
                manifest, existing=state.values, triggering_event=state.triggering_event
            )
            restricted = bool(manifest.get("restricted"))
            fallback = bool(manifest.get("fallback_required"))
            expansions = int(state.values.get("context_expansions") or 0)
        evaluations = BudgetEvaluator(profile).evaluate(state)
        evidence = ExecutionEvidence(
            format_version=EVIDENCE_FORMAT_VERSION,
            execution_id=arguments.execution_id,
            repository_commit=commit,
            operation="budget_evaluation",
            budget_evaluations=evaluations,
            context_expansions=expansions,
            restricted_context_present=restricted,
            fallback_required=fallback,
            human_required=any(
                item.required_response is BudgetAction.REQUEST_HUMAN
                for item in evaluations
            ),
        )
        write_json(evidence.to_dict(), arguments.output)
        print("Evaluated {} budget dimensions.".format(len(evaluations)))
        print("Evidence: {}".format(arguments.output))
        return 0

    if arguments.command == "checkpoint":
        if arguments.checkpoint_command == "create":
            checkpoint = ExecutionCheckpoint.from_dict(read_json(arguments.input))
            CheckpointStore.write(checkpoint, arguments.output)
            print("Checkpoint: {}".format(arguments.output))
            return 0
        checkpoint = CheckpointStore.read(arguments.checkpoint)
        resume = CheckpointStore.resume(checkpoint, commit)
        print("{}: {}".format(resume.status, "; ".join(resume.reasons) or "compatible"))
        return 0 if resume.compatible else 1

    if arguments.command == "loop":
        value = read_json(arguments.events)
        events = tuple(FailureEvent(**item) for item in value.get("events", []))
        evaluation = LoopDetector().evaluate(
            events,
            threshold=arguments.threshold,
            response=LoopResponse(arguments.response),
        )
        write_json(evaluation.to_dict(), arguments.output)
        print("{}: {}".format(evaluation.response.value, evaluation.reason))
        print("Evidence: {}".format(arguments.output))
        return 0

    value = read_json(arguments.factors)
    factors = _factors(value)
    decision = Router(RoutingPolicy.baseline()).decide(
        CapabilityTier(arguments.current_tier), factors
    )
    write_json(decision.to_dict(), arguments.output)
    print(
        "Tier {} -> Tier {} ({}).".format(
            int(decision.current_tier), int(decision.recommended_tier), decision.transition
        )
    )
    print("Evidence: {}".format(arguments.output))
    return 0


def _repository_path(root: Path, raw_path: str) -> Path:
    candidate = (root / raw_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        raise ValueError("execution evidence path resolves outside the repository")
    return candidate


def _profile(value: Dict[str, Any]) -> BudgetProfile:
    return BudgetProfile(
        profile_id=value["profile_id"],
        limits=tuple(
            BudgetLimit(
                dimension=item["dimension"],
                threshold=float(item["threshold"]),
                action=BudgetAction(item["action"]),
                hard=bool(item["hard"]),
            )
            for item in value["limits"]
        ),
    )


def _factors(value: Dict[str, Any]) -> RoutingFactors:
    level_fields = {
        "complexity",
        "change_scope",
        "security_sensitivity",
        "production_impact",
        "architecture_significance",
        "ambiguity",
        "reversibility",
        "reasoning_depth",
        "required_tool_capability",
    }
    converted = dict(value)
    for field_name in level_fields:
        if field_name in converted:
            raw = converted[field_name]
            converted[field_name] = FactorLevel[raw] if isinstance(raw, str) else FactorLevel(raw)
    return RoutingFactors(**converted)
