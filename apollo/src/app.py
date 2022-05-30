from PySide6 import QtWidgets, QtCore, QtGui

from configs import settings
from configs.config import write_config
from apollo.layout.mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.utils import get_logger
from apollo.src.tabs.playback_bar import Playback_Bar

CONFIG = settings
LOGGER = get_logger(__name__)


class Apollo(QtWidgets.QMainWindow, Apollo_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setup_interactions()
        self.setup_defaults()

        self.playback_bar = Playback_Bar(self)

    def setup_interactions(self):
        self.library_tab_switch_button.pressed.connect(lambda: (self.main_tabs_stack_widget.setCurrentIndex(0)))
        self.now_playing_tab_switch_button.pressed.connect(lambda: (self.main_tabs_stack_widget.setCurrentIndex(1)))
        self.playlist_tab_switch_button.pressed.connect(lambda: (self.main_tabs_stack_widget.setCurrentIndex(2)))
        self.audiofx_tab_switch_button.pressed.connect(lambda: (self.main_tabs_stack_widget.setCurrentIndex(3)))

    def setup_defaults(self):
        self.main_tabs_stack_widget.setCurrentIndex(CONFIG.get('APOLLO.MAIN.CURRENT_TAB', 0))

    def save_states(self):
        CONFIG['APOLLO.MAIN.CURRENT_TAB'] = self.main_tabs_stack_widget.currentIndex()

    def shutdown(self):
        self.save_states()
        self.playback_bar.shutdown()
        write_config()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.shutdown()
