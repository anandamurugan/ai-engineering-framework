"""Configurable deterministic execution-budget evaluation."""

from typing import Dict, Iterable, Optional, Tuple

from .models import (
    BudgetAction,
    BudgetEvaluation,
    BudgetProfile,
    BudgetState,
    BudgetStatus,
)


SUPPORTED_DIMENSIONS = (
    "files_loaded",
    "context_bytes",
    "context_expansions",
    "repository_traversals",
    "retrieval_operations",
    "tool_invocations",
    "execution_invocations",
    "retries",
    "equivalent_failures",
    "elapsed_duration_seconds",
    "tokens",
)


class BudgetEvaluator:
    """Evaluate supplied measurements without inferring unavailable usage."""

    def __init__(self, profile: BudgetProfile):
        unsupported = sorted(
            item.dimension
            for item in profile.limits
            if item.dimension not in SUPPORTED_DIMENSIONS
        )
        if unsupported:
            raise ValueError("unsupported budget dimensions: {}".format(", ".join(unsupported)))
        self.profile = profile

    def evaluate(self, state: BudgetState) -> Tuple[BudgetEvaluation, ...]:
        return tuple(self._evaluate_limit(limit, state) for limit in self.profile.limits)

    @staticmethod
    def from_context_manifest(
        manifest: Dict[str, object],
        *,
        existing: Optional[Dict[str, Optional[float]]] = None,
        triggering_event: str = "context_manifest_loaded",
    ) -> BudgetState:
        values = dict(existing or {})
        metrics = manifest.get("metrics", {})
        selected = manifest.get("selected", [])
        if isinstance(metrics, dict):
            files_selected = metrics.get("files_selected")
            if isinstance(files_selected, (int, float)):
                values["files_loaded"] = float(files_selected)
            levels = metrics.get("expansion_levels")
            if isinstance(levels, list):
                values["context_expansions"] = float(len([level for level in levels if level > 0]))
        if isinstance(selected, list):
            values.setdefault("files_loaded", float(len(selected)))
        return BudgetState(values=values, triggering_event=triggering_event)

    def _evaluate_limit(self, limit, state):
        current = state.values.get(limit.dimension)
        if current is None:
            return BudgetEvaluation(
                dimension=limit.dimension,
                current_value=None,
                limit=limit.threshold,
                status=BudgetStatus.UNAVAILABLE,
                required_response=None,
                triggering_event=state.triggering_event,
                message="Usage was not supplied or measured; no value was inferred.",
            )
        reached = current >= limit.threshold
        if not reached:
            return BudgetEvaluation(
                dimension=limit.dimension,
                current_value=current,
                limit=limit.threshold,
                status=BudgetStatus.WITHIN_BUDGET,
                required_response=None,
                triggering_event=state.triggering_event,
                message="Measured usage remains within the configured threshold.",
            )
        if limit.action is BudgetAction.REQUEST_HUMAN:
            status = BudgetStatus.HUMAN_REQUIRED
        elif limit.action in (BudgetAction.REASSESS, BudgetAction.REQUIRE_JUSTIFICATION):
            status = BudgetStatus.REASSESS_REQUIRED
        else:
            status = BudgetStatus.HARD_LIMIT if limit.hard else BudgetStatus.SOFT_LIMIT
        return BudgetEvaluation(
            dimension=limit.dimension,
            current_value=current,
            limit=limit.threshold,
            status=status,
            required_response=limit.action,
            triggering_event=state.triggering_event,
            message=(
                "Configured {} threshold reached; required response is {}. "
                "Required context, validation, evidence, and review must not be removed."
            ).format("hard" if limit.hard else "soft", limit.action.value),
        )
