"""This example demonstrates how contractors can build homes in a new
development in parallel.
"""
from logging import getLogger
from pprint import pprint
from time import sleep

from blaster import Blaster

LOG = getLogger('blaster')


class House(object):
    """Class to build a house."""

    def __init__(self, style, **kwargs):
        """Constructor."""
        self.style = style

    def foundation(self):
        LOG.info('Building the foundation for %s house..' % self.style)
        sleep(1)

    def frame(self):
        LOG.info('Frame the house for %s house..' % self.style)
        sleep(1)

    def roof(self):
        LOG.info('Roof the house for %s house..' % self.style)
        sleep(1)

    def furnish(self):
        LOG.info('Furnish the house for %s house..' % self.style)
        sleep(1)

    def enjoy(self):
        LOG.info('Enjoy your new %s house :)' % self.style)
        sleep(1)

    def post_build_tasks(self):
        LOG.info('Perform post building tasks for %s house..' % self.style)
        sleep(1)


if __name__ == '__main__':
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
