import configparser
import os
import sys
import time
import traceback
import shutil
from pathlib import Path

import qt_material

ROOT = os.path.dirname(__file__)


def timeit(method):
    def exec(*args, **kwargs):
        try:
            t1 = time.time()
            method(*args, **kwargs)
            print(method, round(time.time() - t1, 8))
        except Exception as e:
            print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
            raise e

    return exec


def execLine(msg, method):
    try:
        t1 = time.time()
        method()
        print(msg, round(time.time() - t1, 8))
    except Exception as e:
        print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
        raise e


def default_config():
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


def getConfigParser():
    default_config()
    config = configparser.ConfigParser()
    config.read(os.path.join(ROOT, '.ini'))
    return config


def writeConfig(config: configparser.ConfigParser):
    with open(os.path.join(ROOT, '.ini'), 'w') as file:
        config.write(file)


class ResourseGenerator(qt_material.ResourseGenerator):

    def __init__(self, root, primary, secondary, disabled, source, parent = 'theme'):
        """Constructor"""
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
