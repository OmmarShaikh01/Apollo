import datetime

from PySide6 import QtWidgets

from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.src.main_content import MainContent


class Apollo(QtWidgets.QMainWindow, Apollo_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setupUX()
        self.main_content_controller = MainContent(self)

    def setupUX(self):
        self.main_content_splitterframe.setCollapsible(0, False)
