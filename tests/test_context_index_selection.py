"""Focused tests for repository indexing and targeted context selection."""

import json
from datetime import datetime
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.context.cli import main
from tools.context.models import RepositoryIndex
from tools.context.repository import RepositoryView
from tools.context.selector import ContextSelector


class ContextFixture:
    def __init__(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / ".git").mkdir()
        (self.root / "tools").mkdir()
        (self.root / ".gitignore").write_text(
            "/.context-reports/\n__pycache__/\n*.pyc\n", encoding="utf-8"
        )
        (self.root / "AGENTS.md").write_text(
            "# Mandatory Repository Instructions\n", encoding="utf-8"
        )
        for directory in (
            "product/releases",
            "product/epics",
            "product/sprints",
            "product/stories",
            "standards/api",
            "standards/testing",
            "docs/architecture",
        ):
            (self.root / directory).mkdir(parents=True)
        self.write(
            "product/releases/REL-v0.5.md",
            """---
id: REL-005
title: Release
version: 0.5.0
status: In Progress
owner: PMO
target_release: Unscheduled
---
# Release
""",
        )
        self.write(
            "product/epics/EPIC-002.md",
            """---
id: EPIC-002
title: Epic
version: 0.5.0
status: In Progress
owner: PMO
release: REL-005
priority: Critical
---
# Epic
""",
        )
        self.write(
            "product/sprints/SPR-005-002.md",
            """---
id: SPR-005-002
title: Sprint
version: 0.5.0
status: In Progress
owner: PMO
release: REL-005
epic: EPIC-002
---
# Sprint
""",
        )
        self.write(
            "standards/api/STD-API-001.md",
            """---
id: STD-API-001
title: API Standard
version: 0.4.0
status: Draft
owner: API
related_standards:
  - STD-TEST-001
---
# API Standard

## Related Standards

[STD-TEST-001](../testing/STD-TEST-001.md)
""",
        )
        self.write(
            "standards/testing/STD-TEST-001.md",
            """---
id: STD-TEST-001
title: Testing Standard
version: 0.4.0
status: Draft
owner: Test
---
# Testing Standard
""",
        )
        self.write(
            "docs/architecture/CONTEXT.md",
            """---
id: architecture.context
title: Context Contract
version: 0.5.0
status: proposed
owner: Maintainers
---
# Context Contract
""",
        )
        self.write(
            "product/stories/EFF-IDX-001.md",
            """---
id: STORY-EFF-IDX-001
title: Index Story
version: 0.5.0
status: In Progress
owner: PMO
release: REL-005
epic: EPIC-002
sprint: SPR-005-002
priority: Critical
---
# Story

[Context](../../docs/architecture/CONTEXT.md)
[API](../../standards/api/STD-API-001.md)

## Required Deliverable

[Context](../../docs/architecture/CONTEXT.md)

UNIQUE_BODY_MARKER_SHOULD_NOT_BE_INDEXED
""",
        )

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def close(self):
        self.temporary.cleanup()


class RepositoryIndexTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ContextFixture()
        self.view = RepositoryView(self.fixture.root)

    def tearDown(self):
        self.fixture.close()

    def build(self):
        return self.view.build(source_commit="abc123", generated_at="2026-08-09T00:00:00Z")

    def test_valid_assets_and_relationships_are_indexed(self):
        index = self.build()
        assets = {item.framework_id: item for item in index.assets}
        self.assertEqual(7, len(assets))
        self.assertEqual("story", assets["STORY-EFF-IDX-001"].asset_type)
        relationships = assets["STORY-EFF-IDX-001"].relationships
        self.assertTrue(any(item.target == "REL-005" for item in relationships))
        self.assertTrue(any(item.target == "STD-API-001" for item in relationships))
        self.assertTrue(any(item.relationship_type == "produces" for item in relationships))

    def test_index_generation_is_deterministic_except_runtime_measurement(self):
        first = self.build().to_dict()
        second = self.build().to_dict()
        first["metrics"]["generation_duration_ms"] = 0
        second["metrics"]["generation_duration_ms"] = 0
        self.assertEqual(first, second)

    def test_duplicate_identity_is_visible(self):
        self.fixture.write(
            "product/stories/DUPLICATE.md",
            """---
id: STORY-EFF-IDX-001
title: Duplicate
version: 0.5.0
status: Proposed
owner: PMO
release: REL-005
epic: EPIC-002
sprint: SPR-005-002
priority: High
---
# Duplicate
""",
        )
        index = self.build()
        self.assertEqual(2, len(index.duplicates["STORY-EFF-IDX-001"]))

    def test_provenance_and_stale_fingerprint(self):
        index = self.build()
        self.assertEqual("abc123", index.source_commit)
        with mock.patch.object(self.view, "current_commit", return_value="abc123"):
            fresh, reasons = self.view.freshness(index)
            self.assertTrue(fresh)
            self.assertEqual((), reasons)
            self.fixture.write("product/stories/EXTRA.md", "---\nid: STORY-EXTRA-001\n---\n")
            fresh, reasons = self.view.freshness(index)
            self.assertFalse(fresh)
            self.assertTrue(any("governed files differ" in item for item in reasons))

    def test_json_round_trip_and_output_stability(self):
        index = self.build()
        path = self.fixture.root / ".context-reports" / "index.json"
        self.view.write(index, path)
        loaded = self.view.read(path)
        self.assertEqual(index.to_dict(), loaded.to_dict())
        first = path.read_text(encoding="utf-8")
        self.view.write(index, path)
        self.assertEqual(first, path.read_text(encoding="utf-8"))

    def test_index_contains_metadata_not_source_body(self):
        serialized = json.dumps(self.build().to_dict())
        self.assertNotIn("UNIQUE_BODY_MARKER_SHOULD_NOT_BE_INDEXED", serialized)
        self.assertIn("STORY-EFF-IDX-001", serialized)

    def test_gitignore_exclusions_are_recorded(self):
        index = self.build()
        self.assertIn("/.context-reports/", index.exclusions)
        self.assertNotIn(".context-reports/index.json", [item.path for item in index.assets])

    def test_cli_regenerates_stale_index_before_selection(self):
        index_path = self.fixture.root / ".context-reports" / "index.json"
        manifest_path = self.fixture.root / ".context-reports" / "manifest.json"
        self.view.write(self.build(), index_path)
        previous_fingerprint = self.build().source_fingerprint
        self.fixture.write(
            "docs/architecture/NEW.md",
            "---\nid: architecture.new\ntitle: New\nversion: 0.5.0\nstatus: proposed\nowner: Maintainers\n---\n# New\n",
        )
        result = main(
            (
                "--root",
                str(self.fixture.root),
                "select",
                "--story",
                "EFF-IDX-001",
                "--index",
                ".context-reports/index.json",
                "--output",
                ".context-reports/manifest.json",
            )
        )
        self.assertEqual(0, result)
        refreshed = self.view.read(index_path)
        self.assertNotEqual(previous_fingerprint, refreshed.source_fingerprint)
        self.assertTrue(manifest_path.exists())


class ContextSelectionTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ContextFixture()
        self.view = RepositoryView(self.fixture.root)
        self.index = self.view.build(
            source_commit="abc123", generated_at="2026-08-09T00:00:00Z"
        )

    def tearDown(self):
        self.fixture.close()

    def selector(self, **kwargs):
        return ContextSelector(self.fixture.root, self.index, **kwargs)

    def test_story_resolves_product_hierarchy_and_governing_context(self):
        self.fixture.write(
            "docs/architecture/UNRELATED.md",
            "---\nid: architecture.unrelated\ntitle: Unrelated\nversion: 0.5.0\n"
            "status: proposed\nowner: Maintainers\n---\n# Unrelated\n",
        )
        index = self.view.build(source_commit="abc123", generated_at="2026-08-09T00:00:00Z")
        manifest = ContextSelector(self.fixture.root, index).select(task_reference="EFF-IDX-001")
        ids = {item.asset_id for item in manifest.selected}
        self.assertTrue({"REL-005", "EPIC-002", "SPR-005-002"}.issubset(ids))
        self.assertIn("architecture.context", ids)
        self.assertIn("AGENTS.md", {item.path for item in manifest.selected})
        self.assertTrue(manifest.completeness["repository_instructions_resolved"])
        self.assertTrue(manifest.completeness["applicable_standards_resolved"])
        self.assertTrue(manifest.completeness["task_governance_resolved"])
        self.assertTrue(manifest.completeness["governing_context_complete"])
        self.assertNotIn("architecture.unrelated", ids)
        self.assertLess(len(manifest.selected), len(index.assets) + 1)  # AGENTS.md is direct context.

    def test_applicable_standard_and_direct_relationship_are_selected(self):
        manifest = self.selector().select(task_reference="EFF-IDX-001")
        ids = {item.asset_id for item in manifest.selected}
        self.assertIn("STD-API-001", ids)
        manifest = self.selector().select(task_reference="STD-API-001")
        ids = {item.asset_id for item in manifest.selected}
        self.assertIn("STD-TEST-001", ids)

    def test_explicit_target_and_irrelevant_file_behavior(self):
        self.fixture.write("unrelated.txt", "not selected\n")
        manifest = self.selector().select(
            task_reference="EFF-IDX-001", target_paths=("unrelated.txt",)
        )
        paths = {item.path for item in manifest.selected}
        self.assertIn("unrelated.txt", paths)
        self.assertNotIn(".gitignore", paths)

    def test_restricted_required_context_is_reported_not_selected(self):
        manifest = self.selector(restricted_patterns=("standards/api/*",)).select(
            task_reference="EFF-IDX-001"
        )
        self.assertTrue(any(item.asset_id == "STD-API-001" for item in manifest.restricted))
        self.assertTrue(manifest.fallback_required)
        self.assertFalse(manifest.completeness["restricted_required_context_clear"])

    def test_restricted_repository_instruction_makes_governance_incomplete(self):
        manifest = self.selector(restricted_patterns=("AGENTS.md",)).select(
            task_reference="EFF-IDX-001"
        )
        self.assertTrue(any(item.path == "AGENTS.md" for item in manifest.restricted))
        self.assertTrue(manifest.completeness["restricted_governance_present"])
        self.assertFalse(manifest.completeness["repository_instructions_resolved"])
        self.assertFalse(manifest.completeness["governing_context_complete"])
        self.assertTrue(manifest.fallback_required)

    def test_missing_repository_instruction_makes_governance_incomplete(self):
        (self.fixture.root / "AGENTS.md").unlink()
        manifest = self.selector().select(task_reference="EFF-IDX-001")
        self.assertFalse(manifest.completeness["repository_instructions_resolved"])
        self.assertFalse(manifest.completeness["governing_context_complete"])
        self.assertTrue(manifest.fallback_required)
        self.assertTrue(any(item.reference == "AGENTS.md" for item in manifest.unresolved))

    def test_level_zero_does_not_claim_unloaded_standards_complete(self):
        manifest = self.selector().select(task_reference="EFF-IDX-001", expansion_level=0)
        self.assertFalse(manifest.completeness["applicable_standards_resolved"])
        self.assertFalse(manifest.completeness["governing_context_complete"])
        self.assertTrue(manifest.fallback_required)

    def test_unresolved_relationship_requires_fallback(self):
        asset = next(item for item in self.index.assets if item.framework_id == "STORY-EFF-IDX-001")
        altered = asset.__class__(
            **{
                **asset.__dict__,
                "relationships": asset.relationships
                + (asset.relationships[0].__class__("depends_on", "MISSING-001", None, False),),
            }
        )
        index = RepositoryIndex(
            **{
                **self.index.__dict__,
                "assets": tuple(altered if item == asset else item for item in self.index.assets),
            }
        )
        manifest = ContextSelector(self.fixture.root, index).select(
            task_reference="EFF-IDX-001"
        )
        self.assertTrue(manifest.fallback_required)
        self.assertTrue(any(item.reference == "MISSING-001" for item in manifest.unresolved))

    def test_stale_index_requires_fallback(self):
        manifest = self.selector(
            index_fresh=False, freshness_reasons=("source commit differs",)
        ).select(task_reference="EFF-IDX-001")
        self.assertTrue(manifest.fallback_required)
        self.assertFalse(manifest.completeness["index_fresh"])

    def test_progressive_expansion_is_deterministic(self):
        level_zero = self.selector().select(
            task_reference="EFF-IDX-001", expansion_level=0
        )
        level_four = self.selector().select(
            task_reference="EFF-IDX-001", expansion_level=4
        )
        self.assertLess(len(level_zero.selected), len(level_four.selected))
        first = level_four.to_dict()
        second = self.selector().select(task_reference="EFF-IDX-001", expansion_level=4).to_dict()
        first["provenance"].pop("generated_at")
        second["provenance"].pop("generated_at")
        self.assertEqual(first, second)

    def test_manifest_serializes_with_completeness_and_metrics(self):
        value = self.selector().select(task_reference="EFF-IDX-001").to_dict()
        serialized = json.dumps(value, sort_keys=True)
        self.assertIn("fallback_required", serialized)
        self.assertIn("files_selected", serialized)
        self.assertIn("relationship_path", serialized)
        provenance = value["provenance"]
        self.assertEqual("context_manifest", provenance["evidence_type"])
        self.assertEqual("DERIVED_EXECUTION_EVIDENCE_NOT_APPROVAL", provenance["authority"])
        self.assertTrue(provenance["runtime"])
        self.assertIsNotNone(datetime.fromisoformat(provenance["generated_at"]))
        self.assertNotIn("source_body", serialized)


if __name__ == "__main__":
    unittest.main()
