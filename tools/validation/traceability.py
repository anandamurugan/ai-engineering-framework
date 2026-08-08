"""Standards catalog parity and product hierarchy traceability validation."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .markdown import extract_links, markdown_section, resolve_local_target
from .metadata import governed_product_files, standard_files
from .models import Severity, Status, ValidationContext, ValidationResult, Validator
from .yaml_subset import extract_frontmatter


def _table_rows(section: str) -> Sequence[List[str]]:
    rows = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] in ("ID", "Sprint ID", "Story"):
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def _tracking_id(metadata_id: str) -> str:
    return metadata_id[6:] if metadata_id.startswith("STORY-") else metadata_id


class StandardsCatalogValidator(Validator):
    validator_id = "VAL-TRACE-CATALOG-001"
    name = "Standards catalog parity"
    description = "Compare catalog identity, metadata fields, and paths with governed standards."
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext):
        root = context.repository_root
        catalog_path = root / "standards" / "README.md"
        catalog_text = catalog_path.read_text(encoding="utf-8")
        section = markdown_section(catalog_text, "Versioned standards")
        entries = {}
        for cells in _table_rows(section):
            if len(cells) == 8:
                entries[cells[0]] = cells

        standards = {}
        for path in standard_files(root):
            metadata, _ = extract_frontmatter(path.read_text(encoding="utf-8"))
            standards[metadata["id"]] = (path, metadata)

        results = []  # type: List[ValidationResult]
        mismatches = 0
        for standard_id, (path, metadata) in sorted(standards.items()):
            if standard_id not in entries:
                mismatches += 1
                results.append(
                    self._finding(
                        "standards/README.md", standard_id, "catalog_entry",
                        "Standard exists but is absent from the catalog.",
                    )
                )
                continue
            cells = entries[standard_id]
            expected = {
                "title": metadata["title"],
                "category": metadata["category"],
                "version": metadata["version"],
                "status": metadata["status"],
                "owner": metadata["owner"],
                "mandatory": "Yes" if metadata["mandatory"] else "No",
            }
            actual = dict(zip(expected, cells[1:7]))
            for field, expected_value in expected.items():
                if actual[field] != str(expected_value):
                    mismatches += 1
                    results.append(
                        self._finding(
                            "standards/README.md", standard_id, "catalog_{}".format(field),
                            "Expected '{}'; found '{}'.".format(expected_value, actual[field]),
                        )
                    )
            links = extract_links(cells[7])
            expected_path = path.relative_to(catalog_path.parent).as_posix()
            actual_path = links[0].target if links else ""
            if actual_path != expected_path:
                mismatches += 1
                results.append(
                    self._finding(
                        "standards/README.md", standard_id, "catalog_path",
                        "Expected '{}'; found '{}'.".format(expected_path, actual_path),
                    )
                )

        for standard_id in sorted(set(entries) - set(standards)):
            mismatches += 1
            results.append(
                self._finding(
                    "standards/README.md", standard_id, "catalog_entry",
                    "Catalog entry references a nonexistent standard.",
                )
            )
        results.append(
            self.result(
                status=Status.PASS,
                severity=Severity.INFO,
                asset="standards/README.md",
                message="Checked {} catalog entries; {} mismatches.".format(
                    len(entries), mismatches
                ),
            )
        )
        return results

    def _finding(
        self, asset: str, standard_id: str, relationship_type: str, message: str
    ) -> ValidationResult:
        return self.result(
            status=Status.FAIL,
            asset=asset,
            framework_id=standard_id,
            target=standard_id,
            relationship_type=relationship_type,
            message="{}: {}".format(standard_id, message),
        )


class ProductTraceabilityValidator(Validator):
    validator_id = "VAL-TRACE-PRODUCT-001"
    name = "Product hierarchy traceability"
    description = "Validate product parents, tracked children, deliverables, and explicit lifecycle rules."
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext):
        root = context.repository_root
        assets = {}  # type: Dict[str, Tuple[Path, dict, str, str]]
        by_type = {}  # type: Dict[str, Dict[str, Tuple[Path, dict, str, str]]]
        for path, _contract in governed_product_files(root):
            metadata, body = extract_frontmatter(path.read_text(encoding="utf-8"))
            asset_type = path.parent.name
            record = (path, metadata, body, asset_type)
            assets[metadata["id"]] = record
            by_type.setdefault(asset_type, {})[metadata["id"]] = record

        results = []  # type: List[ValidationResult]
        relationships = 0
        failures = 0
        lifecycle_failures = 0

        parent_fields = {
            "epics": (("release", "releases"),),
            "sprints": (("release", "releases"), ("epic", "epics")),
            "stories": (
                ("release", "releases"),
                ("epic", "epics"),
                ("sprint", "sprints"),
            ),
        }
        for asset_type, fields in parent_fields.items():
            for source_id, (path, metadata, _body, _kind) in by_type.get(
                asset_type, {}
            ).items():
                for field, target_type in fields:
                    relationships += 1
                    target_id = metadata.get(field)
                    target = by_type.get(target_type, {}).get(target_id)
                    if target is None:
                        failures += 1
                        results.append(
                            self._finding(
                                root, path, source_id, str(target_id), "belongs_to",
                                "Referenced {} parent does not exist.".format(field),
                            )
                        )

        failures += self._validate_parent_tables(root, by_type, results)

        for source_id, (path, metadata, body, _kind) in by_type.get(
            "stories", {}
        ).items():
            section = markdown_section(body, "Required Deliverable")
            links = extract_links(section)
            if links:
                relationships += 1
                target_path, _fragment, error = resolve_local_target(
                    root, path, links[0].target
                )
                if error or target_path is None or not target_path.exists():
                    failures += 1
                    results.append(
                        self._finding(
                            root, path, source_id, links[0].target, "produces",
                            "Required deliverable does not exist.",
                        )
                    )
            elif metadata.get("status") in ("Completed", "Done"):
                lifecycle_failures += 1
                results.append(
                    self._finding(
                        root, path, source_id, "required_deliverable", "produces",
                        "Completed story must identify an existing required deliverable.",
                    )
                )

        for sprint_id, (path, metadata, body, _kind) in by_type.get(
            "sprints", {}
        ).items():
            if metadata.get("status") != "Completed":
                continue
            for tracking_id in self._linked_ids(markdown_section(body, "Stories")):
                story = self._story_by_tracking_id(by_type.get("stories", {}), tracking_id)
                if story and story[1].get("status") not in (
                    "Completed", "Done", "Approved"
                ):
                    lifecycle_failures += 1
                    results.append(
                        self._finding(
                            root, path, sprint_id, tracking_id, "contains",
                            "Completed sprint contains an incomplete story.",
                        )
                    )

        results.append(
            self.result(
                status=Status.PASS,
                severity=Severity.INFO,
                asset="product",
                message=(
                    "Checked {} product traceability relationships; {} relationship "
                    "failures and {} lifecycle failures."
                ).format(relationships, failures, lifecycle_failures),
            )
        )
        return results

    def _validate_parent_tables(self, root, by_type, results):
        failures = 0
        configurations = (
            ("releases", "Deliverables", "epics", "release"),
            ("releases", "Deliverables", "sprints", "release"),
            ("epics", "Sprint Breakdown", "sprints", "epic"),
            ("sprints", "Stories", "stories", "sprint"),
        )
        for parent_type, section_name, child_type, parent_field in configurations:
            for parent_id, (path, _metadata, body, _kind) in by_type.get(
                parent_type, {}
            ).items():
                declared = set(self._linked_ids(markdown_section(body, section_name)))
                actual = {
                    _tracking_id(metadata["id"])
                    for _child_id, (_path, metadata, _body, _type) in by_type.get(
                        child_type, {}
                    ).items()
                    if metadata.get(parent_field) == parent_id
                }
                relevant_declared = {
                    item
                    for item in declared
                    if item.startswith(
                        {"epics": "EPIC-", "sprints": "SPR-", "stories": ""}[child_type]
                    )
                }
                for child_id in sorted(actual - relevant_declared):
                    failures += 1
                    results.append(
                        self._finding(
                            root, path, parent_id, child_id, "contains",
                            "Child belongs to parent but is absent from '{}' tracking.".format(
                                section_name
                            ),
                        )
                    )
                for child_id in sorted(relevant_declared - actual):
                    failures += 1
                    results.append(
                        self._finding(
                            root, path, parent_id, child_id, "contains",
                            "Tracked child is missing or does not belong to this parent.",
                        )
                    )
        return failures

    @staticmethod
    def _linked_ids(section: str) -> Sequence[str]:
        ids = []
        for row in _table_rows(section):
            first = row[0] if row else ""
            links = extract_links(first)
            ids.append(links[0].label if links else first)
        return ids

    @staticmethod
    def _story_by_tracking_id(stories, tracking_id):
        return next(
            (
                record
                for story_id, record in stories.items()
                if _tracking_id(story_id) == tracking_id
            ),
            None,
        )

    def _finding(
        self, root, path, source_id, target_id, relationship_type, message
    ):
        return self.result(
            status=Status.FAIL,
            asset=path.relative_to(root).as_posix(),
            framework_id=source_id,
            target=target_id,
            relationship_type=relationship_type,
            message="{} -> {} ({}): {}".format(
                source_id, target_id, relationship_type, message
            ),
        )
