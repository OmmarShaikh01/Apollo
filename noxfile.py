import os
import shutil
from pathlib import PurePath

import nox
import tomli

SUPPORTED_PYTHON = ['3.9']
SILENT = True
nox.options.pythons = SUPPORTED_PYTHON
nox.options.reuse_existing_virtualenvs = True


def _upgrade_basic(session: nox.Session, install_dev: bool = True):
    session.install("--upgrade", "pip", silent = SILENT)
    session.install("--upgrade", "setuptools", silent = SILENT)
    session.install("poetry", silent = SILENT)
    session.run_always('poetry', 'shell', silent = SILENT)
    cmd = ['poetry', 'install']
    if not install_dev:
        cmd.append('--no-dev')
    session.run_always(*cmd, silent = SILENT)


@nox.session(python = SUPPORTED_PYTHON)
def testing_pytest(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS = 'false')
    for test_directory in ['pytest_apollo', 'pytest_qt_apollo']:
        test_directory = os.path.join(os.path.dirname(__file__), 'tests', test_directory)
        session.run('pytest', '--show-capture=no', '-c', './pytest.ini', test_directory, env = envvars)


@nox.session(python = SUPPORTED_PYTHON)
def testing_benchmarked(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS = 'true')
    for test_directory in ['pytest_apollo', 'pytest_qt_apollo']:
        test_directory = os.path.join(os.path.dirname(__file__), 'tests', test_directory)
        session.run('pytest', '-r', 'fE', '--show-capture', 'no', '-c', './pytest.ini', test_directory, env = envvars)


@nox.session(python = SUPPORTED_PYTHON)
def testing_coverage(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS = 'false')
    for test_directory in ['pytest_apollo', 'pytest_qt_apollo']:
        test_directory = os.path.join(os.path.dirname(__file__), 'tests', test_directory)
        CMD = ['pytest', '--show-capture', 'no', '--cov', './apollo', '--cov-config',
               '.coveragerc', '-c', 'pytest.ini', '--cov-report', 'html'
        ]
        session.run(*CMD, test_directory, env = envvars)


@nox.session(python = SUPPORTED_PYTHON)
def build_documentation_sphinx(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)
    # session.run('sphinx-autogen.exe', '-o', './docs/source/_autosummary', './docs/source/index.rst', silent = SILENT)
    session.run('sphinx-apidoc.exe', '-f', '-e', '-M', '-o', './docs/source/_modules', './apollo', silent = SILENT)
    session.run('sphinx-build.exe', '-b', 'html', './docs/source', './docs/build', silent = SILENT)


@nox.session(python = SUPPORTED_PYTHON)
def production_build(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)
    # Builds Apollo
    session.run('poetry', 'build', '-f', 'sdist', silent = SILENT)


@nox.session(python = SUPPORTED_PYTHON)
def production_launch(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    toml = PurePath(os.path.dirname(__file__), 'pyproject.toml')

    # Extracts Package
    file = os.listdir("./dist")[0]
    os.chdir('./dist')
    pycmd = f"import tarfile; file = tarfile.open('{file}'); file.extractall('.'); file.close()"
    session.run(*['python', '-c', pycmd], silent = SILENT)
    os.chdir(file.replace('.tar.gz', ''))

    # Executes Apollo
    try:
        with open(toml, 'rb') as file:
            parsed = tomli.load(file).get('tool').get('poetry').get('dependencies')
            del parsed['python']
            packages = list(f'{k}{v}'.replace('^', '==') for k, v in parsed.items())
        session.run('pip', 'install', *packages, silent = SILENT)

        session.run(*['python', '-m', 'apollo'], silent = SILENT)
    finally:
        # Cleanup
        os.chdir(os.path.dirname(__file__))
        shutil.rmtree('./dist')


# custom sessions for githu workflows
@nox.session(python = SUPPORTED_PYTHON)
def unit_testing_apollo(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS = 'true')
    for test_directory in ['pytest_apollo']:
        test_directory = os.path.join(os.path.dirname(__file__), 'tests', test_directory)
    session.run('pytest', '--show-capture=no', '-c', './pytest.ini', test_directory, env = envvars)


@nox.session(python = SUPPORTED_PYTHON)
def production_testing_apollo(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS = 'true')
    for test_directory in ['pytest_qt_apollo']:
        test_directory = os.path.join(os.path.dirname(__file__), 'tests', test_directory)
        session.run('pytest', '--show-capture=no', '-c', './pytest.ini', test_directory, env = envvars)
