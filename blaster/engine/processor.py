"""Blaster processor.

The processor module contains the main class which handles running tasks
using the built-in Python multiprocessing library.
"""
from multiprocessing import Process
from traceback import print_exc


class Processor(Process):
    """Processor class to handle calling all methods for a given task."""

    def __init__(self, in_queue, out_queue):
        """Constructor.

        :param in_queue: Input queue.
        :type in_queue: object
        :param out_queue: Output queue.
        :type out_queue: object
        """
        super(Processor, self).__init__()
        self.input = in_queue
        self.output = out_queue

    def run(self):
        """Run the task methods."""
        for task_def in iter(self.input.get, 'STOP'):
            task_id = task_def['_id']
            task_name = task_def['name']
            task_cls = task_def['task']
            methods = task_def['methods']

            # results template
            _res_struct = dict(
                _id=task_id,
                name=task_name,
                task=task_cls,
                status=None,
                methods=list()
            )

            try:
                # initialize object
                task_obj = task_cls(**task_def)

                # run through task methods sequentially
                for method in methods:
                    # call method
                    getattr(task_obj, method)()

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
                # update task definition into queue
                _res_struct.update(task_def)

                # put results into queue
                self.output.put(_res_struct)
