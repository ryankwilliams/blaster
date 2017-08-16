"""Blaster blast.

The blast module contains the main blaster class to run.
"""
from multiprocessing import Queue
from uuid import uuid4

from .core import BlasterError
from .core import CalcTimeMixin, LoggerMixin, ResultsList, TaskDefinition
from .engine.processor import Processor


class Blaster(CalcTimeMixin, LoggerMixin):
    """Blaster's main class."""

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

    def blastoff(self, raise_on_failure=False):
        """Blast off a list of tasks concurrently calling each tasks methods
        defined.

        :param raise_on_failure: Whether to raise exception on failure.
        :type raise_on_failure: bool
        :return: Content from task method calls.
        :rtype: list
        """
        self.logger.info('.' * 30)
        self.logger.info('START: BLASTER PREPARATION')
        self.logger.info('.' * 30)

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
            task['_id'] = str(uuid4())

            self.logger.info('%s. TASK ~ %s, METHODS: %s' %
                             (index, task['task'].__name__, task['methods']))

            # add updated task to list
            self.updated_tasks.append(task)

        self.logger.info('.' * 30)
        self.logger.info('END: BLASTER PREPARATION')
        self.logger.info('.' * 30)

        # submit tasks to queue
        for task in self.updated_tasks:
            self.task_queue.put(task)

        self.logger.info('.' * 30)
        self.logger.info('START: BLASTER BLAST OFF')
        self.logger.info('.' * 30)

        # determine number of processes to start based on total tasks
        if len(self.updated_tasks) >= 10:
            NUMBER_OF_PROCESSES = 10
        else:
            NUMBER_OF_PROCESSES = len(self.updated_tasks)

        self.logger.info(
            'Total processes used by blaster is %s.' % NUMBER_OF_PROCESSES
        )

        # create worker processes
        for i in range(NUMBER_OF_PROCESSES):
            self.processes.append(Processor(self.task_queue, self.done_queue))

        # start worker processes
        for p in self.processes:
            p.start()

        try:
            # get status
            for i in range(len(self.updated_tasks)):
                self.results.append(self.done_queue.get())

            # stop worker processes
            for i in range(NUMBER_OF_PROCESSES):
                self.task_queue.put('STOP')

            # correlate the results with initial tasks
            for task in self.updated_tasks:
                data = self.results.coordinate(task)
                task.pop('_id')
                data.pop('_id')
                for key, value in data.items():
                    if key in task:
                        task[key] = value
        except KeyboardInterrupt:
            # get status
            for i in range(len(self.updated_tasks)):
                self.results.append(self.done_queue.get())

            # correlate the results with initial tasks
            for task in self.updated_tasks:
                data = self.results.coordinate(task)
                task.pop('_id')
                data.pop('_id')
                for key, value in data.items():
                    if key in task:
                        task[key] = value

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

            self.logger.info('.' * 30)
            self.logger.info('END: BLASTER BLAST OFF')
            self.logger.info('.' * 30)

            # handle the return
            if raise_on_failure and self.results.analyze():
                raise BlasterError(
                    'One or more tasks got a status of non zero.',
                    results=self.results
                )
            else:
                return self.results
