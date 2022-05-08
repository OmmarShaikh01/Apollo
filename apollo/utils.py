import configparser
import logging
import os
import shutil
import sys
import threading
import time
import traceback
from typing import (Callable)

import qt_material

from configs import settings as _settings


ROOT = _settings.project_root


def get_logger(name: str) -> logging.Logger:
    """
    returns a configured logger

    Args:
        name (str): name of the logger instance
        level (int): logging level

    Returns:
        logging.Logger: return the logger instance
    """
    logger = logging.getLogger(name)
    log_level = logging.INFO
    env = str(_settings.current_env).upper()
    if env in ['TESTING', 'PRODUCTION']:
        if env == 'TESTING':
            log_path = os.path.join(ROOT, 'apollo_test.log')
            log_mode = "w"
            log_level = logging.DEBUG
        else:
            log_path = os.path.join(ROOT, 'apollo_prod.log')
            log_mode = "a"
            log_level = logging.INFO

        formatter = logging.Formatter('%(asctime)s: %(levelname)s:: %(name)-12s: %(funcName)s: %(message)s')
        file_handler = logging.FileHandler(log_path, mode = log_mode)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if env in ['PRODUCTION']:
        formatter = logging.Formatter('%(levelname)s:: %(name)-12s: %(funcName)s: %(message)s')
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    logger.setLevel(log_level)
    return logger


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
            method(*args, **kwargs)
            _LOGGER.info(f"Method: {method}> Time: {round(time.time() - t1, 8)}")
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
        _LOGGER.info(f"Message: {msg}> Time: {round(time.time() - t1, 8)}")
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
        thread = threading.Thread(target = lambda: (
            _LOGGER.info(f"Thread {thread.native_id}: {method}"),
            method(*args, **kwargs)
        ))
        thread.start()

    return exe


def default_config() -> configparser.ConfigParser:
    """
    Holds the factory configuration of the application that can be written and fetched at any time.

    Returns:
        a config parser that holds the application configuration.
    """
    config = configparser.ConfigParser()
    path = os.path.join(ROOT, 'apollo.ini')
    if not os.path.isfile(path):
        with open(path, 'w') as file:
            config["GLOBALS"] = dict(
                    database_location = os.path.join(ROOT, 'db', 'default.db'),
                    current_theme = 'dark_teal.xml',
                    loaded_playlist = ''
            )
            config["PLAYLISTS"] = dict()
            config["WATCHER/FILES"] = dict()
            config["WATCHER/MONITOR"] = dict()
            config["APPLICATION/MAIN"] = dict()
            config["APPLICATION/LIBRARY"] = dict()
            config["APPLICATION/QUEUE"] = dict()
            config["APPLICATION/PLAYLIST"] = dict()
            config["APPLICATION/PLAYBAR"] = dict()
            config.write(file)
    return config


def get_configparser() -> configparser.ConfigParser:
    """
    Initializes a config parser that holds the application configuration.

    Returns:
        a config parser that holds the application configuration.
    """
    default_config()
    config = configparser.ConfigParser()
    config.read(os.path.join(ROOT, 'apollo.ini'))
    return config


def write_config(config: configparser.ConfigParser):
    """
    Writes the loaded config to a file

    Args:
        config (configparser.ConfigParser): config parser that holds config to be written
    """
    with open(os.path.join(ROOT, 'apollo.ini'), 'w') as file:
        config.write(file)


# noinspection PyPep8Naming
def add_to_config(key: str, value: str, config: configparser.ConfigParser, hasDupes: bool = False):
    """
    appends an item to a config dict

    Args:
        key (str): top level key of the dict
        value (str): value of the dict
        config (configparser.ConfigParser): config to edit
        hasDupes (bool): adds duplicates of true

    Returns:
        config (configparser.ConfigParser): edited config
    """
    temp_config = {}
    index_key = 0
    field = config[key].values()
    if 0 < len(field):
        for index_key, prev_value in enumerate(field):
            temp_config['/'.join((key, str(index_key)))] = prev_value
            index_key += 1

    if not hasDupes:
        if value not in field:
            temp_config['/'.join((key, str(index_key)))] = value
    else:
        temp_config['/'.join((key, str(index_key)))] = value

    config[key] = temp_config
    return config


class ResourceGenerator(qt_material.ResourseGenerator):

    # noinspection PyMissingConstructor
    def __init__(self, root: str, primary: str, secondary: str, disabled: str, source: str, parent: str = 'theme'):
        """
        Constructor

        Args:
            root(str): resource root folder
            primary(str): primary colour value
            secondary(str): secondary colour value
            disabled(str): disabled colour value
            source(str): source svg directory
            parent(str, optional): parent directory name
        """
        self.index = os.path.join(root, parent)

        self.contex = [
            (os.path.join(self.index, 'disabled'), disabled),
            (os.path.join(self.index, 'primary'), primary),
        ]

        self.source = source
        self.secondary = secondary

        for folder, _ in self.contex:
            shutil.rmtree(folder, ignore_errors = True)
            os.makedirs(folder, exist_ok = True)


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
