"""
Main Class for Apollo Includes all sub tabs and components

## Design guidelines for all Sub tabs defined under Apollo
1. Needs an interaction class. Interaction class must be an ABC and must bind
   interaction to cb methods ABM. All ABM must be implemented in main
   component class
2. Needs to have a controller class which handles all communication to
   all resources. Controller class must be an ABC
3. Needs to have a main component class that has load and save state function
   to handle interaction with the congif files

"""
from __future__ import annotations

import abc
import os.path
from pathlib import PurePath
from typing import Union

from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QSystemTrayIcon

from apollo.layout.mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.src.tabs import Library_Tab, Playback_Bar
from apollo.utils import get_logger
from configs import settings
from configs.config import write_config


CONFIG = settings
LOGGER = get_logger(__name__)


class Apollo_Interactions(abc.ABC):
    UI: Union[Apollo_MainWindow, QtWidgets.QMainWindow] = None

    def __init__(self: Apollo):
        self.connect_interactions()
        self.load_states()

    # pragma: no cover
    def connect_interactions(self):
        self.UI.library_tab_switch_button.pressed.connect(lambda: (self.call_tab_switch(0)))
        self.UI.now_playing_tab_switch_button.pressed.connect(lambda: (self.call_tab_switch(1)))
        self.UI.playlist_tab_switch_button.pressed.connect(lambda: (self.call_tab_switch(2)))
        self.UI.audiofx_tab_switch_button.pressed.connect(lambda: (self.call_tab_switch(3)))
        self.UI.closeEvent = lambda e: self.cb_shutdown()

    def call_tab_switch(self, tab_index: int):
        self.UI.main_tabs_stack_widget.setCurrentIndex(tab_index)

    @abc.abstractmethod
    def cb_shutdown(self):
        ...

    def load_states(self):  # pragma: no cover
        """
        loads session states of Apollo
        """
        pass

    def save_states(self):  # pragma: no cover
        """
        saves session states of Apollo
        """
        pass


class Apollo_Controller(abc.ABC):
    UI: Union[Apollo_MainWindow, QtWidgets.QMainWindow] = None

    def __init__(self: Apollo):
        self.load_states()

    def load_states(self):  # pragma: no cover
        """
        loads session states of Apollo
        """
        pass

    def save_states(self):  # pragma: no cover
        """
        saves session states of Apollo
        """
        pass


class Apollo_UI(QtWidgets.QMainWindow, Apollo_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_app_icon()

    def set_app_icon(self):
        icon_path = (
            PurePath(os.path.dirname(os.path.dirname(__file__)))
            / "assets"
            / "Apollo_App_Icon_Small.svg"
        ).as_posix()
        pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(icon_path)).scaled(48, 48)
        self.setWindowIcon(QtGui.QIcon(pixmap))


class Apollo(Apollo_Interactions, Apollo_Controller):
    UI: Union[Apollo_MainWindow, QtWidgets.QMainWindow] = None
    _LIBRARY: Library_Tab = None
    _NOW_PLAYING: Playback_Bar = None

    def __init__(self):
        self.UI = Apollo_UI()

        Apollo_Interactions.__init__(self)
        Apollo_Controller.__init__(self)
        self.load_states()

        self._load_sub_tabs()

    def _load_sub_tabs(self):
        self._LIBRARY = Library_Tab(self.UI)
        # self._NOW_PLAYING = Playback_Bar(self.UI)

    def load_states(self):
        current = CONFIG.get("APOLLO.MAIN.CURRENT_TAB", 0)
        if current == 0:
            self.UI.library_tab_switch_button.click()
        elif current == 1:
            self.UI.now_playing_tab_switch_button.click()
        elif current == 2:
            self.UI.playlist_tab_switch_button.click()
        elif current == 3:
            self.UI.audiofx_tab_switch_button.click()

    def save_states(self):
        Apollo_Interactions.save_states(self)
        Apollo_Controller.save_states(self)
        CONFIG["APOLLO.MAIN.CURRENT_TAB"] = self.UI.main_tabs_stack_widget.currentIndex()

    def cb_shutdown(self):  # pragma: no cover
        self.save_states()
        self._LIBRARY.save_states()
        write_config()
