"""Blaster constants.

The constants module contains commonly used constants by blaster.
"""
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

__all__ = [
    "LOG_LEVELS",
    "LOG_FORMAT",
    "REQ_TASK_KEYS"
]

LOG_LEVELS = {
    'debug': DEBUG,
    'info': INFO,
    'warning': WARNING,
    'error': ERROR,
    'critical': CRITICAL
}

LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

REQ_TASK_KEYS = [
    'name',
    'task',
    'methods'
]
