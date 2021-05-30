import sys

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from apollo.gui.ui_mainwindow_apollo import Ui_MainWindow as MainWindow
from apollo.utils import AppConfig
from apollo.plugins.app_theme import Theme
from apollo.db import LibraryManager

# from apollo.app.library_tab import LibraryTab
# from apollo.app.nowplaying_tab import NowPlayingTab
# from apollo.app.dataproviders import ApolloDataProvider

class ApolloUX(QtWidgets.QMainWindow, MainWindow):
    """
    Info: Initilizes Apollo and all related functions
    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self):
        """
        Info:
        Class Constructor

        Args: None
        Returns: None
        Errors: None
        """
        super().__init__()
        self.setupUi(self)
        self.AppConfig = AppConfig()


class ApolloTabBindings(ApolloUX):
    """
    Info: binds all the tabs with the UI
    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self):
        """
        Info:
        Class Constructor

        Args: None
        Returns: None
        Errors: None
        """
        super().__init__()
        self.DBManager = LibraryManager(self.AppConfig.get("current_db_path"))

    def InitTabs(self):
        """
        Info: Initilizes all the tabs for apollo
        Args: None
        Returns: None
        Errors: None
        """
        self.NowPlayingTab = NowPlayingTab(self) # type: ignore
        self.LibraryTab = LibraryTab(self) # type: ignore


class ApolloMain(ApolloTabBindings):
    """
    Info:
    Initilizes Apollo and all related functions

    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self):
        """
        Info:
        Class Constructor

        Args: None
        Returns: None
        Errors: None
        """
        super().__init__()


if __name__ == "__main__":
    from apollo.app.mainapp import ApolloExecute

    app = ApolloExecute()
    app.Execute()
