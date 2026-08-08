"""Tests for link, cross-reference, catalog, and product traceability checks."""

import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from tools.validation.cli import main
from tools.validation.models import Severity, Status, ValidationContext
from tools.validation.references import RelativeLinkValidator, StandardReferenceValidator
from tools.validation.registry import VALIDATORS
from tools.validation.traceability import ProductTraceabilityValidator, StandardsCatalogValidator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ReferenceFixture:
    def __init__(self, root):
        self.root = Path(root)
        for directory in (
            "schemas",
            "templates",
            "standards/testing",
            "product/releases",
            "product/epics",
            "product/sprints",
            "product/stories",
            "docs/child",
        ):
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        (self.root / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
        (self.root / ".git").mkdir()
        shutil.copy(REPOSITORY_ROOT / "schemas" / "standard.schema.yaml", self.root / "schemas")
        shutil.copy(REPOSITORY_ROOT / "templates" / "standard-template.md", self.root / "templates")

    def context(self):
        return ValidationContext(self.root, tuple(item.validator_id for item in VALIDATORS))

    def standard(self, standard_id, title, related=(), links=(), supersedes=()):
        relationship_lines = "\n".join("  - {}".format(item) for item in related)
        supersedes_lines = "\n".join("  - {}".format(item) for item in supersedes)
        link_lines = "\n".join(
            "- [{} — Target](../testing/{}.md)".format(item, item) for item in links
        ) or "None."
        text = """---
id: {standard_id}
title: {title}
version: 0.4.0
status: Draft
category: Testing
owner: Framework PMO
mandatory: true
ai_consumable: true
human_review_required: true
supersedes:{supersedes_block}
related_standards:{relationship_block}
related_playbooks: []
tags: []
---
# {standard_id} – {title}

## Related Standards

{link_lines}
""".format(
            standard_id=standard_id,
            title=title,
            relationship_block="\n" + relationship_lines if relationship_lines else " []",
            supersedes_block="\n" + supersedes_lines if supersedes_lines else " []",
            link_lines=link_lines,
        )
        path = self.root / "standards" / "testing" / "{}.md".format(standard_id)
        path.write_text(text, encoding="utf-8")
        return path

    def catalog(self, rows):
        text = """# Standards Catalog

## Versioned standards

| ID | Title | Category | Version | Status | Owner | Mandatory | Link |
| --- | --- | --- | --- | --- | --- | --- | --- |
{}
""".format("\n".join(rows))
        (self.root / "standards" / "README.md").write_text(text, encoding="utf-8")

    def product_chain(self, story_status="In Progress", sprint_status="In Progress"):
        release = """---
id: REL-004
title: Release
version: 0.4.0
status: In Progress
owner: PMO
target_release: TBD
---
# Release

## Deliverables

| ID | Deliverable |
| --- | --- |
| EPIC-001 | Epic |
| SPR-004-004 | Sprint |
"""
        epic = """---
id: EPIC-001
title: Epic
version: 0.4.0
status: In Progress
owner: PMO
release: REL-004
priority: High
---
# Epic

## Sprint Breakdown

| Sprint ID | Sprint | Goal | Progress |
| --- | --- | --- | --- |
| SPR-004-004 | Sprint | Goal | In Progress |
"""
        sprint = """---
id: SPR-004-004
title: Sprint
version: 0.4.0
status: {status}
owner: PMO
release: REL-004
epic: EPIC-001
---
# Sprint

## Stories

| Story | Deliverable |
| --- | --- |
| [STD-TEST-999](../stories/STD-TEST-999.md) | Standard |
""".format(status=sprint_status)
        story = """---
id: STORY-STD-TEST-999
title: Story
version: 0.4.0
status: {status}
owner: PMO
release: REL-004
epic: EPIC-001
sprint: SPR-004-004
priority: High
---
# Story

## Required Deliverable

[STD-TEST-999](../../standards/testing/STD-TEST-999.md)
""".format(status=story_status)
        (self.root / "product" / "releases" / "REL-v0.4.md").write_text(release, encoding="utf-8")
        (self.root / "product" / "epics" / "EPIC-001.md").write_text(epic, encoding="utf-8")
        (self.root / "product" / "sprints" / "SPR-004-004.md").write_text(sprint, encoding="utf-8")
        (self.root / "product" / "stories" / "STD-TEST-999.md").write_text(story, encoding="utf-8")
        self.standard("STD-TEST-999", "Fixture Standard")


class RelativeLinkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = ReferenceFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def _errors(self):
        return [
            item
            for item in RelativeLinkValidator().validate(self.fixture.context())
            if item.status is Status.FAIL and item.severity is Severity.ERROR
        ]

    def test_valid_relative_link_and_parent_resolution_pass(self):
        (self.fixture.root / "docs" / "target.md").write_text("# Target\n", encoding="utf-8")
        (self.fixture.root / "docs" / "child" / "source.md").write_text(
            "[Target](../target.md)\n", encoding="utf-8"
        )
        self.assertEqual(self._errors(), [])

    def test_missing_target_fails(self):
        (self.fixture.root / "docs" / "source.md").write_text(
            "[Missing](missing.md)\n", encoding="utf-8"
        )
        self.assertTrue(any("target does not exist" in item.message for item in self._errors()))

    def test_external_url_is_ignored(self):
        (self.fixture.root / "docs" / "source.md").write_text(
            "[External](https://example.com/path)\n", encoding="utf-8"
        )
        self.assertEqual(self._errors(), [])

    def test_valid_fragment_passes(self):
        (self.fixture.root / "docs" / "target.md").write_text("# Target\n\n## Details Here\n", encoding="utf-8")
        (self.fixture.root / "docs" / "source.md").write_text(
            "[Details](target.md#details-here)\n", encoding="utf-8"
        )
        self.assertEqual(self._errors(), [])


class StandardReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = ReferenceFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_valid_reciprocal_relationship_and_conceptual_cycle_pass(self):
        self.fixture.standard("STD-TEST-001", "One", ["STD-TEST-002"], ["STD-TEST-002"])
        self.fixture.standard("STD-TEST-002", "Two", ["STD-TEST-001"], ["STD-TEST-001"])
        results = StandardReferenceValidator().validate(self.fixture.context())
        self.assertFalse(any(item.severity is Severity.ERROR for item in results if item.status is Status.FAIL))

    def test_nonexistent_relationship_target_fails(self):
        self.fixture.standard("STD-TEST-001", "One", ["STD-TEST-404"], ["STD-TEST-404"])
        results = StandardReferenceValidator().validate(self.fixture.context())
        self.assertTrue(any("does not exist" in item.message for item in results))

    def test_relationship_link_id_mismatch_fails(self):
        source = self.fixture.standard(
            "STD-TEST-001", "One", ["STD-TEST-002"], ["STD-TEST-002"]
        )
        self.fixture.standard("STD-TEST-002", "Two", ["STD-TEST-001"], ["STD-TEST-001"])
        self.fixture.standard("STD-TEST-003", "Three")
        source.write_text(
            source.read_text(encoding="utf-8").replace(
                "../testing/STD-TEST-002.md", "../testing/STD-TEST-003.md"
            ),
            encoding="utf-8",
        )
        results = StandardReferenceValidator().validate(self.fixture.context())
        self.assertTrue(any("resolves to framework ID 'STD-TEST-003'" in item.message for item in results))

    def test_optional_missing_reciprocal_is_warning(self):
        self.fixture.standard("STD-TEST-001", "One", ["STD-TEST-002"], ["STD-TEST-002"])
        self.fixture.standard("STD-TEST-002", "Two")
        results = StandardReferenceValidator().validate(self.fixture.context())
        self.assertTrue(
            any(item.status is Status.FAIL and item.severity is Severity.WARNING for item in results)
        )

    def test_directional_supersedes_cycle_fails(self):
        self.fixture.standard("STD-TEST-001", "One", supersedes=["STD-TEST-002"])
        self.fixture.standard("STD-TEST-002", "Two", supersedes=["STD-TEST-001"])
        results = StandardReferenceValidator().validate(self.fixture.context())
        self.assertTrue(any("Prohibited directional cycle" in item.message for item in results))


class CatalogTraceabilityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = ReferenceFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    @staticmethod
    def row(standard_id="STD-TEST-999", title="Fixture Standard"):
        return "| {} | {} | Testing | 0.4.0 | Draft | Framework PMO | Yes | [Read](testing/{}.md) |".format(
            standard_id, title, standard_id
        )

    def test_valid_catalog_parity_passes(self):
        self.fixture.standard("STD-TEST-999", "Fixture Standard")
        self.fixture.catalog([self.row()])
        results = StandardsCatalogValidator().validate(self.fixture.context())
        self.assertFalse(any(item.status is Status.FAIL for item in results))

    def test_missing_catalog_entry_fails(self):
        self.fixture.standard("STD-TEST-999", "Fixture Standard")
        self.fixture.catalog([])
        results = StandardsCatalogValidator().validate(self.fixture.context())
        self.assertTrue(any("absent from the catalog" in item.message for item in results))

    def test_stale_catalog_entry_fails(self):
        self.fixture.catalog([self.row("STD-TEST-404", "Missing")])
        results = StandardsCatalogValidator().validate(self.fixture.context())
        self.assertTrue(any("nonexistent standard" in item.message for item in results))

    def test_catalog_parity_field_mismatch_fails(self):
        self.fixture.standard("STD-TEST-999", "Fixture Standard")
        self.fixture.catalog([self.row(title="Wrong Title")])
        results = StandardsCatalogValidator().validate(self.fixture.context())
        self.assertTrue(any("Expected 'Fixture Standard'" in item.message for item in results))

    def test_valid_product_chain_passes(self):
        self.fixture.product_chain()
        results = ProductTraceabilityValidator().validate(self.fixture.context())
        self.assertFalse(any(item.status is Status.FAIL for item in results))

    def test_missing_parent_and_invalid_sprint_fail(self):
        self.fixture.product_chain()
        story = self.fixture.root / "product" / "stories" / "STD-TEST-999.md"
        story.write_text(
            story.read_text(encoding="utf-8").replace("sprint: SPR-004-004", "sprint: SPR-004-404"),
            encoding="utf-8",
        )
        results = ProductTraceabilityValidator().validate(self.fixture.context())
        self.assertTrue(any("sprint parent does not exist" in item.message for item in results))

    def test_nonexistent_deliverable_fails(self):
        self.fixture.product_chain()
        story = self.fixture.root / "product" / "stories" / "STD-TEST-999.md"
        story.write_text(
            story.read_text(encoding="utf-8").replace("STD-TEST-999.md", "STD-TEST-404.md"),
            encoding="utf-8",
        )
        results = ProductTraceabilityValidator().validate(self.fixture.context())
        self.assertTrue(any("deliverable does not exist" in item.message for item in results))

    def test_authoritative_completed_sprint_rule_fails(self):
        self.fixture.product_chain(story_status="In Progress", sprint_status="Completed")
        results = ProductTraceabilityValidator().validate(self.fixture.context())
        self.assertTrue(any("Completed sprint contains an incomplete story" in item.message for item in results))

    def test_registry_and_cli_json_include_new_finding(self):
        registered = {item.validator_id for item in VALIDATORS}
        self.assertTrue(
            {
                "VAL-REF-LINK-001",
                "VAL-REF-STD-001",
                "VAL-TRACE-CATALOG-001",
                "VAL-TRACE-PRODUCT-001",
            }
            <= registered
        )
        (self.fixture.root / "docs" / "broken.md").write_text(
            "[Missing](missing.md)\n", encoding="utf-8"
        )
        report = self.fixture.root / "report.json"
        with redirect_stdout(StringIO()):
            exit_code = main(["--root", str(self.fixture.root), "--report", str(report)])
        evidence = json.loads(report.read_text(encoding="utf-8"))
        self.assertNotEqual(exit_code, 0)
        self.assertTrue(
            any(item["validator_id"] == "VAL-REF-LINK-001" for item in evidence["results"])
        )


if __name__ == "__main__":
    unittest.main()
