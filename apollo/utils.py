import logging
import os
import sys
import threading
import time
import traceback
from typing import (Callable)

from configs import settings as _settings

ROOT = _settings.project_root
_LOGGER = None


def get_logger(name: str) -> logging.Logger:
    """
    returns a configured logger

    Args:
        name (str): name of the logger instance
        level (int): logging level

    Returns:
        logging.Logger: return the logger instance
    """
    if _LOGGER is not None:
        return _LOGGER

    logger = logging.getLogger(name)
    log_level = logging.INFO
    env = str(_settings.current_env).upper()
    if env in ['TESTING', 'PRODUCTION']:
        formatter = logging.Formatter(
            '%(asctime)s: %(levelname)8s:: [%(module)s/%(funcName)s (Line %(lineno)d)]: %(message)s'
        )

        if env == 'TESTING':
            log_path = os.path.join(ROOT, 'apollo_test.log')
            log_mode = "w"
            log_level = logging.DEBUG
            formatter.default_time_format = '%H:%M:%S'
        else:
            log_path = os.path.join(ROOT, 'apollo_prod.log')
            log_mode = "a"
            log_level = logging.INFO

        file_handler = logging.FileHandler(log_path, mode = log_mode)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if env in ['PRODUCTION']:
        formatter = logging.Formatter('%(levelname)8s:: [%(module)s/%(funcName)s (Line %(lineno)d)]: %(message)s')
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    logger.setLevel(log_level)
    return logger


# noinspection PyRedeclaration
_LOGGER = get_logger(__name__)


def timeit(method: Callable) -> Callable:
    """
    Decorator for executing callbacks inside a timed context that is printed to stdout

    Args:
        method (Callable): Callback object to be used

    Returns:
        a wrapped function object that can be executed
    """

    def exe(*args, **kwargs):
        try:
            t1 = time.time()
            result = method(*args, **kwargs)
            _LOGGER.debug(f"{method} Executed in {round(time.time() - t1, 8)}s")
            return result
        except Exception as e:
            print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
            _LOGGER.error(e)
            raise e

    return exe


def exec_line(msg: str, method: Callable):
    """
    Decorator for executing callbacks inside a timed context that is printed to stdout

    Args:
        msg (str): Message to print to stdout
        method (Callable): Callback object to be used
    """
    try:
        t1 = time.time()
        method()
        _LOGGER.debug(f"Message: {msg}> Time: {round(time.time() - t1, 8)}")
    except Exception as e:
        print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
        _LOGGER.error(e)
        raise e


def threadit(method: Callable) -> Callable:
    """
    Decorator for executing callbacks inside a thread

    Args:
        method (Callable): Callback object to be used

    Returns:
        a wrapped function object that can be executed
    """

    def exe(*args, **kwargs) -> None:
        thread = threading.Thread(
                target = lambda: (_LOGGER.info(f"Thread {thread.native_id}: {method}"), method(*args, **kwargs)))
        thread.start()

    return exe


class ApolloSignal:
    """ Signals for attaching slots"""

    def __init__(self):
        """constructor"""
        self.connected_callback = None

    def connect(self, callback: Callable):
        """
        Connector to add a callback to the instance

        Args:
            callback: callback attached to the instance
        """
        self.connected_callback = callback

    def disconnect(self):
        """
        Removes the callback attached to the instance
        """
        self.connected_callback = None

    def emit(self, *args, **kwargs):
        """
        Emits the signals and executed the attached callback

        Args:
            *args: misc args
            **kwargs: misc kwargs
        """
        if self.connected_callback is not None:
            self.connected_callback(*args, **kwargs)
