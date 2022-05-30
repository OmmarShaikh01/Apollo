import os
import shutil
from pathlib import PurePath

import pytest

from configs import settings
settings.setenv("TESTING")
settings.validators.validate()

from apollo.utils import get_logger
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
    if os.path.isdir(path):
        os.remove(path)


@pytest.fixture(scope = 'session', autouse = True)
def create_session():
    create_temp_dir()
    yield None
    remove_temp_dir()
    remove_local_config()
    LOGGER.info(f"CONFIG {settings.to_dict()}")
    LOGGER.info(f"Application Exited with Error code: {get_qt_application().exit()}")
# END REGION
