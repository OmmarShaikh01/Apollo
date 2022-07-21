from PySide6 import QtCore, QtGui, QtWidgets
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from apollo.src.app import Apollo
from apollo.utils import get_logger
from configs import settings
from tests.pytest_qt_apollo.conftest import clean_temp_dir, copy_mock_data, remove_local_config
from tests.testing_utils import screenshot_widget


CONFIG = settings
LOGGER = get_logger(__name__)


class Test_Apollo:
    def setup_class(self):
        copy_mock_data()
        self.APOLLO = Apollo()
        self.APOLLO.UI.setScreen(QtWidgets.QApplication.screens()[0])
        self.APOLLO.UI.move(QtCore.QPoint(0, 0))
        self.APOLLO.UI.showFullScreen()

    def teardown_class(self):
        self.APOLLO.UI.close()
        del self.APOLLO
        clean_temp_dir()
        remove_local_config()
        QtWidgets.QApplication.closeAllWindows()

    def test_startup(self, qtbot: QtBot):
        with qtbot.waitActive(self.APOLLO.UI, timeout=5000):
            screenshot_widget(self.APOLLO.UI, "Test_App.test_startup")
            assert self.APOLLO.UI.isVisible()

    def test_tab_button_clicked(self):
        self.APOLLO.UI.library_tab_switch_button.click()
        assert self.APOLLO.UI.main_tabs_stack_widget.currentIndex() == 0
        self.APOLLO.UI.now_playing_tab_switch_button.click()
        assert self.APOLLO.UI.main_tabs_stack_widget.currentIndex() == 1
        self.APOLLO.UI.playlist_tab_switch_button.click()
        assert self.APOLLO.UI.main_tabs_stack_widget.currentIndex() == 2
        self.APOLLO.UI.audiofx_tab_switch_button.click()
        assert self.APOLLO.UI.main_tabs_stack_widget.currentIndex() == 3

    def test_cb_shutdown(self, mocker: MockerFixture):
        spy_1 = mocker.spy(self.APOLLO.UI, "closeEvent")
        spy_2 = mocker.spy(self.APOLLO, "cb_shutdown")
        self.APOLLO.UI.library_tab_switch_button.click()
        self.APOLLO.UI.closeEvent(QtGui.QCloseEvent())
        assert CONFIG["APOLLO.MAIN.CURRENT_TAB"] == 0
        assert spy_1.called and spy_2.called
