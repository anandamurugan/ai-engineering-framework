"""Shared execution-control models and machine-readable evidence contracts."""

from dataclasses import asdict, dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, Optional, Tuple


CHECKPOINT_FORMAT_VERSION = "1.0"
EVIDENCE_FORMAT_VERSION = "1.0"


class BudgetAction(str, Enum):
    WARN = "WARN"
    CHECKPOINT = "CHECKPOINT"
    REASSESS = "REASSESS"
    REQUIRE_JUSTIFICATION = "REQUIRE_JUSTIFICATION"
    ESCALATE = "ESCALATE"
    STOP = "STOP"
    REQUEST_HUMAN = "REQUEST_HUMAN"


class BudgetStatus(str, Enum):
    WITHIN_BUDGET = "WITHIN_BUDGET"
    SOFT_LIMIT = "SOFT_LIMIT"
    HARD_LIMIT = "HARD_LIMIT"
    REASSESS_REQUIRED = "REASSESS_REQUIRED"
    HUMAN_REQUIRED = "HUMAN_REQUIRED"
    UNAVAILABLE = "UNAVAILABLE"


class ExecutionStatus(str, Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    REASSESS = "REASSESS"
    WAITING_FOR_CONTEXT = "WAITING_FOR_CONTEXT"
    ESCALATION_REQUIRED = "ESCALATION_REQUIRED"
    WAITING_FOR_HUMAN = "WAITING_FOR_HUMAN"
    STOPPED = "STOPPED"
    COMPLETED = "COMPLETED"


class CapabilityTier(IntEnum):
    DETERMINISTIC = 1
    LIGHTWEIGHT_REASONING = 2
    GENERAL_ENGINEERING = 3
    ADVANCED_REASONING = 4
    HUMAN_SPECIALIST = 5


class FactorLevel(IntEnum):
    NONE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4


class LoopResponse(str, Enum):
    RETRY_ALLOWED = "RETRY_ALLOWED"
    REASSESS = "REASSESS"
    EXPAND_CONTEXT = "EXPAND_CONTEXT"
    ESCALATE_CAPABILITY = "ESCALATE_CAPABILITY"
    STOP = "STOP"
    REQUEST_HUMAN = "REQUEST_HUMAN"


@dataclass(frozen=True)
class BudgetLimit:
    dimension: str
    threshold: float
    action: BudgetAction
    hard: bool

    def __post_init__(self):
        if self.threshold < 0:
            raise ValueError("budget threshold cannot be negative")


@dataclass(frozen=True)
class BudgetProfile:
    profile_id: str
    limits: Tuple[BudgetLimit, ...]

    def __post_init__(self):
        dimensions = [item.dimension for item in self.limits]
        if len(dimensions) != len(set(dimensions)):
            raise ValueError("budget profile dimensions must be unique")


@dataclass(frozen=True)
class BudgetState:
    values: Dict[str, Optional[float]]
    triggering_event: str
    measured_at: Optional[str] = None


@dataclass(frozen=True)
class BudgetEvaluation:
    dimension: str
    current_value: Optional[float]
    limit: float
    status: BudgetStatus
    required_response: Optional[BudgetAction]
    triggering_event: str
    message: str

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["status"] = self.status.value
        value["required_response"] = (
            self.required_response.value if self.required_response else None
        )
        return value


@dataclass(frozen=True)
class FailureEvent:
    action_type: str
    tool_identifier: str
    outcome: str
    error_category: str
    affected_asset: Optional[str] = None


@dataclass(frozen=True)
class LoopEvaluation:
    signature: str
    equivalent_failures: int
    threshold: int
    detected: bool
    response: LoopResponse
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["response"] = self.response.value
        return value


@dataclass(frozen=True)
class RoutingFactors:
    task_classification: str
    complexity: FactorLevel = FactorLevel.LOW
    change_scope: FactorLevel = FactorLevel.LOW
    security_sensitivity: FactorLevel = FactorLevel.NONE
    production_impact: FactorLevel = FactorLevel.NONE
    architecture_significance: FactorLevel = FactorLevel.NONE
    ambiguity: FactorLevel = FactorLevel.LOW
    reversibility: FactorLevel = FactorLevel.LOW
    reasoning_depth: FactorLevel = FactorLevel.LOW
    required_tool_capability: FactorLevel = FactorLevel.LOW
    validation_failures: int = 0
    equivalent_failures: int = 0
    restricted_context: bool = False
    hard_budget_pressure: bool = False
    governance_decision: Optional[str] = None


@dataclass(frozen=True)
class RoutingDecision:
    current_tier: CapabilityTier
    recommended_tier: CapabilityTier
    reasons: Tuple[str, ...]
    triggering_factors: Tuple[str, ...]
    escalation_mandatory: bool
    human_authority_required: bool
    transition: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_tier": int(self.current_tier),
            "current_tier_name": self.current_tier.name,
            "recommended_tier": int(self.recommended_tier),
            "recommended_tier_name": self.recommended_tier.name,
            "reasons": list(self.reasons),
            "triggering_factors": list(self.triggering_factors),
            "escalation_mandatory": self.escalation_mandatory,
            "human_authority_required": self.human_authority_required,
            "transition": self.transition,
        }


