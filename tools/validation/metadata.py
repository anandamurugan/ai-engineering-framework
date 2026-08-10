"""Metadata, schema, and framework-identifier validation."""

import re
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from .models import ScopeCapability, Severity, Status, ValidationContext, ValidationResult, Validator
from .yaml_subset import YamlError, extract_frontmatter, parse_yaml


SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)

PRODUCT_CONTRACTS = {
    "releases": {
        "required": ("id", "title", "version", "status", "owner", "target_release"),
        "id": r"^REL-[0-9]{3,}$",
        "statuses": ("Planned", "In Progress", "Approved", "Released", "Superseded", "Retired"),
    },
    "epics": {
        "required": ("id", "title", "version", "status", "owner", "release", "priority"),
        "id": r"^EPIC-[0-9]{3,}$",
        "statuses": ("Planned", "In Progress", "Approved", "Completed", "Retired"),
    },
    "sprints": {
        "required": ("id", "title", "version", "status", "owner", "release", "epic"),
        "id": r"^SPR-[0-9]{3,}-[0-9]{3,}[A-Z]?$",
        "statuses": ("Planned", "In Progress", "In Review", "Approved", "Completed"),
    },
    "stories": {
        "required": (
            "id", "title", "version", "status", "owner", "release", "epic", "sprint", "priority"
        ),
        "id": r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-[0-9]{3,}$",
        "statuses": ("Proposed", "Ready", "In Progress", "In Review", "Approved", "Done", "Completed"),
    },
}


def governed_product_files(root: Path) -> Iterable[Tuple[Path, Dict[str, Any]]]:
    for asset_type, contract in PRODUCT_CONTRACTS.items():
        for path in sorted((root / "product" / asset_type).glob("*.md")):
            yield path, contract


def standard_files(root: Path) -> Iterable[Path]:
    yield from sorted(path for path in (root / "standards").glob("*/*.md"))


def metadata_bearing_files(root: Path) -> Iterable[Path]:
    excluded = {".git", ".validation-reports", "__pycache__"}
    for path in sorted(root.rglob("*.md")):
        if any(part in excluded for part in path.parts):
            continue
        try:
            with path.open(encoding="utf-8") as document:
                first_line = document.readline().strip()
        except OSError:
            continue
        if first_line == "---":
            yield path


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _schema_errors(value: Any, schema: Dict[str, Any], location: str = "metadata") -> List[str]:
    errors = []  # type: List[str]
    allowed_types = schema.get("type")
    if allowed_types:
        if not isinstance(allowed_types, list):
            allowed_types = [allowed_types]
        type_matches = {
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "boolean": isinstance(value, bool),
            "null": value is None,
        }
        if not any(type_matches.get(item, False) for item in allowed_types):
            return ["{} must have type {}".format(location, " or ".join(allowed_types))]

    if isinstance(value, dict):
        required = schema.get("required") or []
        for field in required:
            if field not in value:
                errors.append("missing required field '{}'".format(field))
        properties = schema.get("properties") or {}
        if schema.get("additionalProperties") is False:
            for field in value:
                if field not in properties:
                    errors.append("unexpected field '{}'".format(field))
        for field, child in value.items():
            if field in properties:
                errors.extend(_schema_errors(child, properties[field], field))

    if isinstance(value, list):
        item_schema = schema.get("items") or {}
        for index, item in enumerate(value):
            errors.extend(_schema_errors(item, item_schema, "{}[{}]".format(location, index)))
        if schema.get("uniqueItems") and len({repr(item) for item in value}) != len(value):
            errors.append("{} must contain unique items".format(location))

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append("{} is shorter than {} characters".format(location, schema["minLength"]))
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append("{} is longer than {} characters".format(location, schema["maxLength"]))
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            errors.append("{} does not match {}".format(location, schema["pattern"]))
        if schema.get("format") == "date":
            try:
                date.fromisoformat(value)
            except ValueError:
                errors.append("{} must be an ISO 8601 date".format(location))

    if "enum" in schema and value not in schema["enum"]:
        errors.append("{} must be one of {}".format(location, ", ".join(schema["enum"])))
    return errors


