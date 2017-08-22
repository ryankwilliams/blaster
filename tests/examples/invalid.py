"""Blaster invalid tests.

Invalid classes used by blaster tests.
"""
from logging import getLogger
from time import sleep

LOG = getLogger('blaster')


class InvalidCar(object):
    """Class to build a invalid car."""

    def __init__(self, **kwargs):
        """Constructor."""
        pass

    @staticmethod
    def exterior():
        LOG.info('Build exterior.')
        raise Exception('Unable to build exterior today.')
        sleep(1)

    @staticmethod
    def interior():
        LOG.info('Build interior')
        sleep(1)
