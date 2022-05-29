import copy
import json
import os
import re
import shutil
import warnings
from pathlib import PurePath
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.utils import ApolloWarning, get_logger
from configs import settings

CONFIG = settings
LOGGER = get_logger(__name__)
ASSETS = PurePath(os.path.dirname(os.path.dirname(__file__)))

_JINJA = False
try:
    # noinspection PyUnresolvedReferences
    import jinja2
    # noinspection PyUnresolvedReferences
    from jinja2 import Environment
    # noinspection PyUnresolvedReferences
    from jinja2.loaders import FileSystemLoader

    _JINJA = True
except ImportError:
    _JINJA = False


# Template functions anv variable declaration --------------------------------------------------------------------------
def opacity(color: str, value: Optional[float] = 0.5) -> str:
    """
    Colour opacity filter

    Args:
        color (str): color
        value (Optional[float]): opacity value (0 to 1)

    Returns:
        str: rgba string
    """
    r, g, b = color[1:][0:2], color[1:][2:4], color[1:][4:]
    color = QtGui.QColor.fromRgb(int(r, 16), int(g, 16), int(b, 16))
    color.setAlphaF(value)
    return f"rgba({color.red()}, {color.green()}, {color.blue()}, {round(color.alphaF(), 3)})"


def luminosity(color: str, brightness: Optional[float] = 0) -> str:
    """
    Colour luminosity filter

    Args:
        color (str): color
        brightness (Optional[float]): luminosity value (-1 to 1)

    Returns:
        str: rgba string
    """
    r, g, b = color[1:][0:2], color[1:][2:4], color[1:][4:]
    r, g, b = int(r, 16), int(g, 16), int(b, 16)
    lumin = lambda x: int(min(255, (x + (255 * brightness))))
    return f'rgba({lumin(r)}, {lumin(g)}, {lumin(b)}, {float(1)})'


# End region -----------------------------------------------------------------------------------------------------------


# noinspection PyUnboundLocalVariable,SpellCheckingInspection,PyDictCreation
def get_stylesheet(colors: dict) -> str:
    """
    Generates stylesheet using jinja templates

    Args:
        colors (dict): Theme dict with UI colours

    Returns:
        str: compiled stylesheet
    """
    if not _JINJA:
        return ''

    theme = copy.deepcopy(colors)

    theme['FONT_FAMILY'] = 'Roboto'

    theme['FILTER_OPACITY'] = opacity
    theme['FILTER_LUMINOSITY'] = luminosity

    template_root = PurePath(os.path.dirname(__file__), 'templates')
    loader = jinja2.FileSystemLoader(template_root.as_posix())
    env = Environment(loader = loader, autoescape = False, trim_blocks = True, lstrip_blocks = True)

    template = env.get_template('main.css.jinja')
    rendered = template.render(theme)
    rendered, _ = re.subn('/\*.*\*/', '', rendered)
    rendered = rendered.replace(";\n", '; ').replace("{\n", '{ ').replace("    ", '')
    rendered = '\n'.join(filter(lambda x: x != '', rendered.splitlines()))

    return rendered


