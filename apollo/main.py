import sys
import os
import configparser
import typing
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import QDir
from qt_material import apply_stylesheet

try:
    from apollo.src.app import Apollo
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from apollo.src.app import Apollo
from apollo.utils import get_configparser, ROOT, ResourceGenerator
# END REGION


CONFIG = get_configparser()
STYLED = True


def set_icons_theme(theme: dict, parent: str = 'theme_customs') -> None:
    """
    Creates an icon pack for the given theme palette

    Note:
        Replace the fill color to #0000ff for the compiler to work
    Args:
        theme (dict): theme colors to replace placeholders with
        parent (str, optional): parent folder name
    """
    RESOURCES_PATH = os.path.join(ROOT, "assets", 'generated')
    if not os.path.isdir(os.path.join(RESOURCES_PATH, parent)):
        source = os.path.join(ROOT, 'assets', 'icons')
        resources = ResourceGenerator(
            root = RESOURCES_PATH,
            primary = theme['QTMATERIAL_PRIMARYCOLOR'],
            secondary = theme['QTMATERIAL_SECONDARYCOLOR'],
            disabled = theme['QTMATERIAL_SECONDARYLIGHTCOLOR'],
            source = source,
            parent = parent
        )
        resources.generate()
    if os.path.isdir(os.path.join(RESOURCES_PATH, parent)):
        QDir.addSearchPath(parent, os.path.join(RESOURCES_PATH, parent))


def style_app(app: QtWidgets.QApplication) -> None:
    """
    Applies the stylesheet to the application

    Args:
        app (QtWidgets.QApplication): Application
    """
    apply_stylesheet(app, theme = CONFIG['DEFAULT']['current_theme'])
    with open(os.path.join(ROOT, 'assets', 'custom.css')) as file:
        set_icons_theme(dict(os.environ), "theme_custom")
        stylesheet = app.styleSheet()
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))


def main() -> None:
    """
    Main entry point to launch Apollo
    """
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    style_app(app)
    window = Apollo()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
