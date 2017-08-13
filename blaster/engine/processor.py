"""Blaster processor.

The processor module contains the main class which handles running tasks
using the built-in Python multiprocessing library.
"""
from multiprocessing import Process
from traceback import print_exc


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
        self.task_id = self.task_def['_id']
        self.task_name = self.task_def['name']
        self.task_cls = self.task_def.pop('task')
        self.methods = self.task_def.pop('methods')

    def run(self):
        """Run the task methods."""

        # results template
        _res_struct = dict(
            _id=self.task_id,
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
            # update task definition into queue
            _res_struct.update(self.task_def)

            # put results into queue
            self.queue.put(_res_struct)
