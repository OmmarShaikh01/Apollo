"""
Misc utilities used by apollo
"""
import logging
import os
import sys
import threading
import time
import traceback
import warnings
from typing import Callable

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

    if _settings.LOGGER_LEVEL == "debug":
        log_level = logging.DEBUG
    elif _settings.LOGGER_LEVEL == "info":
        log_level = logging.INFO
    elif _settings.LOGGER_LEVEL == "warning":
        log_level = logging.WARNING
    elif _settings.LOGGER_LEVEL == "error":
        log_level = logging.ERROR
    elif _settings.LOGGER_LEVEL == "critical":
        log_level = logging.CRITICAL
    else:
        log_level = logging.INFO

    logger = logging.getLogger(name)
    env = str(_settings.current_env).upper()

    if env in ["TESTING", "PRODUCTION", "QT_TESTING"]:
        # pylint: disable=C0301
        formatter = logging.Formatter(
            f"[{env}] [%(asctime)s: %(levelname)8s]:: [%(module)s/%(funcName)s (Line %(lineno)d)]: %(message)s"
        )
        if not os.path.isdir(os.path.join(ROOT, "logs")):
            os.mkdir(os.path.join(ROOT, "logs"))
        log_path = os.path.join(ROOT, "logs", f"apollo_{env.lower()}.log")
        log_mode = "w"
        formatter.default_time_format = "%H:%M:%S"
        file_handler = logging.FileHandler(log_path, mode=log_mode)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if env in ["PRODUCTION"]:
        formatter = logging.Formatter(
            f"[{env}] [%(levelname)8s]:: [%(module)s/%(funcName)s (Line %(lineno)d)]: %(message)s"
        )
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
            # pylint: disable=W1203
            _LOGGER.debug(f"{method} Executed in {round(time.time() - t1, 8)}s")
            return result
        except Exception as e:
            print(e, "\n", traceback.print_tb(sys.exc_info()[-1]))
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
        # pylint: disable=W1203
        _LOGGER.debug(f"Message: {msg}> Time: {round(time.time() - t1, 8)}")
    except Exception as e:
        print(e, "\n", traceback.print_tb(sys.exc_info()[-1]))
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
            target=lambda: (
                # pylint: disable=W1203
                _LOGGER.info(f"Thread {thread.native_id}: {method}"),
                method(*args, **kwargs),
            )
        )
        thread.start()

    return exe


# pylint: disable=C0415
# pylint check ignored cause env need to be set locally inside function
def compile_all():
    """
    Compiles all stored themes into zip file
    """
    from apollo.assets import generate_resource
    from apollo.assets.stylesheets import ResourceGenerator

    for name in os.listdir(ResourceGenerator.THEMES):
        name, _ = os.path.splitext(name)
        _, name = os.path.split(name)
        generate_resource(str(name))


class ApolloSignal:
    """Signals for attaching slots"""

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


class ApolloWarning:
    """
    Warning classs used to raise warnings and log them at the same tinme
    """

    def __init__(self, msg: str) -> None:
        warnings.warn(UserWarning(msg))
        _LOGGER.warning(msg)
