from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets
import pytest
import pytest_mock
from PySide6 import QtCore, QtWidgets
from pytestqt.qtbot import QtBot

from apollo.layout.mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.src.tabs.playback_bar import TrackRatingWidget, Playback_Bar
from apollo.utils import get_logger
from configs import settings
from tests.testing_utils import screenshot_widget

CONFIG = settings
LOGGER = get_logger(__name__)


class Apollo_MOCK(Apollo_MainWindow, QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.sub_tabs = None


@pytest.fixture
def get_TrackRatingWidget(qtbot) -> tuple[TrackRatingWidget, QtBot]:
    bot = qtbot
    app = TrackRatingWidget()
    app.setMaximumSize(QtCore.QSize(100, 28))
    return app, bot


@pytest.fixture
def get_Playback_Bar(qtbot) -> tuple[Apollo_MOCK, QtBot]:
    bot = qtbot
    app = Apollo_MOCK()
    app.sub_tabs = Playback_Bar(app)
    app.setScreen(QtWidgets.QApplication.screens()[0])
    app.showFullScreen()
    app.closeEvent = lambda eve: (app.sub_tabs.shutdown())
    return app, bot

@pytest.mark.skip
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
            bot.mousePress(app, QtCore.Qt.LeftButton, pos = QtCore.QPoint(int(app.width() / 2), 14))
            assert app._rating == 2.5
            screenshot_widget(app, "Test_TrackRatingWidget.test_change_rating_mouse")
        app.close()


class Test_Playback_Bar:

    def test_init(self, get_Playback_Bar: (Apollo_MOCK, QtBot)):
        app, bot = get_Playback_Bar

        screenshot_widget(app, "Test_Playback_Bar.test_init")
        app.close()

    def test_default_startup(self, get_Playback_Bar: (Apollo_MOCK, QtBot)):
        app, bot = get_Playback_Bar

        screenshot_widget(app, "Test_Playback_Bar.test_default_startup")
        app.close()

    def test_default_interactions(self, get_Playback_Bar: (Apollo_MOCK, QtBot), mocker: pytest_mock.MockerFixture):
        app, bot = get_Playback_Bar

        screenshot_widget(app, "Test_Playback_Bar.test_default_interactions")
        mocked_obj = lambda *x, **kx: LOGGER.info(f"MOCKED args: {x}, kwargs: {kx}")

        mocker.patch.object(app.sub_tabs, 'call_state_change_play', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_state_change_play')
        app.playback_button_play_pause.click()
        spy.assert_called_with('PLAY')
        app.playback_button_play_pause.click()
        spy.assert_called_with('PAUSE')

        mocker.patch.object(app.sub_tabs, 'call_state_change_shuffle', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_state_change_shuffle')
        app.playback_button_play_shuffle.click()
        spy.assert_called_with("SHUFFLE")
        app.playback_button_play_shuffle.click()
        spy.assert_called_with("NONE")

        mocker.patch.object(app.sub_tabs, 'call_state_change_repeat', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_state_change_repeat')
        app.playback_button_play_repeat.click()
        spy.assert_called_with('REPEAT')
        app.playback_button_play_repeat.click()
        spy.assert_called_with('REPEAT_ONE')
        app.playback_button_play_repeat.click()
        spy.assert_called_with('NONE')

        mocker.patch.object(app.sub_tabs, 'call_state_change_volume_level', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_state_change_volume_level')
        app.playback_slider_volume_control.setValue(0)
        spy.assert_called_with(0)
        assert app.playback_button_volume_control.property('STATE_VOLUME_LEVEL') == 'MUTE'
        app.playback_slider_volume_control.setValue(25)
        spy.assert_called_with(25)
        assert app.playback_button_volume_control.property('STATE_VOLUME_LEVEL') == 'QUARTER'
        app.playback_slider_volume_control.setValue(50)
        spy.assert_called_with(50)
        assert app.playback_button_volume_control.property('STATE_VOLUME_LEVEL') == 'HALF'
        app.playback_slider_volume_control.setValue(99)
        spy.assert_called_with(99)
        assert app.playback_button_volume_control.property('STATE_VOLUME_LEVEL') == 'FULL'

        mocker.patch.object(app.sub_tabs, 'call_state_change_volume_level', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_state_change_volume_level')
        app.playback_button_volume_control.click()
        assert app.playback_slider_volume_control.value() == 0
        spy.assert_called_with(0)
        app.playback_button_volume_control.click()
        assert app.playback_slider_volume_control.value() == 25
        spy.assert_called_with(25)
        app.playback_button_volume_control.click()
        assert app.playback_slider_volume_control.value() == 50
        spy.assert_called_with(50)
        app.playback_button_volume_control.click()
        assert app.playback_slider_volume_control.value() == 99
        spy.assert_called_with(99)

        mocker.patch.object(app.sub_tabs, 'call_track_prev', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_track_prev')
        app.playback_button_prev.click()
        assert spy.called

        mocker.patch.object(app.sub_tabs, 'call_track_next', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_track_next')
        app.playback_button_next.click()
        assert spy.called

        mocker.patch.object(app.sub_tabs, 'call_bypass_processor', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_bypass_processor')
        app.playback_button_audio_bypass.click()
        assert spy.called

        mocker.patch.object(app.sub_tabs, 'call_state_change_seek_slider', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_state_change_seek_slider')
        app.playback_footer_track_seek_slider.setValue(int(app.playback_footer_track_seek_slider.maximum() / 2))
        assert spy.called

        mocker.patch.object(app.sub_tabs, 'call_track_rating', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_track_rating')
        app.playback_footer_track_rating.setRating(4)
        assert spy.called
        spy.assert_called_with(4)

        mocker.patch.object(app.sub_tabs, 'call_on_shutdown', mocked_obj)
        spy = mocker.spy(app.sub_tabs, 'call_on_shutdown')
        app.close()
        assert spy.called
