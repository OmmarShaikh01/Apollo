import os
import shutil

import pytest

from configs import settings
from apollo.utils import get_logger

# SESSION STARTUP
settings.setenv("testing")
settings.validators.validate()

LOGGER = get_logger(__name__)


@pytest.fixture(scope = 'session', autouse = True)
def create_temp_dir():
    path = os.path.join(os.path.dirname(__file__), 'tempdir')
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    LOGGER.info(f"Created {path}")
    yield None
    if os.path.isdir(path):
        shutil.rmtree(path)
        LOGGER.info(f"Deleted {path}")
# END REGION
