"""REL-005 deterministic integration and governance-invariant evidence."""

import tempfile
import unittest
from pathlib import Path

from tools.context.repository import RepositoryView
from tools.context.selector import ContextSelector
from tools.execution.budget import BudgetEvaluator
from tools.execution.checkpoint import CheckpointStore
from tools.execution.loop import LoopDetector
from tools.execution.models import (
    CHECKPOINT_FORMAT_VERSION,
    BudgetAction,
    BudgetLimit,
    BudgetProfile,
    BudgetStatus,
    CapabilityTier,
    ExecutionCheckpoint,
    ExecutionStatus,
    FailureEvent,
    LoopResponse,
    RoutingFactors,
)
from tools.execution.routing import Router, RoutingPolicy
from tools.validation.models import Severity, Status, ValidationMode, Validator
from tools.validation.runner import run_validators
from tools.validation.targeting import AffectedScopePlanner


ROOT = Path(__file__).resolve().parents[1]


class FailingValidator(Validator):
    validator_id = "TEST-ERROR-001"
    name = "Governance error fixture"
    description = "Proves an error remains release-blocking in targeted execution."
    default_severity = Severity.ERROR

    def validate(self, context):
        return (self.result(status=Status.FAIL, message="Required control failed."),)


class ReleaseEfficiencyScenarioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view = RepositoryView(ROOT)
        cls.index = cls.view.build(source_commit=cls.view.current_commit())

    def test_end_to_end_failure_path_reaches_human_with_attributable_evidence(self):
        manifest = ContextSelector(ROOT, self.index).select(
            task_reference="EFF-GOV-001", expansion_level=1
        )
        self.assertTrue(manifest.selected)
        self.assertTrue(all(item.reason for item in manifest.selected))
        self.assertTrue(manifest.completeness["index_fresh"])

        budget = BudgetEvaluator(
            BudgetProfile(
                "release-closeout-fixture",
                (
                    BudgetLimit(
                        "files_loaded", 1, BudgetAction.REASSESS, True
                    ),
                    BudgetLimit("tokens", 1, BudgetAction.WARN, False),
                ),
            )
        ).evaluate(BudgetEvaluator.from_context_manifest(manifest.to_dict()))
        self.assertEqual(BudgetStatus.REASSESS_REQUIRED, budget[0].status)
        self.assertIn("validation, evidence, and review", budget[0].message)
        self.assertEqual(BudgetStatus.UNAVAILABLE, budget[1].status)

        initial_route = Router(RoutingPolicy.baseline()).decide(
            CapabilityTier.DETERMINISTIC,
            RoutingFactors(
                task_classification="general_engineering", hard_budget_pressure=True
            ),
        )
        self.assertGreaterEqual(initial_route.recommended_tier, CapabilityTier.GENERAL_ENGINEERING)

        failure = FailureEvent(
            "validation", "tools.validation", "required control failed", "validation_error"
        )
        loop = LoopDetector().evaluate(
            (failure, failure), threshold=2, response=LoopResponse.REQUEST_HUMAN
        )
        self.assertTrue(loop.detected)
        self.assertEqual(LoopResponse.REQUEST_HUMAN, loop.response)

        human_route = Router(RoutingPolicy.baseline()).decide(
            CapabilityTier.ADVANCED_REASONING,
            RoutingFactors(
                task_classification="advanced_reasoning",
                equivalent_failures=loop.equivalent_failures,
                governance_decision="release_approval",
            ),
        )
        self.assertEqual(CapabilityTier.HUMAN_SPECIALIST, human_route.recommended_tier)
        self.assertTrue(human_route.human_authority_required)

        with tempfile.TemporaryDirectory() as directory:
            checkpoint_path = Path(directory) / "checkpoint.json"
            checkpoint = ExecutionCheckpoint(
                format_version=CHECKPOINT_FORMAT_VERSION,
                repository_commit=self.index.source_commit,
                execution_id="REL005-E2E-001",
                task_id="EFF-GOV-001",
                objective="Validate release governance integration",
                scope=("REL-005",),
                selected_context=tuple(item.path for item in manifest.selected),
                inspected_assets=("tools/context", "tools/execution", "tools/validation"),
                changed_assets=(),
                applicable_standards=("STD-REL-001", "STD-TEST-001"),
                decisions=(),
                assumptions=("Structured fixture does not invoke a model",),
                evidence_references=("validation-report.json",),
                validation_status="FAIL",
                unresolved_items=("Human release decision required",),
                budget_state={item.dimension: item.current_value for item in budget},
                retry_state={"equivalent_failures": loop.equivalent_failures},
                loop_state=loop.to_dict(),
                routing_tier=human_route.recommended_tier,
                escalation_history=("Tier 4 to Tier 5",),
                next_recommended_action="Request accountable human review",
                execution_status=ExecutionStatus.WAITING_FOR_HUMAN,
            )
            CheckpointStore.write(checkpoint, checkpoint_path)
            restored = CheckpointStore.read(checkpoint_path)
            self.assertEqual("DERIVED_EXECUTION_STATE_NOT_APPROVAL", restored.to_dict()["authority"])
            self.assertTrue(CheckpointStore.resume(restored, self.index.source_commit).compatible)

        plan = AffectedScopePlanner(ROOT, self.index).plan(
            ValidationMode.TARGETED_ASSET,
            asset_ids=("EFF-GOV-001",),
            head_commit=self.index.source_commit,
        )
        validation = run_validators(ROOT, (FailingValidator(),), plan=plan, repository_view=self.index)
        self.assertEqual(ValidationMode.TARGETED_ASSET, validation.mode)
        self.assertEqual("FAIL", validation.overall)
        self.assertEqual(1, validation.errors)
        self.assertNotEqual("entire repository", "selected and affected scope only")
        evidence = validation.to_dict()
        self.assertEqual(self.index.source_commit, evidence["provenance"]["repository_commit"])
        self.assertEqual("TARGETED_ASSET", evidence["provenance"]["validation_mode"])
        self.assertTrue(evidence["provenance"]["validator_ids"])
        self.assertTrue(evidence["provenance"]["affected_closure"])

    def test_restricted_mandatory_governance_context_cannot_be_optimized_away(self):
        manifest = ContextSelector(
            ROOT,
            self.index,
            restricted_patterns=("product/releases/**",),
        ).select(task_reference="EFF-GOV-001", expansion_level=0)
        self.assertTrue(manifest.restricted)
        self.assertTrue(all(item.mandatory for item in manifest.restricted))
        self.assertTrue(manifest.fallback_required)
        self.assertFalse(manifest.completeness["restricted_required_context_clear"])
        decision = Router(RoutingPolicy.baseline()).decide(
            CapabilityTier.ADVANCED_REASONING,
            RoutingFactors(
                task_classification="advanced_reasoning", restricted_context=True
            ),
        )
        self.assertEqual(CapabilityTier.HUMAN_SPECIALIST, decision.recommended_tier)
        self.assertTrue(decision.human_authority_required)

    def test_stale_index_and_checkpoint_require_refresh_or_revalidation(self):
        stale_selector = ContextSelector(
            ROOT,
            self.index,
            index_fresh=False,
            freshness_reasons=("source commit differs",),
        )
        manifest = stale_selector.select(task_reference="EFF-GOV-001")
        self.assertTrue(manifest.fallback_required)
        self.assertFalse(manifest.completeness["index_fresh"])

        checkpoint = ExecutionCheckpoint(
            format_version=CHECKPOINT_FORMAT_VERSION,
            repository_commit="old",
            execution_id="REL005-STALE-001",
            task_id="EFF-GOV-001",
            objective="Prove stale state is rejected",
            scope=("REL-005",),
            selected_context=(),
            inspected_assets=(),
            changed_assets=(),
            applicable_standards=(),
            decisions=(),
            assumptions=(),
            evidence_references=(),
            validation_status="UNKNOWN",
            unresolved_items=("Revalidation required",),
            budget_state={},
            retry_state={},
            loop_state={},
            routing_tier=CapabilityTier.DETERMINISTIC,
            escalation_history=(),
            next_recommended_action="Refresh state",
            execution_status=ExecutionStatus.REASSESS,
        )
        resume = CheckpointStore.resume(checkpoint, self.index.source_commit)
        self.assertFalse(resume.compatible)
        self.assertTrue(resume.revalidation_required)


if __name__ == "__main__":
    unittest.main()
