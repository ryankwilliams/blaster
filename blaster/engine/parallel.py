"""Blaster parallel.

The parallel module contains the main class which handles running tasks in
parallel (concurrently). It uses the built-in Python multiprocessing library.
"""
from multiprocessing import Process
from traceback import format_tb

from ..core import EngineMixin


class BlasterParallel(EngineMixin, Process):
    """Blaster parallel class to call all methods for a given task."""

    def __init__(self, in_queue, out_queue):
        """Constructor.

        :param in_queue: Input queue.
        :type in_queue: object
        :param out_queue: Output queue.
        :type out_queue: object
        """
        super(BlasterParallel, self).__init__()
        self.input = in_queue
        self.output = out_queue

    def run(self):
        """Run the task methods."""
        for task_def in iter(self.input.get, 'STOP'):
            task_id = task_def['bid']
            task_name = task_def['name']
            task_cls = task_def.pop('task')
            methods = task_def.pop('methods')

            # results template
            results = dict(
                bid=task_id,
                name=task_name,
                task=task_cls,
                methods=list()
            )

            try:
                # initialize object
                task_obj = task_cls(**task_def)

                # run through task methods sequentially
                for method in methods:
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
            except Exception:
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
            except KeyboardInterrupt:
                # get traceback information
                exc_data = self.get_traceback()

                # put method call results into queue
                results['methods'].append(dict(
                    name=method,
                    status=1,
                    rvalue=None,
                    traceback=format_tb(exc_data[2])
                ))

                # put overall status
                results.update(dict(status=1))
            finally:
                # update task definition into queue
                results.update(task_def)

                # put results into queue
                self.output.put(results)
