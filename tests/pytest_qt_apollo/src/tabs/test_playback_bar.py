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


@pytest.fixture
def get_TrackRatingWidget(qtbot) -> tuple[TrackRatingWidget, QtBot]:
    bot = qtbot
    app = TrackRatingWidget()
    app.setMaximumSize(QtCore.QSize(100, 28))
    return app, bot


class Test_TrackRatingWidget:
    def test_init(self, get_TrackRatingWidget: (TrackRatingWidget, QtBot)):
        app, bot = get_TrackRatingWidget
        screenshot_widget(app, "Test_TrackRatingWidget.test_init")
        app.close()

    def test_change_rating(self, get_TrackRatingWidget: (TrackRatingWidget, QtBot)):
        app, bot = get_TrackRatingWidget

        app.setRating(0)
        screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating.0")
        app.setRating(2)
        screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating.2")
        app.setRating(2.5)
        screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating.2_5")
        app.setRating(5)
        screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating.5")

        with bot.wait_signal(app.RatingChangedSignal):
            app.setRating(5)
        app.close()

    def test_change_rating_mouse(self, get_TrackRatingWidget: (TrackRatingWidget, QtBot)):
        app, bot = get_TrackRatingWidget

        with bot.wait_signal(app.RatingChangedSignal):
            bot.mouseMove(app, QtCore.QPoint(int(app.width() / 2), 14))
            bot.mousePress(app, QtCore.Qt.LeftButton, pos=QtCore.QPoint(int(app.width() / 2), 14))
            assert app._rating == 2.5
            screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating_mouse")
        app.close()


class Test_Playback_Bar(Setup_Apollo):
    def test_1(self):
        pass