class ResourceGenerator:
    """
    Resource Generator that compiles and build the application stylesheet and icons
    """
    STYLESHEETS = PurePath(ASSETS, 'stylesheets')
    ICONS = PurePath(ASSETS, STYLESHEETS, 'icons')
    FONTS = PurePath(ASSETS, STYLESHEETS, 'fonts')
    THEMES = PurePath(ASSETS, STYLESHEETS, 'themes')
    GENERATED = PurePath(ASSETS, STYLESHEETS, 'generated')
    BUILD = PurePath(ASSETS, STYLESHEETS, 'build')

    # noinspection PyMissingConstructor,PyDictCreation,SpellCheckingInspection
    def __init__(self, name: str, theme: Optional[dict] = None):
        """
        Constructor

        Args:
            name (str): name the theme to load and generate
            theme (dict): Theme dict with UI colours
        """
        self.theme_name = name

        if theme is None:
            name += '.json'
            LOGGER.info(f"Loading {(self.THEMES / name)} theme")
            if os.path.exists(self.THEMES / name):
                with open(self.THEMES / name) as file:
                    theme = json.load(file)
            else:
                LOGGER.error(f"Loading {(self.THEMES / name)} theme failed")
                raise FileNotFoundError("Failed to load theme file")
        try:
            self.app_theme = {}
            self.app_theme['QTCOLOR_PRIMARYCOLOR'] = theme["primaryColor"]
            self.app_theme['QTCOLOR_PRIMARYLIGHTCOLOR'] = theme["primaryLightColor"]
            self.app_theme['QTCOLOR_PRIMARYDARKCOLOR'] = theme["primaryDarkColor"]
            self.app_theme['QTCOLOR_SECONDARYCOLOR'] = theme["secondaryColor"]
            self.app_theme['QTCOLOR_SECONDARYLIGHTCOLOR'] = theme["secondaryLightColor"]
            self.app_theme['QTCOLOR_SECONDARYDARKCOLOR'] = theme["secondaryDarkColor"]
            self.app_theme['QTCOLOR_PRIMARYTEXTCOLOR'] = theme["primaryTextColor"]
            self.app_theme['QTCOLOR_SECONDARYTEXTCOLOR'] = theme["secondaryTextColor"]
            self.app_theme['QTCOLOR_DANGER'] = '#DC3545'
            self.app_theme['QTCOLOR_WARNING'] = '#FFC107'
            self.app_theme['QTCOLOR_SUCCESS'] = '#17A2B8'
        except KeyError:
            raise KeyError("Theme dict has missing keys")

    def generate_theme_icons(self):
        """
        Uses the themes colours to generate the icon pack
        """
        rgba = lambda r, g, b, a: QtGui.QColor.fromRgb(r, g, b, a).name()
        primary = str(eval(luminosity(self.app_theme['QTCOLOR_PRIMARYTEXTCOLOR'], 0.4)))
        secondary = str(eval(luminosity(self.app_theme['QTCOLOR_SECONDARYLIGHTCOLOR'], 0.4)))
        disabled = str(eval(luminosity(self.app_theme['QTCOLOR_PRIMARYLIGHTCOLOR'], 0.5)))
        success = str(eval(luminosity(self.app_theme['QTCOLOR_SUCCESS'], 0.1)))
        warning = str(eval(luminosity(self.app_theme['QTCOLOR_WARNING'], 0)))
        danger = str(eval(luminosity(self.app_theme['QTCOLOR_DANGER'], 0)))

        self._validate_output_dir()
        for _dir, _sdir, _files in os.walk(self.ICONS):
            for file in filter(lambda ext: str(os.path.splitext(ext)[1]).lower() == '.svg', _files):
                with open(PurePath(_dir, file)) as svg_file:
                    content = svg_file.read()
                    with open((self.GENERATED / 'icons' / 'primary' / file), 'w') as file_output:
                        file_output.write(self.replace_svg_colour(content, primary))
                    with open((self.GENERATED / 'icons' / 'secondary' / file), 'w') as file_output:
                        file_output.write(self.replace_svg_colour(content, secondary))
                    with open((self.GENERATED / 'icons' / 'disabled' / file), 'w') as file_output:
                        file_output.write(self.replace_svg_colour(content, disabled))
                    with open((self.GENERATED / 'icons' / 'success' / file), 'w') as file_output:
                        file_output.write(self.replace_svg_colour(content, success))
                    with open((self.GENERATED / 'icons' / 'warning' / file), 'w') as file_output:
                        file_output.write(self.replace_svg_colour(content, warning))
                    with open((self.GENERATED / 'icons' / 'danger' / file), 'w') as file_output:
                        file_output.write(self.replace_svg_colour(content, danger))

    @staticmethod
    def replace_svg_colour(content: str, replace: str, placeholder: Optional[str] = '#0000FF') -> str:
        """
        Replaces the placeholder fill colour in svg files

        Args:
            content (str): content of the read svg file
            replace (str): replacement colour
            placeholder (str): placeholder colour

        Returns:
            str: modified contents of the svg file
        """
        content = content.replace(placeholder.upper(), replace)
        content = content.replace(placeholder.lower(), replace)
        replace = '#ffffff00'
        placeholder = '#000000'
        content = content.replace(placeholder, replace)
        return content

    def generate_theme_stylesheet(self) -> str:
        """
        Generates and saves the compiles stylesheet into a file

        Returns:
            str: compiled stylesheet
        """
        self._validate_output_dir()
        stylesheet = get_stylesheet(self.app_theme)
        with open(self.GENERATED / 'stylesheet.css', 'w') as css:
            css.write(stylesheet)
        return stylesheet

    def build_theme(self):
        """
        Builds the theme pack for the application
        """
        self.generate_theme_icons()
        self.generate_theme_stylesheet()

    def package_theme(self):
        """
        Packages the generated theme pack into a theme zip
        """
        path = self.BUILD
        if not os.path.exists(path):
            os.mkdir(path)
        shutil.make_archive((path / self.theme_name).as_posix(), 'zip', self.GENERATED)
        shutil.rmtree(self.GENERATED)

    def _validate_output_dir(self):
        """
        Validates the output directory for the theme pack
        """
        paths = (self.GENERATED, self.GENERATED / 'icons', self.GENERATED / 'icons' / 'primary',
                 self.GENERATED / 'icons' / 'secondary', self.GENERATED / 'icons' / 'disabled',
                 self.GENERATED / 'icons' / 'success', self.GENERATED / 'icons' / 'warning',
                 self.GENERATED / 'icons' / 'danger',)
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

        path = self.GENERATED / 'stylesheet.css'
        if not os.path.exists(path):
            with open(path, 'w') as file:
                file.close()


