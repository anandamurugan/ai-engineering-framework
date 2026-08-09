"""Required standard section and document-structure validation."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .metadata import standard_files
from .models import ScopeCapability, Severity, Status, ValidationContext, ValidationResult, Validator
from .yaml_subset import YamlError, extract_frontmatter


H1 = re.compile(r"^# (.+)$", re.MULTILINE)
H2 = re.compile(r"^## (.+)$", re.MULTILINE)


class DocumentStructureValidator(Validator):
    validator_id = "VAL-STRUCT-001"
    name = "Standard document structure"
    description = "Validate standard H1 identity, required sections, order, and structural tables."
    default_severity = Severity.ERROR
    scope_capability = ScopeCapability.TARGETABLE

    def validate(self, context: ValidationContext):
        root = context.repository_root
        template_path = root / "templates" / "standard-template.md"
        try:
            _, template_body = extract_frontmatter(template_path.read_text(encoding="utf-8"))
            required_sections = H2.findall(template_body)
        except (OSError, YamlError) as error:
            return [
                self.result(
                    status=Status.FAIL,
                    asset=template_path.relative_to(root).as_posix(),
                    message="Cannot load authoritative section order: {}".format(error),
                )
            ]

        results = []  # type: List[ValidationResult]
        for path in standard_files(root):
            if not context.includes(path):
                continue
            asset = path.relative_to(root).as_posix()
            try:
                metadata, body = extract_frontmatter(path.read_text(encoding="utf-8"))
                errors = self._errors(body, metadata, required_sections)
            except (OSError, YamlError) as error:
                errors = ["Cannot inspect structure: {}".format(error)]
                metadata = {}
            if errors:
                results.extend(
                    self.result(
                        status=Status.FAIL,
                        asset=asset,
                        framework_id=metadata.get("id"),
                        message=message,
                    )
                    for message in errors
                )
            else:
                results.append(
                    self.result(
                        status=Status.PASS,
                        severity=Severity.INFO,
                        asset=asset,
                        framework_id=metadata.get("id"),
                        message="Required standard structure and section order conform.",
                    )
                )
        return results

    @staticmethod
    def _errors(
        body: str, metadata: Dict[str, object], required_sections: Sequence[str]
    ) -> List[str]:
        errors = []  # type: List[str]
        h1s = H1.findall(body)
        expected_h1 = "{} – {}".format(metadata.get("id", ""), metadata.get("title", ""))
        if len(h1s) != 1:
            errors.append("Expected exactly one H1 heading; found {}.".format(len(h1s)))
        elif h1s[0] != expected_h1:
            errors.append("H1 must be '# {}'; found '# {}'.".format(expected_h1, h1s[0]))

        actual_sections = H2.findall(body)
        positions = {}  # type: Dict[str, List[int]]
        for index, heading in enumerate(actual_sections):
            positions.setdefault(heading, []).append(index)
        for heading in required_sections:
            count = len(positions.get(heading, []))
            if count == 0:
                errors.append("Missing required section '## {}'.".format(heading))
            elif count > 1:
                errors.append("Required section '## {}' appears {} times.".format(heading, count))

        present = [heading for heading in required_sections if len(positions.get(heading, [])) == 1]
        for previous, current in zip(present, present[1:]):
            if positions[previous][0] > positions[current][0]:
                errors.append(
                    "Expected '{}' before '{}'; actual order is reversed.".format(previous, current)
                )

        sections = DocumentStructureValidator._section_bodies(body)
        mandatory = sections.get("Mandatory Rules", "")
        if mandatory and not re.search(r"^\d+\.\s+", mandatory, re.MULTILINE):
            errors.append("Mandatory Rules must contain at least one numbered rule.")
        revision = sections.get("Revision History", "")
        expected_header = "| Version | Date | Change | Author | Approval |"
        expected_separator = "| --- | --- | --- | --- | --- |"
        if revision and (expected_header not in revision or expected_separator not in revision):
            errors.append("Revision History must use the five-column template table.")
        return errors

    @staticmethod
    def _section_bodies(body: str) -> Dict[str, str]:
        matches = list(H2.finditer(body))
        sections = {}
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
            sections[match.group(1)] = body[match.end() : end]
        return sections
