"""Blaster serial.

The serial module contains the main class which handles running tasks in
serial (sequentially - aka one by one). This can be used over the main
functionality of running tasks concurrently (default behavior for blaster).
"""
from sys import exc_info
from traceback import format_tb, print_exc


class BlasterSerial(object):
    """Blaster serial class to call all methods for a given task."""

    def __init__(self, task_def, output):
        """Constructor."""
        self.task_def = task_def
        self.output = output

    def run(self):
        """Run the task methods."""
        task_id = self.task_def['bid']
        task_name = self.task_def['name']
        task_cls = self.task_def.pop('task')
        methods = self.task_def.pop('methods')

        # results template
        results = dict(
            bid=task_id,
            name=task_name,
            task=task_cls,
            methods=list()
        )

        try:
            # initialize object
            task_obj = task_cls(**self.task_def)

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
            results.update(self.task_def)

            # put results into queue
            self.output.append(results)

    @staticmethod
    def get_traceback():
        """Get traceback when exception is raised. Will log traceback as well.

        :return: Exception information.
        :rtype: tuple
        """
        print_exc()
        return exc_info()