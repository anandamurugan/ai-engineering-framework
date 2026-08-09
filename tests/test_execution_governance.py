"""Focused tests for Sprint 5.3 deterministic execution governance."""

import json
import tempfile
import unittest
from pathlib import Path

from tools.execution.budget import BudgetEvaluator
from tools.execution.checkpoint import CheckpointStore
from tools.execution.loop import LoopDetector
from tools.execution.models import (
    CHECKPOINT_FORMAT_VERSION,
    BudgetAction,
    BudgetLimit,
    BudgetProfile,
    BudgetState,
    BudgetStatus,
    CapabilityTier,
    ExecutionCheckpoint,
    ExecutionStatus,
    FactorLevel,
    FailureEvent,
    LoopResponse,
    RoutingFactors,
)
from tools.execution.routing import Router, RoutingPolicy


class BudgetTests(unittest.TestCase):
    def profile(self, *limits):
        return BudgetProfile("test-profile", tuple(limits))

    def test_within_budget(self):
        profile = self.profile(
            BudgetLimit("files_loaded", 10, BudgetAction.WARN, False)
        )
        result = BudgetEvaluator(profile).evaluate(
            BudgetState({"files_loaded": 4}, "file_loaded")
        )[0]
        self.assertEqual(BudgetStatus.WITHIN_BUDGET, result.status)
        self.assertIsNone(result.required_response)

    def test_soft_threshold(self):
        profile = self.profile(
            BudgetLimit("tool_invocations", 5, BudgetAction.CHECKPOINT, False)
        )
        result = BudgetEvaluator(profile).evaluate(
            BudgetState({"tool_invocations": 5}, "tool_completed")
        )[0]
        self.assertEqual(BudgetStatus.SOFT_LIMIT, result.status)
        self.assertEqual(BudgetAction.CHECKPOINT, result.required_response)

    def test_hard_threshold(self):
        profile = self.profile(
            BudgetLimit("retries", 2, BudgetAction.STOP, True)
        )
        result = BudgetEvaluator(profile).evaluate(
            BudgetState({"retries": 3}, "retry_failed")
        )[0]
        self.assertEqual(BudgetStatus.HARD_LIMIT, result.status)
        self.assertIn("must not be removed", result.message)

    def test_reassess_and_human_states(self):
        profile = self.profile(
            BudgetLimit("context_expansions", 2, BudgetAction.REASSESS, False),
            BudgetLimit("equivalent_failures", 2, BudgetAction.REQUEST_HUMAN, True),
        )
        results = BudgetEvaluator(profile).evaluate(
            BudgetState(
                {"context_expansions": 2, "equivalent_failures": 2}, "loop_detected"
            )
        )
        self.assertEqual(BudgetStatus.REASSESS_REQUIRED, results[0].status)
        self.assertEqual(BudgetStatus.HUMAN_REQUIRED, results[1].status)

    def test_multiple_dimensions_are_independent(self):
        profile = self.profile(
            BudgetLimit("files_loaded", 3, BudgetAction.WARN, False),
            BudgetLimit("context_bytes", 100, BudgetAction.STOP, True),
        )
        results = BudgetEvaluator(profile).evaluate(
            BudgetState({"files_loaded": 2, "context_bytes": 100}, "context_loaded")
        )
        self.assertEqual(BudgetStatus.WITHIN_BUDGET, results[0].status)
        self.assertEqual(BudgetStatus.HARD_LIMIT, results[1].status)

    def test_unknown_token_telemetry_is_not_inferred(self):
        profile = self.profile(
            BudgetLimit("tokens", 1000, BudgetAction.WARN, False)
        )
        result = BudgetEvaluator(profile).evaluate(BudgetState({}, "measurement"))[0]
        self.assertEqual(BudgetStatus.UNAVAILABLE, result.status)
        self.assertIsNone(result.current_value)

    def test_thresholds_are_profile_configurable(self):
        low = BudgetEvaluator(
            self.profile(BudgetLimit("files_loaded", 2, BudgetAction.WARN, False))
        ).evaluate(BudgetState({"files_loaded": 3}, "load"))[0]
        high = BudgetEvaluator(
            self.profile(BudgetLimit("files_loaded", 4, BudgetAction.WARN, False))
        ).evaluate(BudgetState({"files_loaded": 3}, "load"))[0]
        self.assertEqual(BudgetStatus.SOFT_LIMIT, low.status)
        self.assertEqual(BudgetStatus.WITHIN_BUDGET, high.status)

    def test_context_manifest_metrics_are_consumed_without_duplication(self):
        manifest = {
            "selected": [{"path": "one"}, {"path": "two"}],
            "metrics": {"files_selected": 2, "expansion_levels": [0, 1, 3]},
        }
        state = BudgetEvaluator.from_context_manifest(manifest)
        self.assertEqual(2.0, state.values["files_loaded"])
        self.assertEqual(2.0, state.values["context_expansions"])

    def test_unsupported_and_duplicate_dimensions_fail(self):
        with self.assertRaises(ValueError):
            BudgetEvaluator(
                self.profile(BudgetLimit("imaginary", 1, BudgetAction.WARN, False))
            )
        with self.assertRaises(ValueError):
            self.profile(
                BudgetLimit("retries", 1, BudgetAction.WARN, False),
                BudgetLimit("retries", 2, BudgetAction.STOP, True),
            )


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.path = Path(self.temporary.name) / "checkpoint.json"

    def tearDown(self):
        self.temporary.cleanup()

    def checkpoint(self, **overrides):
        values = {
            "format_version": CHECKPOINT_FORMAT_VERSION,
            "repository_commit": "abc123",
            "execution_id": "EXEC-001",
            "task_id": "EFF-BUD-001",
            "objective": "Test execution governance",
            "scope": ("tools/execution",),
            "selected_context": ("product/stories/EFF-BUD-001.md",),
            "inspected_assets": ("tools/context/README.md",),
            "changed_assets": ("tools/execution/models.py",),
            "applicable_standards": ("STD-TEST-001",),
            "decisions": ("Use deterministic policy",),
            "assumptions": ("Repository is current",),
            "evidence_references": (".execution-reports/budget.json",),
            "validation_status": "PASS",
            "unresolved_items": (),
            "budget_state": {"retries": 1, "tokens": None},
            "retry_state": {"attempts": 1},
            "loop_state": {"detected": False},
            "routing_tier": CapabilityTier.GENERAL_ENGINEERING,
            "escalation_history": ("Tier 2 to Tier 3",),
            "next_recommended_action": "Run tests",
            "execution_status": ExecutionStatus.RUNNING,
            "restricted_context_present": True,
        }
        values.update(overrides)
        return ExecutionCheckpoint(**values)

    def test_serialization_and_state_preservation(self):
        checkpoint = self.checkpoint()
        CheckpointStore.write(checkpoint, self.path)
        loaded = CheckpointStore.read(self.path)
        self.assertEqual(checkpoint, loaded)
        self.assertEqual({"retries": 1, "tokens": None}, loaded.budget_state)
        self.assertEqual({"attempts": 1}, loaded.retry_state)
        self.assertEqual(CapabilityTier.GENERAL_ENGINEERING, loaded.routing_tier)
        self.assertTrue(loaded.restricted_context_present)

    def test_current_checkpoint_resume(self):
        result = CheckpointStore.resume(self.checkpoint(), "abc123")
        self.assertEqual("CURRENT_CHECKPOINT", result.status)
        self.assertTrue(result.compatible)

    def test_stale_checkpoint_requires_revalidation(self):
        result = CheckpointStore.resume(self.checkpoint(), "different")
        self.assertEqual("STALE_CHECKPOINT", result.status)
        self.assertTrue(result.revalidation_required)

    def test_unsupported_checkpoint_is_rejected(self):
        with self.assertRaises(ValueError):
            CheckpointStore.validate(self.checkpoint(format_version="99"))

    def test_checkpoint_is_explicitly_not_approval(self):
        value = self.checkpoint().to_dict()
        self.assertEqual("DERIVED_EXECUTION_STATE_NOT_APPROVAL", value["authority"])
        self.assertNotIn("approved", value)

    def test_checkpoint_does_not_store_source_bodies(self):
        value = json.dumps(self.checkpoint().to_dict())
        self.assertNotIn("source_body", value)
        self.assertNotIn("raw_log", value)


