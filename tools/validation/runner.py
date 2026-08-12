"""Deterministic validator execution, aggregation, and reporting."""

import json
import hashlib
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from tools.provenance import evidence_provenance, runtime_identity, utc_timestamp

from .models import (
    Severity, Status, ValidationContext, ValidationMode, ValidationResult, Validator,
)


@dataclass(frozen=True)
class ValidationRun:
    """Complete evidence for one validation execution."""

    validators_executed: int
    results: Sequence[ValidationResult]
    mode: ValidationMode = ValidationMode.FULL
    requested_mode: ValidationMode = ValidationMode.FULL
    repository_commit: str = "unavailable"
    executed_at: str = "unavailable"
    runtime: str = "unavailable"
    validator_ids: Tuple[str, ...] = ()
    scoped_paths: Tuple[str, ...] = ()
    affected_paths: Tuple[str, ...] = ()
    changed_paths: Tuple[str, ...] = ()
    ignored_paths: Tuple[str, ...] = ()
    fallback_reasons: Tuple[str, ...] = ()
    base_commit: Optional[str] = None
    head_commit: Optional[str] = None
    policy_fingerprint: str = "unavailable"
    repository_fingerprint: str = "unavailable"
    repository_files_inspected: int = 0
    repository_source_reads: int = 0
    elapsed_ms: int = 0

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
    def findings(self) -> int:
        return sum(result.status is Status.FAIL for result in self.results)

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
            "governed_assets_evaluated": self.assets_scanned,
            "scoped_assets": len(self.scoped_paths),
            "affected_assets": len(self.affected_paths),
            "findings": self.findings,
            "repository_files_inspected": self.repository_files_inspected,
            "repository_source_reads": self.repository_source_reads,
            "errors": self.errors,
            "warnings": self.warnings,
            "passed_checks": self.passed_checks,
            "overall": self.overall,
            "elapsed_ms": self.elapsed_ms,
        }

    def to_dict(self) -> Dict[str, Any]:
        common = evidence_provenance(
            evidence_type="validation_report",
            repository_commit=self.repository_commit,
            generated_at=self.executed_at,
            runtime=self.runtime,
            operation="validation",
            requested_scope=self.scoped_paths,
            effective_scope=self.affected_paths,
            result=self.overall,
        )
        return {
            "report_version": "2.0",
            "provenance": {
                **common,
                "repository_commit": self.repository_commit,
                "base_commit": self.base_commit,
                "head_commit": self.head_commit or self.repository_commit,
                "executed_at": self.executed_at,
                "runtime": self.runtime,
                "validator_ids": list(self.validator_ids),
                "validation_mode": self.mode.value,
                "requested_mode": self.requested_mode.value,
                "validation_scope": list(self.scoped_paths),
                "changed_paths": list(self.changed_paths),
                "affected_closure": list(self.affected_paths),
                "ignored_paths": list(self.ignored_paths),
                "fallback_reasons": list(self.fallback_reasons),
                "policy_fingerprint": self.policy_fingerprint,
                "repository_fingerprint": self.repository_fingerprint,
            },
            "summary": self.summary(),
            "results": [result.to_dict() for result in self.results],
        }

    def write_json(self, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def validate_registry(validators: Iterable[Validator]) -> Tuple[Validator, ...]:
    """Fail deterministically for invalid or duplicate registry entries."""

    registered = tuple(validators)
    seen = set()
    for item in registered:
        if not isinstance(item, Validator):
            raise ValueError("Registry entry does not implement Validator: {!r}".format(item))
        if not isinstance(item.validator_id, str) or not item.validator_id.strip():
            raise ValueError("Registered validator has an invalid or missing validator ID")
        if item.validator_id in seen:
            raise ValueError("Duplicate validator ID: {}".format(item.validator_id))
        seen.add(item.validator_id)
    return registered


def run_validators(
    repository_root: Path, validators: Iterable[Validator], *,
    plan: Optional[Any] = None, repository_view: Optional[Any] = None,
) -> ValidationRun:
    """Execute validators without changing governed repository content."""

    started = time.monotonic()
    registered = validate_registry(validators)
    mode = plan.effective_mode if plan else ValidationMode.FULL
    scoped = plan.requested_paths if plan else ()
    affected = plan.affected_paths if plan else ()
    context = ValidationContext(
        repository_root=repository_root.resolve(),
        registered_validator_ids=tuple(item.validator_id for item in registered),
        mode=mode,
        scoped_paths=scoped,
        affected_paths=affected,
        repository_view=repository_view,
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
                    asset=(affected[0] if len(affected) == 1 else "validation_scope"),
                    message="Validator execution failed with unexpected {}.".format(
                        type(error).__name__
                    ),
                )
            )

    ids = tuple(item.validator_id for item in registered)
    fingerprint = hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()
    return ValidationRun(
        validators_executed=len(registered), results=tuple(results), mode=mode,
        requested_mode=plan.requested_mode if plan else ValidationMode.FULL,
        repository_commit=plan.head_commit if plan else _git_commit(repository_root),
        executed_at=utc_timestamp(),
        runtime=runtime_identity(),
        validator_ids=ids, scoped_paths=scoped, affected_paths=affected,
        changed_paths=plan.requested_paths if plan else (),
        ignored_paths=plan.ignored_paths if plan else (),
        fallback_reasons=plan.fallback_reasons if plan else (),
        base_commit=plan.base_commit if plan else None,
        head_commit=plan.head_commit if plan else None,
        policy_fingerprint=fingerprint,
        repository_fingerprint=getattr(repository_view, "source_fingerprint", "unavailable"),
        repository_files_inspected=getattr(getattr(repository_view, "metrics", None), "files_inspected", 0),
        repository_source_reads=getattr(getattr(repository_view, "metrics", None), "source_reads", 0),
        elapsed_ms=int((time.monotonic() - started) * 1000),
    )


def _git_commit(root: Path) -> str:
    try:
        import subprocess
        return subprocess.run(
            ("git", "rev-parse", "HEAD"), cwd=str(root), check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


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
            "Scoped assets: {scoped_assets}".format(**summary),
            "Affected assets: {affected_assets}".format(**summary),
            "Findings: {findings}".format(**summary),
            "Repository files inspected: {repository_files_inspected}".format(**summary),
            "Repository source reads: {repository_source_reads}".format(**summary),
            "Errors: {errors}".format(**summary),
            "Warnings: {warnings}".format(**summary),
            "Passed checks: {passed_checks}".format(**summary),
            "Overall: {overall}".format(**summary),
            "Mode: {}".format(validation_run.mode.value),
            "Coverage: {}".format(
                "entire repository" if validation_run.mode is ValidationMode.FULL
                else "selected and affected scope only"
            ),
        ]
    )
    return "\n".join(lines)
