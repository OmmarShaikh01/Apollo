import pyautogui
from PySide6 import QtCore, QtGui, QtWidgets
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from apollo.src.app import Apollo
from apollo.src.tabs.library import Library_Tab
from apollo.src.views.delegates import ViewDelegates
from apollo.utils import get_logger
from configs import settings
from tests.pytest_qt_apollo.conftest import clean_temp_dir, copy_mock_data, remove_local_config
from tests.testing_utils import screenshot_widget


CONFIG = settings
LOGGER = get_logger(__name__)


class Test_Apollo_Library:
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
            screenshot_widget(self.APOLLO.UI, "Test_Apollo_Library.test_startup")
            assert self.APOLLO.UI.isVisible()

    def test_view_scroll_events(self, mocker: MockerFixture):
        view = self.APOLLO.UI.library_main_listview
        model = self.APOLLO._LIBRARY.library_model
        spy_1 = mocker.spy(self.APOLLO._LIBRARY.library_model, "fetch_data")
        view.scrollToBottom()
        spy_1.assert_called_with(model.FETCH_DATA_DOWN)
        assert spy_1.return_value

        spy_1 = mocker.spy(self.APOLLO._LIBRARY.library_model, "fetch_data")
        view.scrollToBottom()
        view.scrollToBottom()
        view.scrollToTop()
        spy_1.assert_called_with(model.FETCH_DATA_UP)
        assert spy_1.return_value

    def test_view_delegates(self, mocker: MockerFixture):
        self.APOLLO._LIBRARY.set_model_delegate(self.APOLLO.UI.library_main_listview)
        assert self.APOLLO._LIBRARY._DELEGATE_TYPE == "TrackDelegate_Small"
        screenshot_widget(self.APOLLO.UI, "Test_Apollo_Library.test_view_delegate.None")

        self.APOLLO._LIBRARY.set_model_delegate(
            self.APOLLO.UI.library_main_listview, ViewDelegates.TrackDelegate_Small
        )
        assert self.APOLLO._LIBRARY._DELEGATE_TYPE == "TrackDelegate_Small"
        screenshot_widget(
            self.APOLLO.UI, "Test_Apollo_Library.test_view_delegate.TrackDelegate_Small"
        )

        self.APOLLO._LIBRARY.set_model_delegate(
            self.APOLLO.UI.library_main_listview, ViewDelegates.TrackDelegate_Mid
        )
        assert self.APOLLO._LIBRARY._DELEGATE_TYPE == "TrackDelegate_Mid"
        screenshot_widget(
            self.APOLLO.UI, "Test_Apollo_Library.test_view_delegate.TrackDelegate_Mid"
        )

    def test_view_item_doubleclick(self, qtbot: QtBot, mocker: MockerFixture):
        spy_1 = mocker.spy(self.APOLLO._LIBRARY, "cb_list_item_clicked")
        view = self.APOLLO.UI.library_main_listview
        self.APOLLO._LIBRARY.set_model_delegate(view, ViewDelegates.TrackDelegate_Mid)
        pos = view.viewport().mapToGlobal(QtCore.QPoint(10, 10))
        with qtbot.wait_signal(view.doubleClicked, timeout=1000):
            pyautogui.doubleClick(pos.x(), pos.y())
        spy_1.assert_called_with(view.indexAt(QtCore.QPoint(10, 10)))
