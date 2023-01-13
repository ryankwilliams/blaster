"""Build various types of homes.

This module contains a class which has methods for building different aspects
to a house.
"""
from logging import getLogger
from logging import Logger
from time import sleep
from typing import Any
from typing import Dict


LOG: Logger = getLogger("blaster")


class House:
    """Build a house."""

    def __init__(self, style: str, **kwargs: Dict[str, Any]) -> None:
        """Constructor.

        :param style: style of the house to build
        """
        self.style: str = style

    def foundation(self) -> None:
        """Build the foundation."""
        LOG.info(f"Building the foundation for {self.style} house..")
        sleep(1)

    def frame(self) -> None:
        """Frame the house."""
        LOG.info(f"Frame the house for {self.style} house..")
        sleep(1)

    def roof(self) -> None:
        """Roof the house."""
        LOG.info(f"Roof the house for {self.style} house..")
        sleep(1)

    def furnish(self) -> None:
        """Furnish the house."""
        LOG.info(f"Furnish the house for {self.style} house..")
        sleep(1)

    def enjoy(self) -> None:
        """Enjoy the house."""
        LOG.info(f"Enjoy your new {self.style} house :)")
        sleep(1)

    def post_build_tasks(self) -> None:
        """Post build tasks after house is built."""
        LOG.info(f"Perform post building tasks for {self.style} house..")
        sleep(1)
