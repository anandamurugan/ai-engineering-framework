"""Shared validator and result contracts."""

from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple


class Severity(str, Enum):
    """Impact assigned to an individual validation result."""

    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class Status(str, Enum):
    """Outcome of an individual validation check."""

    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class ValidationContext:
    """Read-only inputs shared with registered validators."""

    repository_root: Path
    registered_validator_ids: Tuple[str, ...]


@dataclass(frozen=True)
class ValidationResult:
    """Attributable evidence emitted by a validator."""

    validator_id: str
    name: str
    description: str
    status: Status
    severity: Severity
    asset: Optional[str]
    framework_id: Optional[str]
    message: str

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation."""

        data = asdict(self)
        data["status"] = self.status.value
        data["severity"] = self.severity.value
        return data


class Validator:
    """Minimal contract implemented by every registered validator."""

    validator_id = ""
    name = ""
    description = ""
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext) -> Sequence[ValidationResult]:
        raise NotImplementedError

    def result(
        self,
        *,
        status: Status,
        message: str,
        asset: Optional[str] = None,
        framework_id: Optional[str] = None,
        severity: Optional[Severity] = None,
    ) -> ValidationResult:
        """Build a result carrying this validator's identity and purpose."""

        return ValidationResult(
            validator_id=self.validator_id,
            name=self.name,
            description=self.description,
            status=status,
            severity=severity or self.default_severity,
            asset=asset,
            framework_id=framework_id,
            message=message,
        )
