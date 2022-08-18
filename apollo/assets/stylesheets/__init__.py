import copy
import json
import os
import re
import shutil
from pathlib import PurePath
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.utils import ApolloWarning, get_logger


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


# Template functions anv variable declaration ---------------------------------
def opacity(
    color: str, value: Optional[float] = 0.5, as_str: Optional[bool] = True
) -> Union[QtGui.QColor, str]:
    """
    Colour opacity filter

    Args:
        color (str): color
        value (Optional[float]): opacity value (0 to 1)
        as_str (Optional[bool]): set true to return value as str

    Returns:
        str: rgba string
        QtGui.QColor: Colour object
    """
    r, g, b = color[1:][0:2], color[1:][2:4], color[1:][4:]
    color = QtGui.QColor.fromRgbF(int(r, 16), int(g, 16), int(b, 16), value)

    if as_str:
        return f"rgba({color.red()}, {color.green()}, {color.blue()}, {round(color.alphaF(), 3)})"
    return color


def luminosity(
    color: str, brightness: Optional[float] = 0, as_str: Optional[bool] = True
) -> Union[QtGui.QColor, str]:
    """
    Colour luminosity filter

    Args:
        color (str): color
        brightness (Optional[float]): luminosity value (-1 to 1)
        as_str (Optional[bool]): set true to return value as str

    Returns:
        str: rgba string
        QtGui.QColor: Colour object
    """
    r, g, b = color[1:][0:2], color[1:][2:4], color[1:][4:]
    r, g, b = int(r, 16), int(g, 16), int(b, 16)
    # pylint: disable=C3001
    lumin = lambda x: int(min(255, (x + (255 * brightness))))
    color = QtGui.QColor.fromRgb(lumin(r), lumin(g), lumin(b))

    if as_str:
        return f"rgba({color.red()}, {color.green()}, {color.blue()}, {float(1)})"
    return color


# End region ------------------------------------------------------------------


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
        return ""

    theme = copy.deepcopy(colors)

    theme["FONT_FAMILY"] = "Roboto"
    theme["FILTER_OPACITY"] = opacity
    theme["FILTER_LUMINOSITY"] = luminosity

    template_root = PurePath(os.path.dirname(__file__), "templates")
    loader = jinja2.FileSystemLoader(template_root.as_posix())
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    template = env.get_template("main.css.jinja")
    rendered = template.render(theme)
    rendered, _ = re.subn(r"/\*.*\*/", "", rendered)
    rendered = (
        rendered.replace(";\n", "; ").replace(",\n", ", ").replace("{\n", "{ ").replace("    ", "")
    )
    rendered = "\n".join(filter(lambda x: x != "", rendered.splitlines()))

    return rendered


