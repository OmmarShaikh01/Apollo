import os
import shutil

import pytest

from apollo.utils import get_logger
from configs import settings

from tests.testing_utils import get_qt_application
# SESSION STARTUP

settings.setenv("TESTING")
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


@pytest.fixture(scope = 'session', autouse = True)
def create_session():
    create_temp_dir()
    yield None
    remove_temp_dir()
    LOGGER.info(f"CONFIG {settings.to_dict()}")
    LOGGER.info(f"Application Exited with Error code: {get_qt_application().exit()}")
# END REGION
