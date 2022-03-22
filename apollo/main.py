import configparser
import os
import sys
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import QDir
from qt_material import apply_stylesheet, ResourseGenerator, export_theme

from src.apollo import Apollo

PARENT_ROOT = os.path.dirname(__file__)
STYLED = True

if os.path.isfile(os.path.join(PARENT_ROOT, '.ini')):
    config = configparser.ConfigParser()
    config.read(os.path.join(PARENT_ROOT, '.ini'))
else:
    # create config file
    config = configparser.ConfigParser()
    config.read(os.path.join(PARENT_ROOT, '.ini'))


def set_icons_theme(theme, parent = 'theme_customs'):
    # Replace the fill color to #0000ff for the compiler to work
    HOME = Path.home()
    RESOURCES_PATH = os.path.join(HOME, '.qt_material')
    if not os.path.isdir(os.path.join(RESOURCES_PATH, parent)):
        source = os.path.join(PARENT_ROOT, 'assets', 'icons')
        resources = ResourseGenerator(primary = theme['QTMATERIAL_PRIMARYCOLOR'],
                                      secondary = theme['QTMATERIAL_SECONDARYCOLOR'],
                                      disabled = theme['QTMATERIAL_SECONDARYLIGHTCOLOR'],
                                      source = source,
                                      parent = parent)
        resources.generate()
    if os.path.isdir(os.path.join(RESOURCES_PATH, parent)):
        QDir.addSearchPath(parent, os.path.join(RESOURCES_PATH, parent))


def style_app(app):
    apply_stylesheet(app, theme = 'dark_teal.xml')
    stylesheet = app.styleSheet()
    with open(os.path.join(PARENT_ROOT, 'assets', 'custom.css')) as file:
        set_icons_theme(os.environ, "theme_custom")
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Apollo()
    if STYLED:
        window.play_pushbutton.clicked.connect(lambda x: style_app(app))
        style_app(app)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
