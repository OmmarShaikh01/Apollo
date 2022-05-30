import os
import shutil
from pathlib import PurePath

import pytest
from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from configs import settings

settings.setenv("QT_TESTING")
settings.validators.validate()

from apollo.utils import get_logger
from apollo.assets.stylesheets import load_theme
from apollo.src.app import Apollo
from tests.testing_utils import get_qt_application

# SESSION STARTUP
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


def remove_local_config():
    path = PurePath(settings.project_root, 'configs', 'qt_testing_settings.local.toml')
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def get_apollo(qtbot) -> tuple[Apollo, QtBot]:
    APOLLO = Apollo()
    APOLLO.setScreen(QtWidgets.QApplication.screens()[0])
    APOLLO.showFullScreen()
    load_theme(get_qt_application(), settings.loaded_theme, recompile = settings.recompile_theme)
    return APOLLO, qtbot


@pytest.fixture(scope = 'session', autouse = True)
def create_session():
    create_temp_dir()
    yield None
    remove_temp_dir()
    remove_local_config()
    LOGGER.info(f"CONFIG {settings.to_dict()}")
    LOGGER.info(f"Application Exited with Error code: {get_qt_application().exit()}")  # END REGION
