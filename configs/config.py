import os
import shutil

from dynaconf import Dynaconf, Validator, loaders
from dynaconf.loaders.toml_loader import write


settings = Dynaconf(
    load_dotenv = True,
    project_root = os.path.dirname(os.path.dirname(__file__)),
    settings_files = [
        os.path.join(os.path.dirname(__file__), 'default_settings.toml'),
        os.path.join(os.path.dirname(__file__), 'default_testing_settings.toml'),
        os.path.join(os.path.dirname(__file__), 'settings.local.toml'),
        os.path.join(os.path.dirname(__file__), 'testing_settings.local.toml'),
    ],
    envvar_prefix = "DYNACONF",
    environments = True,
    env_switcher = "ENV_FOR_DYNACONF",
    validate_only_current_env=True,
)


# REGISTER VALIDATORS FOR [SHARED SESSION]
ENVS = ('TESTING', 'QT_TESTING', 'PRODUCTION')
for ENV in ENVS:
    settings.validators.register(
        Validator('loaded_theme', env = ENV, must_exist = True),
        Validator('recompile_theme', env = ENV, must_exist = True),  # NO DEFAULTS
        Validator('supported_formats', env = ENV, must_exist = True),
        Validator('enabled_formats', env = ENV, must_exist = True),
        Validator("server.rate", "server.chnl", "server.format", env = ENV, must_exist = True)
    )


# REGISTER VALIDATORS FOR [PRODUCTION]
env = 'PRODUCTION'
settings.validators.register(
    Validator('db_path', default = os.path.join(settings.project_root, 'apollo', 'db', 'apollo.db'), must_exist = True, env = env),
    Validator(
        'APOLLO.PLAYBACK_BAR.STATE_PLAY',
        'APOLLO.PLAYBACK_BAR.STATE_SHUFFLE',
        'APOLLO.PLAYBACK_BAR.STATE_REPEAT',
    ),
)


# REGISTER VALIDATORS FOR [QT_TESTING]
env = 'QT_TESTING'
settings.validators.register(
    Validator('temp_dir', default = os.path.join(settings.project_root, 'tests', 'tempdir'), must_exist = True, env = env),
    Validator('assets_dir', default = os.path.join(settings.project_root, 'tests', 'assets'), must_exist = True, env = env),
    Validator('db_path', default = os.path.join(settings.project_root, 'tests', 'tempdir', 'testing.db'), must_exist = True, env = env),

    Validator('benchmark_formats', 'nox_execution_verbosity_disabled', must_exist = True),  # NO DEFAULTS
    Validator('sox_path', must_exist = True, messages = {"must_exist_true": "Download and Set SOX_PATH sox from http://sox.sourceforge.net/"}),  # NO DEFAULTS
)


# REGISTER VALIDATORS FOR [TESTING]
env = 'TESTING'
settings.validators.register(
    Validator('temp_dir', default = os.path.join(settings.project_root, 'tests', 'tempdir'), must_exist = True, env = env),
    Validator('assets_dir', default = os.path.join(settings.project_root, 'tests', 'assets'), must_exist = True, env = env),
    Validator('db_path', default = os.path.join(settings.project_root, 'tests', 'tempdir', 'testing.db'), must_exist = True, env = env),

    Validator('benchmark_runs', default = 1000, must_exist = True, env = env),
    Validator('benchmark_formats', 'nox_execution_verbosity_disabled', must_exist = True),  # NO DEFAULTS
    Validator('sox_path', must_exist = True, messages = {"must_exist_true": "Download and Set SOX_PATH sox from http://sox.sourceforge.net/"}),  # NO DEFAULTS
)

settings.validators.validate()


def write_config():
    """
    Writes the Settings to a file
    """
    # noinspection PyShadowingNames
    env: str = settings.current_env
    if env == "PRODUCTION":
        file = os.path.join(os.path.dirname(__file__), 'settings.local.toml')
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
