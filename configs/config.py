import os

from dynaconf import Dynaconf
from dynaconf.loaders.toml_loader import write

from configs.validate import validate


ROOT = os.path.dirname(__file__)
settings = Dynaconf(
    load_dotenv=False,
    project_root=os.path.dirname(ROOT),
    settings_files=[
        os.path.join(ROOT, "default_settings.toml"),
        os.path.join(ROOT, "default_testing_settings.toml"),
        os.path.join(ROOT, "default_qt_testing_settings.toml"),
        os.path.join(ROOT, "settings.toml"),
        os.path.join(ROOT, "testing_settings.toml"),
        os.path.join(ROOT, "qt_testing_settings.toml"),
    ],
    envvar_prefix="DYNACONF",
    environments=True,
    env_switcher="ENV_FOR_DYNACONF",
    validate_only_current_env=True,
    validators=validate(),
)
# END REGION


def write_config():
    """
    Writes the Settings to a file
    """
    # noinspection PyShadowingNames
    env: str = str(settings.current_env).upper()
    file = None

    if env == "PRODUCTION":
        file = os.path.join(os.path.dirname(__file__), "settings.local.toml")
    elif env == "QT_TESTING":
        file = os.path.join(os.path.dirname(__file__), "qt_testing_settings.local.toml")
    elif env == "TESTING":
        file = os.path.join(os.path.dirname(__file__), "testing_settings.local.toml")

    if file is not None:
        write(file, {env: settings.to_dict()}, merge=True)
    else:
        raise NotImplementedError(f"{env} Environment Doesnt Exist")


if __name__ == "__main__":
    import json

    env = ("TESTING", "QT_TESTING", "PRODUCTION")
    for _env in env:
        settings.setenv(_env)
        settings.validators.validate_all()
        print()
        print(_env)
        print(json.dumps(settings.to_dict(), indent=2))
