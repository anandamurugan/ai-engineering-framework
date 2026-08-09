"""Conservative vendor-neutral capability routing recommendations."""

from dataclasses import dataclass
from typing import Dict, FrozenSet, Tuple

from .models import CapabilityTier, FactorLevel, RoutingDecision, RoutingFactors


HUMAN_ONLY_DECISIONS = frozenset(
    {
        "architecture_approval",
        "risk_acceptance",
        "security_exception",
        "production_authorization",
        "release_approval",
        "governance_exception",
    }
)


@dataclass(frozen=True)
class RoutingPolicy:
    """Small explicit routing policy with no provider or model mapping."""

    minimum_tiers: Dict[str, CapabilityTier]
    human_only_decisions: FrozenSet[str]
    repeated_failure_escalation_threshold: int

    def __post_init__(self):
        if self.repeated_failure_escalation_threshold < 1:
            raise ValueError("repeated-failure threshold must be at least one")

    @classmethod
    def baseline(cls) -> "RoutingPolicy":
        return cls(
            minimum_tiers={
                "deterministic": CapabilityTier.DETERMINISTIC,
                "lightweight_reasoning": CapabilityTier.LIGHTWEIGHT_REASONING,
                "general_engineering": CapabilityTier.GENERAL_ENGINEERING,
                "advanced_reasoning": CapabilityTier.ADVANCED_REASONING,
                "governance_decision": CapabilityTier.HUMAN_SPECIALIST,
            },
            human_only_decisions=HUMAN_ONLY_DECISIONS,
            repeated_failure_escalation_threshold=2,
        )


class Router:
    """Recommend a conceptual capability tier without executing a model."""

    def __init__(self, policy: RoutingPolicy):
        self.policy = policy

    def decide(
        self, current_tier: CapabilityTier, factors: RoutingFactors
    ) -> RoutingDecision:
        reasons = []
        triggers = []
        human_required = False
        mandatory = False

        if factors.governance_decision:
            triggers.append("governance_decision={}".format(factors.governance_decision))
            if factors.governance_decision in self.policy.human_only_decisions:
                human_required = True
                mandatory = True
                reasons.append("Governed decision requires accountable human or specialist authority.")
        if factors.restricted_context:
            triggers.append("restricted_context=true")
            human_required = True
            mandatory = True
            reasons.append("Restricted required context needs authorization before use.")
        if factors.hard_budget_pressure:
            triggers.append("hard_budget_pressure=true")
            reasons.append("Hard budget pressure requires reassessment; controls cannot be skipped.")

        if human_required:
            recommended = CapabilityTier.HUMAN_SPECIALIST
        else:
            recommended = self.policy.minimum_tiers.get(
                factors.task_classification, CapabilityTier.GENERAL_ENGINEERING
            )
            high_factors = {
                "complexity": factors.complexity,
                "change_scope": factors.change_scope,
                "security_sensitivity": factors.security_sensitivity,
                "production_impact": factors.production_impact,
                "architecture_significance": factors.architecture_significance,
                "ambiguity": factors.ambiguity,
                "reasoning_depth": factors.reasoning_depth,
            }
            for name, value in high_factors.items():
                if value >= FactorLevel.HIGH:
                    triggers.append("{}={}".format(name, value.name))
            if any(value >= FactorLevel.HIGH for value in high_factors.values()):
                recommended = max(recommended, CapabilityTier.ADVANCED_REASONING)
                reasons.append("High complexity, ambiguity, impact, sensitivity, or architecture significance requires advanced reasoning.")
            if (
                factors.equivalent_failures
                >= self.policy.repeated_failure_escalation_threshold
                or factors.validation_failures
                >= self.policy.repeated_failure_escalation_threshold
            ):
                triggers.append("repeated_lower_tier_failure")
                recommended = max(
                    recommended,
                    CapabilityTier(min(int(current_tier) + 1, int(CapabilityTier.ADVANCED_REASONING))),
                )
                reasons.append("Repeated failure justifies one bounded capability escalation.")
            if factors.hard_budget_pressure:
                recommended = max(recommended, current_tier)
                mandatory = True

        if recommended is CapabilityTier.HUMAN_SPECIALIST:
            human_required = True
            mandatory = True
            if not any("human" in reason.lower() for reason in reasons):
                reasons.append("Tier 5 always represents accountable human or specialist authority.")

        if recommended > current_tier:
            transition = "ESCALATE"
        elif recommended < current_tier:
            transition = "DE_ESCALATE"
            reasons.append("Current task factors permit return to a lower sufficient tier.")
        else:
            transition = "RETAIN"
        if not reasons:
            reasons.append("Configured minimum tier satisfies the supplied structured factors.")
        return RoutingDecision(
            current_tier=current_tier,
            recommended_tier=recommended,
            reasons=tuple(reasons),
            triggering_factors=tuple(sorted(set(triggers))),
            escalation_mandatory=mandatory,
            human_authority_required=human_required,
            transition=transition,
        )
