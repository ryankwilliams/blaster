"""Compatibility module.

Focused on support both Python 2 and Python 3.
"""

try:
    # Python 3
    import queue
except ImportError:
    # Python 2
    import Queue as queue
