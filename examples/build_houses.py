"""This example demonstrates how contractors can build homes in a new
development in parallel.
"""
from logging import getLogger
from pprint import pprint
from time import sleep

from blaster import Blaster

LOG = getLogger('blaster')


class House(object):
    """Build a house."""

    def __init__(self, style, **kwargs):
        """Constructor.

        :param style: Style of the house to build.
        :type style: str
        """
        self.style = style

    def foundation(self):
        """Build the foundation."""
        LOG.info('Building the foundation for %s house..' % self.style)
        sleep(1)

    def frame(self):
        """Frame the house."""
        LOG.info('Frame the house for %s house..' % self.style)
        sleep(1)

    def roof(self):
        """Roof the house."""
        LOG.info('Roof the house for %s house..' % self.style)
        sleep(1)

    def furnish(self):
        """Furnish the house."""
        LOG.info('Furnish the house for %s house..' % self.style)
        sleep(1)

    def enjoy(self):
        """Enjoy the house."""
        LOG.info('Enjoy your new %s house :)' % self.style)
        sleep(1)

    def post_build_tasks(self):
        """Post build tasks after house is built."""
        LOG.info('Perform post building tasks for %s house..' % self.style)
        sleep(1)


if __name__ == '__main__':
    # list of tasks (houses to be built) concurrently to save time
    tasks = [
        {
            'name': 'House 1',
            'task': House,
            'methods': [
                'foundation',
                'frame',
                'roof',
                'furnish',
                'enjoy'
            ],
            'style': 'contemporary'
        },
        {
            'name': 'House 2',
            'task': House,
            'methods': [
                'foundation',
                'frame',
                'roof',
                'furnish',
                'post_build_tasks',
                'enjoy'
            ],
            'style': 'cape'
        },
        {
            'name': 'House 3',
            'task': House,
            'methods': [
                'foundation',
                'frame',
                'roof',
                'furnish',
                'post_build_tasks',
                'enjoy'
            ],
            'style': 'colonial'
        },
        {
            'name': 'House 4',
            'task': House,
            'methods': [
                'foundation',
                'frame',
                'roof',
                'furnish',
                'post_build_tasks',
                'enjoy'
            ],
            'style': 'ranch'
        },
        {
            'name': 'House 5',
            'task': House,
            'methods': [
                'foundation',
                'frame',
                'roof',
                'furnish',
                'post_build_tasks',
                'enjoy'
            ],
            'style': 'split'
        }
    ]

    # create blaster object
    blast = Blaster(tasks)

    # blast off tasks
    data = blast.blastoff()

    # log results
    sleep(2)
    pprint(data, indent=4)
