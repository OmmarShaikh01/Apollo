import pyautogui
import pytest
from PySide6 import QtCore, QtWidgets
from pytestqt.qtbot import QtBot

from apollo.src.app import Apollo
from apollo.src.tabs.playback_bar import TrackRatingWidget
from apollo.utils import get_logger
from configs import settings
from tests.pytest_qt_apollo.conftest import clean_temp_dir, copy_mock_data, remove_local_config
from tests.testing_utils import screenshot_widget


CONFIG = settings
LOGGER = get_logger(__name__)


@pytest.fixture
def get_TrackRatingWidget(qtbot) -> tuple[TrackRatingWidget, QtBot]:
    bot = qtbot
    app = TrackRatingWidget()
    bot.addWidget(app)
    app.setScreen(QtWidgets.QApplication.screens()[0])
    app.setMaximumSize(QtCore.QSize(100, 28))
    app.setMinimumSize(QtCore.QSize(100, 28))
    app.move(QtCore.QPoint(0, 0))
    app.showFullScreen()
    yield app, bot
    app.close()
    QtWidgets.QApplication.closeAllWindows()


class Test_TrackRatingWidget:
    def test_init(self, get_TrackRatingWidget: (TrackRatingWidget, QtBot)):
        app, qtbot = get_TrackRatingWidget

        screenshot_widget(app, "Test_TrackRatingWidget.test_init")

    def test_change_rating(self, get_TrackRatingWidget: (TrackRatingWidget, QtBot)):
        app, qtbot = get_TrackRatingWidget

        app.setRating(0)
        screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating.0")
        app.setRating(2)
        screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating.2")
        app.setRating(2.5)
        screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating.2_5")
        app.setRating(5)
        screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating.5")

        with qtbot.wait_signal(app.RatingChangedSignal):
            app.setRating(5)

    def test_change_rating_mouse(self, get_TrackRatingWidget: (TrackRatingWidget, QtBot)):
        app, qtbot = get_TrackRatingWidget
        pos = app.mapToGlobal(app.rect().center())
        with qtbot.wait_signal(app.RatingChangedSignal):
            pyautogui.click(pos.x(), pos.y())
            qtbot.wait(100)
            assert app._rating == 2.5
            screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating_mouse")


@pytest.mark.skip
class Test_Apollo_Playback_Bar:
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

    def test_1(self):
        pass
