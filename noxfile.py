import os

import nox

SUPPORTED_PYTHON = ['3.9']

nox.options.pythons = SUPPORTED_PYTHON
nox.options.reuse_existing_virtualenvs = True


def _upgrade_basic(session: nox.Session):
    session.install("--upgrade", "pip", silent = 0)
    session.install("--upgrade", "setuptools", silent = 0)
    session.install("poetry", silent = 0)


@nox.session(python = SUPPORTED_PYTHON)
def testing_pytest(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    os.environ["DYNACONF_BENCHMARK_FORMATS"] = 'false'
    _upgrade_basic(session)
    session.run('poetry', 'shell')
    session.run('poetry', 'install')
    session.run('pytest', '--rootdir', './tests/src', '-c', './pytest.ini')


@nox.session(python = SUPPORTED_PYTHON)
def testing_coverage(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    os.environ["DYNACONF_BENCHMARK_FORMATS"] = 'false'
    _upgrade_basic(session)
    session.run('poetry', 'shell')
    session.run('poetry', 'install')


@nox.session(python = SUPPORTED_PYTHON)
def testing_benchmarked(session: nox.Session):
    os.chdir(os.path.dirname(__file__))
    os.environ["DYNACONF_BENCHMARK_FORMATS"] = 'true'
    _upgrade_basic(session)
    session.run('poetry', 'shell')
    session.run('poetry', 'install')
    session.run('pytest', '--rootdir', './tests/src', '-c', './pytest.ini')
