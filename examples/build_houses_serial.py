"""This example demonstrates how contractors can build homes in a new
development in sequential.
"""
from pprint import pprint
from time import sleep

from blaster import Blaster
from examples.house import House

if __name__ == "__main__":
    # list of tasks (houses to be built)
    tasks = [
        {
            "name": "House 1",
            "task": House,
            "methods": ["foundation", "frame", "roof", "furnish", "enjoy"],
            "style": "contemporary",
        },
        {
            "name": "House 2",
            "task": House,
            "methods": [
                "foundation",
                "frame",
                "roof",
                "furnish",
                "post_build_tasks",
                "enjoy",
            ],
            "style": "cape",
        },
        {
            "name": "House 3",
            "task": House,
            "methods": [
                "foundation",
                "frame",
                "roof",
                "furnish",
                "post_build_tasks",
                "enjoy",
            ],
            "style": "colonial",
        },
        {
            "name": "House 4",
            "task": House,
            "methods": [
                "foundation",
                "frame",
                "roof",
                "furnish",
                "post_build_tasks",
                "enjoy",
            ],
            "style": "ranch",
        },
        {
            "name": "House 5",
            "task": House,
            "methods": [
                "foundation",
                "frame",
                "roof",
                "furnish",
                "post_build_tasks",
                "enjoy",
            ],
            "style": "split",
        },
    ]

    # create blaster object
    blast = Blaster(tasks)

    # blast off tasks in sequential
    data = blast.blastoff(serial=True)

    # log results
    sleep(2)
    pprint(data, indent=4)
