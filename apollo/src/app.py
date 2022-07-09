from PySide6 import QtGui, QtWidgets

from apollo.layout.mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.src.tabs import Library_Tab, Playback_Bar
from apollo.utils import get_logger
from configs import settings
from configs.config import write_config


CONFIG = settings
LOGGER = get_logger(__name__)


class Apollo(QtWidgets.QMainWindow, Apollo_MainWindow):
    """
    Apollo main Widget
    """

    def __init__(self) -> None:
        super().__init__()
        self.playback_bar = None

        self.setupUi(self)
        self.setup_interactions()
        self.setup_defaults()
        self.setup_subtabs()

    # noinspection PyAttributeOutsideInit
    def setup_subtabs(self):
        """
        Sets up sub tabs and interactions
        """
        self.library_tab = Library_Tab(self)
        self.playback_bar = Playback_Bar(self)

    def setup_interactions(self):
        """
        Sets interactions
        """
        self.library_tab_switch_button.pressed.connect(
            lambda: (self.main_tabs_stack_widget.setCurrentIndex(0))
        )
        self.now_playing_tab_switch_button.pressed.connect(
            lambda: (self.main_tabs_stack_widget.setCurrentIndex(1))
        )
        self.playlist_tab_switch_button.pressed.connect(
            lambda: (self.main_tabs_stack_widget.setCurrentIndex(2))
        )
        self.audiofx_tab_switch_button.pressed.connect(
            lambda: (self.main_tabs_stack_widget.setCurrentIndex(3))
        )
        self.search_button.pressed.connect(
            lambda: (
                self.call_on_clear_search()
                if self.search_lineEdit.text() == ""
                else self.call_on_search()
            )
        )
        self.search_lineEdit.textChanged.connect(
            lambda x: (self.call_on_clear_search() if x == "" else self.call_on_search())
        )

    def setup_defaults(self):
        """
        sets up defaults states
        """
        current = CONFIG.get("APOLLO.MAIN.CURRENT_TAB", 0)
        if current == 0:
            self.library_tab_switch_button.click()
        elif current == 1:
            self.now_playing_tab_switch_button.click()
        elif current == 2:
            self.playlist_tab_switch_button.click()
        elif current == 3:
            self.audiofx_tab_switch_button.click()
        else:
            pass

    def save_states(self):
        """
        saves session states of Apollo
        """
        CONFIG["APOLLO.MAIN.CURRENT_TAB"] = self.main_tabs_stack_widget.currentIndex()

    def shutdown(self):
        """
        Shutdown callback
        """
        self.save_states()
        self.playback_bar.shutdown()
        self.library_tab.shutdown()
        write_config()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.shutdown()

    def call_on_search(self):
        self.playback_bar.call_on_search()
        self.library_tab.call_on_search()

    def call_on_clear_search(self):
        self.playback_bar.call_on_clear_search()
        self.library_tab.call_on_clear_search()
