import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from apollo.gui.ui_mainwindow_apollo import Ui_MainWindow as MainWindow
from apollo.app.library_tab import LibraryTab
from apollo.app.nowplaying_tab import NowPlayingTab
from apollo.plugins.app_theme import Theme
from apollo.utils import ConfigManager
from apollo.db.library_manager import DataBaseManager
from apollo.app.dataproviders import ApolloDataProvider



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
        self.ConfigManager = ConfigManager()


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
        self.DBManager = DataBaseManager()
        self.DBManager.connect("C:\\Users\\Ommar\\Desktop\\Apollo\\apollo\\db\\default.db")
        self.DataProvider = ApolloDataProvider()
        self.InitTabs()

    def InitTabs(self):
        """
        Info: Initilizes all the tabs for apollo
        Args: None
        Returns: None
        Errors: None
        """
        self.NowPlayingTab = NowPlayingTab(self)
        self.LibraryTab = LibraryTab(self)


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

    Theme().LoadAppIcons("GRAY_100")
    app = ApolloExecute()
    app.Execute()
