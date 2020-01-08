"""Engine module.

This module is the worker which processes all the tasks/methods provided.
"""

import signal

from multiprocessing import Process, Queue
from sys import exc_info
from traceback import format_tb
from traceback import print_exc

from blaster.core import LoggerMixin


class Engine(Process, LoggerMixin):
    """Blaster engine.

    This class handles processing all tasks in the queue and their associated
    methods.
    """

    def __init__(self, in_queue, out_queue, serial):
        """Constructor.

        :param Queue in_queue: input queue
        :param Queue out_queue: output queue
        :param bool serial: whether tasks are run concurrently or sequentially
        """
        super(Engine, self).__init__()

        self.input = in_queue
        self.output = out_queue
        self.serial = serial

    @staticmethod
    def get_traceback():
        """Get stack trace from exception raised.

        :return: exception stack trace
        :rtype: tuple
        """
        print_exc()
        return exc_info()

    @staticmethod
    def init_results(task):
        """Initialize variable storing task results.

        :param dict task: task definition
        :return: task definition result variable
        :rtype: dict
        """
        return dict(
            bid=task['bid'],
            name=task['name'],
            task=task['task'],
            methods=list()
        )

    def run(self):
        """Process the task."""
        for task in iter(self.input.get, "STOP"):
            method = None

            results = self.init_results(task)

            task_cls = task.pop('task')
            methods = task.pop('methods')
            timeout = task.pop('timeout', None)

            def timeout_handler(signum, frame):
                """Timeout handler."""
                raise RuntimeError("Task: %s, method: %s, reached timeout!" %
                                   (task['name'], method))

            try:
                # initialize task object
                task_obj = task_cls(**task)

                # run through task methods sequentially
                for method in methods:
                    signal.signal(signal.SIGALRM, timeout_handler)
                    if timeout:
                        signal.alarm(timeout)

                    # call method
                    value = getattr(task_obj, method)()

                    # put method call results into queue
                    results['methods'].append(dict(
                        name=method,
                        status=0,
                        rvalue=value
                    ))

                # put overall status
                results.update(dict(status=0))
            except (Exception, KeyboardInterrupt):
                # get traceback information
                exc_data = self.get_traceback()

                try:
                    # put method call results into queue
                    results['methods'].append(dict(
                        name=method,
                        status=1,
                        rvalue=None,
                        traceback=format_tb(exc_data[2])
                    ))
                except UnboundLocalError:
                    results.update(dict(
                        status=1,
                        traceback=format_tb(exc_data[2])
                    ))

                # put overall status
                results.update(dict(status=1))

                # flush out tasks on error when execution is sequential
                if self.serial:
                    self.logger.warning(
                        "Flush out tasks in queue due to prior task failure. "
                        "Happening since execution is sequential.")

                    while not self.input.empty():
                        _task = self.input.get(False)

                        _results = self.init_results(_task)
                        _results.update(dict(status="n/a"))
                        self.output.put(_results)
            finally:
                signal.alarm(0)

                # update task definition into queue
                results.update(task)

                # put results into queue
                self.output.put(results)

                if self.serial and self.input.empty():
                    break
