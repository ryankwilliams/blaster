"""Blaster, a simple package to easily run a set of tasks either concurrently
or sequentially. Only using Python's built-in libraries.

Blaster is here to help other Python applications run tasks. Removing the
need for each application to write their own code to run tasks. Leave all of
this work up to blaster and just provide the classes and methods you would
like to run.
"""
import multiprocessing
import queue
import signal
import sys
import time
import traceback
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from blaster.core import *
from blaster.metadata import __version__


class Worker(LoggerMixin):
    """Worker class."""

    def __init__(self) -> None:
        """Constructor."""
        pass

    @staticmethod
    def get_traceback() -> tuple:
        """Return stack trace from the exception raised."""
        traceback.print_exc()
        return sys.exc_info()

    def run(
        self,
        task_queue: Union[queue.Queue, multiprocessing.Queue],
        task_complete_queue: Union[queue.Queue, multiprocessing.Queue],
        serial: bool,
    ) -> None:
        """Process the tasks methods from the given queues.

        :param task_queue: the queue containing the tasks to process.
        :param task_complete_queue: the queue containing updated tasks that
            have been or failed to fully process
        :param serial: whether this method is being run concurrently or
            sequentially
        """
        # Controls if remaining tasks in the queue should be flushed out
        flush_queue: bool = False

        # Holds the type of exception thrown
        exception_type: str = ""

        for task in iter(task_queue.get, "STOP"):
            self.logger.debug("Processing task: %s" % task["name"])

            # Instantiate task class
            task_obj = task["task"](**task)

            # Get the task timeout
            timeout = task.pop("timeout", None)

            # A list holding all methods processed with their results
            methods: List[Dict[str, Any]] = []

            def timeout_handler(signum, frame) -> None:
                """Timeout handler."""
                raise RuntimeError(
                    f"Task: {task['name']}, method: {method}, reached timeout!"
                )

            # Loop through and run all task methods
            for index, method in enumerate(task["methods"]):
                self.logger.debug("Running method %s" % method)

                try:
                    # Set task alarm timeout if supplied
                    if timeout:
                        signal.signal(signal.SIGALRM, timeout_handler)
                        signal.alarm(timeout)

                    # Run the task method
                    value = getattr(task_obj, method)()

                    # Set the tasks method results
                    methods.append({"name": method, "status": 0, "rvalue": value})
                    task["status"] = 0
                except (Exception, KeyboardInterrupt) as e:
                    self.logger.error(
                        "A exception was raised while processing task: %s "
                        "method: %s" % (task["name"], method)
                    )
                    task["status"] = 1

                    # Get stack trace
                    stack_trace: tuple = self.get_traceback()

                    # Set the tasks method results
                    methods.append(
                        {
                            "name": method,
                            "status": 1,
                            "rvalue": None,
                            "traceback": traceback.format_tb(stack_trace[2]),
                        }
                    )

                    # Set the remaining method results since they were not
                    # able to run
                    for item in task["methods"][index + 1 :]:
                        methods.append({"name": item, "status": "n/a", "rvalue": None})

                    # Since a failure happened, we need to flush out the queue
                    flush_queue = True

                    # Save the name of the exception thrown
                    exception_type = str(type(e).__name__).lower()
                    break
                finally:
                    # Reset the alarm if timeout was supplied
                    if timeout:
                        signal.alarm(0)

            task["methods"] = methods
            task_complete_queue.put(task)

            # Break out of the loop and flush out remaining tasks in the queue
            #  - expr_1 = parallel mode
            #  - expr_2 = sequential mode
            expr_1 = (
                flush_queue and exception_type == "keyboardinterrupt" and not serial
            )
            expr_2 = flush_queue and serial
            if expr_1 or expr_2:
                time.sleep(1)
                # Flush out remaining tasks in the queue
                while not task_queue.empty():
                    task = task_queue.get()
                    if task == "STOP":
                        break
                    methods = task.pop("methods")
                    _methods = []
                    for method in methods:
                        _methods.append(
                            {"name": method, "status": "n/a", "rvalue": None}
                        )
                    task["status"] = "n/a"
                    task["methods"] = _methods
                    task_complete_queue.put(task)
                break

            if (serial and task_queue.qsize() == 0) or expr_1:
                break


