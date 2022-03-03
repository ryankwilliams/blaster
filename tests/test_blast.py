"""Blaster blast (tests).

Test cases to test the blaster blast module.
"""
import pytest

from blaster import Blaster, BlasterError
from tests.examples.invalid import InvalidCar
from tests.examples.valid import ValidCar


class TestBlast(object):
    """Unit tests to cover blast module.

    Class provides both positive and negative tests to gain better code
    coverage.
    """

    @staticmethod
    def test_create_blaster_object():
        """Create a blaster object.

        This method tests creating a blaster object from the Blaster class.
        Once the object is created, it will verify it is an instance of the
        Blaster class.
        """
        blaster = Blaster(list())
        assert isinstance(blaster, Blaster)

    @staticmethod
    def test_valid_blastoff_serial():
        """Run blaster blastoff method with valid task in sequential.

        This method tests the blaster blastoff method. (positive test)
        """
        blaster = Blaster(
            tasks=[
                {"name": "car", "task": ValidCar, "methods": ["exterior", "interior"]}
            ]
        )
        blaster.blastoff(serial=True)

    @staticmethod
    def test_blastoff_serial_invalid_task():
        """Run blaster blastoff method with an invalid task in sequential.

        This method tests the blaster blastoff method. (negative test)
        """
        with pytest.raises(BlasterError):
            blaster = Blaster(
                tasks=[{"task": ValidCar, "methods": ["exterior", "interior"]}]
            )
            blaster.blastoff(serial=True)

    @staticmethod
    def test_blastoff_serial_failure():
        """Run blaster blastoff method with a task raising a failure in
        sequential.

        This method tests the blaster blastoff method with a task raising an
        exception. (negative test)
        """
        with pytest.raises(BlasterError):
            blaster = Blaster(
                tasks=[
                    {
                        "name": "car",
                        "task": InvalidCar,
                        "methods": ["exterior", "interior"],
                    }
                ]
            )
            blaster.blastoff(serial=True, raise_on_failure=True)

    @staticmethod
    def test_valid_blastoff_parallel():
        """Run blaster blastoff method with valid task in parallel.

        This method tests the blaster blastoff method. (positive test)
        """
        blaster = Blaster(
            tasks=[
                {"name": "car", "task": ValidCar, "methods": ["exterior", "interior"]}
            ]
        )
        blaster.blastoff()

    @staticmethod
    def test_blastoff_parallel_invalid_task():
        """Run blaster blastoff method with an invalid task in parallel.

        This method tests the blaster blastoff method. (negative test)
        """
        with pytest.raises(BlasterError):
            blaster = Blaster(
                tasks=[{"task": ValidCar, "methods": ["exterior", "interior"]}]
            )
            blaster.blastoff()

    @staticmethod
    def test_blastoff_parallel_failure():
        """Run blaster blastoff method with a task raising a failure in
        parallel.

        This method tests the blaster blastoff method with a task raising an
        exception. (negative test)
        """
        with pytest.raises(BlasterError):
            blaster = Blaster(
                tasks=[
                    {
                        "name": "car",
                        "task": InvalidCar,
                        "methods": ["exterior", "interior"],
                    }
                ]
            )
            blaster.blastoff(raise_on_failure=True)

    def test_blaster_limit_processes(self):
        """Run blaster blastoff method limiting number of processes.

        This method tests the blaster blastoff method to limit the number of
        processes to launch based on the total number of tasks to call.
        (positive test)
        """
        tasks = list()
        for i in range(10):
            i += 1
            tasks.append(
                {"name": "car", "task": ValidCar, "methods": ["exterior", "interior"]}
            )
        blaster = Blaster(tasks=tasks)
        blaster.blastoff()
