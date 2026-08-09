"""Deterministic Git change discovery and affected-scope planning."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from tools.context.models import RepositoryIndex
from tools.context.repository import RepositoryView

from .models import ValidationMode


FULL_FALLBACK_PREFIXES = (
    ".github/workflows/",
    "schemas/",
    "templates/",
    "tools/validation/",
)
FULL_FALLBACK_PATHS = {
    "docs/architecture/CROSS_REFERENCE_MODEL.md",
    "docs/framework/FRAMEWORK_ASSETS.md",
    "product/releases/REL-v0.5.md",
    "standards/README.md",
}


@dataclass(frozen=True)
class ChangeSet:
    base: Optional[str]
    head: str
    changed_paths: Tuple[str, ...]
    ignored_paths: Tuple[str, ...] = ()
    unresolved_paths: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ValidationPlan:
    requested_mode: ValidationMode
    effective_mode: ValidationMode
    requested_paths: Tuple[str, ...]
    affected_paths: Tuple[str, ...]
    affected_ids: Tuple[str, ...]
    ignored_paths: Tuple[str, ...]
    unresolved_paths: Tuple[str, ...]
    fallback_reasons: Tuple[str, ...]
    base_commit: Optional[str]
    head_commit: str

    @property
    def fallback_used(self) -> bool:
        return self.effective_mode is ValidationMode.FULL and self.requested_mode is not ValidationMode.FULL


class GitChangeDiscovery:
    """Discover changes with fixed Git argument arrays and no shell execution."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    def discover(
        self, *, base: Optional[str] = None, head: str = "HEAD", working_tree: bool = False
    ) -> ChangeSet:
        if working_tree:
            command = ("git", "status", "--porcelain=v1", "-z", "--untracked-files=all")
            output = self._run(command)
            paths = self._porcelain_paths(output)
            resolved_head = self._revision("HEAD")
            resolved_base = None
        else:
            if not base:
                raise ValueError("base is required for commit-range discovery")
            command = (
                "git", "diff", "--name-status", "-z", "--find-renames", base, head, "--"
            )
            output = self._run(command)
            paths = self._name_status_paths(output)
            resolved_base = self._revision(base)
            resolved_head = self._revision(head)
        ignored, changed = self._partition_ignored(paths)
        return ChangeSet(resolved_base, resolved_head, tuple(sorted(changed)), tuple(sorted(ignored)))

    def _run(self, command: Sequence[str]) -> str:
        return subprocess.run(
            tuple(command), cwd=str(self.root), check=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True,
        ).stdout

    def _revision(self, revision: str) -> str:
        return self._run(("git", "rev-parse", "--verify", revision)).strip()

    @staticmethod
    def _porcelain_paths(output: str) -> Set[str]:
        fields = output.split("\0")
        paths = set()
        index = 0
        while index < len(fields):
            field = fields[index]
            if not field:
                index += 1
                continue
            status, path = field[:2], field[3:]
            paths.add(path)
            if status[0] in ("R", "C") and index + 1 < len(fields):
                paths.add(fields[index + 1])
                index += 1
            index += 1
        return paths

    @staticmethod
    def _name_status_paths(output: str) -> Set[str]:
        fields = [field for field in output.split("\0") if field]
        paths = set()
        index = 0
        while index < len(fields):
            status = fields[index]
            index += 1
            count = 2 if status.startswith(("R", "C")) else 1
            for _ in range(count):
                if index < len(fields):
                    paths.add(fields[index])
                    index += 1
        return paths

    def _partition_ignored(self, paths: Iterable[str]) -> Tuple[Set[str], Set[str]]:
        ignored, changed = set(), set()
        for path in paths:
            result = subprocess.run(
                ("git", "check-ignore", "-q", "--", path), cwd=str(self.root),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            (ignored if result.returncode == 0 else changed).add(path)
        return ignored, changed


class AffectedScopePlanner:
    """Map requested paths/assets onto authoritative indexed relationships."""

    def __init__(self, root: Path, index: RepositoryIndex):
        self.root = root.resolve()
        self.index = index
        self.by_path = {asset.path: asset for asset in index.assets}
        self.by_id = {asset.framework_id: asset for asset in index.assets}

    def plan(
        self,
        mode: ValidationMode,
        *,
        paths: Sequence[str] = (),
        asset_ids: Sequence[str] = (),
        base_commit: Optional[str] = None,
        head_commit: Optional[str] = None,
        ignored_paths: Sequence[str] = (),
        unresolved_paths: Sequence[str] = (),
    ) -> ValidationPlan:
        head = head_commit or RepositoryView(self.root).current_commit()
        requested = set(path.replace("\\", "/") for path in paths)
        unresolved = set(unresolved_paths)
        reasons = []  # type: List[str]

        if mode is ValidationMode.FULL:
            return self._full_plan(mode, requested, ignored_paths, unresolved, (), base_commit, head)
        fresh, freshness_reasons = RepositoryView(self.root).freshness(self.index)
        if not fresh:
            reasons.extend("Stale repository index: {}".format(item) for item in freshness_reasons)
        if self.index.duplicates:
            reasons.append("Repository index contains duplicate framework identities.")
        for asset_id in asset_ids:
            asset = self.by_id.get(asset_id) or self.by_id.get("STORY-" + asset_id)
            if asset:
                requested.add(asset.path)
            else:
                unresolved.add(asset_id)
        for path in tuple(requested):
            if self._requires_full(path):
                reasons.append("Governance-sensitive path requires full validation: {}".format(path))
            if path not in self.by_path:
                unresolved.add(path)
        if unresolved:
            reasons.append("Changed or requested paths could not be mapped safely.")
        if reasons:
            return self._full_plan(mode, requested, ignored_paths, unresolved, reasons, base_commit, head)

        affected_ids = set()  # type: Set[str]
        affected_paths = set(requested)
        frontier = [self.by_path[path].framework_id for path in sorted(requested)]
        reverse = self._reverse_relationships()
        while frontier:
            source_id = frontier.pop(0)
            if source_id in affected_ids:
                continue
            affected_ids.add(source_id)
            source = self.by_id[source_id]
            affected_paths.add(source.path)
            neighbors = self._propagated_targets(source_id, reverse)
            for target_id in sorted(neighbors):
                target = self.by_id.get(target_id)
                if target and target_id not in affected_ids:
                    affected_paths.add(target.path)
                    frontier.append(target_id)
        return ValidationPlan(
            mode, mode, tuple(sorted(requested)), tuple(sorted(affected_paths)),
            tuple(sorted(affected_ids)), tuple(sorted(ignored_paths)), tuple(sorted(unresolved)),
            (), base_commit, head,
        )

    def _propagated_targets(self, source_id: str, reverse: Dict[str, Set[str]]) -> Set[str]:
        asset = self.by_id[source_id]
        targets = set()
        authoritative = {"belongs_to", "produces", "supersedes", "related_to"}
        for relationship in asset.relationships:
            if relationship.resolved and relationship.relationship_type in authoritative:
                targets.add(relationship.target)
        targets.update(reverse.get(source_id, set()))
        return targets

    def _reverse_relationships(self) -> Dict[str, Set[str]]:
        reverse = {}  # type: Dict[str, Set[str]]
        for asset in self.index.assets:
            for relationship in asset.relationships:
                if relationship.resolved and relationship.relationship_type in {
                    "belongs_to", "produces", "supersedes", "related_to"
                }:
                    reverse.setdefault(relationship.target, set()).add(asset.framework_id)
        return reverse

    @staticmethod
    def _requires_full(path: str) -> bool:
        return path in FULL_FALLBACK_PATHS or path.startswith(FULL_FALLBACK_PREFIXES)

    def _full_plan(
        self, requested_mode: ValidationMode, requested: Set[str], ignored: Sequence[str],
        unresolved: Set[str], reasons: Sequence[str], base: Optional[str], head: str,
    ) -> ValidationPlan:
        return ValidationPlan(
            requested_mode, ValidationMode.FULL, tuple(sorted(requested)),
            tuple(asset.path for asset in self.index.assets),
            tuple(asset.framework_id for asset in self.index.assets), tuple(sorted(ignored)),
            tuple(sorted(unresolved)), tuple(reasons), base, head,
        )
