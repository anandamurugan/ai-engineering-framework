"""Contract tests for the framework-validation GitHub Actions workflow."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "framework-validation.yml"


class FrameworkValidationWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_runs_for_default_branch_changes_and_manual_dispatch(self):
        self.assertIn("pull_request:", self.workflow)
        self.assertIn("push:", self.workflow)
        self.assertGreaterEqual(self.workflow.count("      - main"), 2)
        self.assertIn("workflow_dispatch:", self.workflow)

    def test_uses_read_only_permissions_and_pinned_actions(self):
        self.assertIn("permissions:\n  contents: read", self.workflow)
        self.assertNotIn("contents: write", self.workflow)
        uses_lines = [
            line.strip() for line in self.workflow.splitlines() if "uses:" in line
        ]
        self.assertTrue(uses_lines)
        for line in uses_lines:
            reference = line.split("@", 1)[1].split()[0]
            self.assertEqual(40, len(reference))
            self.assertTrue(
                all(character in "0123456789abcdef" for character in reference)
            )

    def test_runs_local_equivalent_commands_and_preserves_report(self):
        self.assertIn("run: python -m tools.validation", self.workflow)
        self.assertIn("run: python -m unittest discover -s tests", self.workflow)
        self.assertIn("if: ${{ always() }}", self.workflow)
        self.assertIn("path: .validation-reports/validation-report.json", self.workflow)
        self.assertIn("include-hidden-files: true", self.workflow)
        self.assertIn("retention-days: 14", self.workflow)


if __name__ == "__main__":
    unittest.main()
