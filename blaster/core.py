"""Blaster core.

The core module contains commonly used classes and functions by blaster.
"""
from inspect import getmodule, stack
from logging import Formatter, getLogger, StreamHandler
from sys import exc_info
from time import time
from traceback import print_exc

from .constants import LOG_FORMAT, LOG_LEVELS, REQ_TASK_KEYS

LOG = getLogger(__name__)


class BlasterError(Exception):
    """Blaster's base error to raise."""

    def __init__(self, message, results=list()):
        """Constructor.

        :param message: Detailed error message.
        :type message: str
        :param results: Blaster results data.
        :type results: list
        """
        super(BlasterError, self).__init__(message)
        self.results = results


class LoggerMixin(object):
    """Blaster's logger class to handle configuring loggers."""

    @staticmethod
    def create_blaster_logger(log_level=None):
        """Blaster logger creation.

        :param log_level: Logging level.
        :type log_level: str
        :return: Blaster logger.
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

    def start(self):
        """Save the start time."""
        self._start_time = time()

    def end(self):
        """Save the end time."""
        self._end_time = time()

    def delta(self):
        """Calculate time delta between start and end times.

        :return: Hours, minutes, seconds
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

        :param args: Variable number of arguments.
        :type args: n/a
        :param kwargs: Key word arguments.
        :type kwargs: n/a
        """
        super(TaskDefinition, self).__init__(*args, **kwargs)

    def is_valid(self):
        """Ensure the task definition is valid.

        :return: Whether required keys are set.
        :rtype: bool
        """
        count = 0
        for key in REQ_TASK_KEYS:
            if key not in self:
                LOG.error('Req. key %s missing from task definition!' % key)
                count += 1
        return True if count == 0 else False


class ResultsList(list):
    """The standard results for a blaster run."""

    def __init__(self):
        """Constructor."""
        super(ResultsList, self).__init__()

    def analyze(self):
        """Analyze the list of results based on overall task status.

        :return: Whether task run was pass or fail.
        :rtype: int
        """
        for item in self:
            if item['status'] != 0:
                return 1
        return 0

    def coordinate(self, task):
        """Update results with their corresponding task definitions.

        :param task: Task definition to compare too.
        :type task: dict
        :return: Matching result task to the task given.
        :rtype: dict
        """
        for item in self:
            try:
                if item['bid'] == task['bid']:
                    return item
            except KeyError as ex:
                raise KeyError(ex)


class EngineMixin(object):
    """The standard blaster engine mixin class.

    The primary purpose of this mixin class is to provide blaster engine
    classes with commonly used methods. It removes the need to duplicate
    code between engine modules.
    """

    @staticmethod
    def get_traceback():
        """Get traceback when exception is raised. Will log traceback as well.

        :return: Exception information.
        :rtype: tuple
        """
        print_exc()
        return exc_info()
