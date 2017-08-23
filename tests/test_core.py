"""Blaster core (tests).

Test cases to test the blaster core module.
"""
from time import sleep

from nose.tools import assert_equal, assert_is_instance, assert_is_not_none, \
    assert_true, assert_false, raises

from blaster.core import BlasterError, CalcTimeMixin, LoggerMixin, \
    ResultsList, TaskDefinition


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
            raise BlasterError('Blaster error!')
        except BlasterError as ex:
            assert_equal('Blaster error!', ex.message)
            assert_equal(list(), ex.results)


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
        logger.create_blaster_logger('info')
        assert_is_instance(logger, LoggerMixin)

    @staticmethod
    def test_logger_object():
        """Log a message with a logger mixin object.

        This method tests logging a message with a logger mixin object.
        """
        logger = LoggerMixin()
        logger.create_blaster_logger('info')
        logger.logger.info('Blaster!')


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
        calc.start()
        assert_is_not_none(calc._start_time)

    @staticmethod
    def test_save_end_time():
        """Save end time.

        This method tests saving the end time. It will verify that the value
        saved is not none.
        """
        calc = CalcTimeMixin()
        calc.end()
        assert_is_not_none(calc._end_time)

    @staticmethod
    def test_time_delta():
        """Calculate delta between two time endpoints.

        This method tests calculating the time delta between two endpoints
        (start and end). It will verify the returned values are the correct
        data type.
        """
        calc = CalcTimeMixin()
        calc.start()
        sleep(1)
        calc.end()
        hour, minute, second = calc.delta()
        assert_true(isinstance(hour, (float, int)))
        assert_true(isinstance(minute, (float, int)))
        assert_true(isinstance(second, (float, int)))


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
        task_def = TaskDefinition(name='blaster')
        assert_is_instance(task_def, TaskDefinition)
        assert_true(hasattr(task_def, 'name'))

    @staticmethod
    def test_valid_task_definition():
        """Checks if a task definition is valid.

        This method tests if a task definition is valid by calling the
        is_valid method that each task has.
        """
        task_def = TaskDefinition(
            dict(
                name='test',
                task='task',
                methods=list()
            )
        )
        assert_true(task_def.is_valid())

    @staticmethod
    def test_invalid_task_definition():
        """Check if a task definition is invalid.

        This method tests if a task definition is invalid by calling the
        is_valid method that each task has.
        """
        task_def = TaskDefinition(
            dict(
                name='test',
                task='task',
            )
        )
        assert_false(task_def.is_valid())


class TestResultsList(object):
    """Unit tests to cover blaster results list class."""

    @staticmethod
    def create_results():
        """Create blaster results.

        This method tests creating a blaster results list. It will verify
        the object is an instance of the results list class.
        """
        res = ResultsList()
        assert_is_instance(res, ResultsList)

    @staticmethod
    def test_analyze_pass_results():
        """Analyze passed blaster results.

        This method tests the results list object to see if the results are
        valid. (positive test)
        """
        res = ResultsList()
        res.append(dict(name='item1', status=0))
        assert_equal(res.analyze(), 0)

    @staticmethod
    def test_analyze_failed_results():
        """Analyze failed blaster results.

        This method tests the results list object to see if the results are
        invalid. (negative test)
        """
        res = ResultsList()
        res.append(dict(name='item1', status=1))
        assert_equal(res.analyze(), 1)

    @staticmethod
    def test_coordinate_valid_results():
        """Coordinate passed blaster results.

        This method tests coordinating task data to the results data.
        (positive test)
        """
        res = ResultsList()
        res.append(dict(name='item1', bid='1234', status=1))
        task = dict(name='item1', bid='1234')
        assert_is_instance(res.coordinate(task), dict)

    @staticmethod
    @raises(KeyError)
    def test_coordinate_invalid_results():
        """Coordinate failed blaster results.

        This method tests coordinating task data to the results data.
        (negative test)
        """
        res = ResultsList()
        res.append(dict(name='item1', bid='1234', status=1))
        task = dict(name='item1')
        assert_is_instance(res.coordinate(task), dict)
