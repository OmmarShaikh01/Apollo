from configs import settings
from tests.pytest_config.conftest import write_config


def test_settings():
    settings.setenv("QT_TESTING")
    settings.validators.validate_all(only_current_env=True)
    write_config(settings)
