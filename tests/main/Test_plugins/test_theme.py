import sys
import os
import pytest


from PySide6 import QtGui
from PySide6 import QtWidgets

from apollo.plugins.app_theme import Theme
from apollo import PathUtils as PU
from apollo.utils import ThreadIt, dedenter
from tests.main.fixtures import TESTFILES

SKIP = True

class Test_Theme:

    @classmethod
    def setup_class(cls):
        if not QtWidgets.QApplication.instance():
            cls.App = QtWidgets.QApplication()

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        if QtWidgets.QApplication.instance() and hasattr(cls, "App"):
            cls.App.quit()
            del cls.App

    @pytest.mark.skipif(SKIP, reason = "Skip if not needed to be tested")
    def test_GenStyleSheet(self):
        theme = Theme()
        Sheet = """
        background-color: $ui-01
        background-color: $ui-01
        background-color: $ui-01
        """
        ExpectedSheet = """
        background-color: #262626
        background-color: #262626
        background-color: #262626
        """
        assert ExpectedSheet == theme.GenStyleSheet(theme.DefaultPallete(), Sheet)

    @pytest.mark.skipif(SKIP, reason = "Skip if not needed to be tested")
    def test_GenIconResource(self):
        theme = Theme()
        Expected = r"""        <RCC>
            <qresource prefix="icon_pack">
                <file>png\1</file>
                <file>png\2</file>
                <file>png\3</file>
                <file>png\4</file>
                <file>png\5</file>
                <file>png\6</file>
                <file>png\7</file>
                <file>png\8</file>
            </qresource>
        </RCC>"""
        assert dedenter(Expected, 8) == (theme.GenIconResource(["1","2","3","4","5","6","7","8"]))

    @pytest.mark.skipif(SKIP, reason = "Skip if not needed to be tested")
    def test_ImageOverlay(self):
        theme = Theme()
        SVG = PU.PathJoin(os.path.split(theme.ROOTPATH)[0], "svg", "app.svg")
        THEME = "icon-01"
        DEST = PU.PathJoin(f"{TESTFILES}","png", "64")
        os.mkdir(PU.PathJoin(f"{TESTFILES}","png"))
        os.mkdir(PU.PathJoin(f"{TESTFILES}","png", "64"))
        COLOR = QtGui.QColor(theme.DefaultPallete().get(THEME))

        assert os.path.isfile(".\\" + theme.ImageOverlay(SVG, THEME, DEST, COLOR, 64))

        PU.PurgeDirectory(PU.PathJoin(f"{TESTFILES}","png")) # cleanup

    @pytest.mark.skipif(SKIP, reason = "Skip if not needed to be tested")
    def test_GenAppIcons(self):
        theme = Theme()
        theme.GenAppIcons(theme.DefaultPallete(), TESTFILES)

        assert os.path.isdir(PU.PathJoin(f"{TESTFILES}","png"))
        assert os.path.isdir(PU.PathJoin(f"{TESTFILES}","png", "16"))
        assert os.path.isdir(PU.PathJoin(f"{TESTFILES}","png", "24"))
        assert os.path.isdir(PU.PathJoin(f"{TESTFILES}","png", "32"))
        assert os.path.isdir(PU.PathJoin(f"{TESTFILES}","png", "48"))
        assert os.path.isdir(PU.PathJoin(f"{TESTFILES}","png", "64"))

        PU.PurgeDirectory(PU.PathJoin(f"{TESTFILES}","png")) # cleanup

    @pytest.mark.skipif(SKIP, reason = "Skip if not needed to be tested")
    def test_CreateThemePack(self):
        theme = Theme()
        theme.CreateThemePack(TESTFILES, "TEST_theme", theme.DefaultPallete())

        assert not os.path.isdir(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "png"))
        assert not os.path.isdir(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "png", "16"))
        assert not os.path.isdir(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "png", "24"))
        assert not os.path.isdir(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "png", "32"))
        assert not os.path.isdir(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "png", "48"))
        assert not os.path.isdir(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "png", "64"))
        assert not os.path.isfile(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "app_icons.qrc"))

        assert os.path.isfile(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "stylesheet.css"))
        assert os.path.isfile(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "__init__.py"))
        assert os.path.isfile(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "app_icons.py"))
        assert os.path.isfile(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "theme.json"))

        PU.PurgeDirectory(PU.PathJoin(f"{TESTFILES}", "TEST_theme")) # cleanup

    @pytest.mark.skipif(SKIP, reason = "Skip if not needed to be tested")
    def test_GetStyleSheet(self):
        os.mkdir(PU.PathJoin(f"{TESTFILES}", "TEST_theme"))
        with open(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "stylesheet.css"), "w") as FH:
            SHEET = """
            background-colour: black
            """
            FH.write(SHEET)

        theme = Theme()
        theme.ROOTPATH = TESTFILES
        assert SHEET == theme.GetStyleSheet("TEST_theme")

        PU.PurgeDirectory(PU.PathJoin(f"{TESTFILES}", "TEST_theme")) # cleanup

    @pytest.mark.skipif(SKIP, reason = "Skip if not needed to be tested")
    def test_LoadAppIcons(self):
        os.mkdir(PU.PathJoin(f"{TESTFILES}", "TEST_theme"))
        with open(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "app_icons.py"), "w") as FH:
            FH.write("""import pytest\nwith pytest.raises(Exception):\n    raise Exception""")
        with open(PU.PathJoin(f"{TESTFILES}", "TEST_theme", "__init__.py"), "w") as FH:
            FH.write("""from .app_icons import *""")

        theme = Theme()
        theme.ROOTPATH = TESTFILES
        theme.LoadAppIcons("TEST_theme", "tests.testing_tools.test_files")
        PU.PurgeDirectory(PU.PathJoin(f"{TESTFILES}", "TEST_theme")) # cleanup
