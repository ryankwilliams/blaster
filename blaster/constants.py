"""Blaster constants.

The constant's module contains commonly used constants by blaster.
"""
from logging import CRITICAL
from logging import DEBUG
from logging import ERROR
from logging import INFO
from logging import WARNING
from typing import Dict
from typing import List

__all__: List[str] = ["LOG_LEVELS", "LOG_FORMAT", "REQ_TASK_KEYS"]

LOG_LEVELS: Dict[str, int] = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL,
}

LOG_FORMAT: str = "%(asctime)s %(levelname)s %(message)s"

REQ_TASK_KEYS: List[str] = ["name", "task", "methods"]
