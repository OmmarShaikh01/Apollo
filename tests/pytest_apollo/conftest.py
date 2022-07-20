import cProfile
import os
import pstats
import shutil
import time
from pathlib import PurePath

import memory_profiler
import pytest
from _pytest.compat import is_async_function
from _pytest.python import async_warn_and_skip

from configs import settings


settings.setenv("TESTING")
settings.validators.validate_all(only_current_env=True)

from apollo.utils import get_logger
from tests.testing_utils import get_qt_application


# SESSION STARTUP
LOGGER = get_logger(__name__)
PROFILE = settings["PROFILE_RUNS"]  # disable profiling when debugging


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

        profile_root = PurePath(settings.project_root, "tests", ".profiles")
        if not os.path.exists(profile_root):
            os.mkdir(profile_root)

        with open((profile_root / f"{settings.current_env}.memprofile"), "a") as stream:
            stream.write(f"[{time.asctime(time.localtime())}] {mname}::{name}\n")
            memory_profiler.show_results(prof, stream=stream, precision=2)

        with open((profile_root / f"{settings.current_env}.profile"), "a") as stream:
            stream.write(f"[{time.asctime(time.localtime())}] {mname}::{name}\n")
            stats = pstats.Stats(cprof, stream=stream)
            stats.strip_dirs().sort_stats("tottime").print_stats()

    else:
        LOGGER.critical(f"TESTING> {mname}::{name}")
        val = testfunction(**testargs)

    if hasattr(val, "__await__") or hasattr(val, "__aiter__"):
        async_warn_and_skip(pyfuncitem.nodeid)
    return True


def create_temp_dir():
    path = settings.temp_dir
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def remove_temp_dir():
    path = settings.temp_dir
    if os.path.isdir(path):
        shutil.rmtree(path)


def clean_temp_dir():
    remove_temp_dir()
    create_temp_dir()


def remove_local_config():
    path = PurePath(settings.project_root, "configs", "testing_settings.local.toml")
    if os.path.exists(path):
        os.remove(path)


def copy_mock_data():
    src = PurePath((settings["mock_data"])) / "testing.db"
    dest = PurePath(settings["db_path"])
    shutil.copy(src, dest)


def clean_profile():
    profile_root = PurePath(settings.project_root, "tests", ".profiles")
    if os.path.exists(profile_root / f"{settings.current_env}.memprofile"):
        os.remove(profile_root / f"{settings.current_env}.memprofile")
    if os.path.exists(profile_root / f"{settings.current_env}.profile"):
        os.remove(profile_root / f"{settings.current_env}.profile")


@pytest.fixture(scope="package", autouse=True)
def create_session():
    settings.setenv("TESTING")
    settings.validators.validate_all()
    LOGGER.info(f"CONFIG {settings.current_env}: {settings.to_dict()}")

    clean_profile()
    create_temp_dir()

    yield None

    remove_temp_dir()
    remove_local_config()

    LOGGER.info(f"CONFIG {settings.current_env}: {settings.to_dict()}")
    LOGGER.info(f"Application Exited with Error code: {get_qt_application().exit()}")


# END REGION
