"""Durable, provenance-aware execution checkpoint persistence."""

import json
from pathlib import Path

from .models import CHECKPOINT_FORMAT_VERSION, ExecutionCheckpoint, ResumeEvaluation


class CheckpointStore:
    """Read, write, and evaluate checkpoint compatibility without approving state."""

    @staticmethod
    def write(checkpoint: ExecutionCheckpoint, path: Path) -> None:
        CheckpointStore.validate(checkpoint)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(checkpoint.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def read(path: Path) -> ExecutionCheckpoint:
        value = json.loads(path.read_text(encoding="utf-8"))
        checkpoint = ExecutionCheckpoint.from_dict(value)
        CheckpointStore.validate(checkpoint)
        return checkpoint

    @staticmethod
    def validate(checkpoint: ExecutionCheckpoint) -> None:
        if checkpoint.format_version != CHECKPOINT_FORMAT_VERSION:
            raise ValueError("unsupported checkpoint format version")
        if not checkpoint.execution_id or not checkpoint.task_id:
            raise ValueError("checkpoint requires execution and task identifiers")
        if not checkpoint.objective or not checkpoint.next_recommended_action:
            raise ValueError("checkpoint requires objective and next action")

    @staticmethod
    def resume(
        checkpoint: ExecutionCheckpoint, current_repository_commit: str
    ) -> ResumeEvaluation:
        reasons = []
        if checkpoint.format_version != CHECKPOINT_FORMAT_VERSION:
            reasons.append("checkpoint format version is unsupported")
        if checkpoint.repository_commit != current_repository_commit:
            reasons.append("repository commit differs from checkpoint provenance")
        if reasons:
            return ResumeEvaluation(
                status="STALE_CHECKPOINT",
                compatible=False,
                revalidation_required=True,
                reasons=tuple(reasons),
            )
        return ResumeEvaluation(
            status="CURRENT_CHECKPOINT",
            compatible=True,
            revalidation_required=False,
            reasons=(),
        )