class Blaster(CalcTimeMixin, LoggerMixin):
    """Blaster class."""

    def __init__(self, tasks: List[Dict[str, Any]], log_level: str = "info") -> None:
        """Constructor.

        Responsible for initializing attributes and performing any base
        configuration required.

        :param tasks: list of tasks to be processed
        :param log_level: logging level to be used when logging messages
        """
        self.tasks: List[Dict[str, Any]] = tasks

        # Set place holder attributes for queues
        self.task_queue: Union[queue.Queue, multiprocessing.Queue]
        self.task_complete_queue: Union[queue.Queue, multiprocessing.Queue]

        self.results: ResultsList = ResultsList()

        # Configure blasters logger
        self.create_blaster_logger(log_level.lower())

    def total_processes(self) -> int:
        """Return the total number of worker processes to use."""
        count: int = 10
        total_tasks: int = len(self.tasks)
        if total_tasks < 10:
            count = total_tasks
        self.logger.debug(f"Processor count: {count}")
        return count

    def blastoff(
        self, serial: bool = False, raise_on_failure: bool = False
    ) -> List[Dict[str, int]]:
        """Blast off tasks concurrently or sequentially calling their defined
                methods.

        :param serial: whether to run tasks sequentially
        :param raise_on_failure: whether to raise exception on failure
        :return: content from task method calls
        """
        self.logger.info("--> Blaster v%s <--" % __version__)
        self.logger.info(
            "Task Execution: %s" % ("Sequential" if serial else "Concurrent")
        )

        # Initialize queues based on execution type
        if serial:
            self.task_queue = queue.Queue()
            self.task_complete_queue = queue.Queue()
        else:
            self.task_queue = multiprocessing.Queue()
            self.task_complete_queue = multiprocessing.Queue()

        self.logger.info("Tasks:")
        for index, task in enumerate(self.tasks, start=1):
            task = TaskDefinition(task)  # type: ignore
            self.logger.info(
                """%s. Task     : %s
                                Class    : %s
                                Methods  : %s"""
                % (index, task["name"], task["task"], task["methods"])
            )
            self.task_queue.put(task)

        # Save start time
        self.start_time()

        self.logger.info("** BLASTER BEGIN **")

        worker: Worker = Worker()
        if serial:
            worker.run(self.task_queue, self.task_complete_queue, serial)
        else:
            # Determine the number of processes to use
            processes_count: int = self.total_processes()

            # Build processes
            processes: List[multiprocessing.Process] = []
            for i in range(processes_count):
                processes.append(
                    multiprocessing.Process(
                        target=worker.run,
                        args=(self.task_queue, self.task_complete_queue, serial),
                    )
                )

            # Start processes
            for p in processes:
                p.start()

            try:
                for i in range(len(self.tasks)):
                    self.results.append(self.task_complete_queue.get())
                for i in range(processes_count):
                    self.task_queue.put("STOP")
            except KeyboardInterrupt:
                self.logger.warning(
                    "Delaying 15 seconds to allow worker processes to flush "
                    "out any remaining items in the queue."
                )
                time.sleep(15)

                while not self.task_complete_queue.empty():
                    self.results.append(self.task_complete_queue.get())

                for i in range(processes_count):
                    self.task_queue.put("STOP")

                for p in processes:
                    self.logger.error("Terminating child process: %s" % p.name)
                    p.terminate()
                    p.join(2)
                self.logger.error("All child processes were terminated.")

        # Save end time
        self.end_time()

        # Get tasks and their results
        while not self.task_complete_queue.empty():
            self.results.append(self.task_complete_queue.get())

        # Calculate time delta
        hour, minutes, seconds = self.time_delta()
        self.logger.info("** BLASTER COMPLETE **")
        self.logger.info(
            "    -> TOTAL DURATION: %dh:%dm:%ds" % (hour, minutes, seconds)
        )

        # Determine how to return results based on users input
        if raise_on_failure and self.results.analyze():
            raise BlasterError(
                "One or more tasks got a status of non zero.", results=self.results
            )
        else:
            return self.results
