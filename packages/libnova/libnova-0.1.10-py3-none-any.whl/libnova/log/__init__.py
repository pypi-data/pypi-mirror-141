"""
Log module exports for libnova
"""

import libnova.log.log
from typing import Any, Dict, List
from logging import getLogger


def l(*args: List[Any], **kwargs: Dict[str, Any]) -> None:
    """
    Logging wrapper for libnova.
    """
    lg = getLogger(__file__)
    lg.log(*args, **kwargs)  # type: ignore
