"""Privacy-aware deterministic equivalent-failure detection."""

import hashlib
import re
from typing import Sequence

from .models import FailureEvent, LoopEvaluation, LoopResponse


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


class LoopDetector:
    """Detect repeated normalized event signatures using an explicit policy threshold."""

    @staticmethod
    def signature(event: FailureEvent) -> str:
        material = "\x1f".join(
            _normalize(value)
            for value in (
                event.action_type,
                event.tool_identifier,
                event.outcome,
                event.error_category,
                event.affected_asset or "",
            )
        )
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def evaluate(
        self,
        events: Sequence[FailureEvent],
        *,
        threshold: int,
        response: LoopResponse,
    ) -> LoopEvaluation:
        if threshold < 1:
            raise ValueError("loop threshold must be at least one")
        if not events:
            return LoopEvaluation(
                signature="",
                equivalent_failures=0,
                threshold=threshold,
                detected=False,
                response=LoopResponse.RETRY_ALLOWED,
                reason="No failure event was supplied.",
            )
        current_signature = self.signature(events[-1])
        count = sum(self.signature(item) == current_signature for item in events)
        detected = count >= threshold
        return LoopEvaluation(
            signature=current_signature,
            equivalent_failures=count,
            threshold=threshold,
            detected=detected,
            response=response if detected else LoopResponse.RETRY_ALLOWED,
            reason=(
                "Equivalent failure threshold reached; apply configured response."
                if detected
                else "Equivalent failure remains below the configured threshold."
            ),
        )
