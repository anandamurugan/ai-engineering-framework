"""Deterministic relationship-aware Minimum Sufficient Context selection."""

import fnmatch
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .models import (
    MANIFEST_FORMAT_VERSION,
    AssetRecord,
    ContextManifest,
    RepositoryIndex,
    SelectedContext,
    SelectionMetrics,
    UnresolvedContext,
)


class ContextSelector:
    """Select explainable context from an immutable repository index."""

    def __init__(
        self,
        root: Path,
        index: RepositoryIndex,
        *,
        restricted_patterns: Sequence[str] = (),
        index_fresh: bool = True,
        freshness_reasons: Sequence[str] = (),
    ):
        self.root = root.resolve()
        self.index = index
        self.restricted_patterns = tuple(restricted_patterns)
        self.index_fresh = index_fresh
        self.freshness_reasons = tuple(freshness_reasons)
        self.by_id = {asset.framework_id: asset for asset in index.assets}
        self.by_path = {asset.path: asset for asset in index.assets}
        self.reverse = self._reverse_relationships(index.assets)

    def select(
        self,
        *,
        task_reference: Optional[str] = None,
        target_paths: Sequence[str] = (),
        expansion_level: int = 4,
        full_fallback: bool = False,
    ) -> ContextManifest:
        if not task_reference and not target_paths:
            raise ValueError("selection requires a task/asset reference or target path")
        if expansion_level < 0 or expansion_level > 5:
            raise ValueError("expansion level must be between 0 and 5")

        selected = {}  # type: Dict[str, SelectedContext]
        restricted = {}  # type: Dict[str, SelectedContext]
        unresolved = []  # type: List[UnresolvedContext]
        fallback_reasons = list(self.freshness_reasons)
        files_excluded = 0

        repository_instruction_paths = ("AGENTS.md",)
        missing_repository_instructions = []  # type: List[str]
        missing_governance = []  # type: List[str]
        for instruction_path in repository_instruction_paths:
            if not (self.root / instruction_path).is_file():
                unresolved.append(
                    UnresolvedContext(
                        instruction_path,
                        "mandatory repository governing instruction is missing",
                    )
                )
                missing_repository_instructions.append(instruction_path)
                missing_governance.append(instruction_path)
                fallback_reasons.append("mandatory repository governing instruction is unresolved")
                continue
            self._add(
                selected,
                restricted,
                instruction_path,
                None,
                "repository_governing_instruction",
                "mandatory repository-level agent instruction",
                (instruction_path,),
                None,
                True,
                0,
            )

        task_asset = self._resolve_reference(task_reference) if task_reference else None
        if task_reference and task_asset is None:
            unresolved.append(
                UnresolvedContext(task_reference, "task or asset identity did not resolve")
            )
            fallback_reasons.append("task identity is unresolved")
        elif task_asset is not None:
            self._add(
                selected,
                restricted,
                task_asset.path,
                task_asset,
                "task_product_context",
                "bounded task or governed asset reference",
                (task_asset.framework_id,),
                task_asset.framework_id,
                True,
                0,
            )
            self._add_product_hierarchy(selected, restricted, task_asset)

        seeds = []  # type: List[AssetRecord]
        if task_asset:
            seeds.append(task_asset)
        for raw_path in target_paths:
            normalized, error = self._normalize_target(raw_path)
            if error:
                unresolved.append(UnresolvedContext(raw_path, error))
                fallback_reasons.append("explicit target is unresolved")
                continue
            if self._is_excluded(normalized):
                files_excluded += 1
                unresolved.append(
                    UnresolvedContext(raw_path, "explicit target is excluded by repository policy")
                )
                fallback_reasons.append("an explicit target is excluded")
                continue
            asset = self.by_path.get(normalized)
            if asset:
                seeds.append(asset)
            self._add(
                selected,
                restricted,
                normalized,
                asset,
                "target_implementation_context",
                "explicit target path",
                tuple(filter(None, (task_asset.framework_id if task_asset else None, asset.framework_id if asset else None))),
                task_asset.framework_id if task_asset else None,
                True,
                2,
            )

        if expansion_level >= 1:
            self._add_applicable_standards(selected, restricted, seeds)
            self._add_governing_documents(selected, restricted, seeds)
        if expansion_level >= 3:
            self._add_direct_dependencies(
                selected, restricted, unresolved, fallback_reasons, seeds
            )
        if expansion_level >= 4:
            self._add_affected_relationships(selected, restricted, seeds)

        if restricted:
            fallback_reasons.append("required context is restricted")
        if not self.index_fresh:
            fallback_reasons.append("index is stale")

        fallback_required = bool(fallback_reasons or unresolved or self.index.duplicates)
        if self.index.duplicates:
            fallback_reasons.append("duplicate framework identities prevent complete lookup")
            fallback_required = True

        if (full_fallback or expansion_level == 5) and fallback_required:
            for asset in self.index.assets:
                if self._is_excluded(asset.path):
                    files_excluded += 1
                    continue
                self._add(
                    selected,
                    restricted,
                    asset.path,
                    asset,
                    "broader_repository_context",
                    "full governed-asset fallback required by incomplete selection",
                    (asset.framework_id,),
                    task_asset.framework_id if task_asset else None,
                    False,
                    5,
                )

        ordered_selected = tuple(sorted(selected.values(), key=self._selection_key))
        ordered_restricted = tuple(sorted(restricted.values(), key=self._selection_key))
        restricted_governance = tuple(
            item
            for item in ordered_restricted
            if item.mandatory
            and item.category in {
                "repository_governing_instruction",
                "task_product_context",
                "governing_standard",
                "governing_context",
            }
        )
        task_governance_resolved = task_asset is not None if task_reference else True
        if task_asset is not None:
            for target_id in (task_asset.release, task_asset.epic, task_asset.sprint):
                if target_id and target_id not in self.by_id:
                    task_governance_resolved = False
                    missing_governance.append(target_id)
        applicable_standard_ids = {
            relation.target
            for seed in seeds
            for relation in seed.relationships
            if relation.target.startswith("STD-")
        }
        unresolved_standard_ids = {
            standard_id
            for standard_id in applicable_standard_ids
            if standard_id not in self.by_id
        }
        for standard_id in sorted(unresolved_standard_ids):
            if not any(item.reference == standard_id for item in unresolved):
                unresolved.append(
                    UnresolvedContext(standard_id, "applicable governing standard is unresolved")
                )
            missing_governance.append(standard_id)
            fallback_reasons.append("applicable governing standard is unresolved")
        repository_instructions_resolved = not missing_repository_instructions and not any(
            item.path in repository_instruction_paths for item in restricted_governance
        )
        selected_ids = {item.asset_id for item in ordered_selected}
        applicable_standards_resolved = (
            not unresolved_standard_ids
            and applicable_standard_ids.issubset(selected_ids)
            and not any(item.category == "governing_standard" for item in restricted_governance)
        )
        governing_context_complete = all(
            (
                repository_instructions_resolved,
                task_governance_resolved,
                applicable_standards_resolved,
                not restricted_governance,
                self.index_fresh,
            )
        )
        if not governing_context_complete:
            fallback_reasons.append("mandatory governing context is incomplete or unauthorized")
            fallback_required = True
        levels = tuple(sorted({item.expansion_level for item in ordered_selected}))
        completeness = {
            "target_resolved": not any("target" in item.reason for item in unresolved),
            "governing_context_resolved": governing_context_complete,
            "repository_instructions_resolved": repository_instructions_resolved,
            "applicable_standards_resolved": applicable_standards_resolved,
            "task_governance_resolved": task_governance_resolved,
            "restricted_governance_present": bool(restricted_governance),
            "governing_context_complete": governing_context_complete,
            "dependencies_resolved": not any("relationship" in item.reason for item in unresolved),
            "index_fresh": self.index_fresh,
            "restricted_required_context_clear": not bool(ordered_restricted),
            "unresolved_references_clear": not bool(unresolved),
        }
        return ContextManifest(
            format_version=MANIFEST_FORMAT_VERSION,
            operation="select_context",
            repository_commit=self.index.source_commit,
            index_fingerprint=self.index.source_fingerprint,
            task_reference=task_reference,
            target_paths=tuple(target_paths),
            selected=ordered_selected,
            restricted=ordered_restricted,
            unresolved=tuple(sorted(unresolved, key=lambda item: (item.reference, item.reason))),
            exclusions=self.index.exclusions,
            completeness=completeness,
            fallback_required=fallback_required,
            fallback_reasons=tuple(sorted(set(fallback_reasons))),
            metrics=SelectionMetrics(
                files_selected=len(ordered_selected),
                files_restricted=len(ordered_restricted),
                files_excluded=files_excluded,
                expansion_levels=levels,
                unresolved_references=len(unresolved),
                fallback_decisions=1 if fallback_required else 0,
            ),
        )

    def _resolve_reference(self, reference: Optional[str]) -> Optional[AssetRecord]:
        if reference is None:
            return None
        if reference in self.by_id:
            return self.by_id[reference]
        story_id = reference if reference.startswith("STORY-") else "STORY-{}".format(reference)
        return self.by_id.get(story_id)

    def _add_product_hierarchy(
        self,
        selected: Dict[str, SelectedContext],
        restricted: Dict[str, SelectedContext],
        task_asset: AssetRecord,
    ) -> None:
        for target_id in (task_asset.release, task_asset.epic, task_asset.sprint):
            if not target_id or target_id not in self.by_id:
                continue
            asset = self.by_id[target_id]
            self._add(
                selected,
                restricted,
                asset.path,
                asset,
                "task_product_context",
                "parent product context for {}".format(task_asset.framework_id),
                (task_asset.framework_id, target_id),
                task_asset.framework_id,
                True,
                0,
            )

    def _add_applicable_standards(
        self,
        selected: Dict[str, SelectedContext],
        restricted: Dict[str, SelectedContext],
        seeds: Sequence[AssetRecord],
    ) -> None:
        for seed in seeds:
            candidates = [seed] if seed.asset_type == "standard" else []
            related_assets = [
                self.by_id[item.target]
                for item in seed.relationships
                if item.target in self.by_id
            ]
            candidates.extend(item for item in related_assets if item.asset_type == "standard")
            for related in related_assets:
                candidates.extend(
                    self.by_id[item.target]
                    for item in related.relationships
                    if item.target in self.by_id
                    and self.by_id[item.target].asset_type == "standard"
                )
            for standard in candidates:
                self._add(
                    selected,
                    restricted,
                    standard.path,
                    standard,
                    "governing_standard",
                    "standard explicitly related to selected asset",
                    (seed.framework_id, standard.framework_id),
                    seed.framework_id,
                    True,
                    1,
                )

    def _add_governing_documents(
        self,
        selected: Dict[str, SelectedContext],
        restricted: Dict[str, SelectedContext],
        seeds: Sequence[AssetRecord],
    ) -> None:
        for seed in seeds:
            related_assets = [
                self.by_id[relation.target]
                for relation in seed.relationships
                if relation.target in self.by_id
            ]
            candidates = list(related_assets)
            for related in related_assets:
                candidates.extend(
                    self.by_id[relation.target]
                    for relation in related.relationships
                    if relation.target in self.by_id
                )
            for target in candidates:
                if target and target.asset_type in ("architecture_document", "governance_document"):
                    self._add(
                        selected,
                        restricted,
                        target.path,
                        target,
                        "governing_context",
                        "governing document linked by selected asset",
                        (seed.framework_id, target.framework_id),
                        seed.framework_id,
                        True,
                        1,
                    )

    def _add_direct_dependencies(
        self,
        selected: Dict[str, SelectedContext],
        restricted: Dict[str, SelectedContext],
        unresolved: List[UnresolvedContext],
        fallback_reasons: List[str],
        seeds: Sequence[AssetRecord],
    ) -> None:
        for seed in seeds:
            for relationship in seed.relationships:
                if not relationship.resolved or relationship.target not in self.by_id:
                    if relationship.target_path and (self.root / relationship.target_path).exists():
                        self._add(
                            selected,
                            restricted,
                            relationship.target_path,
                            None,
                            "dependency_context",
                            "direct {} relationship from {}".format(
                                relationship.relationship_type, seed.framework_id
                            ),
                            (seed.framework_id, relationship.target),
                            seed.framework_id,
                            relationship.relationship_type in ("belongs_to", "produces"),
                            3,
                        )
                        continue
                    unresolved.append(
                        UnresolvedContext(
                            relationship.target,
                            "direct relationship from {} did not resolve".format(
                                seed.framework_id
                            ),
                        )
                    )
                    fallback_reasons.append("direct dependency is unresolved")
                    continue
                target = self.by_id[relationship.target]
                self._add(
                    selected,
                    restricted,
                    target.path,
                    target,
                    "dependency_context",
                    "direct {} relationship from {}".format(
                        relationship.relationship_type, seed.framework_id
                    ),
                    (seed.framework_id, target.framework_id),
                    seed.framework_id,
                    relationship.relationship_type in ("belongs_to", "produces"),
                    3,
                )

    def _add_affected_relationships(
        self,
        selected: Dict[str, SelectedContext],
        restricted: Dict[str, SelectedContext],
        seeds: Sequence[AssetRecord],
    ) -> None:
        for seed in seeds:
            for source_id, relationship_type in self.reverse.get(seed.framework_id, ()):
                source = self.by_id[source_id]
                self._add(
                    selected,
                    restricted,
                    source.path,
                    source,
                    "affected_relationship_context",
                    "{} references selected asset through {}".format(
                        source_id, relationship_type
                    ),
                    (seed.framework_id, source_id),
                    seed.framework_id,
                    False,
                    4,
                )

    def _add(
        self,
        selected: Dict[str, SelectedContext],
        restricted: Dict[str, SelectedContext],
        path: str,
        asset: Optional[AssetRecord],
        category: str,
        reason: str,
        relationship_path: Tuple[str, ...],
        source_framework_id: Optional[str],
        mandatory: bool,
        expansion_level: int,
    ) -> None:
        restriction = "REQUIRED BUT RESTRICTED" if self._is_restricted(path) else "AUTHORIZED"
        item = SelectedContext(
            path=path,
            asset_id=asset.framework_id if asset else None,
            category=category,
            reason=reason,
            relationship_path=relationship_path,
            source_framework_id=source_framework_id,
            mandatory=mandatory,
            restriction=restriction,
            expansion_level=expansion_level,
        )
        destination = restricted if restriction != "AUTHORIZED" else selected
        prior = destination.get(path)
        if prior is None or self._selection_key(item) < self._selection_key(prior):
            destination[path] = item

    def _normalize_target(self, raw_path: str) -> Tuple[str, Optional[str]]:
        candidate = (self.root / raw_path).resolve()
        try:
            relative = candidate.relative_to(self.root).as_posix()
        except ValueError:
            return raw_path, "target resolves outside the repository"
        if not candidate.exists() or not candidate.is_file():
            return relative, "target file does not exist"
        return relative, None

    def _is_excluded(self, path: str) -> bool:
        normalized = path.rstrip("/")
        for pattern in self.index.exclusions:
            clean = pattern.lstrip("/").rstrip("/")
            if fnmatch.fnmatch(normalized, clean) or normalized.startswith(clean + "/"):
                return True
        return False

    def _is_restricted(self, path: str) -> bool:
        return any(
            fnmatch.fnmatch(path, pattern) or path.startswith(pattern.rstrip("/") + "/")
            for pattern in self.restricted_patterns
        )

    @staticmethod
    def _reverse_relationships(
        assets: Sequence[AssetRecord],
    ) -> Dict[str, Tuple[Tuple[str, str], ...]]:
        reverse = {}  # type: Dict[str, List[Tuple[str, str]]]
        for asset in assets:
            for relationship in asset.relationships:
                reverse.setdefault(relationship.target, []).append(
                    (asset.framework_id, relationship.relationship_type)
                )
        return {
            key: tuple(sorted(values)) for key, values in reverse.items()
        }

    @staticmethod
    def _selection_key(item: SelectedContext) -> Tuple[int, str, str]:
        return item.expansion_level, item.category, item.path
