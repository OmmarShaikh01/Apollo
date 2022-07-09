from PySide6 import QtCore, QtWidgets
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from apollo.src.app import Apollo
from apollo.utils import get_logger
from configs import settings
from tests.pytest_qt_apollo.conftest import clean_temp_dir, copy_mock_data, remove_local_config
from tests.testing_utils import screenshot_widget


CONFIG = settings
LOGGER = get_logger(__name__)


class Setup_Apollo:
    def setup_class(self):
        copy_mock_data()
        APOLLO = Apollo()
        APOLLO.setScreen(QtWidgets.QApplication.screens()[0])
        APOLLO.move(QtCore.QPoint(0, 0))
        APOLLO.showFullScreen()
        # noinspection PyAttributeOutsideInit
        self._application_apollo = APOLLO

    def teardown_class(self):
        del self._application_apollo
        clean_temp_dir()
        remove_local_config()


class Test_App(Setup_Apollo):
    def test_startup(self, qtbot: QtBot):
        with qtbot.waitActive(self._application_apollo, timeout=5000):
            screenshot_widget(self._application_apollo, "Test_App.test_startup")
            assert self._application_apollo.isVisible()

    def test_startup_defaults(self, qtbot: QtBot):
        self._application_apollo.setup_defaults()
        assert self._application_apollo.main_tabs_stack_widget.currentIndex() == 0

    def test_startup_interactions(self, qtbot: QtBot, mocker: MockerFixture):
        spy = mocker.spy(self._application_apollo.main_tabs_stack_widget, "setCurrentIndex")
        self._application_apollo.library_tab_switch_button.click()
        spy.assert_called_with(0)
        self._application_apollo.now_playing_tab_switch_button.click()
        spy.assert_called_with(1)
        self._application_apollo.playlist_tab_switch_button.click()
        spy.assert_called_with(2)
        self._application_apollo.audiofx_tab_switch_button.click()
        spy.assert_called_with(3)

        mocker.patch.object(self._application_apollo, "call_on_search", lambda: None)
        mocker.patch.object(self._application_apollo, "call_on_clear_search", lambda: None)

        spy = mocker.spy(self._application_apollo, "call_on_search")
        self._application_apollo.search_lineEdit.setText("TEST")
        self._application_apollo.search_button.click()
        spy.assert_called()

        spy = mocker.spy(self._application_apollo, "call_on_clear_search")
        self._application_apollo.search_lineEdit.setText("")
        self._application_apollo.search_button.click()
        spy.assert_called()

    def test_shutdown(self):
        # set states
        self._application_apollo.audiofx_tab_switch_button.click()
        self._application_apollo.close()

        assert CONFIG["APOLLO.MAIN.CURRENT_TAB"] == 3
