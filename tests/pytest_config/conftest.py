import os

import pytest
from dynaconf import LazySettings
from dynaconf.loaders.toml_loader import write


def write_config(config: LazySettings):
    """
    Writes the Settings to a file
    """
    # noinspection PyShadowingNames
    env: str = config.current_env
    if env == "PRODUCTION":
        file = os.path.join(os.path.dirname(__file__), "settings.local.toml")
    elif env == "QT_TESTING":
        file = os.path.join(os.path.dirname(__file__), "qt_testing_settings.local.toml")
    else:
        file = os.path.join(os.path.dirname(__file__), "testing_settings.local.toml")
    write(file, {env: config.to_dict()}, merge=True)


@pytest.fixture(scope="package", autouse=True)
def create_session():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    configs = [
        "settings.toml",
        "testing_settings.toml",
        "qt_testing_settings.toml",
    ]
    for config in configs:
        if os.path.exists(os.path.join(project_root, "configs", f"{config}")):
            os.rename(
                os.path.join(project_root, "configs", f"{config}"),
                os.path.join(project_root, "configs", f"_{config}"),
            )

    configs = [
        "settings.local.toml",
        "testing_settings.local.toml",
        "qt_testing_settings.local.toml",
        os.path.join(os.path.dirname(__file__), "settings.local.toml"),
        os.path.join(os.path.dirname(__file__), "qt_testing_settings.local.toml"),
        os.path.join(os.path.dirname(__file__), "testing_settings.local.toml"),
    ]
    for config in configs:
        if os.path.exists(os.path.join(project_root, "configs", f"{config}")):
            os.remove(os.path.join(project_root, "configs", f"{config}"))

    yield None

    configs = [
        "settings.toml",
        "testing_settings.toml",
        "qt_testing_settings.toml",
    ]
    for config in configs:
        if os.path.exists(os.path.join(project_root, "configs", f"_{config}")):
            os.rename(
                os.path.join(project_root, "configs", f"_{config}"),
                os.path.join(project_root, "configs", f"{config}"),
            )

    configs = [
        "settings.local.toml",
        "testing_settings.local.toml",
        "qt_testing_settings.local.toml",
    ]
    for config in configs:
        if os.path.exists(os.path.join(project_root, "configs", f"{config}")):
            os.remove(os.path.join(project_root, "configs", f"{config}"))
