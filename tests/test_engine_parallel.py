"""Blaster engine.parallel (tests).

Test cases to test the blaster engine parallel module.
"""
from multiprocessing import Queue

from blaster.blast import Worker
from tests.examples.invalid import InvalidCar
from tests.examples.valid import ValidCar


class TestEngineParallel(object):
    """Unit tests to cover engine.parallel module.

    Class provides both positive and negative tests to gain better code
    coverage.
    """

    def test_create_parallel_object(self):
        """Create parallel object.

        This method tests creating a parallel object from the Parallel
        class. Once the object is created, it will verify it is an instance of
        the Parallel class.
        """
        processor = Worker()
        assert isinstance(processor, Worker)

    def test_get_traceback(self):
        """Get traceback information.

        This method tests the parallel class method to get traceback
        information. It will verify the data type returned is a tuple.
        """
        parallel = Worker()
        assert isinstance(parallel.get_traceback(), tuple)

    def test_valid_run(self):
        """Call the parallel class run method.

        This method tests the parallel run method. (positive test)
        """
        # create queues
        in_queue = Queue()
        out_queue = Queue()

        # append data to in_queue
        in_queue.put(
            {
                "bid": 1234,
                "name": "car",
                "task": ValidCar,
                "methods": ["exterior", "interior"],
            }
        )
        in_queue.put("STOP")
        parallel = Worker()
        parallel.run(in_queue, out_queue, False)

    def test_invalid_run(self):
        """Call the parallel class run method.

        This method tests the parallel run method. (negative test)
        """
        # create queues
        in_queue = Queue()
        out_queue = Queue()

        # append data to in_queue
        in_queue.put(
            {
                "bid": 1234,
                "name": "car",
                "task": InvalidCar,
                "methods": ["exterior", "interior"],
            }
        )
        in_queue.put("STOP")
        parallel = Worker()
        parallel.run(in_queue, out_queue, False)