def load_theme(app: QtWidgets.QApplication, name: str, recompile: Optional[bool] = False):
    """
    Loads the theme into the applicationto display

    Args:
        app (QtWidgets.QApplication): QtApplication
        name (str): theme pack name
        recompile (Optional[Boolean]): Recompile resources
    """

    def loader(_loaded_theme: PurePath):
        if os.path.exists(_loaded_theme):
            QtCore.QDir.addSearchPath('icons_primary', (_loaded_theme / 'icons' / 'primary').as_posix())
            QtCore.QDir.addSearchPath('icons_secondary', (_loaded_theme / 'icons' / 'secondary').as_posix())
            QtCore.QDir.addSearchPath('icons_disabled', (_loaded_theme / 'icons' / 'disabled').as_posix())
            QtCore.QDir.addSearchPath('icons_success', (_loaded_theme / 'icons' / 'success').as_posix())
            QtCore.QDir.addSearchPath('icons_danger', (_loaded_theme / 'icons' / 'danger').as_posix())
            QtCore.QDir.addSearchPath('icons_warning', (_loaded_theme / 'icons' / 'warning').as_posix())
            filtr = filter(lambda ext: os.path.splitext(ext)[1].lower() == '.ttf', os.listdir(ResourceGenerator.FONTS))
            for file in filtr:
                QtGui.QFontDatabase.addApplicationFont((ResourceGenerator.FONTS / str(file)).as_posix())

            with open(_loaded_theme / 'stylesheet.css') as file_output:
                app.setStyleSheet(file_output.read())
                app.setStyle('Fusion')

    app_theme = ASSETS / 'app_themes'
    loaded_theme = app_theme / '__loaded_theme__'
    theme_zip = app_theme / (name + '.zip')

    if not os.path.exists(loaded_theme):
        os.mkdir(loaded_theme)

    if not os.path.exists(theme_zip) or recompile:
        if ((name + '.json') in os.listdir(ResourceGenerator.THEMES)) and _JINJA:
            res = ResourceGenerator(name)
            res.build_theme()
            res.package_theme()
            shutil.move(res.BUILD / (name + '.zip'), theme_zip)
            shutil.rmtree(res.BUILD)
        else:
            if not (name + '.json') in os.listdir(ResourceGenerator.THEMES):
                ApolloWarning("Theme JSON missing")

            if not _JINJA:
                ApolloWarning('Failed to build theme pack, Jinja is Missing')

    if os.path.exists(theme_zip):
        if os.path.exists((loaded_theme / 'icons')):
            shutil.rmtree(loaded_theme / 'icons')
        if os.path.exists((loaded_theme / 'stylesheet.css')):
            os.remove(loaded_theme / 'stylesheet.css')
        shutil.unpack_archive(theme_zip, loaded_theme)
        loader(loaded_theme)
