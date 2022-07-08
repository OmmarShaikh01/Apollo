import cProfile
import os
import pstats
import shutil
import time
from pathlib import PurePath

import memory_profiler
import pytest
from PySide6 import QtCore, QtWidgets
from _pytest.compat import is_async_function
from _pytest.python import async_warn_and_skip
from pytestqt.qtbot import QtBot

from configs import settings

settings.setenv("QT_TESTING")
settings.validators.validate(only_current_env=True)

from apollo.src.app import Apollo
from apollo.utils import get_logger
from apollo.assets.stylesheets import load_theme
from tests.testing_utils import get_qt_application

# SESSION STARTUP
# To test UI:
# 1. check if the states are loaded
# 2. events are connected and triggered with appropriate values
# 3. UI interactions are valid
# 4. states are saved appropriately

LOGGER = get_logger(__name__)
PROFILE = settings["PROFILE_RUNS"]  # disable profiling when debugging


@pytest.fixture
def get_apollo_application(qtbot) -> tuple[Apollo, QtBot]:
    APOLLO = Apollo()
    APOLLO.setScreen(QtWidgets.QApplication.screens()[0])
    APOLLO.move(QtCore.QPoint(0, 0))
    APOLLO.showFullScreen()
    return APOLLO, qtbot


def copy_mock_data():
    src = PurePath((settings["mock_data"])) / "testing.db"
    dest = PurePath(settings["db_path"])
    shutil.copy(src, dest)


def create_temp_dir():
    path = settings.temp_dir
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    LOGGER.info(f"Created {path}")


def clean_temp_dir():
    remove_temp_dir()
    create_temp_dir()


def remove_temp_dir():
    path = settings.temp_dir
    if os.path.isdir(path):
        shutil.rmtree(path)
        LOGGER.info(f"Deleted {path}")


def remove_local_config():
    path = PurePath(settings.project_root, "configs", "qt_testing_settings.local.toml")
    if os.path.exists(path):
        os.remove(path)


def pytest_pyfunc_call(pyfuncitem: pytest.Function):
    pyfuncitem.__name__ = pyfuncitem.name
    testfunction = pyfuncitem.obj

    if is_async_function(testfunction):
        async_warn_and_skip(pyfuncitem.nodeid)

    funcargs = pyfuncitem.funcargs
    testargs = {arg: funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames}
    name = testfunction.__qualname__
    mname = testfunction.__module__

    if PROFILE:
        prof = memory_profiler.LineProfiler(backend="psutil")
        cprof = cProfile.Profile(subcalls=True, builtins=False)
        cprof.enable()
        LOGGER.critical(f"TESTING> {mname}::{name}")
        val = prof(testfunction)(**testargs)
        cprof.disable()

        path = PurePath(
            settings.project_root, "tests", ".profiles", f"{settings.current_env}.memprofile"
        )
        with open(path, "a") as stream:
            stream.write(f"[{time.asctime(time.localtime())}] {mname}::{name}\n")
            memory_profiler.show_results(prof, stream=stream, precision=2)

        path = PurePath(
            settings.project_root, "tests", ".profiles", f"{settings.current_env}.profile"
        )
        with open(path, "a") as stream:
            stream.write(f"[{time.asctime(time.localtime())}] {mname}::{name}\n")
            stats = pstats.Stats(cprof, stream=stream)
            stats.strip_dirs().sort_stats("tottime").print_stats()

    else:
        LOGGER.critical(f"TESTING> {mname}::{name}")
        val = testfunction(**testargs)

    if hasattr(val, "__await__") or hasattr(val, "__aiter__"):
        async_warn_and_skip(pyfuncitem.nodeid)
    return True


def clean_output():
    path = os.path.join(os.path.dirname(__file__), "output")
    if os.path.exists(path):
        shutil.rmtree(path)


@pytest.fixture(scope="package", autouse=True)
def create_session():
    settings.setenv("QT_TESTING")
    settings.validators.validate()
    LOGGER.info(f"CONFIG {settings.current_env}: {settings.to_dict()}")

    clean_output()
    create_temp_dir()
    load_theme(get_qt_application(), settings.loaded_theme, recompile=settings.recompile_theme)

    yield None

    remove_temp_dir()
    remove_local_config()

    LOGGER.info(f"CONFIG {settings.current_env}: {settings.to_dict()}")
    LOGGER.info(f"Application Exited with Error code: {get_qt_application().exit()}")
    LOGGER.info(f"Completed {os.path.dirname(__file__)}")


# END REGION
