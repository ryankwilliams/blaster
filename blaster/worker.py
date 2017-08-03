from multiprocessing import Process, Queue
from pprint import pformat
from time import sleep
from traceback import print_exc
from uuid import uuid4

from . import BlasterError
from .constants import REQ_TASK_KEYS
from .core import CalcTimeMixin, LoggerMixin


class Processor(Process):
    """Processor class to handle calling all methods for a given task."""

    def __init__(self, task_def, queue):
        """Constructor.

        :param task_def: The task definition.
        :type task_def: dict
        :param queue: The queue to store process results.
        :type queue: object
        """
        super(Processor, self).__init__()
        self.task_def = task_def
        self.queue = queue

        self.task_obj = object
        self.task_id = self.task_def['id']
        self.task_name = self.task_def['name']
        self.task_cls = self.task_def.pop('task')
        self.methods = self.task_def.pop('methods')

    def run(self):
        """Run the task methods."""

        # results template
        _res_struct = dict(
            id=self.task_id,
            name=self.task_name,
            task=self.task_cls,
            status=None,
            methods=list()
        )

        try:
            # initialize task object
            self.task_obj = self.task_cls(**self.task_def)

            # run through tasks methods sequentially
            for method in self.methods:
                # call method
                getattr(self.task_obj, method)()

                # put method call results into queue
                _res_struct['methods'].append(dict(
                    name=method,
                    status=0
                ))

                # put overall status
                _res_struct.update(dict(status=0))
        except Exception as ex:
            # log traceback
            print_exc()

            try:
                # put method call results into queue
                _res_struct['methods'].append(dict(
                    name=method,
                    status=1,
                    traceback=ex
                ))
            except UnboundLocalError:
                _res_struct.update(dict(status=1, traceback=ex))

            # put overall status
            _res_struct.update(dict(status=1))
        except KeyboardInterrupt as ex:
            # log traceback
            print_exc()

            # put method call results into queue
            _res_struct['methods'].append(dict(
                name=method,
                status=1,
                traceback=ex
            ))

            # put overall status
            _res_struct.update(dict(status=1))
        finally:
            # put results into queue
            self.queue.put(_res_struct)


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
        self.results = list()
        self.queue = Queue()
        self.create_blaster_logger(log_level.lower())

    def validate_task_def(self, task_def):
        """Validate a task definition to ensure required keys are set.

        :param task_def: The task definition.
        :type task_def: dict
        :return: Whether required keys are set.
        :rtype: bool
        """
        count = 0
        for key in REQ_TASK_KEYS:
            if key not in task_def:
                self.logger.error('Missing key: %s from task definition' % key)
                count += 1

        return True if count == 0 else False

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
            # check if required task definition keys exist
            if not self.validate_task_def(task):
                raise BlasterError(
                    'Not all required keys are defined for task definition.'
                )

            # generate random unique id
            task['id'] = str(uuid4())

            self.logger.info('%s. TASK ~ %s, METHODS: %s' %
                             (index, task['task'].__name__, task['methods']))

            self.processes.append(Processor(task, self.queue))
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

            # correlate the data
            for res in self.results:
                data = self.map_task_to_results(res)
                res.update(data)
                res.pop('id')

            self.logger.info('Blast off was able to run all tasks given!')
        except KeyboardInterrupt:
            # collect results
            for p in self.processes:
                self.results.append(self.queue.get())

            # correlate the data
            for res in self.results:
                data = self.map_task_to_results(res)
                res.update(data)
                res.pop('id')

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

            # calculate time delta
            hour, minutes, seconds = self.delta()
            self.logger.info('Total blast off duration: %dh:%dm:%ds' %
                             (hour, minutes, seconds))

            self.logger.info('.' * 30)
            self.logger.info('END: BLASTER BLAST OFF')
            self.logger.info('.' * 30)

            # handle the return
            if raise_on_failure and self.analyze_results():
                raise BlasterError(
                    'One or more tasks got a status of non zero.',
                    results=self.results
                )
            else:
                return self.results

    def map_task_to_results(self, res):
        """Map the task to the one defined in the results. This is needed to
        correlate the data.

        :param res: Resource element.
        :type res: dict
        :return: The matching task element.
        :rtype: dict
        """
        element = None

        for item in self.tasks:
            if res['id'] == item['id']:
                element = item
                break
        return element

    def analyze_results(self):
        """Analyze the results to determine overall status."""
        status = 0
        for item in self.results:
            if item['status'] != 0:
                status = 1
                break
        return status
