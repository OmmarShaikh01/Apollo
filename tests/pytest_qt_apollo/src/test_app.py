import time

from pytestqt.qtbot import QtBot

from apollo.src.app import Apollo
from tests.testing_utils import screenshot_widget


class Test_Apollo_validate_startup:

    def test_init(self, get_apollo: (Apollo, QtBot)):
        app, bot = get_apollo
        screenshot_widget(app, "test_init")
        app.close()
