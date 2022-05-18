import os.path
import shutil

from dynaconf import Dynaconf, Validator, loaders
from dynaconf.loaders.toml_loader import write

settings = Dynaconf(
        load_dotenv = True,
        project_root = os.path.dirname(os.path.dirname(__file__)),
        settings_files = ['settings.toml', '.secrets.toml'],
        envvar_prefix = "DYNACONF",
        environments = True,
        env_switcher = "ENV_FOR_DYNACONF",
)
settings.validators.validate()

# REGISTER VALIDATORS FOR [PRODUCTION]
env = 'PRODUCTION'
settings.validators.register(
    Validator('db_path', default = os.path.join(settings.project_root, 'apollo', 'db', 'apollo.db'), must_exist = True, env = env),
    Validator('supported_formats', default = ['aac', 'aiff', 'flac', 'm4a', 'mp3', 'ogg', 'opus', 'wav'], must_exist = True, env = env),
    Validator('enabled_formats', default = ['mp3'], must_exist = True, env = env),
    (
        Validator("server.rate", env = env, must_exist = True, default = 44100) &
        Validator("server.chnl", env = env, must_exist = True, default = 2) &
        Validator("server.format", env = env, must_exist = True, default = "s16")
    ),
)

# REGISTER VALIDATORS FOR [TESTING]
env = 'TESTING'
settings.validators.register(
    Validator('temp_dir', default = os.path.join(settings.project_root, 'tests', 'tempdir'), must_exist = True, env = env),
    Validator('assets_dir', default = os.path.join(settings.project_root, 'tests', 'assets'), must_exist = True, env = env),
    Validator('db_path', default = os.path.join(settings.project_root, 'tests', 'tempdir', 'testing.db'), must_exist = True, env = env),
    Validator('sox_path', must_exist = True, env = env, messages = {"must_exist_true": "Download and Set DYNACONF_SOX_PATH envvar sox from http://sox.sourceforge.net/"}),  # NO DEFAULTS,

    Validator('supported_formats', default = ['aac', 'aiff', 'flac', 'm4a', 'mp3', 'ogg', 'opus', 'wav'], must_exist = True, env = env),
    Validator('enabled_formats', default = ['mp3'], must_exist = True, env = env),
    Validator('benchmark_runs', default = 1000, must_exist = True, env = env),
    Validator('benchmark_formats', default = False, must_exist = True, env = env, messages = {"must_exist_true": "Set DYNACONF_BENCHMARK_FORMATS envvar"}),  # NO DEFAULTS,
    (
        Validator("server.rate", env = env, must_exist = True, default = 44100) &
        Validator("server.chnl", env = env, must_exist = True, default = 2) &
        Validator("server.format", env = env, must_exist = True, default = "s16")
    ),
)
settings.validators.validate()


def write_config():
    write('settings.toml', {settings.current_env: settings.to_dict()}, merge = True)


if __name__ == '__main__':
    print(settings.to_dict())
