"""
Misc utilities used by apollo
"""
import logging
import os
import sys
import threading
import time
import traceback
from typing import Callable

from PySide6 import QtCore, QtWidgets

from apollo.layout import Apollo_MainWindow_UI
from configs import settings as _CONFIG


_GLOBAL_LOGGER = None


def get_logger(name: str) -> logging.Logger:
    """
    returns a configured logger

    Args:
        name (str): name of the logger instance

    Returns:
        logging.Logger: return the logger instance
    """
    # pylint: disable=W0603
    global _GLOBAL_LOGGER

    if _GLOBAL_LOGGER is None:
        ROOT = _CONFIG.project_root
        if str(_CONFIG.LOGGER_LEVEL).upper() == "DEBUG":
            log_level = logging.DEBUG
        elif str(_CONFIG.LOGGER_LEVEL).upper() == "INFO":
            log_level = logging.INFO
        elif str(_CONFIG.LOGGER_LEVEL).upper() == "WARNING":
            log_level = logging.WARNING
        elif str(_CONFIG.LOGGER_LEVEL).upper() == "ERROR":
            log_level = logging.ERROR
        elif str(_CONFIG.LOGGER_LEVEL).upper() == "CRITICAL":
            log_level = logging.CRITICAL
        else:
            log_level = logging.INFO

        logger = logging.getLogger(name)
        env = str(_CONFIG.current_env).upper()

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
            # pylint: disable=C0301
            formatter = logging.Formatter(
                f"[{env}] [%(levelname)8s]:: [%(module)s/%(funcName)s (Line %(lineno)d)]: %(message)s"
            )
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        logger.setLevel(log_level)
        _GLOBAL_LOGGER = logger

    return _GLOBAL_LOGGER


def timeit(method: Callable) -> Callable:
    """
    Decorator for executing callbacks inside a timed context that is printed to stdout

    Args:
        method (Callable): Callback object to be used

    Returns:
        a wrapped function object that can be executed
    """
    _LOGGER = get_logger(__name__)

    def exe(*args, **kwargs):
        """inner function"""
        try:
            t1 = time.time()
            result = method(*args, **kwargs)
            # pylint: disable=W1203
            _LOGGER.debug(f"{method} Executed in {round(time.time() - t1, 8)}s")
            return result
        except Exception as e:
            _LOGGER.error("".join((e, "\n", traceback.print_tb(sys.exc_info()[-1]))))
            raise e

    return exe


def exec_line(msg: str, method: Callable):
    """
    Decorator for executing callbacks inside a timed context that is printed to stdout

    Args:
        msg (str): Message to print to stdout
        method (Callable): Callback object to be used
    """
    _LOGGER = get_logger(__name__)
    try:
        t1 = time.time()
        method()
        # pylint: disable=W1203
        _LOGGER.debug(f"Message: {msg}> Time: {round(time.time() - t1, 8)}")
    except Exception as e:
        _LOGGER.error("".join((e, "\n", traceback.print_tb(sys.exc_info()[-1]))))
        raise e


def threadit(method: Callable) -> Callable:
    """
    Decorator for executing callbacks inside a thread

    Args:
        method (Callable): Callback object to be used

    Returns:
        a wrapped function object that can be executed
    """
    _LOGGER = get_logger(__name__)

    def exe(*args, **kwargs) -> None:
        """inner function"""
        thread = threading.Thread(
            target=lambda: (  # pylint: disable=W1203
                _LOGGER.debug(f"Thread {thread.native_id}: {method}"),
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


def set_dark_title_bar(window: QtWidgets.QWidget):
    """
    Sets the windows title bar to be black

    Args:
        window (QtWidgets.QWidge): Window to set title bar dark for
    """
    if _CONFIG["APOLLO.MAIN.IS_TITLEBAR_DARK"]:
        import ctypes

        HWND = window.winId()
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            HWND, 20, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2))
        )


class Apollo_Global_Signals(QtCore.QObject):
    """
    Global Signal Handler
    """

    PlayTrackSignal = QtCore.Signal(str)
    BeginPlayTrackSignal = QtCore.Signal(str)


class ApolloSignal:
    """Non Qt Signal for attaching slots"""

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

    _LOGGER = get_logger(__name__)

    def __init__(self, msg: str) -> None:
        # warnings.warn(msg)
        self._LOGGER.warning(msg)


# TypeAlias ---------------------------------------------------------------------------------------
class Apollo_Generic_View:
    """
    Base call For all Views
    """

    SIGNALS = Apollo_Global_Signals()

    def setup_conections(self):
        """
        Sets up all the connection for the UI
        """
        raise NotImplementedError

    def setup_defaults(self):
        """
        Sets up default states for all UI Widgets and objects
        """
        raise NotImplementedError

    def save_states(self):
        """
        Saves current states for all UI Widgets and objects
        """
        raise NotImplementedError


class Apollo_Main_TypeAlias:
    """TypeAlias"""

    UI: Apollo_MainWindow_UI
    SIGNALS: Apollo_Global_Signals
