import datetime

import PySide6.QtGui
from PySide6 import QtWidgets

from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.src.main_content import MainContent
from apollo.utils import get_configparser, get_logger

LOGGER = get_logger(__name__)
CONFIG = get_configparser()


class Apollo(QtWidgets.QMainWindow, Apollo_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setupUX()
        self.main_content_controller = MainContent(self)

    def setupUX(self):
        self.main_content_splitterframe.setCollapsible(0, False)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        super().closeEvent(event)
        self.main_content_controller.SHUTDOWN.emit()
