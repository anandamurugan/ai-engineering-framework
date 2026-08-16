"""Shared repository-containment checks for deterministic tool paths."""

from pathlib import Path
from typing import Union


def contained_repository_path(
    repository_root: Path,
    path: Union[str, Path],
    *,
    description: str = "tool path",
) -> Path:
    """Resolve a path and reject targets outside the repository boundary."""

    root = repository_root.resolve()
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError("{} resolves outside the repository".format(description))
    return resolved
