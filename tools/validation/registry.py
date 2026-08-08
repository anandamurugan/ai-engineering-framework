"""Central, explicit registry for approved validation checks."""

from typing import Tuple

from .models import Validator
from .self_check import FoundationSelfCheck


VALIDATORS = (FoundationSelfCheck(),)  # type: Tuple[Validator, ...]