class LoopTests(unittest.TestCase):
    def event(self, outcome="failure", category="test_failure"):
        return FailureEvent("test", "unit-test", outcome, category, "module.py")

    def test_repeated_identical_failure_detected(self):
        result = LoopDetector().evaluate(
            (self.event(), self.event()), threshold=2, response=LoopResponse.REASSESS
        )
        self.assertTrue(result.detected)
        self.assertEqual(LoopResponse.REASSESS, result.response)

    def test_distinct_failure_is_not_same_loop(self):
        result = LoopDetector().evaluate(
            (self.event(category="syntax"), self.event(category="assertion")),
            threshold=2,
            response=LoopResponse.STOP,
        )
        self.assertFalse(result.detected)
        self.assertEqual(LoopResponse.RETRY_ALLOWED, result.response)

    def test_threshold_is_policy_driven(self):
        events = (self.event(), self.event())
        self.assertTrue(
            LoopDetector().evaluate(events, threshold=2, response=LoopResponse.REASSESS).detected
        )
        self.assertFalse(
            LoopDetector().evaluate(events, threshold=3, response=LoopResponse.REASSESS).detected
        )

    def test_configured_escalate_stop_and_human_responses(self):
        events = (self.event(),)
        for response in (
            LoopResponse.ESCALATE_CAPABILITY,
            LoopResponse.STOP,
            LoopResponse.REQUEST_HUMAN,
            LoopResponse.EXPAND_CONTEXT,
        ):
            self.assertEqual(
                response,
                LoopDetector().evaluate(events, threshold=1, response=response).response,
            )

    def test_signature_normalizes_case_and_whitespace(self):
        first = FailureEvent(" Test ", "UNIT-TEST", "Failed  assertion", "Error", "A.py")
        second = FailureEvent("test", "unit-test", "failed assertion", "error", "a.py")
        self.assertEqual(LoopDetector.signature(first), LoopDetector.signature(second))

    def test_signature_is_bounded_hash_not_raw_log(self):
        signature = LoopDetector.signature(self.event(outcome="secret-looking raw text"))
        self.assertEqual(64, len(signature))
        self.assertNotIn("secret", signature)


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.router = Router(RoutingPolicy.baseline())

    def decide(self, classification, current=CapabilityTier.DETERMINISTIC, **kwargs):
        return self.router.decide(
            current,
            RoutingFactors(task_classification=classification, **kwargs),
        )

    def test_deterministic_work_routes_tier_one(self):
        self.assertEqual(
            CapabilityTier.DETERMINISTIC,
            self.decide("deterministic").recommended_tier,
        )

    def test_lightweight_and_general_reasoning(self):
        self.assertEqual(
            CapabilityTier.LIGHTWEIGHT_REASONING,
            self.decide("lightweight_reasoning").recommended_tier,
        )
        self.assertEqual(
            CapabilityTier.GENERAL_ENGINEERING,
            self.decide("general_engineering").recommended_tier,
        )

    def test_high_complexity_or_ambiguity_routes_tier_four(self):
        for factor in ("complexity", "ambiguity", "architecture_significance"):
            decision = self.decide("general_engineering", **{factor: FactorLevel.HIGH})
            self.assertEqual(CapabilityTier.ADVANCED_REASONING, decision.recommended_tier)

    def test_governance_decision_routes_tier_five(self):
        decision = self.decide(
            "general_engineering", governance_decision="release_approval"
        )
        self.assertEqual(CapabilityTier.HUMAN_SPECIALIST, decision.recommended_tier)
        self.assertTrue(decision.human_authority_required)
        self.assertTrue(decision.escalation_mandatory)

    def test_tier_five_classification_always_requires_human(self):
        decision = self.decide("governance_decision")
        self.assertEqual(CapabilityTier.HUMAN_SPECIALIST, decision.recommended_tier)
        self.assertTrue(decision.human_authority_required)

    def test_repeated_lower_tier_failure_escalates_once(self):
        decision = self.decide(
            "lightweight_reasoning",
            current=CapabilityTier.LIGHTWEIGHT_REASONING,
            equivalent_failures=2,
        )
        self.assertEqual(CapabilityTier.GENERAL_ENGINEERING, decision.recommended_tier)

    def test_ai_tier_cannot_replace_mandatory_human_authority(self):
        decision = self.decide(
            "advanced_reasoning",
            current=CapabilityTier.ADVANCED_REASONING,
            governance_decision="risk_acceptance",
        )
        self.assertEqual(CapabilityTier.HUMAN_SPECIALIST, decision.recommended_tier)
        self.assertNotEqual(CapabilityTier.ADVANCED_REASONING, decision.recommended_tier)

    def test_de_escalation_for_deterministic_work(self):
        decision = self.decide(
            "deterministic", current=CapabilityTier.ADVANCED_REASONING
        )
        self.assertEqual(CapabilityTier.DETERMINISTIC, decision.recommended_tier)
        self.assertEqual("DE_ESCALATE", decision.transition)

    def test_restricted_context_requires_human_authority(self):
        decision = self.decide("deterministic", restricted_context=True)
        self.assertEqual(CapabilityTier.HUMAN_SPECIALIST, decision.recommended_tier)

    def test_decision_is_vendor_neutral_structured_evidence(self):
        value = self.decide("general_engineering").to_dict()
        self.assertIn("recommended_tier", value)
        self.assertIn("triggering_factors", value)
        self.assertNotIn("model", value)
        self.assertNotIn("provider", value)


if __name__ == "__main__":
    unittest.main()
