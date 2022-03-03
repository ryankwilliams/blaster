"""Blaster engine.serial (tests).

Test cases to test the blaster engine serial module.
"""

import queue

from blaster.blast import Worker
from tests.examples.invalid import InvalidCar
from tests.examples.valid import ValidCar


class TestEngineSerial(object):
    """Unit tests to cover engine.serial module.

    Class provides both positive and negative tests to gain better code
    coverage.
    """

    def test_create_serial_object(self):
        """Create serial object.

        This method tests creating a serial object from the Serial
        class. Once the object is created, it will verify it is an instance of
        the Serial class.
        """
        processor = Worker()
        assert isinstance(processor, Worker)

    def test_get_traceback(self):
        """Get traceback information.

        This method tests the serial class method to get traceback
        information. It will verify the data type returned is a tuple.
        """
        serial = Worker()
        assert isinstance(serial.get_traceback(), tuple)

    def test_valid_run(self):
        """Call the serial class run method.

        This method tests the serial run method. (positive test)
        """
        # output results list
        output = queue.Queue()

        # create task definition
        task_def = dict(
            bid=1234, name="car", task=ValidCar, methods=["exterior", "interior"]
        )

        input_queue = queue.Queue()
        input_queue.put(task_def)

        serial = Worker()
        serial.run(input_queue, output, True)

    def test_invalid_run(self):
        """Call the serial class run method.

        This method tests the serial run method. (negative test)
        """
        # output results list
        output = queue.Queue()

        # create task definition
        task_def = dict(
            bid=1234, name="car", task=InvalidCar, methods=["exterior", "interior"]
        )

        input_queue = queue.Queue()
        input_queue.put(task_def)

        serial = Worker()
        serial.run(input_queue, output, True)
