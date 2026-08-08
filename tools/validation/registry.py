"""Central, explicit registry for approved validation checks."""

from typing import Tuple

from .models import Validator
from .metadata import FrameworkIdValidator, MetadataValidator
from .self_check import FoundationSelfCheck
from .structure import DocumentStructureValidator


VALIDATORS = (
    FoundationSelfCheck(),
    MetadataValidator(),
    FrameworkIdValidator(),
    DocumentStructureValidator(),
)  # type: Tuple[Validator, ...]
