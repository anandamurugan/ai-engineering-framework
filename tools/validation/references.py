"""Repository-relative Markdown and standard relationship validation."""

from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

from .markdown import (
    extract_links,
    heading_anchors,
    markdown_files,
    markdown_section,
    resolve_local_target,
)
from .metadata import standard_files
from .models import Severity, Status, ValidationContext, ValidationResult, Validator
from .yaml_subset import YamlError, extract_frontmatter


class RelativeLinkValidator(Validator):
    validator_id = "VAL-REF-LINK-001"
    name = "Repository-relative Markdown links"
    description = "Validate local Markdown paths, filename case, and heading fragments."
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext):
        root = context.repository_root
        results = []  # type: List[ValidationResult]
        files_scanned = 0
        local_links = 0
        broken_links = 0
        for path in markdown_files(root):
            files_scanned += 1
            text = path.read_text(encoding="utf-8")
            asset = path.relative_to(root).as_posix()
            for link in extract_links(text):
                target_path, fragment, error = resolve_local_target(root, path, link.target)
                if target_path is None and error is None:
                    continue
                local_links += 1
                if error is None and fragment:
                    if not target_path.is_file():
                        error = "fragment target is not a Markdown file"
                    elif fragment not in heading_anchors(target_path.read_text(encoding="utf-8")):
                        error = "anchor '#{}' does not exist in target".format(fragment)
                if error:
                    broken_links += 1
                    results.append(
                        self.result(
                            status=Status.FAIL,
                            asset=asset,
                            target=link.target,
                            relationship_type="markdown_link",
                            message="Line {}: {}: {}.".format(link.line, link.target, error),
                        )
                    )
        results.append(
            self.result(
                status=Status.PASS,
                severity=Severity.INFO,
                asset="repository",
                message=(
                    "Scanned {} Markdown files and checked {} local links; {} broken."
                ).format(files_scanned, local_links, broken_links),
            )
        )
        return results


class StandardReferenceValidator(Validator):
    validator_id = "VAL-REF-STD-001"
    name = "Standard cross-references"
    description = "Validate standard relationship targets, navigation, reciprocity, and cycles."
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext):
        root = context.repository_root
        standards = {}
        for path in standard_files(root):
            metadata, body = extract_frontmatter(path.read_text(encoding="utf-8"))
            standards[metadata["id"]] = (path, metadata, body)

        results = []  # type: List[ValidationResult]
        relationships = 0
        failures = 0
        for source_id, (path, metadata, body) in sorted(standards.items()):
            asset = path.relative_to(root).as_posix()
            section_links = extract_links(markdown_section(body, "Related Standards"))
            for relationship_type in ("related_standards", "supersedes"):
                for target_id in metadata.get(relationship_type, []):
                    relationships += 1
                    if target_id not in standards:
                        failures += 1
                        results.append(
                            self._finding(
                                asset, source_id, target_id, relationship_type,
                                "Referenced standard ID does not exist.",
                            )
                        )
                        continue
                    matching_links = [link for link in section_links if target_id in link.label]
                    if relationship_type == "related_standards" and not matching_links:
                        failures += 1
                        results.append(
                            self._finding(
                                asset, source_id, target_id, relationship_type,
                                "Metadata relationship has no matching Related Standards link.",
                            )
                        )
                    for matching_link in matching_links:
                        target_path, _fragment, link_error = resolve_local_target(
                            root, path, matching_link.target
                        )
                        if link_error or target_path is None or not target_path.is_file():
                            continue
                        try:
                            linked_metadata, _ = extract_frontmatter(
                                target_path.read_text(encoding="utf-8")
                            )
                        except (OSError, YamlError):
                            continue
                        if linked_metadata.get("id") != target_id:
                            failures += 1
                            results.append(
                                self._finding(
                                    asset, source_id, target_id, relationship_type,
                                    "Link resolves to framework ID '{}'.".format(
                                        linked_metadata.get("id")
                                    ),
                                )
                            )
                    if relationship_type == "related_standards":
                        target_metadata = standards[target_id][1]
                        if source_id not in target_metadata.get("related_standards", []):
                            results.append(
                                self._finding(
                                    asset, source_id, target_id, relationship_type,
                                    "Optional symmetric navigation is not reciprocal.",
                                    severity=Severity.WARNING,
                                )
                            )
                    if target_id in metadata.get("supersedes", []) and target_id in metadata.get(
                        "related_standards", []
                    ):
                        failures += 1
                        results.append(
                            self._finding(
                                asset, source_id, target_id, relationship_type,
                                "The same target cannot be both related and superseded.",
                            )
                        )

        for cycle in self._supersedes_cycles(standards):
            failures += 1
            source_id = cycle[0]
            path = standards[source_id][0]
            results.append(
                self._finding(
                    path.relative_to(root).as_posix(),
                    source_id,
                    cycle[1],
                    "supersedes",
                    "Prohibited directional cycle: {}.".format(" -> ".join(cycle)),
                )
            )
        results.append(
            self.result(
                status=Status.PASS,
                severity=Severity.INFO,
                asset="standards",
                message="Checked {} standard relationships; {} errors.".format(
                    relationships, failures
                ),
            )
        )
        return results

    def _finding(
        self,
        asset: str,
        source_id: str,
        target_id: str,
        relationship_type: str,
        message: str,
        severity: Severity = Severity.ERROR,
    ) -> ValidationResult:
        return self.result(
            status=Status.FAIL,
            severity=severity,
            asset=asset,
            framework_id=source_id,
            target=target_id,
            relationship_type=relationship_type,
            message="{} -> {} ({}): {}".format(
                source_id, target_id, relationship_type, message
            ),
        )

    @staticmethod
    def _supersedes_cycles(standards: Dict[str, Tuple[Path, dict, str]]) -> Sequence[List[str]]:
        cycles = []
        visited = set()  # type: Set[str]

        def visit(node: str, path: List[str]):
            if node in path:
                cycles.append(path[path.index(node) :] + [node])
                return
            if node in visited or node not in standards:
                return
            for target in standards[node][1].get("supersedes", []):
                visit(target, path + [node])
            visited.add(node)

        for standard_id in standards:
            visit(standard_id, [])
        return cycles
