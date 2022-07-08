import sys

from PySide6 import QtWidgets

from apollo.assets.stylesheets import load_theme
from apollo.src.app import Apollo
from apollo.utils import get_logger
from configs import settings

CONFIG = settings
LOGGER = get_logger(__name__)


def main() -> None:
    """
    Main entry point to launch Apollo
    """

    app = QtWidgets.QApplication(sys.argv)
    load_theme(app, CONFIG.loaded_theme, recompile=CONFIG.recompile_theme)
    window = Apollo()
    LOGGER.info(msg="Application Started")

    # TODO: Disable
    # window.playback_button_play_pause.pressed.connect(
    #     lambda: load_theme(app, name = CONFIG.loaded_theme, recompile = not CONFIG.recompile_theme)
    # )

    window.show()
    app.exec()
    LOGGER.info(msg="Application Exit")
    LOGGER.info(msg=settings.to_dict())


if __name__ == "__main__":
    main()
