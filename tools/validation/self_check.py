"""Foundational checks that prove the runner and registry can execute."""

from .models import Severity, Status, ValidationContext, ValidationResult, Validator


class FoundationSelfCheck(Validator):
    """Verify only foundation prerequisites, not governed content."""

    validator_id = "VAL-FWK-SELF-001"
    name = "Validation framework self-check"
    description = "Verify repository-root resolution and registry loading."
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext):  # type: (ValidationContext) -> list[ValidationResult]
        results = []
        root = context.repository_root

        root_resolved = root.is_dir() and (root / "AGENTS.md").is_file()
        results.append(
            self.result(
                status=Status.PASS if root_resolved else Status.FAIL,
                severity=Severity.INFO if root_resolved else Severity.ERROR,
                asset=str(root),
                message=(
                    "Repository root resolved."
                    if root_resolved
                    else "Repository root must contain AGENTS.md."
                ),
            )
        )

        registry_loaded = bool(context.registered_validator_ids)
        results.append(
            self.result(
                status=Status.PASS if registry_loaded else Status.FAIL,
                severity=Severity.INFO if registry_loaded else Severity.ERROR,
                asset="tools/validation/registry.py",
                message=(
                    "Validator registry loaded."
                    if registry_loaded
                    else "Validator registry did not provide any validators."
                ),
            )
        )
        return results
