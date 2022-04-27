from PySide6 import QtCore, QtWidgets, QtGui

from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo
from apollo.src.tabs import LibraryTab, NowPlayingTab, PlaylistTab
from apollo.utils import ROOT, get_logger, get_configparser, ApolloSignal

LOGGER = get_logger(__name__)
CONFIG = get_configparser()


class MainContent:
    SHUTDOWN = ApolloSignal()

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.setupUI()

        self.LibraryTab = LibraryTab(ui)
        # self.PlaylistTab = PlaylistTab(ui)
        # self.NowPlayingTab = NowPlayingTab(ui)

    def setupUI(self):
        self.SHUTDOWN.connect(self.shutdown)

    def shutdown(self):
        self.LibraryTab.SHUTDOWN.emit()
        # self.PlaylistTab.SHUTDOWN.emit()
        # self.NowPlayingTab.SHUTDOWN.emit()
        LOGGER.info('SHUTDOWN')
