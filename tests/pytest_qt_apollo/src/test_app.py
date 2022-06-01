import time

import pytest
from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from apollo.src.app import Apollo
from apollo.utils import get_logger
from configs import settings
from tests.testing_utils import screenshot_widget

CONFIG = settings
LOGGER = get_logger(__name__)


@pytest.fixture
def get_apollo(qtbot) -> tuple[Apollo, QtBot]:
    APOLLO = Apollo()
    APOLLO.setScreen(QtWidgets.QApplication.screens()[0])
    APOLLO.showFullScreen()
    return APOLLO, qtbot


class Test_Apollo:

    def test_init(self, get_apollo: (Apollo, QtBot)):
        app, bot = get_apollo
        screenshot_widget(app, "Test_Apollo.test_init")
        app.close()

    def test_default_startup(self, get_apollo: (Apollo, QtBot)):
        app, bot = get_apollo

        assert app.main_tabs_stack_widget.currentIndex() == 0

        screenshot_widget(app, "Test_Apollo.test_default_startup")
        app.close()

    def test_default_interactions(self, get_apollo: (Apollo, QtBot)):
        app, bot = get_apollo

        app.library_tab_switch_button.click()
        assert app.main_tabs_stack_widget.currentIndex() == 0
        screenshot_widget(app, "Test_Apollo.test_default_interactions.tab_0")

        app.now_playing_tab_switch_button.click()
        assert app.main_tabs_stack_widget.currentIndex() == 1
        screenshot_widget(app, "Test_Apollo.test_default_interactions.tab_1")

        app.playlist_tab_switch_button.click()
        assert app.main_tabs_stack_widget.currentIndex() == 2
        screenshot_widget(app, "Test_Apollo.test_default_interactions.tab_2")

        app.audiofx_tab_switch_button.click()
        assert app.main_tabs_stack_widget.currentIndex() == 3
        screenshot_widget(app, "Test_Apollo.test_default_interactions.tab_3")

        app.close()
