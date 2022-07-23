"""
Lazy Loads all the application assets
"""
import json
import os
from collections import namedtuple
from pathlib import PurePath

from PySide6 import QtWidgets

from apollo.assets.stylesheets import generate_resource, load_theme
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
        "BRANCH_CLOSED",
        "BRANCH_END",
        "BRANCH_MORE",
        "BRANCH_OPEN",
        "CHECKBOX_CHECKED",
        "CHECKBOX_INDETERMINATE",
        "CHECKBOX_UNCHECKED",
        "CHECKLIST",
        "CHECKLIST_INDETERMINATE",
        "CHECK_BOX",
        "CHECK_BOX_OUTLINE_BLANK",
        "CLOSE",
        "DELETE",
        "DONE",
        "DOWNARROW",
        "DOWNARROW2",
        "EQUALIZER",
        "EXPAND_LESS",
        "EXPAND_MORE",
        "FAVORITE",
        "FAVORITE_FILLED",
        "FILE_DOWNLOAD",
        "FLOAT",
        "HOME",
        "INDETERMINATE_CHECK_BOX",
        "LEFTARROW",
        "LEFTARROW2",
        "LIBRARY_MUSIC",
        "MENU",
        "MUSIC_NOTE",
        "PAUSE",
        "PLAYLIST_ADD",
        "PLAYLIST_PLAY",
        "PLAY_ARROW",
        "POWER_SETTINGS_NEW",
        "QUEUE_MUSIC",
        "RADIOBUTTON_CHECKED",
        "RADIOBUTTON_UNCHECKED",
        "RADIO_BUTTON_CHECKED",
        "RADIO_BUTTON_UNCHECKED",
        "REPEAT_OFF",
        "REPEAT_ON",
        "REPEAT_ONE_ON",
        "RIGHTARROW",
        "RIGHTARROW2",
        "SEARCH",
        "SETTINGS",
        "SHUFFLE",
        "SHUFFLE_OFF",
        "SIZEGRIP",
        "SKIP_NEXT",
        "SKIP_PREVIOUS",
        "SLIDER",
        "SPLITTER_HORIZONTAL",
        "SPLITTER_VERTICAL",
        "STAR",
        "STAR_HALF",
        "STAR_OUTLINE",
        "TAB_CLOSE",
        "TOOLBAR_HANDLE_HORIZONTAL",
        "TOOLBAR_HANDLE_VERTICAL",
        "UPARROW",
        "UPARROW2",
        "VLINE",
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
            if not generate_resource(CONFIG.loaded_theme):
                raise RuntimeError("Failed To generate Resurces")
        loader()


def get_apptheme() -> dict:
    """
    Loads the application theme pallete

    Returns:
        dict: Apptheme load
    """
    path = PurePath(os.path.dirname(__file__), "__loaded_theme__", "apptheme.json")
    if not os.path.exists(path):
        if not generate_resource(CONFIG.loaded_theme):
            raise RuntimeError("Failed To generate Resurces")
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    return dict()


_path = PurePath(os.path.dirname(__file__), "__loaded_theme__")
if not os.path.exists(_path):
    load_theme(
        QtWidgets.QApplication.instance(), CONFIG.loaded_theme, recompile=CONFIG.recompile_theme
    )

AppIcons = _AppIcons()
AppTheme = get_apptheme()
