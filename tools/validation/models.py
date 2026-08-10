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


class ValidationMode(str, Enum):
    """Explicit validation coverage requested by a caller."""

    FULL = "FULL"
    TARGETED_ASSET = "TARGETED_ASSET"
    CHANGED_FILES = "CHANGED_FILES"
    AFFECTED_CLOSURE = "AFFECTED_CLOSURE"


class ScopeCapability(str, Enum):
    """Whether a validator can safely limit file-level evaluation."""

    TARGETABLE = "TARGETABLE"
    REPOSITORY_WIDE = "REPOSITORY_WIDE"


@dataclass(frozen=True)
class ValidationContext:
    """Read-only inputs shared with registered validators."""

    repository_root: Path
    registered_validator_ids: Tuple[str, ...]
    mode: ValidationMode = ValidationMode.FULL
    scoped_paths: Tuple[str, ...] = ()
    affected_paths: Tuple[str, ...] = ()
    repository_view: Optional[Any] = None

    def includes(self, path: Path) -> bool:
        """Return whether a path belongs to the active targeted scope."""

        if self.mode is ValidationMode.FULL:
            return True
        try:
            relative = path.resolve().relative_to(self.repository_root).as_posix()
        except ValueError:
            return False
        return relative in set(self.affected_paths or self.scoped_paths)


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
    target: Optional[str]
    relationship_type: Optional[str]
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
    scope_capability = ScopeCapability.REPOSITORY_WIDE

    def validate(self, context: ValidationContext) -> Sequence[ValidationResult]:
        raise NotImplementedError

    def result(
        self,
        *,
        status: Status,
        message: str,
        asset: Optional[str] = None,
        framework_id: Optional[str] = None,
        target: Optional[str] = None,
        relationship_type: Optional[str] = None,
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
            target=target,
            relationship_type=relationship_type,
            message=message,
        )
