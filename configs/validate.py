import os

import dynaconf
from dynaconf import Validator


def validate(settings: dynaconf.Dynaconf):
    """
    Validates loaded config

    Args:
        settings (dynaconf.Dynaconf): Settings
    """
    # REGISTER VALIDATORS FOR [SHARED SESSION]
    ENVS = ('TESTING', 'QT_TESTING', 'PRODUCTION')
    for ENV in ENVS:
        settings.validators.register(
            Validator('logger_level', env = ENV, must_exist = True),
            Validator('loaded_theme', env = ENV, must_exist = True),
            Validator('recompile_theme', env = ENV, must_exist = True),
            Validator('supported_formats', env = ENV, must_exist = True),
            Validator('enabled_formats', env = ENV, must_exist = True),
            Validator("server.rate", "server.chnl", "server.format", env = ENV, must_exist = True)
        )

    # REGISTER VALIDATORS FOR [PRODUCTION]
    env = 'PRODUCTION'
    settings.validators.register(
        Validator('db_path', default = os.path.join(settings.project_root, 'apollo', 'db', 'apollo.db'), must_exist = True, env = env),
        Validator(
            'APOLLO.MAIN.CURRENT_TAB',
            'APOLLO.PLAYBACK_BAR.STATE_PLAY',
            'APOLLO.PLAYBACK_BAR.STATE_SHUFFLE',
            'APOLLO.PLAYBACK_BAR.STATE_REPEAT',
            'APOLLO.PLAYBACK_BAR.VOLUME_LEVEL',
            'APOLLO.PLAYBACK_BAR.LOADED_TRACK',
            'APOLLO.PLAYBACK_BAR.BYPASS_PROCESSOR',
            'APOLLO.PLAYBACK_BAR.ELAPSED_TIME',
        ),
    )

    # REGISTER VALIDATORS FOR [QT_TESTING]
    env = 'QT_TESTING'
    settings.validators.register(
        Validator('temp_dir', default = os.path.join(settings.project_root, 'tests', 'tempdir'), must_exist = True, env = env),
        Validator('assets_dir', default = os.path.join(settings.project_root, 'tests', 'assets'), must_exist = True, env = env),
        Validator('db_path', default = os.path.join(settings.project_root, 'tests', 'tempdir', 'testing.db'), must_exist = True, env = env),

        Validator('benchmark_runs', default = 1000, must_exist = True, env = env),
        Validator('benchmark_formats', must_exist = True, env = env),  # NO DEFAULTS
        Validator('sox_path', must_exist = True, env = env, messages = {"must_exist_true": "Download and Set SOX_PATH sox from http://sox.sourceforge.net/"}),  # NO DEFAULTS

        Validator(
            'APOLLO.MAIN.CURRENT_TAB',
            'APOLLO.PLAYBACK_BAR.STATE_PLAY',
            'APOLLO.PLAYBACK_BAR.STATE_SHUFFLE',
            'APOLLO.PLAYBACK_BAR.STATE_REPEAT',
            'APOLLO.PLAYBACK_BAR.VOLUME_LEVEL',
            'APOLLO.PLAYBACK_BAR.LOADED_TRACK',
            'APOLLO.PLAYBACK_BAR.BYPASS_PROCESSOR',
            'APOLLO.PLAYBACK_BAR.ELAPSED_TIME',
        ),
    )

    # REGISTER VALIDATORS FOR [TESTING]
    env = 'TESTING'
    settings.validators.register(
        Validator('temp_dir', default = os.path.join(settings.project_root, 'tests', 'tempdir'), must_exist = True, env = env),
        Validator('assets_dir', default = os.path.join(settings.project_root, 'tests', 'assets'), must_exist = True, env = env),
        Validator('db_path', default = os.path.join(settings.project_root, 'tests', 'tempdir', 'testing.db'), must_exist = True, env = env),

        Validator('benchmark_runs', default = 1000, must_exist = True, env = env),
        Validator('benchmark_formats', must_exist = True, env = env),  # NO DEFAULTS
        Validator('sox_path', must_exist = True, env = env, messages = {"must_exist_true": "Download and Set SOX_PATH sox from http://sox.sourceforge.net/"}),  # NO DEFAULTS
    )

    settings.validators.validate()
