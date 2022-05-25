import os
import sys

from PySide6 import QtCore, QtWidgets

try:
    import apollo
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from apollo.src.app import Apollo
from apollo.utils import get_logger
from apollo.assets.stylesheets import load_theme
from configs import settings

CONFIG = settings
settings.setenv("production")
settings.validators.validate()
LOGGER = get_logger(__name__)


def main() -> None:
    """
    Main entry point to launch Apollo

    TODO: add support for hour long tracks
    """
    app = QtWidgets.QApplication(sys.argv)
    window = Apollo()
    LOGGER.info(msg = "Application Started")
    load_theme(app, CONFIG.loaded_theme, recompile = CONFIG.recompile_theme)

    # TODO: Disable
    # window.playback_button_play_pause.pressed.connect(lambda: load_theme(app, recompile = CONFIG.recompile_theme))

    window.show()
    app.exec()


if __name__ == '__main__':
    main()
