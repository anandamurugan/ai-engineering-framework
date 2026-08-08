"""Markdown link extraction and deterministic local-target resolution."""

import re
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


INLINE_LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXTERNAL_SCHEMES = {
    "http",
    "https",
    "mailto",
    "ftp",
    "ftps",
    "tel",
    "data",
    "urn",
}


@dataclass(frozen=True)
class MarkdownLink:
    label: str
    target: str
    line: int


def markdown_files(root: Path) -> Iterable[Path]:
    excluded = {".git", ".validation-reports", "__pycache__"}
    for path in sorted(root.rglob("*.md")):
        if not any(part in excluded for part in path.parts):
            yield path


def extract_links(text: str) -> Sequence[MarkdownLink]:
    links = []  # type: List[MarkdownLink]
    fenced = False
    offset = 0
    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            fenced = not fenced
        if not fenced:
            for match in INLINE_LINK.finditer(line):
                raw_target = match.group(2).strip()
                if raw_target.startswith("<") and raw_target.endswith(">"):
                    raw_target = raw_target[1:-1]
                elif " " in raw_target:
                    raw_target = raw_target.split(" ", 1)[0]
                links.append(MarkdownLink(match.group(1), raw_target, line_number))
        offset += len(line)
    return links


def heading_anchors(text: str) -> Sequence[str]:
    anchors = []  # type: List[str]
    counts = {}
    for heading in HEADING.findall(text):
        label = re.sub(r"<[^>]+>", "", heading)
        label = label.strip().lower()
        label = re.sub(r"[^\w\- ]", "", label, flags=re.UNICODE)
        label = re.sub(r"\s+", "-", label)
        count = counts.get(label, 0)
        counts[label] = count + 1
        anchors.append(label if count == 0 else "{}-{}".format(label, count))
    return anchors


def resolve_local_target(
    root: Path, source: Path, raw_target: str
) -> Tuple[Optional[Path], Optional[str], Optional[str]]:
    """Return resolved path, decoded fragment, and an error message."""

    parsed = urllib.parse.urlsplit(raw_target)
    if parsed.scheme.lower() in EXTERNAL_SCHEMES:
        return None, None, None
    if parsed.scheme or parsed.netloc:
        return None, None, "unsupported URI scheme or network-path reference"
    if parsed.query:
        return None, None, "query strings are not supported for repository links"
    decoded_path = urllib.parse.unquote(parsed.path)
    fragment = urllib.parse.unquote(parsed.fragment)
    if "\\" in decoded_path:
        return None, fragment, "repository links must use forward slashes"
    if decoded_path.startswith("/"):
        return None, fragment, "repository links must be relative"

    candidate = source if not decoded_path else source.parent / decoded_path
    normalized = candidate.resolve()
    try:
        normalized.relative_to(root.resolve())
    except ValueError:
        return None, fragment, "relative target resolves outside the repository"

    current = root.resolve()
    relative = normalized.relative_to(current)
    for component in relative.parts:
        if not current.is_dir():
            return normalized, fragment, "target does not exist"
        names = {entry.name for entry in current.iterdir()}
        if component not in names:
            case_match = next((name for name in names if name.lower() == component.lower()), None)
            if case_match:
                return normalized, fragment, "target path has incorrect filename case"
            return normalized, fragment, "target does not exist"
        current = current / component
    return normalized, fragment, None


def markdown_section(text: str, heading: str) -> str:
    pattern = re.compile(
        r"^##\s+{}\s*$\n(.*?)(?=^##\s+|\Z)".format(re.escape(heading)),
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1) if match else ""
