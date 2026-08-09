"""Build a reusable immutable-per-run view of governed repository assets."""

import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from tools.validation.markdown import extract_links, markdown_section, resolve_local_target
from tools.validation.metadata import metadata_bearing_files
from tools.validation.yaml_subset import YamlError, extract_frontmatter

from .models import (
    INDEX_FORMAT_VERSION,
    AssetRecord,
    IndexMetrics,
    Relationship,
    RepositoryIndex,
)


METADATA_RELATIONSHIPS = {
    "release": "belongs_to",
    "epic": "belongs_to",
    "sprint": "belongs_to",
    "related_standards": "related_to",
    "related_playbooks": "related_to",
    "supersedes": "supersedes",
}


def _asset_type(path: Path, root: Path, metadata: Dict[str, object]) -> str:
    relative = path.relative_to(root)
    if len(relative.parts) >= 3 and relative.parts[0] == "product":
        return {
            "releases": "release",
            "epics": "epic",
            "sprints": "sprint",
            "stories": "story",
        }.get(relative.parts[1], relative.parts[1])
    if relative.parts[0] == "standards":
        return "standard"
    if relative.parts[0] == "docs" and len(relative.parts) > 1:
        return "{}_document".format(relative.parts[1])
    prefix = str(metadata.get("id", "")).split("-", 1)[0].lower()
    return prefix or "governed_asset"


def _validation_relevance(asset_type: str) -> Tuple[str, ...]:
    common = ("metadata", "framework_id", "links", "hygiene")
    if asset_type == "standard":
        return common + ("structure", "standard_relationships", "catalog")
    if asset_type in ("release", "epic", "sprint", "story"):
        return common + ("product_traceability", "lifecycle")
    return common


