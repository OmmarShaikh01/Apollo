import os.path

from dynaconf import Dynaconf, Validator, loaders
from dynaconf.loaders.toml_loader import write

settings = Dynaconf(
        project_root = os.path.dirname(os.path.dirname(__file__)),
        envvar_prefix = "DYNACONF",
        settings_files = ['settings.toml', '.secrets.toml'],
        environments = True,
        load_dotenv = True,
        env_switcher = "ENV_FOR_DYNACONF",
        dotenv_path = "configs/.env",
)
settings.validators.validate()


def write_config():
    write('settings.toml', {settings.current_env: settings.to_dict()}, merge = True)


# REGISTER VALIDATORS FOR [DEFAULT]
env = 'DEFAULT'
settings.validators.register(
        Validator(
                'db_path',
                default = os.path.join(settings.project_root, 'apollo', 'db', 'default.db'),
                must_exist = True, env = env
        ),
)

# REGISTER VALIDATORS FOR [TESTING]
env = 'TESTING'
settings.validators.register(
        Validator('temp_dir',
                  default = os.path.join(settings.project_root, 'tests', 'pytest', 'tempdir'),
                  must_exist = True, env = env
                  ),
        Validator('assets_dir',
                  default = os.path.join(settings.project_root, 'tests', 'assets'),
                  must_exist = True, env = env
                  ),
        Validator('db_path',
                  default = os.path.join(settings.project_root, 'tests', 'pytest', 'tempdir', 'testing.db'),
                  must_exist = True, env = env
                  ),
        Validator('supported_formats',
                  default = ['aac', 'aiff', 'flac', 'm4a', 'mp3', 'ogg', 'opus', 'wav'],
                  must_exist = True,
                  env = env
                  ),
        Validator('enabled_formats',
                  default = ['mp3'],
                  # default = ['aac', 'aiff', 'flac', 'm4a', 'mp3', 'ogg', 'opus', 'wav'],
                  must_exist = True,
                  env = env
                  ),
)
# REGISTER VALIDATORS FOR [PRODUCTION]
env = 'PRODUCTION'
settings.validators.register(
        Validator('db_path',
                  default = os.path.join(settings.project_root, 'apollo', 'db', 'default.db'),
                  must_exist = True, env = env
                  ),
        Validator('supported_formats',
                  default = ['aac', 'aiff', 'flac', 'm4a', 'mp3', 'ogg', 'opus', 'wav'],
                  must_exist = True,
                  env = env
                  ),
        Validator('enabled_formats',
                  default = ['aac', 'aiff', 'flac', 'm4a', 'mp3', 'ogg', 'opus', 'wav'],
                  must_exist = True,
                  env = env
                  ),
)

settings.validators.validate()