class MetadataValidator(Validator):
    validator_id = "VAL-META-001"
    name = "Governed metadata and schema"
    description = "Validate product metadata contracts and the standard metadata schema."
    default_severity = Severity.ERROR
    scope_capability = ScopeCapability.TARGETABLE

    def validate(self, context: ValidationContext):
        root = context.repository_root
        results = []  # type: List[ValidationResult]
        schema_path = root / "schemas" / "standard.schema.yaml"
        try:
            schema = parse_yaml(schema_path.read_text(encoding="utf-8"))
        except (OSError, YamlError) as error:
            return [self.result(status=Status.FAIL, asset=_relative(schema_path, root), message=str(error))]

        for path, contract in governed_product_files(root):
            if not context.includes(path):
                continue
            asset = _relative(path, root)
            try:
                metadata, _ = extract_frontmatter(path.read_text(encoding="utf-8"))
                errors = self._product_errors(metadata, contract)
            except (OSError, YamlError) as error:
                errors = ["malformed frontmatter: {}".format(error)]
                metadata = {}
            results.extend(self._asset_results(asset, metadata.get("id"), errors))

        for path in standard_files(root):
            if not context.includes(path):
                continue
            asset = _relative(path, root)
            try:
                metadata, _ = extract_frontmatter(path.read_text(encoding="utf-8"))
                errors = _schema_errors(metadata, schema)
            except (OSError, YamlError) as error:
                errors = ["malformed frontmatter: {}".format(error)]
                metadata = {}
            results.extend(self._asset_results(asset, metadata.get("id"), errors))
        return results

    def _asset_results(
        self, asset: str, framework_id: Optional[str], errors: Sequence[str]
    ) -> List[ValidationResult]:
        if not errors:
            return [
                self.result(
                    status=Status.PASS,
                    severity=Severity.INFO,
                    asset=asset,
                    framework_id=framework_id,
                    message="Metadata conforms to the authoritative contract.",
                )
            ]
        return [
            self.result(
                status=Status.FAIL,
                asset=asset,
                framework_id=framework_id,
                message=error,
            )
            for error in errors
        ]

    @staticmethod
    def _product_errors(metadata: Dict[str, Any], contract: Dict[str, Any]) -> List[str]:
        errors = []
        for field in contract["required"]:
            if field not in metadata:
                errors.append("missing required field '{}'".format(field))
        for field in contract["required"]:
            if field in metadata and not isinstance(metadata[field], str):
                errors.append("field '{}' must be a string".format(field))
        if isinstance(metadata.get("version"), str) and not SEMVER.fullmatch(metadata["version"]):
            errors.append("version must use semantic versioning without a leading v")
        if isinstance(metadata.get("id"), str) and not re.fullmatch(contract["id"], metadata["id"]):
            errors.append("id '{}' does not match {}".format(metadata["id"], contract["id"]))
        if metadata.get("status") not in contract["statuses"]:
            errors.append("status must be one of {}".format(", ".join(contract["statuses"])))
        return errors


class FrameworkIdValidator(Validator):
    validator_id = "VAL-META-ID-001"
    name = "Framework ID uniqueness"
    description = "Validate defined ID formats and repository-wide uniqueness."
    default_severity = Severity.ERROR
    scope_capability = ScopeCapability.REPOSITORY_WIDE

    def validate(self, context: ValidationContext):
        root = context.repository_root
        results = []  # type: List[ValidationResult]
        occurrences = {}  # type: Dict[str, List[str]]

        if context.repository_view is not None:
            for record in context.repository_view.assets:
                occurrences.setdefault(record.framework_id, []).append(record.path)
            for framework_id, paths in context.repository_view.duplicates.items():
                occurrences[framework_id] = list(paths)
        else:
            for path in metadata_bearing_files(root):
                asset = _relative(path, root)
                try:
                    metadata, _ = extract_frontmatter(path.read_text(encoding="utf-8"))
                except (OSError, YamlError):
                    continue
                framework_id = metadata.get("id")
                if isinstance(framework_id, str):
                    occurrences.setdefault(framework_id, []).append(asset)

        duplicates = {key: paths for key, paths in occurrences.items() if len(paths) > 1}
        for framework_id, paths in sorted(duplicates.items()):
            for asset in paths:
                conflicts = ", ".join(path for path in paths if path != asset)
                results.append(
                    self.result(
                        status=Status.FAIL,
                        asset=asset,
                        framework_id=framework_id,
                        message="Duplicate framework ID '{}'; also defined in {}.".format(
                            framework_id, conflicts
                        ),
                    )
                )
        if not duplicates:
            results.append(
                self.result(
                    status=Status.PASS,
                    severity=Severity.INFO,
                    asset="repository",
                    message="All metadata-bearing framework IDs are unique.",
                )
            )
        return results
