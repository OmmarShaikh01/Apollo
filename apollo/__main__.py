"""
Main entry point to execute Apollo as a Package
"""
import ctypes
import json
import os
import sys

from PySide6 import QtWidgets


# pylint: disable=C0415,C0103
def main() -> None:
    """
    Main entry point to launch Apollo
    """
    # adds project root to system path
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

    # enables code to run in reoduction
    from configs import settings as CONFIG

    CONFIG.setenv("PRODUCTION")
    CONFIG.validators.validate_all(only_current_env=True)

    from apollo.__version__ import __version__
    from apollo.app.main import Apollo
    from apollo.assets.stylesheets import load_theme
    from apollo.utils import get_logger

    LOGGER = get_logger(__name__)

    app = QtWidgets.QApplication(sys.argv)
    load_theme(app, CONFIG.loaded_theme, recompile=CONFIG.recompile_theme)
    LOGGER.info(msg="Application Started")
    window = Apollo()

    # Enables App Icon in Taskbar
    WINDLL = ctypes.windll
    myappid = f"apollo.apollo.player.{'_'.join(map(str, __version__))}"
    WINDLL.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window.UI.show()
    window.UI.raise_()
    window.UI.setFocus()
    window.UI.showMaximized()

    app.exec()
    LOGGER.info(msg="Application Exit")
    LOGGER.debug(msg=f"\n{json.dumps(CONFIG.to_dict(), indent=2)}")


if __name__ == "__main__":
    main()
