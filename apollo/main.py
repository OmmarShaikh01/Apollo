"""
Main entry point to execute Apollo
"""
import ctypes
import json
import sys

from PySide6 import QtWidgets

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
    from apollo.utils import get_logger, set_dark_title_bar

    CONFIG = settings
    LOGGER = get_logger(__name__)

    app = QtWidgets.QApplication(sys.argv)
    load_theme(app, CONFIG.loaded_theme, recompile=CONFIG.recompile_theme)
    LOGGER.info(msg="Application Started")
    window = Apollo()

    # Enables App Icon in Taskbar
    WINDLL = ctypes.windll
    myappid = f"apollo.apollo.player.{'_'.join(map(str, __version__))}"
    WINDLL.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    set_dark_title_bar(window.UI)

    window.UI.show()
    window.UI.raise_()
    window.UI.setFocus()
    window.UI.showMaximized()

    app.exec()
    LOGGER.info(msg="Application Exit")
    LOGGER.info(msg=f"\n{json.dumps(settings.to_dict(), indent=2)}")


if __name__ == "__main__":
    main()
