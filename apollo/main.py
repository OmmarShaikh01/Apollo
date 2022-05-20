import os
import sys

import qt_material
from PySide6 import QtWidgets
from PySide6.QtCore import QDir
from qt_material import apply_stylesheet

try:
    from apollo.src.app import Apollo
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from apollo.src.app import Apollo
from apollo.utils import get_configparser, get_logger, ROOT, ResourceGenerator

# END REGION


CONFIG = get_configparser()
LOGGER = get_logger(__name__)
STYLED = True


# noinspection SpellCheckingInspection
def set_icons_theme(theme: dict, parent: str = 'theme_customs') -> None:
    """
    Creates an icon pack for the given theme palette

    Note:
        Replace the fill color to #0000ff for the compiler to work
    Args:
        theme (dict): theme colors to replace placeholders with
        parent (str, optional): parent folder name
    """
    resources_path = os.path.join(ROOT, "assets", 'generated')
    if not os.path.isdir(os.path.join(resources_path, parent)):
        source = os.path.join(ROOT, 'assets', 'icons')
        resources = ResourceGenerator(root = resources_path, primary = theme['QTMATERIAL_PRIMARYCOLOR'],
                secondary = theme['QTMATERIAL_SECONDARYCOLOR'], disabled = theme['QTMATERIAL_SECONDARYLIGHTCOLOR'],
                source = source, parent = parent)
        resources.generate()
    if os.path.isdir(os.path.join(resources_path, parent)):
        QDir.addSearchPath(parent, os.path.join(resources_path, parent))


def style_app(app: QtWidgets.QApplication) -> None:
    """
    Applies the stylesheet to the application

    Args:
        app (QtWidgets.QApplication): Application
    """
    apply_stylesheet(app, theme = CONFIG['GLOBALS']['current_theme'])
    with open(os.path.join(ROOT, 'assets', 'custom.css')) as file:
        set_icons_theme(dict(os.environ), "theme_custom")
        stylesheet = app.styleSheet()
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))


def main() -> None:
    """
    Main entry point to launch Apollo

    TODO: add support for hour long tracks
    """
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    style_app(app)
    window = Apollo()
    window.show()
    LOGGER.info(msg = "Application Started")
    app.exec()


if __name__ == '__main__':
    main()
