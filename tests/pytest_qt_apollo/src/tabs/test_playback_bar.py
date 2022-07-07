from PySide6 import QtCore, QtWidgets

from apollo.src.app import Apollo
from apollo.utils import get_logger
from configs import settings
from tests.pytest_qt_apollo.conftest import clean_temp_dir, copy_mock_data, remove_local_config

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


class Test_Playback_Bar(Setup_Apollo):

    def test_1(self):
        pass
