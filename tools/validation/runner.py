"""Deterministic validator execution, aggregation, and reporting."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

from .models import Severity, Status, ValidationContext, ValidationResult, Validator


@dataclass(frozen=True)
class ValidationRun:
    """Complete evidence for one validation execution."""

    validators_executed: int
    results: Sequence[ValidationResult]

    @property
    def errors(self) -> int:
        return sum(
            result.status is Status.FAIL and result.severity is Severity.ERROR
            for result in self.results
        )

    @property
    def warnings(self) -> int:
        return sum(
            result.status is Status.FAIL and result.severity is Severity.WARNING
            for result in self.results
        )

    @property
    def passed_checks(self) -> int:
        return sum(result.status is Status.PASS for result in self.results)

    @property
    def assets_scanned(self) -> int:
        return len({result.asset for result in self.results if result.asset})

    @property
    def overall(self) -> str:
        return "FAIL" if self.errors else "PASS"

    @property
    def exit_code(self) -> int:
        return 1 if self.errors else 0

    def summary(self) -> Dict[str, Any]:
        return {
            "validators_executed": self.validators_executed,
            "assets_scanned": self.assets_scanned,
            "errors": self.errors,
            "warnings": self.warnings,
            "passed_checks": self.passed_checks,
            "overall": self.overall,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_version": "1.0",
            "summary": self.summary(),
            "results": [result.to_dict() for result in self.results],
        }

    def write_json(self, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def run_validators(
    repository_root: Path, validators: Iterable[Validator]
) -> ValidationRun:
    """Execute validators without changing governed repository content."""

    registered = tuple(validators)
    context = ValidationContext(
        repository_root=repository_root.resolve(),
        registered_validator_ids=tuple(item.validator_id for item in registered),
    )
    results = []  # type: List[ValidationResult]

    for validator in registered:
        try:
            results.extend(validator.validate(context))
        except Exception as error:  # Convert unexpected check failure into evidence.
            results.append(
                validator.result(
                    status=Status.FAIL,
                    severity=Severity.ERROR,
                    asset=None,
                    message="Validator execution failed: {}".format(error),
                )
            )

    return ValidationRun(validators_executed=len(registered), results=tuple(results))


def format_console_report(validation_run: ValidationRun) -> str:
    """Render concise, deterministic output for developers and CI logs."""

    lines = []
    for result in validation_run.results:
        target = " [{}]".format(result.asset) if result.asset else ""
        lines.append(
            "{} {} {}{}: {}".format(
                result.status.value,
                result.severity.value,
                result.validator_id,
                target,
                result.message,
            )
        )

    summary = validation_run.summary()
    lines.extend(
        [
            "",
            "Validation summary",
            "Validators executed: {validators_executed}".format(**summary),
            "Assets scanned: {assets_scanned}".format(**summary),
            "Errors: {errors}".format(**summary),
            "Warnings: {warnings}".format(**summary),
            "Passed checks: {passed_checks}".format(**summary),
            "Overall: {overall}".format(**summary),
        ]
    )
    return "\n".join(lines)
