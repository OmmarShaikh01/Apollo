import os

import dynaconf
from dynaconf import Validator

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


def _ui_states_validators() -> Validator:
    """
    Validators for the UI states

    Returns:
        Validator: Validators for the UI states
    """
    MAIN = ("CURRENT_TAB",)

    PLAYBACK_BAR = (
        "STATE_PLAY",
        "STATE_SHUFFLE",
        "STATE_REPEAT",
        "VOLUME_LEVEL",
        "LOADED_TRACK",
        "BYPASS_PROCESSOR",
        "ELAPSED_TIME",
    )

    LIBRARY_TAB = ("DELEGATE_TYPE",)

    MAIN = [f"APOLLO.MAIN.{x}" for x in MAIN]
    PLAYBACK_BAR = [f"APOLLO.PLAYBACK_BAR.{x}" for x in PLAYBACK_BAR]
    LIBRARY_TAB = [f"APOLLO.LIBRARY_TAB.{x}" for x in LIBRARY_TAB]
    return Validator(*MAIN, *PLAYBACK_BAR, *LIBRARY_TAB)


def validate() -> list[Validator]:
    """
    Returns Validators to validate loaded config

    Returns:
        list[Validator]: List of setting validator
    """

    VALIDATORS = []
    # REGISTER VALIDATORS FOR [SHARED SESSION]
    FIELDS = (
        "loaded_theme",
        "recompile_theme",
        "supported_formats",
        "enabled_formats", "server.rate", "server.chnl", "server.format"
    )
    envs = ["TESTING", "QT_TESTING", "PRODUCTION"]
    for env in envs:
        validator = (
            Validator(*FIELDS, env=env, must_exist=True),
            Validator("logger_level", env = env, default = "ERROR")
        )
        VALIDATORS.extend(validator)

    # REGISTER VALIDATORS FOR [PRODUCTION]
    env = "PRODUCTION"
    validator = (
        Validator(
            "db_path",
            default=os.path.join(PROJECT_ROOT, "apollo", "db", "apollo.db"),
            must_exist=True,
            env=env,
        ),
        _ui_states_validators(),
    )
    VALIDATORS.extend(validator)

    # REGISTER VALIDATORS FOR [QT_TESTING]
    env = "QT_TESTING"
    validator = (
        Validator(
            "temp_dir",
            default=os.path.join(PROJECT_ROOT, "tests", "tempdir"),
            must_exist=True,
            env=env,
        ),
        Validator(
            "assets_dir",
            default=os.path.join(PROJECT_ROOT, "tests", "assets"),
            must_exist=True,
            env=env,
        ),
        Validator(
            "mock_data",
            default=os.path.join(PROJECT_ROOT, "tests", "assets", "mock_data"),
            must_exist=True,
            env=env,
        ),
        Validator(
            "db_path",
            default=os.path.join(PROJECT_ROOT, "tests", "tempdir", "testing.db"),
            must_exist=True,
            env=env,
        ),
        Validator("profile_runs", default=False, must_exist=True, env=env),
        Validator("benchmark_runs", default=1000, must_exist=True, env=env),
        Validator("benchmark_formats", must_exist=True, env=env),  # NO DEFAULTS
        # Download and Set SOX_PATH sox from http://sox.sourceforge.net/
        Validator("sox_path", env=env),
        _ui_states_validators(),
    )
    VALIDATORS.extend(validator)

    # REGISTER VALIDATORS FOR [TESTING]
    env = "TESTING"
    validator = (
        Validator(
            "temp_dir",
            default=os.path.join(PROJECT_ROOT, "tests", "tempdir"),
            must_exist=True,
            env=env,
        ),
        Validator(
            "assets_dir",
            default=os.path.join(PROJECT_ROOT, "tests", "assets"),
            must_exist=True,
            env=env,
        ),
        Validator(
            "mock_data",
            default=os.path.join(PROJECT_ROOT, "tests", "assets", "mock_data"),
            must_exist=True,
            env=env,
        ),
        Validator(
            "db_path",
            default=os.path.join(PROJECT_ROOT, "tests", "tempdir", "testing.db"),
            must_exist=True,
            env=env,
        ),
        Validator("profile_runs", default=False, must_exist=True, env=env),
        Validator("benchmark_runs", default=1000, must_exist=True, env=env),
        Validator("benchmark_formats", must_exist=True, env=env),  # NO DEFAULTS
        # Download and Set SOX_PATH sox from http://sox.sourceforge.net/
        Validator(
            "sox_path",
            env=env,
        ),
    )
    VALIDATORS.extend(validator)

    return VALIDATORS
