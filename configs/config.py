import os

from dynaconf import Dynaconf
from dynaconf.loaders.toml_loader import write

from configs.validate import validate

DEFAULT_SETTINGS = os.path.join(os.path.dirname(__file__), 'default_settings.toml')
DEFAULT_TESTING_SETTINGS = os.path.join(os.path.dirname(__file__), 'default_testing_settings.toml')
DEFAULT_QT_TESTING_SETTINGS = os.path.join(os.path.dirname(__file__), 'default_qt_testing_settings.toml')
SETTINGS = os.path.join(os.path.dirname(__file__), 'settings.toml')
TESTING_SETTINGS = os.path.join(os.path.dirname(__file__), 'testing_settings.toml')
QT_TESTING_SETTINGS = os.path.join(os.path.dirname(__file__), 'qt_testing_settings.toml')

settings = Dynaconf(
    load_dotenv = True,
    project_root = os.path.dirname(os.path.dirname(__file__)),
    settings_files = [
        DEFAULT_SETTINGS,
        DEFAULT_TESTING_SETTINGS,
        DEFAULT_QT_TESTING_SETTINGS,
        SETTINGS,
        TESTING_SETTINGS,
        QT_TESTING_SETTINGS,
    ],
    envvar_prefix = "DYNACONF",
    environments = True,
    env_switcher = "ENV_FOR_DYNACONF",
    validate_only_current_env = True,
)
validate(settings)
# END REGION


def write_config():
    """
    Writes the Settings to a file
    """
    # noinspection PyShadowingNames
    env: str = settings.current_env
    if env == "PRODUCTION":
        file = os.path.join(os.path.dirname(__file__), 'settings.local.toml')
    elif env == "QT_TESTING":
        file = os.path.join(os.path.dirname(__file__), 'qt_testing_settings.local.toml')
    else:
        file = os.path.join(os.path.dirname(__file__), 'testing_settings.local.toml')
    write(file, {env: settings.to_dict()}, merge = True)


if __name__ == '__main__':
    import json

    env = ('TESTING', 'QT_TESTING', 'PRODUCTION')
    for _env in env:
        settings.setenv(_env)
        settings.validators.validate()
        print()
        print(_env)
        print(json.dumps(settings.to_dict(), indent = 2))