@dataclass(frozen=True)
class ExecutionCheckpoint:
    format_version: str
    repository_commit: str
    execution_id: str
    task_id: str
    objective: str
    scope: Tuple[str, ...]
    selected_context: Tuple[str, ...]
    inspected_assets: Tuple[str, ...]
    changed_assets: Tuple[str, ...]
    applicable_standards: Tuple[str, ...]
    decisions: Tuple[str, ...]
    assumptions: Tuple[str, ...]
    evidence_references: Tuple[str, ...]
    validation_status: str
    unresolved_items: Tuple[str, ...]
    budget_state: Dict[str, Optional[float]]
    retry_state: Dict[str, int]
    loop_state: Dict[str, Any]
    routing_tier: CapabilityTier
    escalation_history: Tuple[str, ...]
    next_recommended_action: str
    execution_status: ExecutionStatus
    restricted_context_present: bool = False

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["routing_tier"] = int(self.routing_tier)
        value["execution_status"] = self.execution_status.value
        value["authority"] = "DERIVED_EXECUTION_STATE_NOT_APPROVAL"
        return value

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "ExecutionCheckpoint":
        copied = dict(value)
        copied.pop("authority", None)
        for field_name in (
            "scope",
            "selected_context",
            "inspected_assets",
            "changed_assets",
            "applicable_standards",
            "decisions",
            "assumptions",
            "evidence_references",
            "unresolved_items",
            "escalation_history",
        ):
            copied[field_name] = tuple(copied.get(field_name, []))
        copied["routing_tier"] = CapabilityTier(copied["routing_tier"])
        copied["execution_status"] = ExecutionStatus(copied["execution_status"])
        return cls(**copied)


@dataclass(frozen=True)
class ResumeEvaluation:
    status: str
    compatible: bool
    revalidation_required: bool
    reasons: Tuple[str, ...]


@dataclass(frozen=True)
class ExecutionEvidence:
    format_version: str
    execution_id: str
    repository_commit: str
    operation: str
    budget_evaluations: Tuple[BudgetEvaluation, ...] = ()
    retry_events: int = 0
    loop_evaluations: Tuple[LoopEvaluation, ...] = ()
    context_expansions: int = 0
    restricted_context_present: bool = False
    fallback_required: bool = False
    routing_decisions: Tuple[RoutingDecision, ...] = ()
    checkpoint_references: Tuple[str, ...] = ()
    human_required: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "format_version": self.format_version,
            "execution_id": self.execution_id,
            "repository_commit": self.repository_commit,
            "operation": self.operation,
            "budget_evaluations": [item.to_dict() for item in self.budget_evaluations],
            "retry_events": self.retry_events,
            "loop_evaluations": [item.to_dict() for item in self.loop_evaluations],
            "context_expansions": self.context_expansions,
            "restricted_context_present": self.restricted_context_present,
            "fallback_required": self.fallback_required,
            "routing_decisions": [item.to_dict() for item in self.routing_decisions],
            "checkpoint_references": list(self.checkpoint_references),
            "human_required": self.human_required,
            "authority": "EVIDENCE_ONLY_NOT_APPROVAL",
        }
