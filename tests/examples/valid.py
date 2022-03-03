"""Blaster valid tests.

Valid classes used by blaster tests.
"""
from logging import getLogger
from time import sleep

LOG = getLogger("blaster")


class ValidCar(object):
    """Build a valid car."""

    def __init__(self, **kwargs):
        """Constructor."""
        pass

    @staticmethod
    def exterior():
        """Build the car's exterior."""
        LOG.info("Build exterior.")
        sleep(1)

    @staticmethod
    def interior():
        """Build the car's interior."""
        LOG.info("Build interior.")
        sleep(1)
