import sys
import os

import configparser
import typing
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import QDir
from qt_material import apply_stylesheet

try:
    from src.apollo import Apollo
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from src.apollo import Apollo
from apollo.utils import getConfigParser, ROOT, ResourseGenerator, default_config
# END REGION

CONFIG = getConfigParser()
STYLED = True


def set_icons_theme(theme: typing.Dict, parent: typing.AnyStr = 'theme_customs'):
    # Replace the fill color to #0000ff for the compiler to work
    RESOURCES_PATH = os.path.join(ROOT, "assets", 'generated')
    if not os.path.isdir(os.path.join(RESOURCES_PATH, parent)):
        source = os.path.join(ROOT, 'assets', 'icons')
        resources = ResourseGenerator(
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


def style_app(app: QtWidgets.QApplication):
    apply_stylesheet(app, theme = CONFIG['DEFAULT']['current_theme'])
    with open(os.path.join(ROOT, 'assets', 'custom.css')) as file:
        stylesheet = app.styleSheet()
        set_icons_theme(os.environ, "theme_custom")
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    style_app(app)
    window = Apollo()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
