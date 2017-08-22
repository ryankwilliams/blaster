"""Blaster engine.processor (tests).

Test cases to test the blater engine processor module.
"""
from multiprocessing import Queue

from nose.tools import assert_is_instance

from blaster.engine.processor import Processor


class TestEngineProcessor(object):
    """Test engine.processor module."""

    def test_create_processor_object(self):
        """Test creating a processor object."""
        processor = Processor(list(), list())
        assert_is_instance(processor, Processor)

    def test_get_traceback(self):
        """Test getting traceback information."""
        processor = Processor(list(), list())
        assert_is_instance(processor.get_traceback(), tuple)

    def test_run(self):
        """Test process class run method."""
        in_queue = Queue()
        out_queue = Queue()
        in_queue.put('STOP')
        processor = Processor(in_queue, out_queue)
        processor.run()
