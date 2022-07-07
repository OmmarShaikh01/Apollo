import os

import dynaconf
from dynaconf import Validator


def _ui_states_validators() -> Validator:
    """
    Validators for the UI states

    Returns:
        Validator: Validators for the UI states
    """
    MAIN = (
        'CURRENT_TAB'
    )

    PLAYBACK_BAR = (
        'STATE_PLAY',
        'STATE_SHUFFLE',
        'STATE_REPEAT',
        'VOLUME_LEVEL',
        'LOADED_TRACK',
        'BYPASS_PROCESSOR',
        'ELAPSED_TIME'
    )

    LIBRARY_TAB = (
        'DELEGATE_TYPE'
    )

    MAIN = [f"APOLLO.MAIN.{x}" for x in MAIN]
    PLAYBACK_BAR = [f"APOLLO.PLAYBACK_BAR.{x}" for x in PLAYBACK_BAR]
    LIBRARY_TAB = [f"APOLLO.LIBRARY_TAB.{x}" for x in LIBRARY_TAB]
    return Validator(*MAIN, *PLAYBACK_BAR, *LIBRARY_TAB)


def validate(settings: dynaconf.Dynaconf):
    """
    Validates loaded config

    Args:
        settings (dynaconf.Dynaconf): Settings
    """
    # REGISTER VALIDATORS FOR [SHARED SESSION]
    FIELDS = ('logger_level', 'loaded_theme', 'recompile_theme', 'supported_formats', 'enabled_formats')
    settings.validators.register(
        Validator(*FIELDS, "server.rate", "server.chnl", "server.format", env = ['TESTING', 'QT_TESTING', 'PRODUCTION'], must_exist = True)
    )

    # REGISTER VALIDATORS FOR [PRODUCTION]
    env = 'PRODUCTION'
    settings.validators.register(
        Validator('db_path', default = os.path.join(settings.project_root, 'apollo', 'db', 'apollo.db'), must_exist = True, env = env),
        _ui_states_validators(),
    )

    # REGISTER VALIDATORS FOR [QT_TESTING]
    env = 'QT_TESTING'
    settings.validators.register(
        Validator('temp_dir', default = os.path.join(settings.project_root, 'tests', 'tempdir'), must_exist = True, env = env),
        Validator('assets_dir', default = os.path.join(settings.project_root, 'tests', 'assets'), must_exist = True, env = env),
        Validator('mock_data', default = os.path.join(settings.project_root, 'tests', 'assets', 'mock_data'), must_exist = True, env = env),
        Validator('db_path', default = os.path.join(settings.project_root, 'tests', 'tempdir', 'testing.db'), must_exist = True, env = env),

        Validator('profile_runs', default = False, must_exist = True, env = env),
        Validator('benchmark_runs', default = 1000, must_exist = True, env = env),
        Validator('benchmark_formats', must_exist = True, env = env),  # NO DEFAULTS
        Validator('sox_path', must_exist = True, env = env, messages = {"must_exist_true": "Download and Set SOX_PATH sox from http://sox.sourceforge.net/"}),  # NO DEFAULTS

        _ui_states_validators(),
    )

    # REGISTER VALIDATORS FOR [TESTING]
    env = 'TESTING'
    settings.validators.register(
        Validator('temp_dir', default = os.path.join(settings.project_root, 'tests', 'tempdir'), must_exist = True, env = env),
        Validator('assets_dir', default = os.path.join(settings.project_root, 'tests', 'assets'), must_exist = True, env = env),
        Validator('mock_data', default = os.path.join(settings.project_root, 'tests', 'assets', 'mock_data'), must_exist = True, env = env),
        Validator('db_path', default = os.path.join(settings.project_root, 'tests', 'tempdir', 'testing.db'), must_exist = True, env = env),

        Validator('profile_runs', default = False, must_exist = True, env = env),
        Validator('benchmark_runs', default = 1000, must_exist = True, env = env),
        Validator('benchmark_formats', must_exist = True, env = env),  # NO DEFAULTS
        Validator('sox_path', must_exist = True, env = env, messages = {"must_exist_true": "Download and Set SOX_PATH sox from http://sox.sourceforge.net/"}),  # NO DEFAULTS
    )
