from inspect import getmodule, stack
from logging import Formatter, getLogger, StreamHandler
from time import time

from .constants import LOG_FORMAT, LOG_LEVELS

LOG = getLogger(__name__)


class BlasterError(Exception):
    """Blaster's base exception class."""

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
        """
        elapsed = self._end_time - self._start_time
        hours = elapsed // 3600
        elapsed = elapsed - 3600 * hours
        minutes = elapsed // 60
        seconds = elapsed - 60 * minutes
        return hours, minutes, seconds
