"""
Lazy Loads all the application assets
"""
import json
import os
from collections import namedtuple
from pathlib import PurePath

from apollo.assets.stylesheets import generate_resource
from configs import settings


CONFIG = settings


class _AppIcons:
    """
    Container for AppIcon paths
    """

    __slots__ = [
        "ADD",
        "ARROW_BACK",
        "ARROW_FORWARD",
        "AUDIO_FILE",
        "CHECK_BOX",
        "CHECK_BOX_OUTLINE_BLANK",
        "CLOSE",
        "DELETE",
        "DONE",
        "EQUALIZER",
        "EXPAND_LESS",
        "EXPAND_MORE",
        "FAVORITE",
        "FAVORITE_FILLED",
        "FILE_DOWNLOAD",
        "STAR_OUTLINE",
        "HOME",
        "INDETERMINATE_CHECK_BOX",
        "LIBRARY_MUSIC",
        "MENU",
        "MUSIC_NOTE",
        "PAUSE",
        "PLAYLIST_ADD",
        "PLAYLIST_PLAY",
        "PLAY_ARROW",
        "POWER_SETTINGS_NEW",
        "QUEUE_MUSIC",
        "RADIO_BUTTON_CHECKED",
        "RADIO_BUTTON_UNCHECKED",
        "REPEAT_OFF",
        "REPEAT_ON",
        "REPEAT_ONE_ON",
        "SEARCH",
        "SETTINGS",
        "SHUFFLE",
        "SHUFFLE_OFF",
        "SKIP_NEXT",
        "SKIP_PREVIOUS",
        "STAR",
        "STAR_HALF",
        "VOLUME_DOWN",
        "VOLUME_MUTE",
        "VOLUME_OFF",
        "VOLUME_UP",
    ]

    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            self._init_attrs()
            return object.__getattribute__(self, item)

    def _init_attrs(self):
        """
        lazy loader for all icon paths
        """

        def loader():
            Icon = namedtuple(
                "Icon", ["danger", "disabled", "primary", "secondary", "success", "warning"]
            )
            path = PurePath(os.path.dirname(__file__), "__loaded_theme__", "icons")
            for file in os.listdir(path / "primary"):
                name, _ = os.path.splitext(file)
                value = Icon(
                    danger=str((path / "danger" / str(file)).as_posix()),
                    disabled=str((path / "disabled" / str(file)).as_posix()),
                    primary=str((path / "primary" / str(file)).as_posix()),
                    secondary=str((path / "secondary" / str(file)).as_posix()),
                    success=str((path / "success" / str(file)).as_posix()),
                    warning=str((path / "warning" / str(file)).as_posix()),
                )
                object.__setattr__(self, str(name).upper(), value)

        path = PurePath(os.path.dirname(__file__), "__loaded_theme__", "icons")
        if not os.path.exists(path):
            generate_resource(CONFIG.loaded_theme, recompile=True)
        loader()


def get_apptheme() -> dict:
    """
    Loads the application theme pallete

    Returns:
        dict: Apptheme load
    """
    path = PurePath(os.path.dirname(__file__), "__loaded_theme__", "apptheme.json")
    if not os.path.exists(path):
        generate_resource(CONFIG.loaded_theme, recompile=True)
    with open(path, encoding="utf-8") as file:
        return json.load(file)


_path = PurePath(os.path.dirname(__file__), "__loaded_theme__")
if not os.path.exists(_path):
    generate_resource(CONFIG.loaded_theme, recompile=True)

AppIcons = _AppIcons()
AppTheme = get_apptheme()
