import time

from pytestqt.qtbot import QtBot

from apollo.src.app import Apollo


class Test_Apollo_validate_startup:

    def test_init(self, get_apollo: (Apollo, QtBot)):
        app, bot = get_apollo
        app.show()
