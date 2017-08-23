# Blaster

[![Build Status](https://travis-ci.org/rywillia/blaster.svg?branch=master)](https://travis-ci.org/rywillia/blaster)
[![Coverage Status](https://coveralls.io/repos/github/rywillia/blaster/badge.svg)](https://coveralls.io/github/rywillia/blaster)
[![PyPI version](https://img.shields.io/pypi/v/blaster.svg)](https://pypi.python.org/pypi/blaster)

Blaster is a library that provides the ability to blast off a list of tasks
and call each of their given methods concurrently. Blaster uses Python's
built-in multiprocessing library to run the list of tasks.

## Installation

Blaster can be easily installed with a one line command. It is available on
[pypi][1]. It is recommended (as best practice) to create a virtual
environment and install blaster. Please see the commands below to install
blaster.

```
# install python virtualenv
$ pip install python-virtualenv

# create virtualenv
$ virtualenv blaster

# activate virtualenv
$ source blaster/bin/activate

# install blaster
$ (blaster) pip install blaster
```

## Examples

At the root of blaster project, you will see a examples folder. Within this
folder you will find simple examples on how you can use blaster to
efficiently run many tasks.

## Output

When blaster calls its blastoff method, on completion. It will return back
to you a list of task results. Within each task dictionary it will have the
original task data passed in along with a couple new keys. A status key which
is an integer (0 or 1) to determine pass or fail. If a task failed, it would
have a traceback key with the exception raised for helpful troubleshooting.

## Terminology

### Task

A task is a python dictionary that defines the task to be blasted off. A task
must contain three keys **name**, **task** and **methods**. The name key
just tells blaster what the task name is. The task key is a Python class
reference. Finally the methods key is a list of methods to be run for the
given task. You can then define any other key:value pairs that will be passed
to the task given when an object is created for that class.

Below is an example task for building a contemporary house. You will see
the task key has a value of the House class which contains all the methods
defined. Blaster will create a house object (passing any extra data in this
case **style**) and then call the methods defined.

```python
[
    {
        'name': 'House #1',
        'task': House,
        'methods': [
            'foundation',
            'frame',
            'roof',
            'furnish',
            'enjoy'
        ],
        'style': 'contemporary'
    }
]
```

The nice feature with blaster is you can have multiple tasks but each one
can call various methods within that task class. They do not all need to call
the same methods! See the example below:

```python
[
    {
        'name': 'House #1',
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
        'name': 'House #2',
        'task': House,
        'methods': [
            'foundation',
            'frame',
            'roof'
        ],
        'style': 'cape'
    }
]
```

## Issues

For any issues that you may find while using blaster library. Please open a
new issue or you can open pull request.

[1]: https://pypi.python.org/pypi/blaster