class ResourceGenerator:
    """
    Resource Generator that compiles and build the application stylesheet and icons
    """

    STYLESHEETS = PurePath(ASSETS, "stylesheets")
    ICONS = PurePath(ASSETS, STYLESHEETS, "icons")
    FONTS = PurePath(ASSETS, STYLESHEETS, "fonts")
    THEMES = PurePath(ASSETS, STYLESHEETS, "themes")
    GENERATED = PurePath(ASSETS, STYLESHEETS, "generated")
    BUILD = PurePath(ASSETS, STYLESHEETS, "build")

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
            name += ".json"
            LOGGER.info(f"Loading {(self.THEMES / name)} theme")
            if os.path.exists(self.THEMES / name):
                with open(self.THEMES / name, encoding="utf-8") as file:
                    theme = json.load(file)
            else:
                LOGGER.error(f"Loading {(self.THEMES / name)} theme failed")
                raise FileNotFoundError("Failed to load theme file")

        self.app_theme = {}
        self.app_theme["QTCOLOR_PRIMARYCOLOR"] = theme["primaryColor"]
        self.app_theme["QTCOLOR_PRIMARYLIGHTCOLOR"] = theme["primaryLightColor"]
        self.app_theme["QTCOLOR_PRIMARYDARKCOLOR"] = theme["primaryDarkColor"]
        self.app_theme["QTCOLOR_SECONDARYCOLOR"] = theme["secondaryColor"]
        self.app_theme["QTCOLOR_SECONDARYLIGHTCOLOR"] = theme["secondaryLightColor"]
        self.app_theme["QTCOLOR_SECONDARYDARKCOLOR"] = theme["secondaryDarkColor"]
        self.app_theme["QTCOLOR_PRIMARYTEXTCOLOR"] = theme["primaryTextColor"]
        self.app_theme["QTCOLOR_SECONDARYTEXTCOLOR"] = theme["secondaryTextColor"]
        self.app_theme["QTCOLOR_DANGER"] = "#DC3545"
        self.app_theme["QTCOLOR_WARNING"] = "#FFC107"
        self.app_theme["QTCOLOR_SUCCESS"] = "#17A2B8"

    # pylint: disable=W0123,C3001,W0612
    def generate_theme_icons(self):
        """
        Uses the themes colours to generate the icon pack
        """

        def replace_file_content(_file_content: str, _file: str, _type: str, _color: str):
            """
            Replaces placeholder color of the SVG file with given color

            Args:
                _file_content (str): file contents
                _file (str): file name
                _type (str): style type
                _color (str): replacement color
            """
            with open(
                (self.GENERATED / "icons" / _type / _file), "w", encoding="utf-8"
            ) as file_output:
                file_output.write(self.replace_svg_colour(_file_content, _color))

        primary = str(
            luminosity(self.app_theme["QTCOLOR_PRIMARYTEXTCOLOR"], 0.4, as_str=False).name()
        )
        secondary = str(
            luminosity(self.app_theme["QTCOLOR_SECONDARYCOLOR"], 0.1, as_str=False).name()
        )
        disabled = str(luminosity(self.app_theme["QTCOLOR_PRIMARYCOLOR"], 0.5, as_str=False).name())
        success = str(luminosity(self.app_theme["QTCOLOR_SUCCESS"], 0.1, as_str=False).name())
        warning = str(luminosity(self.app_theme["QTCOLOR_WARNING"], as_str=False).name())
        danger = str(luminosity(self.app_theme["QTCOLOR_DANGER"], as_str=False).name())

        self._validate_output_dir()
        for _dir, _sdir, _files in os.walk(self.ICONS):
            for file in filter(lambda ext: str(os.path.splitext(ext)[1]).lower() == ".svg", _files):
                with open(PurePath(_dir, file), encoding="utf-8") as svg_file:
                    content = svg_file.read()
                    replace_file_content(content, file, "primary", primary)
                    replace_file_content(content, file, "secondary", secondary)
                    replace_file_content(content, file, "disabled", disabled)
                    replace_file_content(content, file, "success", success)
                    replace_file_content(content, file, "warning", warning)
                    replace_file_content(content, file, "danger", danger)

    @staticmethod
    def replace_svg_colour(
        content: str, replace: str, placeholder: Optional[str] = "#0000FF"
    ) -> str:
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
        replace = "#ffffff00"
        placeholder = "#000000"
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
        with open(self.GENERATED / "stylesheet.css", "w", encoding="utf-8") as css:
            css.write(stylesheet)
        return stylesheet

    def build_theme(self):
        """
        Builds the theme pack for the application
        """
        self.generate_theme_icons()
        self.generate_theme_stylesheet()
        with open(self.GENERATED / "apptheme.json", "w", encoding="utf-8") as f_json:
            json.dump(self.app_theme, f_json)

    def package_theme(self):
        """
        Packages the generated theme pack into a theme zip
        """
        path = self.BUILD
        if not os.path.exists(path):
            os.mkdir(path)
        shutil.make_archive((path / self.theme_name).as_posix(), "zip", self.GENERATED)
        shutil.rmtree(self.GENERATED)

    def _validate_output_dir(self):
        """
        Validates the output directory for the theme pack
        """
        paths = (
            self.GENERATED,
            self.GENERATED / "icons",
            self.GENERATED / "icons" / "primary",
            self.GENERATED / "icons" / "secondary",
            self.GENERATED / "icons" / "disabled",
            self.GENERATED / "icons" / "success",
            self.GENERATED / "icons" / "warning",
            self.GENERATED / "icons" / "danger",
        )
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

        path = self.GENERATED / "stylesheet.css"
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as file:
                file.close()

        path = self.GENERATED / "apptheme.json"
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as file:
                file.close()


