"""Deterministic repository hygiene checks with governed exclusions."""

import re
import subprocess
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

from .markdown import markdown_files
from .models import Severity, Status, ValidationContext, ValidationResult, Validator


EXCLUDED_DIRECTORIES = {".git", ".validation-reports", "__pycache__"}
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".txt",
}
PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:todo|tbd|fixme|placeholder|lorem\s+ipsum|coming\s+soon)\b",
    re.IGNORECASE,
)
PLACEHOLDER_EXCLUDED_PREFIXES = ("templates/", "tests/")
PLACEHOLDER_EXCLUDED_FILES = {
    "CHANGELOG.md",
    "docs/contributing/DOCUMENTATION_STYLE_GUIDE.md",
    "product/stories/VAL-HYGIENE-001-repository-hygiene-validation.md",
    "tools/validation/README.md",
}
PLACEHOLDER_ALLOWED_LINES = {
    "product/releases/REL-v0.4.md": (re.compile(r"^target_release: TBD$"),),
}
PLACEHOLDER_ALLOWED_GLOBAL_LINES = (
    re.compile(r"^Validate .*placeholder absence\.$"),
    re.compile(r"^- Sprint 4\.3 .*no prohibited placeholder text\.$"),
    re.compile(
        r"^- Metadata, schema, framework ID, structure, link, relationship, "
        r"catalog, traceability, placeholder, whitespace, and Markdown validation$"
    ),
)
IGNORED_TRACKED_PATTERNS = (
    re.compile(r"(^|/)\.validation-reports(/|$)"),
    re.compile(r"(^|/)__pycache__(/|$)"),
    re.compile(r"\.py[cod]$"),
)


def repository_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and not any(part in EXCLUDED_DIRECTORIES for part in path.parts):
            yield path


def text_files(root: Path) -> Iterable[Path]:
    for path in repository_files(root):
        if path.suffix.lower() in TEXT_SUFFIXES or path.name == ".gitignore":
            yield path


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _tracked_paths(root: Path) -> Sequence[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode == 0:
        return tuple(
            item.decode("utf-8") for item in completed.stdout.split(b"\0") if item
        )
    return tuple(_relative(path, root) for path in sorted(root.rglob("*")) if path.is_file())


class PlaceholderValidator(Validator):
    validator_id = "VAL-HYGIENE-PLACEHOLDER-001"
    name = "Unresolved content placeholders"
    description = "Detect unresolved placeholder markers in governed repository content."
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext):
        root = context.repository_root
        results = []  # type: List[ValidationResult]
        scanned = 0
        findings = 0
        for path in text_files(root):
            if path.suffix.lower() not in {".md", ".yaml", ".yml", ".txt"}:
                continue
            asset = _relative(path, root)
            if asset in PLACEHOLDER_EXCLUDED_FILES or asset.startswith(
                PLACEHOLDER_EXCLUDED_PREFIXES
            ):
                continue
            scanned += 1
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if not PLACEHOLDER_PATTERN.search(line):
                    continue
                if any(
                    pattern.fullmatch(line)
                    for pattern in PLACEHOLDER_ALLOWED_LINES.get(asset, ())
                ):
                    continue
                if any(pattern.fullmatch(line) for pattern in PLACEHOLDER_ALLOWED_GLOBAL_LINES):
                    continue
                findings += 1
                results.append(
                    self.result(
                        status=Status.FAIL,
                        asset=asset,
                        message="Line {} contains unresolved placeholder text: {}".format(
                            line_number, PLACEHOLDER_PATTERN.search(line).group(0)
                        ),
                    )
                )
        results.append(
            self.result(
                status=Status.PASS,
                severity=Severity.INFO,
                asset="repository",
                message="Scanned {} governed text files; {} placeholders found.".format(
                    scanned, findings
                ),
            )
        )
        return results


