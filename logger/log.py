"""
FusionStudent logger. Record info, error, warn, debug logs and test log.
"""

import os
import util
from datetime import datetime


def current_time():
    """
    Get current time.
    :return: <str>
    """
    now_date = datetime.today()
    now = now_date.isoformat()[:-3] + " "
    return now


def get_path():
    """
    Get log file path.
    :return: String
    """
    path = util.root_path() + "/log"
    return path


def info(message):
    """
    Write message for info log.
    :param message: string
    :return: None
    """
    now = current_time()
    message = now + message + "\n"
    path = get_path() + "/info.log"

    if os.path.exists(path):
        open(path, "a").write(message)
    else:
        open(path, "w").write(message)
    return


def error(message):
    """
    Write message for error log.
    :param message: string
    :return: None
    """
    now = current_time()
    message = now + message + "\n"
    path = get_path() + "/error.log"

    if os.path.exists(path):
        open(path, "a").write(message)
    else:
        open(path, "w").write(message)
    return


def warn(message):
    """
    Write message for warn log.
    :param message: string
    :return: None
    """
    now = current_time()
    message = now + message + "\n"
    path = get_path() + "/warn.log"

    if os.path.exists(path):
        open(path, "a").write(message)
    else:
        open(path, "w").write(message)
    return


def debug(message):
    """
    Write message for debug log.
    :param message: string
    :return: None
    """
    now = current_time()
    message = now + message + "\n"
    path = get_path() + "/debug.log"

    if os.path.exists(path):
        open(path, "a").write(message)
    else:
        open(path, "w").write(message)
    return