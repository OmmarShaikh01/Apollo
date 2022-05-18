import os

import nox

SUPPORTED_PYTHON = ['3.9']
SILENT = True

nox.options.pythons = SUPPORTED_PYTHON
nox.options.reuse_existing_virtualenvs = True


def _upgrade_basic(session: nox.Session):
    session.install("--upgrade", "pip", silent = SILENT)
    session.install("--upgrade", "setuptools", silent = SILENT)
    session.install("poetry", silent = SILENT)
    session.run_always('poetry', 'shell', silent = SILENT)
    session.run_always('poetry', 'install', silent = SILENT)


@nox.session(python = SUPPORTED_PYTHON)
def testing_pytest(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS = 'false')
    session.run('pytest', '--rootdir', './tests/src', '-c', './pytest.ini', env = envvars, silent = SILENT)


@nox.session(python = SUPPORTED_PYTHON)
def testing_coverage(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS = 'false')
    session.run('pytest', '--cov', './apollo', '--rootdir', './tests/src', '--cov-config', '.coveragerc', '-c',
                'pytest.ini', '--cov-report', 'html', env = envvars, silent = SILENT)


@nox.session(python = SUPPORTED_PYTHON)
def testing_benchmarked(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    _upgrade_basic(session)

    envvars = dict(DYNACONF_BENCHMARK_FORMATS = 'true')
    session.run('pytest', '--rootdir', './tests/src', '-c', './pytest.ini', env = envvars, silent = SILENT)
