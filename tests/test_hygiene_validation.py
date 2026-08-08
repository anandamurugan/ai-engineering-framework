"""Focused tests for repository hygiene validation."""

import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from tools.validation.cli import main
from tools.validation.hygiene import (
    MarkdownHygieneValidator,
    PlaceholderValidator,
    TrackedArtifactValidator,
    TrailingWhitespaceValidator,
)
from tools.validation.models import Severity, Status, ValidationContext
from tools.validation.registry import VALIDATORS


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class HygieneFixture:
    def __init__(self, root):
        self.root = Path(root)
        for directory in (
            "schemas",
            "templates",
            "standards",
            "product/releases",
            "product/epics",
            "product/sprints",
            "product/stories",
            "docs",
            "tests",
            "tools/validation",
        ):
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        (self.root / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
        (self.root / ".git").mkdir()
        (self.root / ".gitignore").write_text(
            "/.validation-reports/\n__pycache__/\n*.py[cod]\n", encoding="utf-8"
        )
        (self.root / "standards" / "README.md").write_text(
            "# Standards Catalog\n\n## Versioned standards\n", encoding="utf-8"
        )
        shutil.copy(REPOSITORY_ROOT / "schemas" / "standard.schema.yaml", self.root / "schemas")
        shutil.copy(REPOSITORY_ROOT / "templates" / "standard-template.md", self.root / "templates")

    def context(self):
        return ValidationContext(self.root, tuple(item.validator_id for item in VALIDATORS))

    @staticmethod
    def errors(results):
        return [
            item
            for item in results
            if item.status is Status.FAIL and item.severity is Severity.ERROR
        ]


class PlaceholderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = HygieneFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_unresolved_todo_and_tbd_fail_case_insensitively(self):
        (self.fixture.root / "docs" / "content.md").write_text(
            "# Content\n\ntodo: finish this\nTBD\n", encoding="utf-8"
        )
        errors = self.fixture.errors(PlaceholderValidator().validate(self.fixture.context()))
        self.assertEqual(len(errors), 2)
        self.assertIn("Line 3", errors[0].message)

    def test_validator_documentation_example_is_excluded(self):
        (self.fixture.root / "tools" / "validation" / "README.md").write_text(
            "# Validation\n\nExamples: TODO, TBD, FIXME, PLACEHOLDER.\n", encoding="utf-8"
        )
        self.assertEqual(
            self.fixture.errors(PlaceholderValidator().validate(self.fixture.context())), []
        )

    def test_test_fixture_placeholder_is_excluded(self):
        (self.fixture.root / "tests" / "fixture.md").write_text(
            "# Fixture\n\ncoming soon\n", encoding="utf-8"
        )
        self.assertEqual(
            self.fixture.errors(PlaceholderValidator().validate(self.fixture.context())), []
        )


class WhitespaceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = HygieneFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_clean_lines_pass(self):
        (self.fixture.root / "docs" / "clean.md").write_text(
            "# Clean\n\nNo trailing whitespace.\n", encoding="utf-8"
        )
        self.assertEqual(
            self.fixture.errors(TrailingWhitespaceValidator().validate(self.fixture.context())), []
        )

    def test_trailing_space_reports_line(self):
        (self.fixture.root / "docs" / "space.md").write_text(
            "# Space\nBad line. \n", encoding="utf-8"
        )
        errors = self.fixture.errors(
            TrailingWhitespaceValidator().validate(self.fixture.context())
        )
        self.assertTrue(any("Line 2" in item.message and "space" in item.message for item in errors))

    def test_trailing_tab_reports_line(self):
        (self.fixture.root / "docs" / "tab.md").write_text(
            "# Tab\nBad line.\t\n", encoding="utf-8"
        )
        errors = self.fixture.errors(
            TrailingWhitespaceValidator().validate(self.fixture.context())
        )
        self.assertTrue(any("Line 2" in item.message and "tab" in item.message for item in errors))


class MarkdownHygieneTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = HygieneFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_valid_fence_and_heading_hierarchy_pass(self):
        (self.fixture.root / "docs" / "valid.md").write_text(
            "# Valid\n\n## Section\n\n```text\n# Not a heading\n```\n",
            encoding="utf-8",
        )
        self.assertEqual(
            self.fixture.errors(MarkdownHygieneValidator().validate(self.fixture.context())), []
        )

    def test_unclosed_fence_fails(self):
        (self.fixture.root / "docs" / "fence.md").write_text(
            "# Fence\n\n```text\nunclosed\n", encoding="utf-8"
        )
        errors = self.fixture.errors(MarkdownHygieneValidator().validate(self.fixture.context()))
        self.assertTrue(any("unclosed fenced code block" in item.message for item in errors))

    def test_skipped_heading_hierarchy_fails(self):
        (self.fixture.root / "docs" / "heading.md").write_text(
            "# Heading\n\n### Skipped\n", encoding="utf-8"
        )
        errors = self.fixture.errors(MarkdownHygieneValidator().validate(self.fixture.context()))
        self.assertTrue(any("skips heading level H1 to H3" in item.message for item in errors))

    def test_duplicate_h1_fails(self):
        (self.fixture.root / "docs" / "duplicate.md").write_text(
            "# One\n\n# Two\n", encoding="utf-8"
        )
        errors = self.fixture.errors(MarkdownHygieneValidator().validate(self.fixture.context()))
        self.assertTrue(any("exactly one H1" in item.message for item in errors))


class ArtifactAndIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = HygieneFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_prohibited_tracked_cache_file_fails(self):
        with patch(
            "tools.validation.hygiene._tracked_paths",
            return_value=("tools/__pycache__/module.pyc",),
        ):
            errors = self.fixture.errors(
                TrackedArtifactValidator().validate(self.fixture.context())
            )
        self.assertTrue(any(".gitignore conventions" in item.message for item in errors))

    def test_untracked_generated_report_passes(self):
        report = self.fixture.root / ".validation-reports" / "report.json"
        report.parent.mkdir()
        report.write_text("{}\n", encoding="utf-8")
        with patch("tools.validation.hygiene._tracked_paths", return_value=("AGENTS.md",)):
            errors = self.fixture.errors(
                TrackedArtifactValidator().validate(self.fixture.context())
            )
        self.assertEqual(errors, [])

    def test_registry_and_cli_json_include_hygiene_finding(self):
        registered = {item.validator_id for item in VALIDATORS}
        self.assertTrue(
            {
                "VAL-HYGIENE-PLACEHOLDER-001",
                "VAL-HYGIENE-WHITESPACE-001",
                "VAL-HYGIENE-MARKDOWN-001",
                "VAL-HYGIENE-ARTIFACT-001",
            }
            <= registered
        )
        (self.fixture.root / "docs" / "failure.md").write_text(
            "# Failure\n\nFIXME\n", encoding="utf-8"
        )
        report = self.fixture.root / "report.json"
        with redirect_stdout(StringIO()):
            exit_code = main(["--root", str(self.fixture.root), "--report", str(report)])
        evidence = json.loads(report.read_text(encoding="utf-8"))
        self.assertNotEqual(exit_code, 0)
        self.assertTrue(
            any(
                item["validator_id"] == "VAL-HYGIENE-PLACEHOLDER-001"
                for item in evidence["results"]
            )
        )


if __name__ == "__main__":
    unittest.main()
