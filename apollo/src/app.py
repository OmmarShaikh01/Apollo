from PySide6 import QtWidgets, QtCore, QtGui

from apollo.layout.mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.utils import get_logger
from configs import settings

CONFIG = settings
LOGGER = get_logger(__name__)


class Apollo(QtWidgets.QMainWindow, Apollo_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
