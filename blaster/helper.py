from logging import getLogger

from .constants import REQ_TASK_KEYS

LOG = getLogger(__name__)


class TaskDefinition(dict):
    """Task definition."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(TaskDefinition, self).__init__(*args, **kwargs)

    def is_valid(self):
        """Ensure the task definition is valid.

        :return: Whether required keys are set.
        :rtype: bool
        """
        count = 0
        for key in REQ_TASK_KEYS:
            if key not in self:
                LOG.error('Req. key %s missing from task definition!' % key)
                count += 1
        return True if count == 0 else False