class TrailingWhitespaceValidator(Validator):
    validator_id = "VAL-HYGIENE-WHITESPACE-001"
    name = "Trailing whitespace"
    description = "Detect trailing spaces and tabs in repository text files."
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext):
        root = context.repository_root
        results = []  # type: List[ValidationResult]
        scanned = 0
        findings = 0
        for path in text_files(root):
            scanned += 1
            asset = _relative(path, root)
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                match = re.search(r"[ \t]+$", line)
                if match:
                    findings += 1
                    kind = "tab" if "\t" in match.group(0) else "space"
                    results.append(
                        self.result(
                            status=Status.FAIL,
                            asset=asset,
                            message="Line {} has trailing {} whitespace.".format(
                                line_number, kind
                            ),
                        )
                    )
        results.append(
            self.result(
                status=Status.PASS,
                severity=Severity.INFO,
                asset="repository",
                message="Scanned {} text files; {} trailing-whitespace findings.".format(
                    scanned, findings
                ),
            )
        )
        return results


class MarkdownHygieneValidator(Validator):
    validator_id = "VAL-HYGIENE-MARKDOWN-001"
    name = "Basic Markdown hygiene"
    description = "Validate H1 count, heading hierarchy, heading syntax, and fenced blocks."
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext):
        root = context.repository_root
        results = []  # type: List[ValidationResult]
        scanned = 0
        findings = 0
        for path in markdown_files(root):
            scanned += 1
            asset = _relative(path, root)
            errors = self._errors(path.read_text(encoding="utf-8"))
            findings += len(errors)
            results.extend(
                self.result(status=Status.FAIL, asset=asset, message=message)
                for message in errors
            )
        results.append(
            self.result(
                status=Status.PASS,
                severity=Severity.INFO,
                asset="repository",
                message="Scanned {} Markdown files; {} hygiene findings.".format(
                    scanned, findings
                ),
            )
        )
        return results

    @staticmethod
    def _errors(text: str) -> Sequence[str]:
        errors = []  # type: List[str]
        headings = []  # type: List[Tuple[int, int]]
        fence = None
        for line_number, line in enumerate(text.splitlines(), start=1):
            fence_match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
            if fence_match:
                marker = fence_match.group(1)
                if fence is None:
                    fence = (marker[0], len(marker), line_number)
                elif marker[0] == fence[0] and len(marker) >= fence[1]:
                    fence = None
                continue
            if fence is not None:
                continue
            if re.match(r"^#{1,6}$", line):
                errors.append("Line {} contains an empty heading.".format(line_number))
                continue
            malformed = re.match(r"^(#{1,6})[^#\s]", line)
            if malformed:
                errors.append(
                    "Line {} has invalid heading formatting; add a space after '#'.".format(
                        line_number
                    )
                )
                continue
            heading = re.match(r"^(#{1,6})\s+\S", line)
            if heading:
                headings.append((len(heading.group(1)), line_number))
        if fence is not None:
            errors.append("Line {} opens an unclosed fenced code block.".format(fence[2]))
        h1_lines = [line for level, line in headings if level == 1]
        if len(h1_lines) != 1:
            errors.append("Expected exactly one H1 heading; found {}.".format(len(h1_lines)))
        for (previous, _line), (current, current_line) in zip(headings, headings[1:]):
            if current > previous + 1:
                errors.append(
                    "Line {} skips heading level H{} to H{}.".format(
                        current_line, previous, current
                    )
                )
        return errors


class TrackedArtifactValidator(Validator):
    validator_id = "VAL-HYGIENE-ARTIFACT-001"
    name = "Tracked generated and cache artifacts"
    description = "Detect tracked files prohibited by repository ignore conventions."
    default_severity = Severity.ERROR

    def validate(self, context: ValidationContext):
        tracked = _tracked_paths(context.repository_root)
        results = []  # type: List[ValidationResult]
        findings = 0
        for asset in tracked:
            if any(pattern.search(asset) for pattern in IGNORED_TRACKED_PATTERNS):
                findings += 1
                results.append(
                    self.result(
                        status=Status.FAIL,
                        asset=asset,
                        message="Tracked artifact conflicts with repository .gitignore conventions.",
                    )
                )
        results.append(
            self.result(
                status=Status.PASS,
                severity=Severity.INFO,
                asset="repository",
                message="Checked {} tracked files; {} prohibited artifacts.".format(
                    len(tracked), findings
                ),
            )
        )
        return results
