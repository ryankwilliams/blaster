"""Blast module.

Main entry point to blaster.
"""

from multiprocessing import Queue
from time import sleep
from uuid import uuid4

from .core import BlasterError
from .core import CalcTimeMixin, LoggerMixin, ResultsList, TaskDefinition
from .engine import Engine
from .metadata import __version__


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

        # set queue attributes (not initialized)
        self.task_queue = Queue()
        self.done_queue = Queue()

        # set list attributes
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

        # perform initialization
        self.initialize()

        self.logger.info("Tasks:")

        # submit tasks to queue
        for index, task in enumerate(self.updated_tasks, start=1):
            self.logger.info("""{}. Task     : {}
                                    Class    : {}
                                    Methods  : {}""".format(
                index, task['name'], task['task'], task['methods']))
            self.task_queue.put(task)

        self.logger.info("3..2..1.. BLAST OFF!")

        if serial:
            # run tasks sequentially, using only 1 process
            process_count = 1
        else:
            # determine number of processes to start based on total tasks
            if len(self.updated_tasks) >= 10:
                process_count = 10
            else:
                process_count = len(self.updated_tasks)

        self.logger.debug("Total processes to run tasks: %s." % process_count)

        # create worker processes
        for i in range(process_count):
            self.processes.append(
                Engine(self.task_queue, self.done_queue, serial)
            )

        # start worker processes
        for p in self.processes:
            p.start()
            sleep(delay)

        try:
            # get status/results
            self.get_results()

            # stop worker processes
            for i in range(process_count):
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
            # save end time
            self.end()

            # calculate time delta
            hour, minutes, seconds = self.delta()
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

    def initialize(self):
        """Perform initial tasks before processing tasks by blaster."""
        self.logger.debug("Blaster initializing..")

        # save start time
        self.start()

        # build updated task list
        self.logger.debug("Verifying required keys are set.")

        for index, task in enumerate(self.tasks, start=1):
            # create task definition
            task = TaskDefinition(task)

            # task definition valid?
            if not task.is_valid():
                raise BlasterError("Req. keys missing for task definition.")

            # generate random unique id
            task['bid'] = str(uuid4())

            self.logger.debug("%s. task: %s, methods: %s" % (
                index, task['task'].__name__, task['methods']))

            # add updated task to list
            self.updated_tasks.append(task)
        self.logger.debug("Blaster initialization complete!")
