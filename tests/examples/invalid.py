"""Blaster invalid tests.

Invalid classes used by blaster tests.
"""
from logging import getLogger
from time import sleep

LOG = getLogger("blaster")


class InvalidCar(object):
    """Build an invalid car."""

    def __init__(self, **kwargs):
        """Constructor."""
        pass

    @staticmethod
    def exterior():
        """Build the car's exterior."""
        LOG.info("Build exterior.")
        raise Exception("Unable to build exterior today.")

    @staticmethod
    def interior():
        """Build the car's interior."""
        LOG.info("Build interior.")
        sleep(1)
