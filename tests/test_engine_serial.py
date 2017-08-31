"""Blaster engine.serial (tests).

Test cases to test the blaster engine serial module.
"""

from nose.tools import assert_is_instance

from blaster.engine import BlasterSerial
from examples.invalid import InvalidCar
from examples.valid import ValidCar


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
        processor = BlasterSerial(list(), list())
        assert_is_instance(processor, BlasterSerial)

    def test_get_traceback(self):
        """Get traceback information.

        This method tests the serial class method to get traceback
        information. It will verify the data type returned is a tuple.
        """
        serial = BlasterSerial(list(), list())
        assert_is_instance(serial.get_traceback(), tuple)

    def test_valid_run(self):
        """Call the serial class run method.

        This method tests the serial run method. (positive test)
        """
        # output results list
        output = list()

        # create task definition
        task_def = dict(
            bid=1234,
            name='car',
            task=ValidCar,
            methods=['exterior', 'interior']
        )
        serial = BlasterSerial(task_def, output)
        serial.run()

    def test_invalid_run(self):
        """Call the serial class run method.

        This method tests the serial run method. (negative test)
        """
        # output results list
        output = list()

        # create task definition
        task_def = dict(
            bid=1234,
            name='car',
            task=InvalidCar,
            methods=['exterior', 'interior']
        )
        serial = BlasterSerial(task_def, output)
        serial.run()
