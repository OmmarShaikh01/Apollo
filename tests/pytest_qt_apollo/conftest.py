import cProfile
import os
import pstats
import shutil
from pathlib import PurePath

import pytest

from configs import settings

settings.setenv("QT_TESTING")
settings.validators.validate(only_current_env = True)

from apollo.utils import get_logger
from apollo.assets.stylesheets import load_theme
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


def profile_stats(prof: cProfile.Profile):
    path = PurePath(settings.project_root, 'tests', '.profiles', f'{settings.current_env}.profile')
    with open(path, 'w') as stats_file:
        stats = pstats.Stats(prof, stream = stats_file)
        stats.strip_dirs().sort_stats('tottime').print_stats()

def clean_output():
    path = os.path.join(os.path.dirname(__file__), 'output')
    if os.path.exists(path):
        shutil.rmtree(path)


@pytest.fixture(scope = 'package', autouse = True)
def create_session():
    settings.setenv("QT_TESTING")
    settings.validators.validate()
    LOGGER.info(f"CONFIG {settings.current_env}: {settings.to_dict()}")
    clean_output()
    create_temp_dir()
    load_theme(get_qt_application(), settings.loaded_theme, recompile = settings.recompile_theme)
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
