"""Blaster valid tests.

Valid classes used by blaster tests.
"""
from logging import getLogger
from time import sleep

LOG = getLogger('blaster')


class ValidCar(object):
    """Class to build a valid car."""

    def __init__(self, **kwargs):
        """Constructor."""
        pass

    @staticmethod
    def exterior():
        LOG.info('Build exterior.')
        sleep(1)

    @staticmethod
    def interior():
        LOG.info('Build interior')
        sleep(1)