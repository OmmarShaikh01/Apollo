import os
import shutil
from typing import Union

import pytest
from pytestqt.qtbot import QtBot

from apollo.utils import get_logger
from assets.stylesheets import load_theme
from configs import settings
from apollo.src.app import Apollo

from tests.testing_utils import get_qt_application

# SESSION STARTUP

settings.setenv("QT_TESTING")
settings.validators.validate()

LOGGER = get_logger(__name__)


def create_temp_dir():
    path = settings.temp_dir
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    LOGGER.info(f"Created {path}")


def remove_temp_dir():
    path = settings.temp_dir
    if os.path.isdir(path):
        shutil.rmtree(path)
        LOGGER.info(f"Deleted {path}")


# Apollo Singleton
_APOLLO: Union[Apollo, None] = None


@pytest.fixture
def get_apollo(qtbot) -> (Apollo, QtBot):
    global _APOLLO
    if _APOLLO is None:
        _APOLLO = Apollo()
        load_theme(get_qt_application(), settings.loaded_theme, recompile = settings.recompile_theme)
    return _APOLLO, qtbot


@pytest.fixture(scope = 'session', autouse = True)
def create_session():
    create_temp_dir()
    yield None
    remove_temp_dir()
    LOGGER.info(f"CONFIG {settings.to_dict()}")
    LOGGER.info(f"Application Exited with Error code: {get_qt_application().exit()}")  # END REGION
