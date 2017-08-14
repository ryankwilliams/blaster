"""Blaster blast.

The blast module contains the main blaster class to run.
"""
from copy import deepcopy
from multiprocessing import Queue
from pprint import pformat
from time import sleep
from uuid import uuid4

from .core import BlasterError
from .core import CalcTimeMixin, LoggerMixin, ResultsList, TaskDefinition
from .engine.processor import Processor


class Blaster(LoggerMixin, CalcTimeMixin):
    """Blaster's main class."""

    def __init__(self, tasks, log_level='info'):
        """Constructor.

        :param tasks: Tasks to be blasted off.
        :type tasks: list
        :param log_level: Logging level to handle logging messages.
        :type log_level: str
        """
        self.tasks = tasks
        self.processes = list()
        self.results = ResultsList()
        self.queue = Queue()
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

        # build the list of processes to run
        self.logger.debug('Start: building processes..')
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

            self.processes.append(Processor(deepcopy(task), self.queue))
        self.logger.debug('End: building processes.')
        self.logger.debug(pformat(self.processes))
        self.logger.info('.' * 30)
        self.logger.info('END: BLASTER PREPARATION')
        self.logger.info('.' * 30)

        self.logger.info('.' * 30)
        self.logger.info('START: BLASTER BLAST OFF')
        self.logger.info('.' * 30)

        try:
            # start processes
            self.logger.info('Starting processes..')
            for p in self.processes:
                p.start()
                self.logger.debug('Process %s started.' % p.name)
                sleep(0.5)

            # wait for all processes to finish
            for p in self.processes:
                sleep(0.5)
                p.join()

            # collect results
            for p in self.processes:
                self.results.append(self.queue.get())

            # correlate the results with initial tasks
            for task in self.tasks:
                data = self.results.coordinate(task)
                task.pop('_id')
                data.pop('_id')
                for key, value in data.items():
                    if key in task:
                        task[key] = value

            self.logger.info('Blast off was able to run all tasks given!')
        except KeyboardInterrupt:
            # collect results
            for p in self.processes:
                self.results.append(self.queue.get())

            # correlate the results with initial tasks
            for task in self.tasks:
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
                sleep(0.5)

            self.logger.info('Blast off was unable to run all tasks given '
                             'due to CRTL+C interrupt.')
        finally:
            # save end time
            self.end()

            # update tasks list
            # self.tasks = self.results

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
