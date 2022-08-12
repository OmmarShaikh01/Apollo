"""
Main Class for Apollo Includes all sub tabs and components
"""
from __future__ import annotations

import os.path
from pathlib import PurePath

from PySide6 import QtGui, QtWidgets

from apollo.layout import Apollo_MainWindow
from apollo.utils import Apollo_Generic_View, Apollo_Global_Signals, get_logger
from apollo.database.models import Model_Provider
from configs import settings as CONFIG

LOGGER = get_logger(__name__)


class Apollo_UI(QtWidgets.QMainWindow, Apollo_MainWindow):
    """
    Apollo Mainwindow implementation class
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_app_icon()

    def set_app_icon(self):
        """
        Sets the title bar icon
        """
        path = PurePath(CONFIG.project_root) / "apollo" / "assets" / "Apollo_App_Icon_Small.svg"
        pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(str(path))).scaled(48, 48)
        self.setWindowIcon(QtGui.QIcon(pixmap))


class Apollo(Apollo_Generic_View):
    """
    Apollo main class
    """

    def __init__(self):
        self.SIGNALS = Apollo_Global_Signals()
        self.UI = Apollo_UI()
        self.MODEL_PROVIDER = Model_Provider()

        self.setup_conections()
        self.setup_defaults()

    def setup_conections(self):
        """
        Sets up all the connection for the UI
        """
        self.UI.library_tab_switch_button.pressed.connect(lambda: (self._cb_on_tab_switch(0)))
        self.UI.now_playing_tab_switch_button.pressed.connect(lambda: (self._cb_on_tab_switch(1)))
        self.UI.playlist_tab_switch_button.pressed.connect(lambda: (self._cb_on_tab_switch(2)))
        self.UI.audiofx_tab_switch_button.pressed.connect(lambda: (self._cb_on_tab_switch(3)))
        self.UI.closeEvent = lambda e: self._cb_shutdown()

    def setup_defaults(self):
        """
        Sets up default states for all UI Widgets and objects
        """

    def save_states(self):
        """
        Saves current states for all UI Widgets and objects
        """
        CONFIG["APOLLO.MAIN.CURRENT_TAB"] = self.UI.main_tabs_stack_widget.currentIndex()

    def _cb_on_tab_switch(self, tab_index: int):
        self.UI.main_tabs_stack_widget.setCurrentIndex(tab_index)

    def _cb_shutdown(self):
        self.save_states()
