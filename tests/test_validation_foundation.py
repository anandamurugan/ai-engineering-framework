"""Focused tests for the validation framework foundation."""

import json
import tempfile
import unittest
from pathlib import Path

from tools.validation.models import Severity, Status, ValidationContext, Validator
from tools.validation.runner import ValidationRun, format_console_report, run_validators
from tools.validation.self_check import FoundationSelfCheck


class ResultValidator(Validator):
    validator_id = "TEST-VALIDATOR"
    name = "Test validator"
    description = "Emit a configured test result."

    def __init__(self, status=Status.PASS, severity=Severity.INFO):
        self.status = status
        self.severity = severity

    def validate(self, context):  # type: (ValidationContext) -> list
        return [
            self.result(
                status=self.status,
                severity=self.severity,
                asset="test-asset",
                message="Configured result.",
            )
        ]


class ValidationFoundationTests(unittest.TestCase):
    def test_empty_validation_run_succeeds(self):
        validation_run = run_validators(Path.cwd(), [])

        self.assertEqual(validation_run.exit_code, 0)
        self.assertEqual(validation_run.validators_executed, 0)
        self.assertEqual(validation_run.overall, "PASS")

    def test_minimal_foundation_run_succeeds(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
            validation_run = run_validators(root, [FoundationSelfCheck()])

        self.assertEqual(validation_run.exit_code, 0)
        self.assertEqual(validation_run.passed_checks, 2)

    def test_error_failure_causes_nonzero_exit(self):
        validation_run = run_validators(
            Path.cwd(), [ResultValidator(Status.FAIL, Severity.ERROR)]
        )

        self.assertEqual(validation_run.errors, 1)
        self.assertEqual(validation_run.exit_code, 1)
        self.assertEqual(validation_run.overall, "FAIL")

    def test_warning_does_not_become_error(self):
        validation_run = run_validators(
            Path.cwd(), [ResultValidator(Status.FAIL, Severity.WARNING)]
        )

        self.assertEqual(validation_run.warnings, 1)
        self.assertEqual(validation_run.errors, 0)
        self.assertEqual(validation_run.exit_code, 0)

    def test_result_and_report_serialization(self):
        validation_run = run_validators(Path.cwd(), [ResultValidator()])

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            validation_run.write_json(output)
            report = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(report["report_version"], "2.0")
        self.assertIn("provenance", report)
        self.assertEqual(report["results"][0]["validator_id"], "TEST-VALIDATOR")
        self.assertEqual(report["results"][0]["severity"], "INFO")
        self.assertEqual(report["results"][0]["status"], "PASS")

    def test_summary_counts_and_console_output(self):
        validation_run = ValidationRun(
            validators_executed=2,
            results=(
                ResultValidator().result(
                    status=Status.PASS,
                    severity=Severity.INFO,
                    asset="one.md",
                    message="Passed.",
                ),
                ResultValidator().result(
                    status=Status.FAIL,
                    severity=Severity.WARNING,
                    asset="two.md",
                    message="Warning.",
                ),
            ),
        )

        summary = validation_run.summary()
        self.assertEqual(summary["validators_executed"], 2)
        self.assertEqual(summary["governed_assets_evaluated"], 2)
        self.assertEqual(summary["findings"], 1)
        self.assertEqual(summary["overall"], "PASS")
        self.assertIn("Overall: PASS", format_console_report(validation_run))


if __name__ == "__main__":
    unittest.main()
