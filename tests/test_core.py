"""Blaster core (tests).

Test cases to test the blaster core module.
"""
from time import sleep

from nose.tools import assert_equal, assert_is_instance, assert_is_not_none, \
    assert_true, assert_false, raises

from blaster.core import BlasterError, CalcTimeMixin, LoggerMixin, \
    ResultsList, TaskDefinition


class TestBlasterError(object):
    """Test blaster error class."""

    @staticmethod
    def test_blaster_error():
        """Test blaster error."""
        try:
            raise BlasterError('Blaster error!')
        except BlasterError as ex:
            assert_equal('Blaster error!', ex.message)
            assert_equal(list(), ex.results)


class TestLoggerMixin(object):
    """Test logger mixin class."""

    @staticmethod
    def test_create_logger():
        """Test create blaster logger."""
        logger = LoggerMixin()
        logger.create_blaster_logger('info')
        assert_is_instance(logger, LoggerMixin)

    @staticmethod
    def test_logger_object():
        """Test blaster logger object."""
        logger = LoggerMixin()
        logger.create_blaster_logger('info')
        logger.logger.info('Blaster!')


class TestCalcTimeMixin(object):
    """Test calculate time mixin class."""

    @staticmethod
    def test_save_start_time():
        """Test saving start time."""
        calc = CalcTimeMixin()
        calc.start()
        assert_is_not_none(calc._start_time)

    @staticmethod
    def test_save_end_time():
        """Test saving end time."""
        calc = CalcTimeMixin()
        calc.end()
        assert_is_not_none(calc._end_time)

    @staticmethod
    def test_time_delta():
        """Test time delta between two endpoints."""
        calc = CalcTimeMixin()
        calc.start()
        sleep(1)
        calc.end()
        hour, minute, second = calc.delta()
        assert_true(isinstance(hour, (float, int)))
        assert_true(isinstance(minute, (float, int)))
        assert_true(isinstance(second, (float, int)))


class TestTaskDefinition(object):
    """Test task definition class."""

    @staticmethod
    def create_task():
        """Test create a task."""
        task_def = TaskDefinition(name='blaster')
        assert_is_instance(task_def, TaskDefinition)
        assert_true(hasattr(task_def, 'name'))

    @staticmethod
    def test_valid_task_definition():
        """Test whether a task definition is valid."""
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
        """Test whether a task definition is invalid."""
        task_def = TaskDefinition(
            dict(
                name='test',
                task='task',
            )
        )
        assert_false(task_def.is_valid())


class TestResultsList(object):
    """Test results list class."""

    @staticmethod
    def create_results():
        """Test create a results list."""
        res = ResultsList()
        assert_is_instance(res, ResultsList)

    @staticmethod
    def test_analyze_pass_results():
        """Test analyzing passed results."""
        res = ResultsList()
        res.append(dict(name='item1', status=0))
        assert_equal(res.analyze(), 0)

    @staticmethod
    def test_analyze_failed_results():
        """Test analyzing failed results."""
        res = ResultsList()
        res.append(dict(name='item1', status=1))
        assert_equal(res.analyze(), 1)

    @staticmethod
    def test_coordinate_valid_results():
        """Test coordinate valid results."""
        res = ResultsList()
        res.append(dict(name='item1', bid='1234', status=1))
        task = dict(name='item1', bid='1234')
        assert_is_instance(res.coordinate(task), dict)

    @staticmethod
    @raises(KeyError)
    def test_coordinate_invalid_results():
        """Test coordinate invalid results."""
        res = ResultsList()
        res.append(dict(name='item1', bid='1234', status=1))
        task = dict(name='item1')
        assert_is_instance(res.coordinate(task), dict)
