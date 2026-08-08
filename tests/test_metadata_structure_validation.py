"""Tests for metadata, framework-ID, and standard-structure validation."""

import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from tools.validation.cli import main
from tools.validation.metadata import FrameworkIdValidator, MetadataValidator
from tools.validation.models import Status, ValidationContext
from tools.validation.registry import VALIDATORS
from tools.validation.structure import DocumentStructureValidator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALID_STANDARD_METADATA = """---
id: STD-TEST-999
title: Fixture Standard
version: 0.4.0
status: Draft
category: Testing
owner: Framework PMO
review_cycle: P12M
mandatory: true
ai_consumable: true
human_review_required: true
effective_date: null
last_reviewed: null
supersedes: []
related_standards: []
related_playbooks: []
tags:
  - testing
---
"""


class RepositoryFixture:
    def __init__(self, root):
        self.root = Path(root)
        (self.root / "schemas").mkdir()
        (self.root / "templates").mkdir()
        (self.root / "standards" / "testing").mkdir(parents=True)
        for asset_type in ("releases", "epics", "sprints", "stories"):
            (self.root / "product" / asset_type).mkdir(parents=True)
        (self.root / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
        (self.root / ".git").mkdir()
        shutil.copy(REPOSITORY_ROOT / "schemas" / "standard.schema.yaml", self.root / "schemas")
        shutil.copy(REPOSITORY_ROOT / "templates" / "standard-template.md", self.root / "templates")

    def write_standard(self, metadata=VALID_STANDARD_METADATA, body=None, name="STD-TEST-999.md"):
        if body is None:
            template = (self.root / "templates" / "standard-template.md").read_text(
                encoding="utf-8"
            )
            body = template.split("---", 2)[2]
            body = body.replace(
                "# <Standard ID> – <Standard Title>",
                "# STD-TEST-999 – Fixture Standard",
            )
        path = self.root / "standards" / "testing" / name
        path.write_text(metadata + body.lstrip("\n"), encoding="utf-8")
        return path

    def context(self):
        return ValidationContext(self.root, tuple(item.validator_id for item in VALIDATORS))


class MetadataValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = RepositoryFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_valid_standard_metadata_passes(self):
        self.fixture.write_standard()
        results = MetadataValidator().validate(self.fixture.context())
        self.assertTrue(results)
        self.assertTrue(all(result.status is Status.PASS for result in results))

    def test_missing_required_field_fails(self):
        metadata = VALID_STANDARD_METADATA.replace("owner: Framework PMO\n", "")
        self.fixture.write_standard(metadata=metadata)
        results = MetadataValidator().validate(self.fixture.context())
        self.assertTrue(any("missing required field 'owner'" in item.message for item in results))

    def test_malformed_frontmatter_fails(self):
        metadata = VALID_STANDARD_METADATA.replace("title: Fixture Standard", "title Fixture Standard")
        self.fixture.write_standard(metadata=metadata)
        results = MetadataValidator().validate(self.fixture.context())
        self.assertTrue(any("malformed frontmatter" in item.message for item in results))

    def test_invalid_controlled_status_fails(self):
        metadata = VALID_STANDARD_METADATA.replace("status: Draft", "status: Unreviewed")
        self.fixture.write_standard(metadata=metadata)
        results = MetadataValidator().validate(self.fixture.context())
        self.assertTrue(any("status must be one of" in item.message for item in results))

    def test_extra_standard_field_fails(self):
        metadata = VALID_STANDARD_METADATA.replace("owner: Framework PMO\n", "owner: Framework PMO\nunknown: value\n")
        self.fixture.write_standard(metadata=metadata)
        results = MetadataValidator().validate(self.fixture.context())
        self.assertTrue(any("unexpected field 'unknown'" in item.message for item in results))

    def test_incorrect_standard_type_fails(self):
        metadata = VALID_STANDARD_METADATA.replace("mandatory: true", "mandatory: required")
        self.fixture.write_standard(metadata=metadata)
        results = MetadataValidator().validate(self.fixture.context())
        self.assertTrue(any("mandatory must have type boolean" in item.message for item in results))

    def test_malformed_framework_id_fails(self):
        metadata = VALID_STANDARD_METADATA.replace("STD-TEST-999", "std-test-999")
        self.fixture.write_standard(metadata=metadata)
        results = MetadataValidator().validate(self.fixture.context())
        self.assertTrue(any("id does not match" in item.message for item in results))

    def test_unique_ids_pass(self):
        self.fixture.write_standard()
        results = FrameworkIdValidator().validate(self.fixture.context())
        self.assertEqual(len(results), 1)
        self.assertIs(results[0].status, Status.PASS)

    def test_duplicate_ids_identify_both_files(self):
        self.fixture.write_standard()
        duplicate = self.fixture.root / "product" / "stories" / "duplicate.md"
        duplicate.write_text(
            "---\nid: STD-TEST-999\ntitle: Duplicate\nversion: 0.4.0\n"
            "status: Ready\nowner: PMO\nrelease: REL-004\nepic: EPIC-001\n"
            "sprint: SPR-004-004\npriority: High\n---\n# Duplicate\n",
            encoding="utf-8",
        )
        results = FrameworkIdValidator().validate(self.fixture.context())
        failed_assets = {item.asset for item in results if item.status is Status.FAIL}
        self.assertEqual(
            failed_assets,
            {"standards/testing/STD-TEST-999.md", "product/stories/duplicate.md"},
        )


class StructureValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = RepositoryFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_valid_document_structure_passes(self):
        self.fixture.write_standard()
        results = DocumentStructureValidator().validate(self.fixture.context())
        self.assertTrue(all(result.status is Status.PASS for result in results))

    def test_missing_required_section_fails(self):
        path = self.fixture.write_standard()
        text = path.read_text(encoding="utf-8").replace("## Purpose", "### Purpose")
        path.write_text(text, encoding="utf-8")
        results = DocumentStructureValidator().validate(self.fixture.context())
        self.assertTrue(any("Missing required section '## Purpose'" in item.message for item in results))

    def test_incorrect_section_order_fails(self):
        path = self.fixture.write_standard()
        text = path.read_text(encoding="utf-8")
        text = text.replace("## Purpose", "## TEMP").replace("## Scope", "## Purpose")
        path.write_text(text.replace("## TEMP", "## Scope"), encoding="utf-8")
        results = DocumentStructureValidator().validate(self.fixture.context())
        self.assertTrue(any("Expected 'Purpose' before 'Scope'" in item.message for item in results))

    def test_duplicate_required_section_fails(self):
        path = self.fixture.write_standard()
        text = path.read_text(encoding="utf-8").replace("## Scope", "## Purpose\n\nDuplicate.\n\n## Scope")
        path.write_text(text, encoding="utf-8")
        results = DocumentStructureValidator().validate(self.fixture.context())
        self.assertTrue(any("'## Purpose' appears 2 times" in item.message for item in results))

    def test_h1_identity_fails(self):
        path = self.fixture.write_standard()
        text = path.read_text(encoding="utf-8").replace(
            "# STD-TEST-999 – Fixture Standard", "# Incorrect Standard"
        )
        path.write_text(text, encoding="utf-8")
        results = DocumentStructureValidator().validate(self.fixture.context())
        self.assertTrue(any("H1 must be" in item.message for item in results))

    def test_revision_history_structure_fails(self):
        path = self.fixture.write_standard()
        text = path.read_text(encoding="utf-8").replace(
            "| Version | Date | Change | Author | Approval |", "| Version | Change |"
        )
        path.write_text(text, encoding="utf-8")
        results = DocumentStructureValidator().validate(self.fixture.context())
        self.assertTrue(any("five-column template table" in item.message for item in results))

    def test_registry_executes_new_validators(self):
        registered = {validator.validator_id for validator in VALIDATORS}
        self.assertTrue({"VAL-META-001", "VAL-META-ID-001", "VAL-STRUCT-001"} <= registered)

    def test_cli_failure_and_json_finding(self):
        release = self.fixture.root / "product" / "releases" / "REL-invalid.md"
        release.write_text(
            "---\nid: rel-4\ntitle: Invalid\nversion: 0.4.0\nstatus: In Progress\n"
            "owner: PMO\ntarget_release: TBD\n---\n# Invalid\n",
            encoding="utf-8",
        )
        report = self.fixture.root / "report.json"
        with redirect_stdout(StringIO()):
            exit_code = main(["--root", str(self.fixture.root), "--report", str(report)])
        evidence = json.loads(report.read_text(encoding="utf-8"))
        self.assertNotEqual(exit_code, 0)
        self.assertEqual(evidence["summary"]["overall"], "FAIL")
        self.assertTrue(
            any(item["validator_id"] == "VAL-META-001" for item in evidence["results"])
        )
        self.assertTrue(any(item["framework_id"] == "rel-4" for item in evidence["results"]))


if __name__ == "__main__":
    unittest.main()
