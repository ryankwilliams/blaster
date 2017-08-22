"""Blaster blast (tests).

Test cases to test the blaster blast module.
"""
from nose.tools import assert_is_instance, raises

from blaster import Blaster, BlasterError
from examples.invalid import InvalidCar
from examples.valid import ValidCar


class TestBlast(object):
    """Test blast module."""

    def test_create_blaster_object(self):
        """Test creating a blaster object."""
        blaster = Blaster(list())
        assert_is_instance(blaster, Blaster)

    def test_valid_blastoff(self):
        """Test a valid blastoff."""
        blaster = Blaster(
            tasks=[
                {
                    'name': 'car',
                    'task': ValidCar,
                    'methods': ['exterior', 'interior']
                }
            ]
        )
        blaster.blastoff()

    @raises(BlasterError)
    def test_blastoff_invalid_task(self):
        """Test blaster blastoff with an invalid task."""
        blaster = Blaster(
            tasks=[
                {
                    'task': ValidCar,
                    'methods': ['exterior', 'interior']
                }
            ]
        )
        blaster.blastoff()

    @raises(BlasterError)
    def test_blastoff_failure(self):
        """Test blaster blastoff with a task raising an exception."""
        blaster = Blaster(
            tasks=[
                {
                    'name': 'car',
                    'task': InvalidCar,
                    'methods': ['exterior', 'interior']
                }
            ]
        )
        blaster.blastoff(raise_on_failure=True)

    def test_blaster_limit_processes(self):
        """Test blaster limiting the number of processes it can run at once."""
        tasks = list()
        for i in range(10):
            i += 1
            tasks.append(
                {
                    'name': 'car',
                    'task': ValidCar,
                    'methods': ['exterior', 'interior']
                }
            )

        blaster = Blaster(tasks=tasks)
        blaster.blastoff()
