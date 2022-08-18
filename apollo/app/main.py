"""
Main Class for Apollo Includes all sub tabs and components
"""
from __future__ import annotations

from pathlib import PurePath

from PySide6 import QtGui, QtWidgets

from apollo.app.sub_tabs import (
    Audio_Interface_Tab,
    Library_Tab,
    Now_Playing_Tab,
    PlayBack_Bar,
    Playlist_Tab,
    Preferences_SubWindow,
)
from apollo.database.models import Model_Provider
from apollo.layout import Apollo_MainWindow_UI
from apollo.utils import Apollo_Generic_View, get_logger
from configs import settings as CONFIG
from configs import write_config


LOGGER = get_logger(__name__)


class Apollo(Apollo_Generic_View):
    """
    Apollo main class
    """

    _library_tab: Library_Tab
    _now_playing_tab: Now_Playing_Tab
    _playlist_tab: Playlist_Tab
    _audio_interface_tab: Audio_Interface_Tab
    _playback_bar: PlayBack_Bar
    _preferences_subwindow: Preferences_SubWindow

    def __init__(self):
        self.UI = Apollo_MainWindow_UI()
        self.MODEL_PROVIDER = Model_Provider

        self.setup_title_menu()
        self.setup_conections()
        self.setup_defaults()
        self.setup_sub_tabs()

    def setup_title_menu(self):
        menuFile = self.UI.menuFile

        menuEdit = self.UI.menuEdit
        menuEdit.addAction("Edit Preferences", self._cb_launch_edit_preference_window)

        menuTools = self.UI.menuTools

        menuHelp = self.UI.menuHelp

    def setup_sub_tabs(self):
        """
        Sets up Sub tabs
        """
        self._library_tab = Library_Tab(self.UI)
        self._now_playing_tab = Now_Playing_Tab(self.UI)
        self._playlist_tab = Playlist_Tab(self.UI)
        self._audio_interface_tab = Audio_Interface_Tab(self.UI)
        self._playback_bar = PlayBack_Bar(self.UI)

    # pylint: disable=E1101
    def setup_conections(self):
        """
        Sets up all the connection for the UI
        """
        self.UI.library_tab_switch_button.pressed.connect(lambda: (self._cb_on_tab_switch(0)))
        self.UI.now_playing_tab_switch_button.pressed.connect(lambda: (self._cb_on_tab_switch(1)))
        self.UI.playlist_tab_switch_button.pressed.connect(lambda: (self._cb_on_tab_switch(2)))
        self.UI.audiofx_tab_switch_button.pressed.connect(lambda: (self._cb_on_tab_switch(3)))
        self.UI.closeEvent = lambda e: self._cb_shutdown()
        self.UI.search_lineEdit.editingFinished.connect(lambda *x: self._cb_on_search_query())
        self.UI.search_lineEdit.textChanged.connect(lambda *x: self._cb_on_search_query())
        self.UI.search_lineEdit.returnPressed.connect(lambda *x: self._cb_on_search_query())
        self.UI.search_button.pressed.connect(lambda *x: self._cb_on_search_query())

    def setup_defaults(self):
        """
        Sets up default states for all UI Widgets and objects
        """
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
        """
        Saves current states for all UI Widgets and objects
        """
        CONFIG["APOLLO.MAIN.CURRENT_TAB"] = self.UI.main_tabs_stack_widget.currentIndex()

    def _cb_on_tab_switch(self, tab_index: int):
        self.UI.main_tabs_stack_widget.setCurrentIndex(tab_index)

    def _cb_shutdown(self):
        self.save_states()
        self._library_tab.save_states()
        self._now_playing_tab.save_states()
        self._playlist_tab.save_states()
        self._audio_interface_tab.save_states()
        self._playback_bar.save_states()
        write_config()

    def _cb_on_search_query(self):
        query = str(self.UI.search_lineEdit.text()).strip()
        current = self.UI.main_tabs_stack_widget.currentIndex()
        if query and current == 0:
            self._library_tab.cb_on_search_query(query=query)
        elif query and current == 1:
            self._now_playing_tab.cb_on_search_query(query=query)
        elif query and current == 2:
            self.UI.playlist_tab_switch_button.click()

    def _cb_launch_edit_preference_window(self):
        def _cb_shutdown():
            self._preferences_subwindow = None

        self._preferences_subwindow = Preferences_SubWindow()
        self._preferences_subwindow.closeEvent = lambda e: (_cb_shutdown())
        self._preferences_subwindow.show()
