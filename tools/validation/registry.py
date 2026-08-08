"""Central, explicit registry for approved validation checks."""

from typing import Tuple

from .models import Validator
from .metadata import FrameworkIdValidator, MetadataValidator
from .hygiene import (
    MarkdownHygieneValidator,
    PlaceholderValidator,
    TrackedArtifactValidator,
    TrailingWhitespaceValidator,
)
from .references import RelativeLinkValidator, StandardReferenceValidator
from .self_check import FoundationSelfCheck
from .structure import DocumentStructureValidator
from .traceability import ProductTraceabilityValidator, StandardsCatalogValidator


VALIDATORS = (
    FoundationSelfCheck(),
    MetadataValidator(),
    FrameworkIdValidator(),
    DocumentStructureValidator(),
    RelativeLinkValidator(),
    StandardReferenceValidator(),
    StandardsCatalogValidator(),
    ProductTraceabilityValidator(),
    PlaceholderValidator(),
    TrailingWhitespaceValidator(),
    MarkdownHygieneValidator(),
    TrackedArtifactValidator(),
)  # type: Tuple[Validator, ...]
