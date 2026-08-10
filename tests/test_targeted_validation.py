"""Focused tests for targeted scope, provenance, and registry integrity."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.context.models import AssetRecord, IndexMetrics, Relationship, RepositoryIndex
from tools.validation.models import (
    ScopeCapability, Severity, Status, ValidationMode, Validator,
)
from tools.validation.runner import run_validators, validate_registry
from tools.validation.references import RelativeLinkValidator
from tools.validation.targeting import AffectedScopePlanner, GitChangeDiscovery, ValidationPlan


def asset(identifier, asset_type, path, relationships=()):
    return AssetRecord(identifier, asset_type, identifier, path, relationships=relationships)


def repository_index(assets, *, commit="abc", duplicates=None, unresolved=()):
    return RepositoryIndex(
        "1.0", commit, "fingerprint", "2026-08-09T00:00:00+00:00", ".",
        tuple(assets), duplicates or {}, tuple(unresolved), (), IndexMetrics(1, 1, len(assets), 0, 1, 1),
    )


class PassingValidator(Validator):
    validator_id = "TEST-SCOPE-001"
    name = "Scope test"
    description = "Test scoped execution."
    scope_capability = ScopeCapability.TARGETABLE

    def validate(self, context):
        return [self.result(status=Status.PASS, severity=Severity.INFO, asset="one.md", message="ok")]


class FailingValidator(PassingValidator):
    validator_id = "TEST-SCOPE-FAIL-001"

    def validate(self, context):
        return [self.result(status=Status.FAIL, severity=Severity.ERROR, asset="one.md", message="bad")]


class ExplodingValidator(PassingValidator):
    validator_id = "TEST-EXPLODE-001"

    def validate(self, context):
        raise RuntimeError("controlled failure")


class InvalidObject:
    validator_id = "INVALID"


class ChangeDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        subprocess.run(("git", "init", "-q"), cwd=str(self.root), check=True)
        subprocess.run(("git", "config", "user.email", "test@example.invalid"), cwd=str(self.root), check=True)
        subprocess.run(("git", "config", "user.name", "Test"), cwd=str(self.root), check=True)
        (self.root / ".gitignore").write_text("reports/\n", encoding="utf-8")
        (self.root / "old.md").write_text("old\n", encoding="utf-8")
        (self.root / "deleted.md").write_text("delete\n", encoding="utf-8")
        subprocess.run(("git", "add", "."), cwd=str(self.root), check=True)
        subprocess.run(("git", "commit", "-qm", "base"), cwd=str(self.root), check=True)
        self.base = subprocess.run(("git", "rev-parse", "HEAD"), cwd=str(self.root), check=True, text=True, stdout=subprocess.PIPE).stdout.strip()

    def tearDown(self):
        self.temporary.cleanup()

    def test_working_tree_finds_modified_added_deleted_and_ignored(self):
        (self.root / "old.md").write_text("changed\n", encoding="utf-8")
        (self.root / "added.md").write_text("added\n", encoding="utf-8")
        (self.root / "deleted.md").unlink()
        (self.root / "reports").mkdir()
        (self.root / "reports" / "result.json").write_text("{}\n", encoding="utf-8")
        changes = GitChangeDiscovery(self.root).discover(working_tree=True)
        self.assertEqual(set(changes.changed_paths), {"added.md", "deleted.md", "old.md"})
        self.assertNotIn("reports/result.json", changes.changed_paths)

    def test_commit_range_supports_rename(self):
        (self.root / "old.md").rename(self.root / "renamed.md")
        subprocess.run(("git", "add", "-A"), cwd=str(self.root), check=True)
        subprocess.run(("git", "commit", "-qm", "rename"), cwd=str(self.root), check=True)
        changes = GitChangeDiscovery(self.root).discover(base=self.base)
        self.assertEqual(set(changes.changed_paths), {"old.md", "renamed.md"})

    def test_git_invocation_uses_argument_sequence_without_shell(self):
        with patch("tools.validation.targeting.subprocess.run") as run:
            run.return_value.stdout = ""
            run.return_value.returncode = 0
            GitChangeDiscovery(self.root).discover(working_tree=True)
        command = run.call_args_list[0].args[0]
        self.assertIsInstance(command, tuple)
        self.assertEqual(command[:2], ("git", "status"))
        self.assertNotIn("shell", run.call_args_list[0].kwargs)


class AffectedClosureTests(unittest.TestCase):
    def setUp(self):
        self.root = Path.cwd()
        self.index = repository_index(
            (
                asset("REL-005", "release", "product/releases/REL-v0.5.md"),
                asset("EPIC-002", "epic", "product/epics/EPIC-002.md", (Relationship("belongs_to", "REL-005", "product/releases/REL-v0.5.md"),)),
                asset("SPR-005-004", "sprint", "product/sprints/SPR-005-004.md", (Relationship("belongs_to", "EPIC-002", "product/epics/EPIC-002.md"),)),
                asset("STORY-EFF-VAL-001", "story", "product/stories/EFF-VAL-001.md", (Relationship("belongs_to", "SPR-005-004", "product/sprints/SPR-005-004.md"), Relationship("produces", "STD-SEC-001", "standards/security/STD-SEC-001.md"))),
                asset("STD-SEC-001", "standard", "standards/security/STD-SEC-001.md"),
                asset("STD-CODE-001", "standard", "standards/coding/STD-CODE-001.md"),
            )
        )

    def plan(self, **kwargs):
        with patch("tools.validation.targeting.RepositoryView.freshness", return_value=(True, ())):
            return AffectedScopePlanner(self.root, self.index).plan(**kwargs)

    def test_story_expands_to_parents_and_deliverable(self):
        plan = self.plan(mode=ValidationMode.TARGETED_ASSET, asset_ids=("EFF-VAL-001",), head_commit="abc")
        self.assertTrue({"REL-005", "EPIC-002", "SPR-005-004", "STD-SEC-001"}.issubset(plan.affected_ids))

    def test_standard_change_includes_reverse_story_reference(self):
        plan = self.plan(mode=ValidationMode.AFFECTED_CLOSURE, paths=("standards/security/STD-SEC-001.md",), head_commit="abc")
        self.assertIn("STORY-EFF-VAL-001", plan.affected_ids)

    def test_unrelated_asset_is_excluded(self):
        plan = self.plan(mode=ValidationMode.TARGETED_ASSET, asset_ids=("EFF-VAL-001",), head_commit="abc")
        self.assertNotIn("STD-CODE-001", plan.affected_ids)

    def test_unknown_path_forces_full_fallback(self):
        plan = self.plan(mode=ValidationMode.CHANGED_FILES, paths=("unknown.txt",), head_commit="abc")
        self.assertEqual(plan.effective_mode, ValidationMode.FULL)
        self.assertTrue(plan.fallback_reasons)

    def test_sensitive_paths_force_full_fallback(self):
        for path in ("schemas/standard.schema.yaml", "templates/standard-template.md", "tools/validation/runner.py", ".github/workflows/framework-validation.yml"):
            plan = self.plan(mode=ValidationMode.CHANGED_FILES, paths=(path,), head_commit="abc")
            self.assertEqual(plan.effective_mode, ValidationMode.FULL)

    def test_stale_index_forces_full_fallback(self):
        with patch("tools.validation.targeting.RepositoryView.freshness", return_value=(False, ("commit differs",))):
            plan = AffectedScopePlanner(self.root, self.index).plan(ValidationMode.TARGETED_ASSET, asset_ids=("EFF-VAL-001",), head_commit="abc")
        self.assertEqual(plan.effective_mode, ValidationMode.FULL)
        self.assertIn("Stale repository index", plan.fallback_reasons[0])

    def test_duplicate_identity_forces_full_fallback(self):
        index = repository_index(self.index.assets, duplicates={"REL-005": ("one", "two")})
        with patch("tools.validation.targeting.RepositoryView.freshness", return_value=(True, ())):
            plan = AffectedScopePlanner(self.root, index).plan(ValidationMode.TARGETED_ASSET, asset_ids=("EFF-VAL-001",), head_commit="abc")
        self.assertEqual(plan.effective_mode, ValidationMode.FULL)


class RunnerAndProvenanceTests(unittest.TestCase):
    def plan(self):
        return ValidationPlan(
            ValidationMode.TARGETED_ASSET, ValidationMode.TARGETED_ASSET,
            ("one.md",), ("one.md", "two.md"), ("ONE", "TWO"), (), (), (),
            "base", "head",
        )

    def test_unique_registry_passes(self):
        self.assertEqual(validate_registry((PassingValidator(),))[0].validator_id, "TEST-SCOPE-001")

    def test_duplicate_validator_id_fails(self):
        with self.assertRaisesRegex(ValueError, "Duplicate validator ID"):
            validate_registry((PassingValidator(), PassingValidator()))

    def test_invalid_registry_entry_fails(self):
        with self.assertRaisesRegex(ValueError, "does not implement Validator"):
            validate_registry((InvalidObject(),))

    def test_missing_validator_identity_fails(self):
        with self.assertRaisesRegex(ValueError, "invalid or missing"):
            validate_registry((Validator(),))

    def test_exception_becomes_structured_error(self):
        run = run_validators(Path.cwd(), (ExplodingValidator(),), plan=self.plan())
        self.assertEqual(run.exit_code, 1)
        self.assertEqual(run.results[0].validator_id, "TEST-EXPLODE-001")
        self.assertEqual(run.results[0].severity, Severity.ERROR)
        self.assertNotIn("Traceback", run.results[0].message)

    def test_targeted_failure_is_nonzero(self):
        run = run_validators(Path.cwd(), (FailingValidator(),), plan=self.plan())
        self.assertEqual(run.exit_code, 1)

    def test_targetable_validator_receives_scope_and_global_check_still_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "one.md").write_text("# One\n\n[bad](missing.md)\n", encoding="utf-8")
            (root / "two.md").write_text("# Two\n\n[bad](other.md)\n", encoding="utf-8")
            plan = ValidationPlan(
                ValidationMode.TARGETED_ASSET, ValidationMode.TARGETED_ASSET,
                ("one.md",), ("one.md",), ("ONE",), (), (), (), "base", "head",
            )
            run = run_validators(
                root, (RelativeLinkValidator(), PassingValidator()), plan=plan
            )
        broken = [result.asset for result in run.results if result.status is Status.FAIL]
        self.assertEqual(broken, ["one.md"])
        self.assertEqual(run.validators_executed, 2)

    def test_report_contains_explicit_provenance_and_counts(self):
        run = run_validators(Path.cwd(), (PassingValidator(),), plan=self.plan())
        report = run.to_dict()
        provenance = report["provenance"]
        self.assertEqual(report["report_version"], "2.0")
        self.assertEqual(provenance["repository_commit"], "head")
        self.assertEqual(provenance["base_commit"], "base")
        self.assertEqual(provenance["validation_mode"], "TARGETED_ASSET")
        self.assertEqual(provenance["validation_scope"], ["one.md"])
        self.assertEqual(provenance["affected_closure"], ["one.md", "two.md"])
        self.assertTrue(provenance["runtime"].startswith("CPython"))
        self.assertIn("executed_at", provenance)
        self.assertIn("repository_fingerprint", provenance)
        self.assertEqual(report["summary"]["scoped_assets"], 1)
        self.assertEqual(report["summary"]["affected_assets"], 2)


if __name__ == "__main__":
    unittest.main()
