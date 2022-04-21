import configparser
import os
import shutil
import sys
import threading
import time
import traceback
from typing import (Callable)

import qt_material

ROOT = os.path.dirname(__file__)


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
            print(method, round(time.time() - t1, 8))
        except Exception as e:
            print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
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
        print(msg, round(time.time() - t1, 8))
    except Exception as e:
        print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
        raise e


def default_config() -> configparser.ConfigParser:
    """
    Holds the factory configuration of the application that can be written and fetched at any time.

    Returns:
        a config parser that holds the application configuration.
    """
    config = configparser.ConfigParser()
    if not os.path.isfile(os.path.join(ROOT, '.ini')):
        with open(os.path.join(ROOT, '.ini'), 'w') as file:
            config["DEFAULT"] = dict(
                    database_location = os.path.join(ROOT, 'db', 'default.db'),
                    current_theme = 'dark_teal.xml',
                    loaded_playlist = '',
                    playlists = list()
            )
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
    config.read(os.path.join(ROOT, '.ini'))
    return config


def write_config(config: configparser.ConfigParser):
    """
    Writes the loaded config to a file

    Args:
        config (configparser.ConfigParser): config parser that holds config to be written
    """
    with open(os.path.join(ROOT, '.ini'), 'w') as file:
        config.write(file)


def threadit(method: Callable) -> Callable:
    """
    Decorator for executing callbacks inside a thread

    Args:
        method (Callable): Callback object to be used

    Returns:
        a wrapped function object that can be executed
    """
    def exe(*args, **kwargs) -> None:
        thread = threading.Thread(target = lambda: (method(*args, **kwargs)))
        thread.start()

    return exe


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
