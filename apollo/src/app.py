from PySide6 import QtWidgets, QtCore, QtGui

from apollo.layout.mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.utils import get_logger
from configs import settings
from configs.config import write_config

CONFIG = settings
LOGGER = get_logger(__name__)


class Apollo(QtWidgets.QMainWindow, Apollo_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setup_interactions()
        self.setup_defaults()

    def setup_interactions(self):
        pass

    def setup_defaults(self):
        pass

    def save_states(self):
        pass

    def shutdown(self):
        self.save_states()
        write_config()
