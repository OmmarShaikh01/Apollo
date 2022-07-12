import os
import sys
from pathlib import PurePath

import nox
import tomli


SUPPORTED_PYTHON = ["3.9"]
SILENT = True
nox.options.pythons = SUPPORTED_PYTHON
nox.options.reuse_existing_virtualenvs = True


def _upgrade_basic(session: nox.Session, install_dev: bool = True):
    """
    upgrades the newly created venv with poetry lock dependencies

    Args:
        session (nox.Session): nox session
        install_dev (bool): flag to install dev dependencies
    """
    session.install("--upgrade", "pip", silent=SILENT)
    session.install("--upgrade", "setuptools", silent=SILENT)
    session.install("poetry", silent=SILENT)
    session.run_always("poetry", "shell", silent=SILENT)
    cmd = ["poetry", "install"]
    if not install_dev:
        cmd.append("--no-dev")
    session.run_always(*cmd, silent=SILENT)
    session.run_always("isort", ".", silent=SILENT)
    session.run_always("black", ".", silent=SILENT)


@nox.session(python=SUPPORTED_PYTHON)
def testing_pytest_unit(session: nox.Session, skip_setup: bool = False):
    """
    runs unit tests

    Args:
        session (nox.Session): nox session
        skip_setup (bool): flag to skip install dependencies
    """
    os.chdir(os.path.dirname(__file__))
    if not skip_setup:
        _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS="false", DYNACONF_PROFILE_RUNS="true")
    test_directory = os.path.join(os.path.dirname(__file__), "tests", "pytest_apollo")
    session.run("pytest", "--no-header", "--show-capture=no", test_directory, env=envvars)


@nox.session(python=SUPPORTED_PYTHON)
def testing_pytest_qt(session: nox.Session, skip_setup: bool = False):
    """
    runs integration tests

    Args:
        session (nox.Session): nox session
        skip_setup (bool): flag to skip install dependencies
    """
    os.chdir(os.path.dirname(__file__))
    if not skip_setup:
        _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS="false", DYNACONF_PROFILE_RUNS="true")
    test_directory = os.path.join(os.path.dirname(__file__), "tests", "pytest_qt_apollo")
    session.run("pytest", "--no-header", "--show-capture=no", test_directory, env=envvars)


@nox.session(python=SUPPORTED_PYTHON)
def testing_pytest_global(session: nox.Session):
    """
    runs unit and integrating testing in combination

    Args:
        session (nox.Session): nox session
    """
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS="false", DYNACONF_PROFILE_RUNS="false")
    CMD = [
        "pytest",
        "--show-capture",
        "no",
        "--no-header",
        "./tests/pytest_apollo",
        "./tests/pytest_qt_apollo",
    ]
    session.run(*CMD, env=envvars)


@nox.session(python=SUPPORTED_PYTHON)
def testing_coverage(session: nox.Session):
    """
    runs unit and integrating testing in combination win coverage on

    Args:
        session (nox.Session): nox session
    """
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS="false", DYNACONF_PROFILE_RUNS="false")
    CMD = [
        "pytest",
        "--no-header",
        "--show-capture",
        "no",
        "--cov",
        "./apollo",
        "--cov-config",
        ".coveragerc",
        "--cov-report",
        "html",
        "./tests/pytest_apollo",
        "./tests/pytest_qt_apollo",
    ]
    session.run(*CMD, env=envvars)


@nox.session(python=SUPPORTED_PYTHON)
def testing_benchmarked(session: nox.Session):
    """
    runs unit and integrating testing in combination with coverage and profiler on

    Args:
        session (nox.Session): nox session
    """
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS="true", DYNACONF_PROFILE_RUNS="true")
    CMD = [
        "pytest",
        "--show-capture",
        "no",
        "--no-header",
        "./tests/pytest_apollo",
        "./tests/pytest_qt_apollo",
    ]
    session.run(*CMD, env=envvars)


@nox.session(python=SUPPORTED_PYTHON)
def build_documentation_sphinx(session: nox.Session):
    """
    compiles and builds the sphinx documentation

    Args:
        session (nox.Session): nox session
    """
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    session.run(
        "sphinx-apidoc.exe",
        "-f",
        "-e",
        "-M",
        "-o",
        "./docs/source/_modules",
        "./apollo",
        silent=SILENT,
    )
    session.run("sphinx-build.exe", "-b", "html", "./docs/source", "./docs/build", silent=SILENT)


@nox.session(python=SUPPORTED_PYTHON)
def lint_apollo(session: nox.Session):
    """
    runs isort, black, pylint on the apollo

    Args:
        session (nox.Session): nox session
    """
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)
    for file in os.listdir(r".\apollo\layout"):
        file, ext = os.path.splitext(file)
        if ext == ".ui":
            CMD = [
                "pyside6-uic.exe",
                "-g",
                "python",
                "-o",
                f".\\apollo\\layout\\{file}.py",
                f".\\apollo\\layout\\{file}.ui",
            ]
            session.run(*CMD)

    session.run("isort", "--quiet", ".")
    session.run("black", "--quiet", ".")
    try:
        session.run("pylint", ".")
    finally:
        pass


@nox.session(python=SUPPORTED_PYTHON)
def production_build(session: nox.Session):
    """
    compiles and builds the complete application dist

    Args:
        session (nox.Session): nox session
    """
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)
    # Builds Apollo
    sys.path.insert(0, os.path.dirname(__file__))
    session.run(
        "python.exe",
        "-c",
        "from apollo.utils import compile_all; compile_all()",
        env=dict(ENV_FOR_DYNACONF="TESTING"),
    )
    sys.path.pop(0)
    session.run("poetry", "build", "-f", "sdist", silent=SILENT)


@nox.session(python=SUPPORTED_PYTHON)
def production_launch(session: nox.Session):
    """
    launches apollo build dist

    NOTE:
        requires a build apollo dist

    Args:
        session (nox.Session): nox session
    """
    os.chdir(os.path.dirname(__file__))
    toml = PurePath(os.path.dirname(__file__), "pyproject.toml")

    # Extracts Package
    path = os.path.join(os.path.dirname(__file__), "dist")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing {path}")

    os.chdir(path)
    file = os.listdir(path)

    if len(file) == 0:
        raise FileNotFoundError("Missing Build archive")

    file = file[0]
    pycmd = f"import tarfile; file = tarfile.open('{file}'); file.extractall('.'); file.close()"
    session.run(*["python", "-c", pycmd], silent=SILENT)
    os.chdir(file.replace(".tar.gz", ""))

    # Executes Apollo
    try:
        with open(toml, "rb") as file:
            parsed = tomli.load(file).get("tool").get("poetry").get("dependencies")
            del parsed["python"]
            packages = list(f"{k}{v}".replace("^", "==") for k, v in parsed.items())
        session.run("pip", "install", *packages, silent=SILENT)
        session.run("python", "-m", "apollo", silent=SILENT)
    finally:
        # Cleanup
        os.chdir(os.path.dirname(__file__))
        shutil.rmtree(os.path.join(os.path.dirname(__file__), "dist"))