class RepositoryView:
    """Parse governed files once and expose a deterministic derived index."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    def build(
        self,
        *,
        source_commit: Optional[str] = None,
        generated_at: Optional[str] = None,
    ) -> RepositoryIndex:
        started = time.monotonic()
        paths = tuple(metadata_bearing_files(self.root))
        parsed = []
        reads = 0
        digest = hashlib.sha256()
        unresolved = []  # type: List[str]
        occurrences = {}  # type: Dict[str, List[str]]

        for path in paths:
            text = path.read_text(encoding="utf-8")
            reads += 1
            relative = path.relative_to(self.root).as_posix()
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(text.encode("utf-8"))
            digest.update(b"\0")
            try:
                metadata, body = extract_frontmatter(text)
            except YamlError as error:
                unresolved.append("{}: malformed metadata: {}".format(relative, error))
                continue
            framework_id = metadata.get("id")
            if not isinstance(framework_id, str):
                unresolved.append("{}: missing string framework ID".format(relative))
                continue
            occurrences.setdefault(framework_id, []).append(relative)
            parsed.append((path, relative, metadata, body))

        duplicates = {
            key: tuple(sorted(values))
            for key, values in occurrences.items()
            if len(values) > 1
        }
        id_to_path = {
            metadata["id"]: relative
            for _path, relative, metadata, _body in parsed
            if metadata["id"] not in duplicates
        }
        path_to_id = {path: framework_id for framework_id, path in id_to_path.items()}

        assets = []  # type: List[AssetRecord]
        relationship_count = 0
        for path, relative, metadata, body in parsed:
            relationships = self._relationships(
                path, relative, metadata, body, id_to_path, path_to_id
            )
            relationship_count += len(relationships)
            for item in relationships:
                if not item.resolved:
                    unresolved.append(
                        "{}: {} target '{}' is unresolved".format(
                            relative, item.relationship_type, item.target
                        )
                    )
            asset_type = _asset_type(path, self.root, metadata)
            assets.append(
                AssetRecord(
                    framework_id=metadata["id"],
                    asset_type=asset_type,
                    title=str(metadata.get("title", metadata["id"])),
                    path=relative,
                    status=self._string(metadata.get("status")),
                    release=self._string(metadata.get("release")),
                    epic=self._string(metadata.get("epic")),
                    sprint=self._string(metadata.get("sprint")),
                    owner=self._string(metadata.get("owner")),
                    validation_relevance=_validation_relevance(asset_type),
                    relationships=relationships,
                )
            )

        duration_ms = int((time.monotonic() - started) * 1000)
        exclusions = tuple(self._gitignore_patterns())
        return RepositoryIndex(
            format_version=INDEX_FORMAT_VERSION,
            source_commit=source_commit or self.current_commit(),
            source_fingerprint=digest.hexdigest(),
            generated_at=generated_at or datetime.now(timezone.utc).isoformat(),
            repository_root=".",
            assets=tuple(sorted(assets, key=lambda item: (item.framework_id, item.path))),
            duplicates=dict(sorted(duplicates.items())),
            unresolved=tuple(sorted(set(unresolved))),
            exclusions=exclusions,
            metrics=IndexMetrics(
                files_inspected=len(paths),
                metadata_files_parsed=len(parsed),
                assets_produced=len(assets),
                relationships_produced=relationship_count,
                source_reads=reads,
                generation_duration_ms=duration_ms,
            ),
        )

    def current_commit(self) -> str:
        try:
            return subprocess.run(
                ("git", "rev-parse", "HEAD"),
                cwd=str(self.root),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return "unavailable"

    def current_fingerprint(self) -> str:
        digest = hashlib.sha256()
        for path in tuple(metadata_bearing_files(self.root)):
            relative = path.relative_to(self.root).as_posix()
            text = path.read_text(encoding="utf-8")
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(text.encode("utf-8"))
            digest.update(b"\0")
        return digest.hexdigest()

    def freshness(self, index: RepositoryIndex) -> Tuple[bool, Tuple[str, ...]]:
        reasons = []
        if index.format_version != INDEX_FORMAT_VERSION:
            reasons.append("index format version is unsupported")
        if index.source_commit != self.current_commit():
            reasons.append("source commit differs from the current repository")
        if index.source_fingerprint != self.current_fingerprint():
            reasons.append("indexed governed files differ from the current repository")
        return not reasons, tuple(reasons)

    @staticmethod
    def write(index: RepositoryIndex, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(index.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def read(path: Path) -> RepositoryIndex:
        return RepositoryIndex.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _relationships(
        self,
        source_path: Path,
        relative: str,
        metadata: Dict[str, object],
        body: str,
        id_to_path: Dict[str, str],
        path_to_id: Dict[str, str],
    ) -> Tuple[Relationship, ...]:
        relationships = []  # type: List[Relationship]
        seen = set()  # type: Set[Tuple[str, str, Optional[str]]]

        def add(kind: str, target: str, target_path: Optional[str], resolved: bool) -> None:
            key = (kind, target, target_path)
            if key not in seen:
                seen.add(key)
                relationships.append(Relationship(kind, target, target_path, resolved))

        for field, relationship_type in METADATA_RELATIONSHIPS.items():
            value = metadata.get(field)
            targets = value if isinstance(value, list) else [value] if isinstance(value, str) else []
            for target in targets:
                target_path = id_to_path.get(target)
                add(relationship_type, target, target_path, target_path is not None)

        for link in extract_links(body):
            target_path, _fragment, error = resolve_local_target(
                self.root, source_path, link.target
            )
            if target_path is None:
                continue
            try:
                target_relative = target_path.relative_to(self.root).as_posix()
            except ValueError:
                continue
            target_id = path_to_id.get(target_relative)
            if target_id:
                add("links_to", target_id, target_relative, error is None)

        if metadata.get("id", "").startswith("STORY-"):
            section = markdown_section(body, "Required Deliverable")
            links = extract_links(section)
            if links:
                target_path, _fragment, error = resolve_local_target(
                    self.root, source_path, links[0].target
                )
                if target_path is not None:
                    target_relative = target_path.relative_to(self.root).as_posix()
                    target = path_to_id.get(target_relative, target_relative)
                    add("produces", target, target_relative, error is None and target_path.exists())

        return tuple(
            sorted(
                relationships,
                key=lambda item: (item.relationship_type, item.target, item.target_path or ""),
            )
        )

    def _gitignore_patterns(self) -> Iterable[str]:
        path = self.root / ".gitignore"
        if not path.exists():
            return (".git/",)
        patterns = [".git/"]
        for raw in path.read_text(encoding="utf-8").splitlines():
            value = raw.strip()
            if value and not value.startswith("#") and not value.startswith("!"):
                patterns.append(value)
        return tuple(dict.fromkeys(patterns))

    @staticmethod
    def _string(value: object) -> Optional[str]:
        return value if isinstance(value, str) else None
