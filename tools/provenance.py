"""Small vendor-neutral provenance helpers shared by derived evidence."""

import platform
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Sequence


COMMON_EVIDENCE_FORMAT_VERSION = "1.0"
DERIVED_EVIDENCE_AUTHORITY = "DERIVED_EXECUTION_EVIDENCE_NOT_APPROVAL"


def utc_timestamp() -> str:
    """Return an attributable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


def runtime_identity() -> str:
    """Return the implementation and version without provider assumptions."""

    return "{} {}".format(platform.python_implementation(), platform.python_version())


def evidence_provenance(
    *,
    evidence_type: str,
    repository_commit: str,
    operation: str,
    generated_at: Optional[str] = None,
    runtime: Optional[str] = None,
    index_fingerprint: Optional[str] = None,
    execution_id: Optional[str] = None,
    task_id: Optional[str] = None,
    requested_scope: Sequence[str] = (),
    effective_scope: Sequence[str] = (),
    source_asset: Optional[str] = None,
    result: Optional[str] = None,
    authority: str = DERIVED_EVIDENCE_AUTHORITY,
) -> Dict[str, Any]:
    """Build the common minimum envelope while leaving unavailable fields absent."""

    value = {
        "evidence_format_version": COMMON_EVIDENCE_FORMAT_VERSION,
        "evidence_type": evidence_type,
        "repository_commit": repository_commit,
        "generated_at": generated_at or utc_timestamp(),
        "runtime": runtime or runtime_identity(),
        "operation": operation,
        "requested_scope": list(requested_scope),
        "effective_scope": list(effective_scope),
        "authority": authority,
    }  # type: Dict[str, Any]
    optional = {
        "index_fingerprint": index_fingerprint,
        "execution_id": execution_id,
        "task_id": task_id,
        "source_asset": source_asset,
        "result": result,
    }
    value.update({key: item for key, item in optional.items() if item is not None})
    return value


def evidence_document(provenance: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
    """Wrap one material result without creating a central evidence platform."""

    return {
        "authority": provenance["authority"],
        "provenance": provenance,
        key: value,
    }
