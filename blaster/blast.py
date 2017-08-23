"""Blaster blast.

The blast module contains the main blaster class to run.
"""
from multiprocessing import Queue
from uuid import uuid4

from .core import BlasterError
from .core import CalcTimeMixin, LoggerMixin, ResultsList, TaskDefinition
from .engine.processor import Processor


class Blaster(CalcTimeMixin, LoggerMixin):
    """Blast a list of tasks concurrently.

    The primary focus of this class is to processes a list of tasks given as
    input and run them all concurrently.
    """

    def __init__(self, tasks, log_level='info'):
        """Constructor.

        :param tasks: Tasks to be blasted off.
        :type tasks: list
        :param log_level: Logging level to handle logging messages.
        :type log_level: str
        """
        self.tasks = tasks

        # create queues
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

    def blastoff(self, raise_on_failure=False):
        """Blast off tasks concurrently call their defined methods.

        Each task has a list of methods to execute. This method will create
        x amount of processes (start them) and then begin to add the tasks to
        a queue. It will begin to process the tasks and run their methods they
        have defined. Once all tasks are finsihed in the queue, it will handle
        the results and return them back to the user.

        :param raise_on_failure: Whether to raise exception on failure.
        :type raise_on_failure: bool
        :return: Content from task method calls.
        :rtype: list
        """
        self.logger.info('Start blaster preparation.')

        # save start time
        self.start()

        # build updated task list
        self.logger.debug('Reviewing tasks to ensure proper keys are defined.')
        for index, task in enumerate(self.tasks):
            index += 1
            task = TaskDefinition(task)

            # task definition valid?
            if not task.is_valid():
                raise BlasterError('Req. keys missing for task definition.')

            # generate random unique id
            task['bid'] = str(uuid4())

            self.logger.info('%s. task: %s, methods: %s' %
                             (index, task['task'].__name__, task['methods']))

            # add updated task to list
            self.updated_tasks.append(task)
        self.logger.info('End blaster preparation.')

        # submit tasks to queue
        for task in self.updated_tasks:
            self.task_queue.put(task)

        self.logger.info('Start blaster.')

        # determine number of processes to start based on total tasks
        if len(self.updated_tasks) >= 10:
            process_count = 10
        else:
            process_count = len(self.updated_tasks)

        self.logger.debug('Total processes to run tasks: %s.' % process_count)

        # create worker processes
        for i in range(process_count):
            self.processes.append(Processor(self.task_queue, self.done_queue))

        # start worker processes
        for p in self.processes:
            p.start()

        try:
            # get status/results
            self.get_results()

            # stop worker processes
            for i in range(process_count):
                self.task_queue.put('STOP')

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

            self.logger.info('Blast off was unable to run all tasks given '
                             'due to CRTL+C interrupt.')
        finally:
            # save end time
            self.end()

            # calculate time delta
            hour, minutes, seconds = self.delta()
            self.logger.info('Total blast off duration: %dh:%dm:%ds' %
                             (hour, minutes, seconds))
            self.logger.info('End blaster.')

            # handle the return
            if raise_on_failure and self.results.analyze():
                raise BlasterError(
                    'One or more tasks got a status of non zero.',
                    results=self.results
                )
            else:
                return self.results
