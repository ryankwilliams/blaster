"""Blaster core.

The core module contains commonly used classes and functions by blaster.
"""
from inspect import getmodule, stack
from logging import Formatter, getLogger, Logger, StreamHandler
from time import time
from typing import Any, List, Optional, Dict, Tuple
from uuid import uuid4

from blaster.constants import *

LOG = getLogger(__name__)

__all__ = [
    "BlasterError",
    "CalcTimeMixin",
    "LoggerMixin",
    "TaskDefinition",
    "ResultsList",
]


class LoggerMixin:
    """Blaster's logger class to handle configuring loggers."""

    @staticmethod
    def create_blaster_logger(log_level: str) -> Logger:
        """Blaster logger creation.

        :param log_level: logging level
        :return: blaster logger
        """
        blogger: Logger = getLogger("blaster")
        if not blogger.handlers:
            chandler: StreamHandler = StreamHandler()
            chandler.setLevel(LOG_LEVELS[log_level])
            chandler.setFormatter(Formatter(LOG_FORMAT))
            blogger.setLevel(LOG_LEVELS[log_level])
            blogger.addHandler(chandler)
        return blogger

    @property
    def logger(self) -> Logger:
        """Returns the default logger object."""
        return getLogger(getmodule(stack()[1][0]).__name__)


class CalcTimeMixin:
    """Blaster's time calculation class to handle determining time deltas."""

    _start_time: float = None
    _end_time: float = None

    def start_time(self) -> None:
        """Save the start time."""
        self._start_time = time()

    def end_time(self) -> None:
        """Save the end time."""
        self._end_time = time()

    def time_delta(self) -> Tuple[float, float, float]:
        """Calculate time delta between start and end times.

        :return: hours, minutes, seconds
        """
        elapsed = self._end_time - self._start_time
        hours = elapsed // 3600
        elapsed = elapsed - 3600 * hours
        minutes = elapsed // 60
        seconds = elapsed - 60 * minutes
        return hours, minutes, seconds


class TaskDefinition(dict):
    """The standard definition of a blaster task."""

    def __init__(self, *args: Tuple[str], **kwargs: Dict[str, Any]) -> None:
        """Constructor.

        :param args: variable number of arguments
        :param kwargs: key word arguments
        """
        super().__init__(*args, **kwargs)
        self.setdefault("bid", str(uuid4()))
        self.validate()

    def validate(self) -> None:
        """Validate task definition to ensure required keys set."""
        for key in REQ_TASK_KEYS:
            if key not in self:
                raise BlasterError(
                    "Required key: '%s' missing from task: %s" % (key, self.get("name"))
                )


class ResultsList(list):
    """The standard results for a blaster run."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()

    def analyze(self) -> int:
        """Analyze the list of results based on overall task status.

        :return: whether task run was pass or fail.
        """
        # TODO: Improve results typing to be a typed dict
        item: Dict[str, int]

        for item in self:
            if item["status"] != 0:
                return 1
        return 0


class BlasterError(Exception):
    """Blaster's base error to raise."""

    # TODO: Improve results typing to be a typed dict
    def __init__(self, message: str, results: Optional[ResultsList] = None) -> None:
        """Constructor.

        :param message: detailed error message
        :param results: blaster results data
        """
        super().__init__(message)

        if results is None:
            results = list()

        self.message: str = message
        self.results: List[Dict[str, Any]] = results
