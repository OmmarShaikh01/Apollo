import os
import sys

from PySide6 import QtCore, QtWidgets

from configs import settings
from apollo.src.app import Apollo
from apollo.utils import get_logger
from apollo.assets.stylesheets import load_theme

CONFIG = settings
LOGGER = get_logger(__name__)


def main() -> None:
    """
    Main entry point to launch Apollo
    """

    app = QtWidgets.QApplication(sys.argv)
    window = Apollo()
    LOGGER.info(msg = "Application Started")
    load_theme(app, CONFIG.loaded_theme, recompile = CONFIG.recompile_theme)

    # TODO: Disable
    # window.playback_button_play_pause.pressed.connect(
    #     lambda: load_theme(app, name = CONFIG.loaded_theme, recompile = not CONFIG.recompile_theme)
    # )

    window.show()
    app.exec()
    LOGGER.info(msg = "Application Exit")
    LOGGER.info(msg = settings.to_dict())


if __name__ == '__main__':
    main()
