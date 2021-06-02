import os
import sys
import re
import importlib
import subprocess
import json

from PySide6 import QtWidgets, QtGui, QtCore

from apollo import PARENT_DIR
from apollo.utils import PathUtils as PU
from apollo.utils import AppConfig

class ThemeLoadFailed(Exception): __module__ = "Theme"


class Theme:
    """
    Theme class for application
    """
    def __init__(self):
        """
        Class Constructor
        """
        self.ROOTPATH = PU.PathJoin(PARENT_DIR, "plugins", "app_theme", "theme_packs")
        self.ThemeConfig = AppConfig()

        if not os.path.isdir(self.ROOTPATH):
            os.mkdir(self.ROOTPATH)
            if not os.path.isfile(PU.PathJoin(self.ROOTPATH, "__init__.py")):
                # Creates an Import
                with open(PU.PathJoin(self.ROOTPATH, "__init__.py"), "w") as FH:
                    FH.write("from . import *")
            if not os.path.isdir(PU.PathJoin(self.ROOTPATH, "GRAY_100")):
                self.CreateThemePack(self.ROOTPATH, "GRAY_100", self.DefaultPallete())

    def LoadTheme(self, app, name = ""): # pragma: no cover
        """
        Loads the theme for the given Application

        Parameters
        ----------
        app : QApplication
            Application to load theme for
        name : str, optional
            Name of the theme, by default ""
        """
        if name in os.listdir(self.ROOTPATH):
            app.setStyleSheet(self.GetStyleSheet(name))
            self.LoadAppIcons(name)

    def GetStyleSheet(self, Name = ""):
        """
        Info: Get the style sheet for the theme
        Args:
        Name: String
            -> theme name
        Returns: String
        Errors: None
        """
        if os.path.isfile(PU.PathJoin(self.ROOTPATH, Name, "stylesheet.css")):
            with open(PU.PathJoin(self.ROOTPATH, Name, "stylesheet.css")) as FH:
                Stylesheet = FH.read()
            return Stylesheet
        else:
            raise ThemeLoadFailed("Stylesheet Not avaliable")

    def LoadAppIcons(self, Name = "", PKG = None):
        """
        Info: Loads the style sheet for the theme
        Args:
        Name: String
            -> theme name
        Returns: None
        Errors: None
        """
        if os.path.isfile(PU.PathJoin(self.ROOTPATH, Name, "app_icons.py")):
            if PKG != None:
                importlib.import_module(f".{Name}", PKG)
            else:
                importlib.import_module(f".{Name}", "apollo.plugins.app_theme.theme_packs")
        else:
            raise ThemeLoadFailed("Resource Not avaliable")

    def CreateThemePack(self, Dest, Name, pallete): #tested
        """
        Info: Creates a Theme Pack
        Args:
        Name: String
            -> name of the theme pack
        pallete: Dict
            -> Dict oft the color pallete
        Returns: None
        Errors: None
        """
        # Creates a theme pack directory
        if PU.WinFileValidator(Name) and not os.path.isdir(PU.PathJoin(Dest, Name)):
            ThemePath = (PU.PathJoin(Dest, Name))
            if os.makedirs(ThemePath):
                self.ThemeConfig[Name] = ThemePath
        else: return None

        if not os.path.isfile(PU.PathJoin(ThemePath, "theme.json")):
            # Creates an app Stylesheet
            with open(PU.PathJoin(ThemePath, "theme.json"), "w") as FH:
                json.dump(pallete, FH)
        else: return None

        if not os.path.isfile(PU.PathJoin(ThemePath, "stylesheet.css")):
            # Creates an app Stylesheet
            with open(PU.PathJoin(ThemePath, "stylesheet.css"), "w") as FH:
                Stylesheet = self.GenStyleSheet(pallete)
                FH.write(Stylesheet)
        else: return None

        if not os.path.isfile(PU.PathJoin(ThemePath, "__init__.py")):
            # Creates an Import
            with open(PU.PathJoin(ThemePath, "__init__.py"), "w") as FH:
                FH.write("from . import app_icons")
        else: return None

        if not os.path.isfile(PU.PathJoin(ThemePath, "app_icons.qrc")):
            # Creates an app icons
            with open(PU.PathJoin(ThemePath, "app_icons.qrc"), "w") as FH:
                resource = self.GenAppIcons(pallete, ThemePath)
                FH.write(resource)
                # processes resource file for icons
                IN = PU.PathJoin(ThemePath, "app_icons.qrc")
                OUT = PU.PathJoin(ThemePath, "app_icons.py")
                if self.CompileResource(IN, OUT):
                    # cleanup
                    PU.PurgeDirectory(PU.PathJoin(ThemePath, "png"))
                    FH.close()
                    PU.PurgeFile(PU.PathJoin(ThemePath, "app_icons.qrc"))
        else: return None

        self.ThemeConfig[f"APPTHEMES/{Name}"] = ThemePath

    def GenStyleSheet(self, pallete, stylesheet = None): # Tested
        """
        Info: Generates stylesheet using a UI colour pallete
        Args:
        pallete: Dict
            -> Dict oft the color pallete
        stylesheet: String
            -> stylesheet to use
        Returns: String
        Errors: None
        """
        if stylesheet == None:
            with open(PU.PathJoin(os.path.split(self.ROOTPATH)[0], "mainwindow_apollo.css")) as style:
                stylesheet = style.read()
        for element, value in pallete.items():
            stylesheet = re.sub(f"[($)]{element}(?!-)", value, stylesheet)
        return stylesheet

    def GenAppIcons(self, pallete, Dest): # Tested
        """
        Info: Generates the theme icons for the app using SVG
        Args:
        Pallete: Dict
            -> Theme dict
        Dest: String
            -> Destination Path
        Returns: String
        Errors: None
        """
        # create the root directory named as "png"
        if not os.path.isdir(PU.PathJoin(Dest, "png")):
            os.mkdir(PU.PathJoin(Dest, "png"))
            Dest = PU.PathJoin(Dest, "png")
            # Dest is <BaseDir//png>
        if not os.path.isdir(PU.PathJoin(Dest, "16")):
            os.mkdir(PU.PathJoin(Dest, "16"))
        if not os.path.isdir(PU.PathJoin(Dest, "24")):
            os.mkdir(PU.PathJoin(Dest, "24"))
        if not os.path.isdir(PU.PathJoin(Dest, "32")):
            os.mkdir(PU.PathJoin(Dest, "32"))
        if not os.path.isdir(PU.PathJoin(Dest, "48")):
            os.mkdir(PU.PathJoin(Dest, "48"))
        if not os.path.isdir(PU.PathJoin(Dest, "64")):
            os.mkdir(PU.PathJoin(Dest, "64"))

        # works for only for SVG files present in root directory
        SVGS = os.listdir(PU.PathJoin(os.path.split(self.ROOTPATH)[0], "svg"))

        # Scans all the SVG file to generate theme images
        for Image in SVGS:
            # SVG image Abs Path
            Image = PU.PathJoin(PU.PathJoin(os.path.split(self.ROOTPATH)[0], "svg"), Image)
            for ThemeName in ["icon-01", "icon-02", "icon-03", "inverse-01", "disabled-02", "disabled-03"]:
                Colour = QtGui.QColor(pallete.get(ThemeName))
                self.ImageOverlay(Image, ThemeName, PU.PathJoin(Dest, "16"), Colour, 16)
                self.ImageOverlay(Image, ThemeName, PU.PathJoin(Dest, "24"), Colour, 24)
                self.ImageOverlay(Image, ThemeName, PU.PathJoin(Dest, "32"), Colour, 32)
                self.ImageOverlay(Image, ThemeName, PU.PathJoin(Dest, "48"), Colour, 48)
                self.ImageOverlay(Image, ThemeName, PU.PathJoin(Dest, "64"), Colour, 64)

        ImgPath = []
        for Dir, SDir, files in os.walk(Dest):
            ImgPath.extend([PU.PathJoin(Dir, file) for file in files])

        return self.GenIconResource(ImgPath)

    def ImageOverlay(self, Image, Theme, Dest, Color, size = 64): # tested
        """
        Overlays and creates a PNG from an SVG

        Parameters
        ----------
        Image : String
            SVG image path
        Theme : String
            Theme name
        Dest : String
            Destination path
        Color : QtGui.QColor
            theme colour
        size : int, optional
            image size, by default 64

        Returns
        -------
        String
            Image Path
        """
        Icon = QtGui.QIcon(Image).pixmap(QtCore.QSize(size, size))
        Painter = QtGui.QPainter(Icon)
        Painter.setBrush(Color)
        Painter.setPen(Color)
        Painter.setCompositionMode(Painter.CompositionMode_SourceIn)
        Painter.drawRect(Icon.rect())
        Painter.end()
        if not Icon.isNull():
            name = os.path.splitext(os.path.split(Image)[1])[0]
            path = PU.PathJoin(Dest, f"{name}_{Theme}.png")
            Icon.save(path)
        return path

    def GenIconResource(self, Files): # Tested
        """
        Generates a resource file for all icons

        Parameters
        ----------
        Files: List[String]
            paths of all file to ad to resource file

        Returns
        -------
        String:
            resource info
        """
        HEADER = """<RCC>\n    <qresource prefix="icon_pack">"""
        Prep = lambda x: "\\".join(x.rsplit("\\", 2)[-2:])
        BODY = "\n".join([f"{' '*8}<file>png\\{Prep(File)}</file>" for File in Files])
        FOOTER = f"""    </qresource>\n</RCC>"""
        String = "\n".join([HEADER, BODY, FOOTER])
        return String

    def CompileResource(self, IN, OUT): # Tested
        from PySide6 import __path__ as PYS_path

        exe = [PU.PathJoin(PYS_path[0], "rcc.exe"), '-g', 'python', "-o", OUT, IN]
        with subprocess.Popen(exe, stderr=subprocess.PIPE) as proc:
            out, err = proc.communicate()
            if err: # pragma: no cover
                msg = err.decode("utf-8")
                command = ' '.join(exe)
                raise Warning(f"Error: {msg}\nwhile executing '{command}'")

        return True

    @classmethod
    def DefaultPallete(cls):
        """
        Info: Default Color pallete
        Args: None
        Returns: Dict
        Errors: None
        """
        JSON = {"ui-background" : "#161616",
                "interactive-01" : "#0f62fe",
                "interactive-02" : "#6f6f6f",
                "interactive-03" : "#ffffff",
                "interactive-04" : "#4589ff",
                "danger" : "#da1e28",
                "ui-01" : "#262626",
                "ui-02" : "#393939",
                "ui-02-alt" : "#525252",
                "ui-03" : "#393939",
                "ui-04" : "#6f6f6f",
                "ui-05" : "#f4f4f4",
                "button-separator" : "#161616",
                "decorative-01" : "#525252",
                "text-01" : "#f4f4f4",
                "text-02" : "#c6c6c6",
                "text-03" : "#6f6f6f",
                "text-04" : "#ffffff",
                "text-05" : "#8d8d8d",
                "text-error" : "#ff8389",
                "link-01" : "#78a9ff",
                "inverse-link" : "#0f62fe",
                "icon-01" : "#f4f4f4",
                "icon-02" : "#c6c6c6",
                "icon-03" : "#ffffff",
                "field-01" : "#262626",
                "field-02" : "#393939",
                "inverse-01" : "#161616",
                "inverse-02" : "#f4f4f4",
                "support-01" : "#fa4d56",
                "support-02" : "#42be65",
                "support-03" : "#f1c21b",
                "support-04" : "#4589ff",
                "inverse-support-01" : "#da1e28",
                "inverse-support-02" : "#24a148",
                "inverse-support-03" : "#f1c21b",
                "inverse-support-04" : "#0043ce",
                "focus" : "#ffffff",
                "inverse-focus-ui" : "#0f62fe",
                "hover-primary" : "#0353e9",
                "hover-primary-text" : "#a6c8ff",
                "hover-secondary" : "#606060",
                "hover-tertiary" : "#f4f4f4",
                "hover-ui" : "#353535",
                "hover-ui-light" : "#525252",
                "hover-selected-ui" : "#4c4c4c",
                "hover-danger" : "#ba1b23",
                "hover-row" : "#353535",
                "inverse-hover-ui" : "#e5e5e5",
                "active-primary" : "#002d9c",
                "active-secondary" : "#393939",
                "active-tertiary" : "#c6c6c6",
                "active-ui" : "#525252",
                "active-danger" : "#750e13",
                "selected-ui" : "#393939",
                "highlight" : "#001d6c",
                "skeleton-01" : "#353535",
                "skeleton-02" : "#393939",
                "visited-link" : "#be95ff",
                "disabled-01" : "#262626",
                "disabled-02" : "#525252",
                "disabled-03" : "#6f6f6f"
            }
        return JSON


if __name__ == "__main__":
    App = QtWidgets.QApplication([])
    Inst = Theme()
