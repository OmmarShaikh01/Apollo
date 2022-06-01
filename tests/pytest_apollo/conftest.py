import cProfile
import os
import pstats
import shutil
from pathlib import PurePath

import pytest

from configs import settings
settings.setenv("TESTING")
settings.validators.validate(only_current_env = True)

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


def profile_stats(prof: cProfile.Profile):
    with open(os.path.join(os.path.dirname(__file__), '.profile'), 'w') as stats_file:
        stats = pstats.Stats(prof, stream = stats_file)
        stats.strip_dirs().sort_stats('tottime').print_stats()


@pytest.fixture(scope = 'package', autouse = True)
def create_session():
    settings.setenv("TESTING")
    settings.validators.validate()
    LOGGER.info(f"CONFIG {settings.current_env}: {settings.to_dict()}")

    create_temp_dir()
    prof = cProfile.Profile()
    prof.enable()
    yield None
    prof.disable()
    profile_stats(prof)

    remove_temp_dir()
    remove_local_config()
    LOGGER.info(f"CONFIG {settings.current_env}: {settings.to_dict()}")
    LOGGER.info(f"Application Exited with Error code: {get_qt_application().exit()}")
    LOGGER.info(f"Completed {os.path.dirname(__file__)}")
# END REGION