def generate_resource(name: str, recompile: Optional[bool] = False) -> bool:
    """
    Generates the theme

    Args:
        recompile (Optional[bool]): recompile te theme for Apollo
        name (str): theme pack name

    Returns:
        bool: true when theme is generated, otherwise false
    """
    app_theme = ASSETS / "app_themes"
    loaded_theme = app_theme / "__loaded_theme__"
    theme_zip = app_theme / (name + ".zip")

    if os.path.exists(ResourceGenerator.BUILD):
        shutil.rmtree(ResourceGenerator.BUILD)

    if os.path.exists(ResourceGenerator.GENERATED):
        shutil.rmtree(ResourceGenerator.GENERATED)

    if recompile and _JINJA:
        if not _JINJA:
            ApolloWarning("Failed to build theme pack, Jinja is Missing")
            return False

        for file in os.listdir(app_theme):
            if os.path.splitext(file)[1] == ".zip":
                os.remove(str(app_theme / str(file)))
        if os.path.exists(loaded_theme):
            shutil.rmtree(loaded_theme)

    if not os.path.exists(loaded_theme):
        os.mkdir(loaded_theme)

    if not os.path.exists(theme_zip):
        if _JINJA:
            for theme in os.listdir(ResourceGenerator.THEMES):
                theme = str(os.path.splitext(theme)[0])
                res = ResourceGenerator(theme)
                res.build_theme()
                res.package_theme()
                shutil.move(res.BUILD / (theme + ".zip"), app_theme / (theme + ".zip"))
                shutil.rmtree(res.BUILD)
        else:
            if not name + ".json" in os.listdir(ResourceGenerator.THEMES):
                ApolloWarning("Theme JSON missing")
            if not _JINJA:
                ApolloWarning("Failed to build theme pack, Jinja is Missing")
            return False

    if os.path.exists(theme_zip):
        if os.path.exists(loaded_theme):
            shutil.rmtree(loaded_theme)
        os.mkdir(loaded_theme)
        shutil.unpack_archive(theme_zip, loaded_theme)
        return True

    return False


def load_theme(app: QtWidgets.QApplication, name: str, recompile: Optional[bool] = False):
    """
    Loads the theme into the applicationto display

    Args:
        app (QtWidgets.QApplication): QtApplication
        name (str): theme pack name
        recompile (Optional[Boolean]): Recompile resources
    """

    app_theme = ASSETS / "app_themes"
    loaded_theme = app_theme / "__loaded_theme__"
    theme_zip = app_theme / (name + ".zip")

    if os.path.exists(ResourceGenerator.BUILD):
        shutil.rmtree(ResourceGenerator.BUILD)

    if os.path.exists(ResourceGenerator.GENERATED):
        shutil.rmtree(ResourceGenerator.GENERATED)

    if recompile and _JINJA:
        if not _JINJA:
            raise RuntimeError("Failed to build theme pack, Jinja is Missing")

        for file in os.listdir(app_theme):
            if os.path.splitext(file)[1] == ".zip":
                os.remove(str(app_theme / str(file)))
        if os.path.exists(loaded_theme):
            shutil.rmtree(loaded_theme)

    if not os.path.exists(loaded_theme):
        if not os.path.exists(theme_zip):
            generate_resource(name)
        else:
            os.mkdir(loaded_theme)

    if len(os.listdir(loaded_theme)) == 0:
        if os.path.exists(theme_zip):
            shutil.unpack_archive(theme_zip, loaded_theme)
        else:
            raise RuntimeError("Failed To generate Resurces")

    if os.path.exists(loaded_theme) and len(os.listdir(loaded_theme)) != 0:
        QtCore.QDir.addSearchPath("icons_primary", str(loaded_theme / "icons" / "primary"))
        QtCore.QDir.addSearchPath("icons_secondary", str(loaded_theme / "icons" / "secondary"))
        QtCore.QDir.addSearchPath("icons_disabled", str(loaded_theme / "icons" / "disabled"))
        QtCore.QDir.addSearchPath("icons_success", str(loaded_theme / "icons" / "success"))
        QtCore.QDir.addSearchPath("icons_danger", str(loaded_theme / "icons" / "danger"))
        QtCore.QDir.addSearchPath("icons_warning", str(loaded_theme / "icons" / "warning"))
        filtr = filter(
            lambda ext: os.path.splitext(ext)[1].lower() == ".ttf",
            os.listdir(ResourceGenerator.FONTS),
        )
        for file in filtr:
            QtGui.QFontDatabase.addApplicationFont((ResourceGenerator.FONTS / str(file)).as_posix())

        with open(loaded_theme / "stylesheet.css", encoding="utf-8") as file_output:
            app.setStyleSheet(file_output.read())
            app.setStyle("Fusion")
