"""Build various types of homes.

This module contains a class which has methods for building different aspects
to a house.
"""
from logging import getLogger
from time import sleep


LOG = getLogger("blaster")


class House:
    """Build a house."""

    def __init__(self, style, **kwargs):
        """Constructor.

        :param style: Style of the house to build.
        :type style: str
        """
        self.style = style

    def foundation(self):
        """Build the foundation."""
        LOG.info("Building the foundation for %s house.." % self.style)
        sleep(1)

    def frame(self):
        """Frame the house."""
        LOG.info("Frame the house for %s house.." % self.style)
        sleep(1)

    def roof(self):
        """Roof the house."""
        LOG.info("Roof the house for %s house.." % self.style)
        sleep(1)

    def furnish(self):
        """Furnish the house."""
        LOG.info("Furnish the house for %s house.." % self.style)
        sleep(1)

    def enjoy(self):
        """Enjoy the house."""
        LOG.info("Enjoy your new %s house :)" % self.style)
        sleep(1)

    def post_build_tasks(self):
        """Post build tasks after house is built."""
        LOG.info("Perform post building tasks for %s house.." % self.style)
        sleep(1)
