"""Immutable models for derived repository intelligence and context evidence."""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Sequence, Tuple

from tools.provenance import evidence_provenance, runtime_identity, utc_timestamp


INDEX_FORMAT_VERSION = "1.0"
MANIFEST_FORMAT_VERSION = "1.0"


@dataclass(frozen=True)
class Relationship:
    """A deterministic relationship derived from repository metadata or links."""

    relationship_type: str
    target: str
    target_path: Optional[str] = None
    resolved: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "Relationship":
        return cls(**value)


@dataclass(frozen=True)
class AssetRecord:
    """Metadata-only representation of a governed repository asset."""

    framework_id: str
    asset_type: str
    title: str
    path: str
    status: Optional[str] = None
    release: Optional[str] = None
    epic: Optional[str] = None
    sprint: Optional[str] = None
    owner: Optional[str] = None
    validation_relevance: Tuple[str, ...] = ()
    relationships: Tuple[Relationship, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["validation_relevance"] = list(self.validation_relevance)
        value["relationships"] = [item.to_dict() for item in self.relationships]
        return value

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "AssetRecord":
        copied = dict(value)
        copied["validation_relevance"] = tuple(copied.get("validation_relevance", []))
        copied["relationships"] = tuple(
            Relationship.from_dict(item) for item in copied.get("relationships", [])
        )
        return cls(**copied)


@dataclass(frozen=True)
class IndexMetrics:
    files_inspected: int
    metadata_files_parsed: int
    assets_produced: int
    relationships_produced: int
    source_reads: int
    generation_duration_ms: int


@dataclass(frozen=True)
class RepositoryIndex:
    """A deterministic, derived repository view tied to source provenance."""

    format_version: str
    source_commit: str
    source_fingerprint: str
    generated_at: str
    repository_root: str
    assets: Tuple[AssetRecord, ...]
    duplicates: Dict[str, Tuple[str, ...]] = field(default_factory=dict)
    unresolved: Tuple[str, ...] = ()
    exclusions: Tuple[str, ...] = ()
    metrics: IndexMetrics = field(
        default_factory=lambda: IndexMetrics(0, 0, 0, 0, 0, 0)
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "format_version": self.format_version,
            "source_commit": self.source_commit,
            "source_fingerprint": self.source_fingerprint,
            "generated_at": self.generated_at,
            "repository_root": self.repository_root,
            "assets": [asset.to_dict() for asset in self.assets],
            "duplicates": {
                key: list(paths) for key, paths in sorted(self.duplicates.items())
            },
            "unresolved": list(self.unresolved),
            "exclusions": list(self.exclusions),
            "metrics": asdict(self.metrics),
        }

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "RepositoryIndex":
        return cls(
            format_version=value["format_version"],
            source_commit=value["source_commit"],
            source_fingerprint=value["source_fingerprint"],
            generated_at=value["generated_at"],
            repository_root=value["repository_root"],
            assets=tuple(AssetRecord.from_dict(item) for item in value["assets"]),
            duplicates={
                key: tuple(paths) for key, paths in value.get("duplicates", {}).items()
            },
            unresolved=tuple(value.get("unresolved", [])),
            exclusions=tuple(value.get("exclusions", [])),
            metrics=IndexMetrics(**value.get("metrics", {})),
        )


@dataclass(frozen=True)
class SelectedContext:
    path: str
    asset_id: Optional[str]
    category: str
    reason: str
    relationship_path: Tuple[str, ...]
    source_framework_id: Optional[str]
    mandatory: bool
    restriction: str
    expansion_level: int

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["relationship_path"] = list(self.relationship_path)
        return value


@dataclass(frozen=True)
class UnresolvedContext:
    reference: str
    reason: str


@dataclass(frozen=True)
class SelectionMetrics:
    files_selected: int
    files_restricted: int
    files_excluded: int
    expansion_levels: Tuple[int, ...]
    unresolved_references: int
    fallback_decisions: int


@dataclass(frozen=True)
class ContextManifest:
    """Machine-readable evidence explaining a context selection."""

    format_version: str
    operation: str
    repository_commit: str
    index_fingerprint: str
    task_reference: Optional[str]
    target_paths: Tuple[str, ...]
    selected: Tuple[SelectedContext, ...]
    restricted: Tuple[SelectedContext, ...]
    unresolved: Tuple[UnresolvedContext, ...]
    exclusions: Tuple[str, ...]
    completeness: Dict[str, bool]
    fallback_required: bool
    fallback_reasons: Tuple[str, ...]
    metrics: SelectionMetrics
    generated_at: str = field(default_factory=utc_timestamp)
    runtime: str = field(default_factory=runtime_identity)

    def to_dict(self) -> Dict[str, Any]:
        effective_scope = tuple(item.path for item in self.selected)
        result = "FALLBACK_REQUIRED" if self.fallback_required else "COMPLETE"
        return {
            "format_version": self.format_version,
            "operation": self.operation,
            "repository_commit": self.repository_commit,
            "index_fingerprint": self.index_fingerprint,
            "task_reference": self.task_reference,
            "target_paths": list(self.target_paths),
            "selected": [item.to_dict() for item in self.selected],
            "restricted": [item.to_dict() for item in self.restricted],
            "unresolved": [asdict(item) for item in self.unresolved],
            "exclusions": list(self.exclusions),
            "completeness": dict(sorted(self.completeness.items())),
            "fallback_required": self.fallback_required,
            "fallback_reasons": list(self.fallback_reasons),
            "metrics": asdict(self.metrics),
            "authority": "DERIVED_EXECUTION_EVIDENCE_NOT_APPROVAL",
            "provenance": evidence_provenance(
                evidence_type="context_manifest",
                repository_commit=self.repository_commit,
                index_fingerprint=self.index_fingerprint,
                generated_at=self.generated_at,
                runtime=self.runtime,
                operation=self.operation,
                task_id=self.task_reference,
                requested_scope=self.target_paths,
                effective_scope=effective_scope,
                source_asset=self.task_reference,
                result=result,
            ),
        }
