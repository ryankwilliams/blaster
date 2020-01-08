"""Blaster core.

The core module contains commonly used classes and functions by blaster.
"""
from inspect import getmodule, stack
from logging import Formatter, getLogger, StreamHandler
from time import time
from uuid import uuid4

from blaster.constants import *

LOG = getLogger(__name__)

__all__ = [
    "BlasterError",
    "CalcTimeMixin",
    "LoggerMixin",
    "TaskDefinition",
    "ResultsList"
]


class BlasterError(Exception):
    """Blaster's base error to raise."""

    def __init__(self, message, results=None):
        """Constructor.

        :param str message: detailed error message
        :param list results: blaster results data
        """
        super(BlasterError, self).__init__(message)

        if results is None:
            results = list()

        self.message = message
        self.results = results


class LoggerMixin(object):
    """Blaster's logger class to handle configuring loggers."""

    @staticmethod
    def create_blaster_logger(log_level=None):
        """Blaster logger creation.

        :param str log_level: logging level
        :return: blaster logger
        :rtype: object
        """
        blogger = getLogger('blaster')
        if not blogger.handlers:
            chandler = StreamHandler()
            chandler.setLevel(LOG_LEVELS[log_level])
            chandler.setFormatter(Formatter(LOG_FORMAT))
            blogger.setLevel(LOG_LEVELS[log_level])
            blogger.addHandler(chandler)
        return blogger

    @property
    def logger(self):
        """Returns the default logger object."""
        return getLogger(getmodule(stack()[1][0]).__name__)


class CalcTimeMixin(object):
    """Blaster's time calculation class to handle determining time deltas."""

    _start_time = None
    _end_time = None

    def start_time(self):
        """Save the start time."""
        self._start_time = time()

    def end_time(self):
        """Save the end time."""
        self._end_time = time()

    def time_delta(self):
        """Calculate time delta between start and end times.

        :return: hours, minutes, seconds
        :rtype: int
        """
        elapsed = self._end_time - self._start_time
        hours = elapsed // 3600
        elapsed = elapsed - 3600 * hours
        minutes = elapsed // 60
        seconds = elapsed - 60 * minutes
        return hours, minutes, seconds


class TaskDefinition(dict):
    """The standard definition of a blaster task."""

    def __init__(self, *args, **kwargs):
        """Constructor.

        :param args: variable number of arguments
        :param kwargs: key word arguments
        """
        super(TaskDefinition, self).__init__(*args, **kwargs)
        self.setdefault("bid", str(uuid4()))
        self.validate()

    def validate(self):
        """Validate task definition to ensure required keys set."""
        for key in REQ_TASK_KEYS:
            if key not in self:
                raise BlasterError(
                    "Required key: '%s' missing from task: %s" %
                    (key, self.get('name')))


class ResultsList(list):
    """The standard results for a blaster run."""

    def __init__(self):
        """Constructor."""
        super(ResultsList, self).__init__()

    def analyze(self):
        """Analyze the list of results based on overall task status.

        :return: whether task run was pass or fail.
        :rtype: int
        """
        for item in self:
            if item['status'] != 0:
                return 1
        return 0

    def coordinate(self, task):
        """Update results with their corresponding task definitions.

        :param dict task: task definition to compare too
        :return: matching result task to the task given
        :rtype: dict
        """
        for item in self:
            try:
                if item['bid'] == task['bid']:
                    return item
            except KeyError as ex:
                raise KeyError(ex)
