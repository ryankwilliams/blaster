"""Blaster engine.processor (tests).

Test cases to test the blaster engine processor module.
"""
from multiprocessing import Queue

from nose.tools import assert_is_instance

from blaster.engine.processor import Processor
from examples.invalid import InvalidCar
from examples.valid import ValidCar


class TestEngineProcessor(object):
    """Unit tests to cover engine.process module.

    Class provides both positive and negative tests to gain better code
    coverage.
    """

    def test_create_processor_object(self):
        """Create process object.

        This method tests creating a processor object from the Processor
        class. Once the object is created, it will verify it is an instance of
        the Processor class.
        """
        processor = Processor(list(), list())
        assert_is_instance(processor, Processor)

    def test_get_traceback(self):
        """Get traceback information.

        This method tests the processor class method to get traceback
        information. It will verify the data type returned is a tuple.
        """
        processor = Processor(list(), list())
        assert_is_instance(processor.get_traceback(), tuple)

    def test_valid_run(self):
        """Call the processor class run method.

        This method tests the processor run method. (positive test)
        """
        # create queues
        in_queue = Queue()
        out_queue = Queue()

        # append data to in_queue
        in_queue.put(
            {
                'bid': 1234,
                'name': 'car',
                'task': ValidCar,
                'methods': ['exterior', 'interior']
            }
        )
        in_queue.put('STOP')
        processor = Processor(in_queue, out_queue)
        processor.run()

    def test_invalid_run(self):
        """Call the processor class run method.

        This method tests the process run method. (negative test)
        """
        # create queues
        in_queue = Queue()
        out_queue = Queue()

        # append data to in_queue
        in_queue.put(
            {
                'bid': 1234,
                'name': 'car',
                'task': InvalidCar,
                'methods': ['exterior', 'interior']
            }
        )
        in_queue.put('STOP')
        processor = Processor(in_queue, out_queue)
        processor.run()
