from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

LOG_LEVELS = {
    'debug': DEBUG,
    'info': INFO,
    'warning': WARNING,
    'error': ERROR,
    'critical': CRITICAL
}

LOG_FORMAT = (
    "%(asctime)s %(levelname)s "
    "[%(name)s.%(funcName)s:%(lineno)d] %(message)s"
)

REQ_TASK_KEYS = [
    'name',
    'task',
    'methods'
]
