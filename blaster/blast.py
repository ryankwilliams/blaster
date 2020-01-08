"""Blast module.

Main entry point to blaster.
"""

from multiprocessing import Queue
from time import sleep

from blaster.core import *
from blaster.engine import Engine
from blaster.metadata import __version__


class Blaster(CalcTimeMixin, LoggerMixin):
    """Blast a list of tasks concurrently or sequentially..

    The primary focus of this class is to processes a list of tasks given as
    input and run its defined methods.
    """

    def __init__(self, tasks, log_level="info"):
        """Constructor.

        :param list tasks: tasks to be processed
        :param str log_level: log level tailoring messages logged
        """
        self.tasks = tasks
        self.task_queue = Queue()
        self.done_queue = Queue()
        self.updated_tasks = list()
        self.processes = list()
        self.results = ResultsList()

        # create blaster logger
        self.create_blaster_logger(log_level.lower())

    def get_results(self):
        """Get results for tasks in the queue."""
        for i in range(len(self.updated_tasks)):
            self.results.append(self.done_queue.get())

    def correlate_data(self):
        """Correlate the task definition to its results data."""
        for task in self.updated_tasks:
            data = self.results.coordinate(task)
            for key, value in data.items():
                if key in task:
                    task[key] = value

    def _total_workers(self, serial):
        """Return the total number of worker processes to use."""
        count = 10
        if serial:
            count = 1
        else:
            if len(self.updated_tasks) < 10:
                count = len(self.updated_tasks)
        return count

    def blastoff(self, serial=False, raise_on_failure=False, delay=5):
        """Blast off tasks concurrently or sequentially calling their defined
        methods.

        :param bool serial: whether to run tasks sequentially
        :param bool raise_on_failure: whether to raise exception on failure
        :param int delay: duration to delay between starting processes
        :return: content from task method calls
        :rtype: list
        """
        self.logger.info("--> Blaster v{} <--".format(__version__))
        self.logger.info("Task Execution: {}".format(
            "Sequential" if serial else "Concurrent"))

        self.logger.info("Tasks:")
        for index, task in enumerate(self.tasks, start=1):
            task = TaskDefinition(task)
            self.logger.info("""{}.     Task     : {}
                                    Class    : {}
                                    Methods  : {}""".format(
                index, task['name'], task['task'], task['methods']))
            self.updated_tasks.append(task)
            self.task_queue.put(task)

        # get total worker processes to use
        worker_count = self._total_workers(serial)

        # create worker processes
        for i in range(worker_count):
            self.processes.append(
                Engine(self.task_queue, self.done_queue, serial)
            )

        # start worker processes
        self.start_time()
        self.logger.info("3..2..1.. BLAST OFF!")
        for p in self.processes:
            p.start()
            sleep(delay)

        try:
            # get status/results
            self.get_results()

            # stop worker processes
            for i in range(worker_count):
                self.task_queue.put("STOP")

            # correlate the results with initial tasks
            self.correlate_data()
        except KeyboardInterrupt:
            # get status/results
            self.get_results()

            # correlate the results with initial tasks
            self.correlate_data()

            # terminate processes
            for p in self.processes:
                p.terminate()
                p.join()

            self.logger.info("Blast off was unable to run all tasks given "
                             "due to CRTL+C interrupt.")
        finally:
            self.end_time()

            # calculate time delta
            hour, minutes, seconds = self.time_delta()
            self.logger.info(
                "BLAST OFF COMPLETE! TOTAL DURATION: %dh:%dm:%ds" %
                (hour, minutes, seconds))

            # handle the return
            if raise_on_failure and self.results.analyze():
                raise BlasterError(
                    "One or more tasks got a status of non zero.",
                    results=self.results
                )
            else:
                return self.results
