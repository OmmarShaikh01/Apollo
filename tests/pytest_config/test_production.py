from pytest_config.conftest import write_config

from configs import settings


def test_settings():
    settings.setenv("PRODUCTION")
    settings.validators.validate(only_current_env=True)
    write_config(settings)