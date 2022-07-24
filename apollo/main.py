"""
Main entry point to execute Apollo
"""
import ctypes
import os
import sys

from PySide6 import QtWidgets


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from configs import settings


settings.setenv("PRODUCTION")
settings.validators.validate_all(only_current_env=True)


def main() -> None:
    """
    Main entry point to launch Apollo
    """

    from apollo.__version__ import __version__
    from apollo.assets.stylesheets import load_theme
    from apollo.src.app import Apollo
    from apollo.utils import get_logger

    # Enables App Icon in Taskbar
    myappid = f"apollo.apollo.player.{'_'.join(map(str, __version__))}"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    CONFIG = settings
    LOGGER = get_logger(__name__)

    app = QtWidgets.QApplication(sys.argv)
    load_theme(app, CONFIG.loaded_theme, recompile=CONFIG.recompile_theme)
    window = Apollo()
    LOGGER.info(msg="Application Started")
    window.UI.show()
    app.exec()
    LOGGER.info(msg="Application Exit")
    LOGGER.info(msg=settings.to_dict())


if __name__ == "__main__":
    main()
