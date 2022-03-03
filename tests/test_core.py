"""Blaster core (tests).

Test cases to test the blaster core module.
"""
from time import sleep

import pytest

from blaster.core import (
    BlasterError,
    CalcTimeMixin,
    LoggerMixin,
    ResultsList,
    TaskDefinition,
)


class TestBlasterError(object):
    """Unit tests to cover blaster error.

    Class provides tests to gain better code coverage.
    """

    @staticmethod
    def test_blaster_error():
        """Raise a blaster error.

        This method tests raising the blaster error class. It will also
        verify the values returned from the exception.
        """
        try:
            raise BlasterError("Blaster error!")
        except BlasterError as ex:
            assert "Blaster error!" == ex.message
            assert list() == ex.results


class TestLoggerMixin(object):
    """Unit tests to cover blaster logger mixin class.

    Class provides both positive and negative tests to gain better code
    coverage.
    """

    @staticmethod
    def test_create_logger():
        """Create a logger mixin object.

        This method tests creating a logger mixin object from the logger mixin
        class. Once the object is created, it will verify it is an instance of
        the logger mixin class.
        """
        logger = LoggerMixin()
        logger.create_blaster_logger("info")
        assert isinstance(logger, LoggerMixin)

    @staticmethod
    def test_logger_object():
        """Log a message with a logger mixin object.

        This method tests logging a message with a logger mixin object.
        """
        logger = LoggerMixin()
        logger.create_blaster_logger("info")
        logger.logger.info("Blaster!")


class TestCalcTimeMixin(object):
    """Unit tests to cover blaster calculate time mixin class.

    Class provides both positive and negative tests to gain better code
    coverage.
    """

    @staticmethod
    def test_save_start_time():
        """Save start time.

        This method tests saving the start time. It will verify that the value
        saved is not none.
        """
        calc = CalcTimeMixin()
        calc.start_time()
        assert calc.start_time is not None

    @staticmethod
    def test_save_end_time():
        """Save end time.

        This method tests saving the end time. It will verify that the value
        saved is not none.
        """
        calc = CalcTimeMixin()
        calc.end_time()
        assert calc.end_time is not None

    @staticmethod
    def test_time_delta():
        """Calculate delta between two time endpoints.

        This method tests calculating the time delta between two endpoints
        (start and end). It will verify the returned values are the correct
        data type.
        """
        calc = CalcTimeMixin()
        calc.start_time()
        sleep(1)
        calc.end_time()
        hour, minute, second = calc.time_delta()
        assert isinstance(hour, (float, int))
        assert isinstance(minute, (float, int))
        assert isinstance(second, (float, int))


class TestTaskDefinition(object):
    """Unit tests to cover blaster task definition class.

    Class provides both positive and negative tests to gain better code
    coverage.
    """

    @staticmethod
    def create_task():
        """Create a task.

        This method tests creating a task. It will verify the task is an
        instance of the task definition class. As well as verify it has the
        name attribute.
        """
        task_def = TaskDefinition(name="blaster")
        assert isinstance(task_def, TaskDefinition)
        assert hasattr(task_def, "name")


class TestResultsList(object):
    """Unit tests to cover blaster results list class."""

    @staticmethod
    def create_results():
        """Create blaster results.

        This method tests creating a blaster results list. It will verify
        the object is an instance of the results list class.
        """
        res = ResultsList()
        assert isinstance(res, ResultsList)

    @staticmethod
    def test_analyze_pass_results():
        """Analyze passed blaster results.

        This method tests the results list object to see if the results are
        valid. (positive test)
        """
        res = ResultsList()
        res.append(dict(name="item1", status=0))
        assert res.analyze() == 0

    @staticmethod
    def test_analyze_failed_results():
        """Analyze failed blaster results.

        This method tests the results list object to see if the results are
        invalid. (negative test)
        """
        res = ResultsList()
        res.append(dict(name="item1", status=1))
        assert res.analyze() == 1
