import os
import re
import shutil
import tempfile
import time
from pathlib import PurePath
from re import Pattern

import pytest
import pytest_mock
from PySide6 import QtWidgets

import apollo.assets.stylesheets
from apollo.assets.stylesheets import ResourceGenerator, load_theme, ASSETS
from apollo.utils import get_logger
from configs import settings
from tests.testing_utils import get_qt_application

CONFIG = settings
LOGGER = get_logger(__name__)


@pytest.fixture
def get_generator() -> ResourceGenerator:
    res = ResourceGenerator(CONFIG.loaded_theme)
    return res


class Test_ResourceGenerator:
    _qt_application = get_qt_application()

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        if os.path.exists(ResourceGenerator.GENERATED):
            shutil.rmtree(ResourceGenerator.GENERATED)
        if os.path.exists(ResourceGenerator.BUILD):
            shutil.rmtree(ResourceGenerator.BUILD)

    def test_init_resource_generator(self):
        res = ResourceGenerator(CONFIG.loaded_theme)
        assert res.app_theme
        res = ResourceGenerator(CONFIG.loaded_theme, dict.fromkeys(
                ["primaryColor", "primaryLightColor", "primaryDarkColor", "secondaryColor", "secondaryLightColor",
                 "secondaryDarkColor", 'primaryTextColor', 'secondaryTextColor']))
        assert res.app_theme

        with pytest.raises(FileNotFoundError) as exception:
            res = ResourceGenerator("null_theme")

        with pytest.raises(KeyError) as exception:
            res = ResourceGenerator(CONFIG.loaded_theme, dict.fromkeys(
                    ["primaryColor", "primaryLightColor", "primaryDarkColor", "secondaryLightColor",
                     "secondaryDarkColor", 'primaryTextColor', ]))

    def test_replace_svg_colour(self, get_generator: ResourceGenerator):
        res = get_generator
        content = """
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
              <path fill="#0000ff" fill-rule="evenodd" d=""/>
              <path fill="#000000" fill-rule="evenodd" d=""/>
            </svg>
        """
        replaced_content = res.replace_svg_colour(content, replace = "#000044", placeholder = "#0000ff")
        expected = """
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
              <path fill="#000044" fill-rule="evenodd" d=""/>
              <path fill="#ffffff00" fill-rule="evenodd" d=""/>
            </svg>
        """
        assert replaced_content == expected

    def test_generate_theme_icons(self, get_generator: ResourceGenerator):
        res = get_generator
        res.generate_theme_icons(res.app_theme['QTCOLOR_PRIMARYLIGHTCOLOR'], res.app_theme['QTCOLOR_PRIMARYLIGHTCOLOR'],
                                 res.app_theme['QTCOLOR_PRIMARYLIGHTCOLOR'])
        assert os.path.exists(res.GENERATED / 'icons' / 'primary')
        assert os.path.exists(res.GENERATED / 'icons' / 'secondary')
        assert os.path.exists(res.GENERATED / 'icons' / 'disabled')

    def test_generate_theme_stylesheet(self, get_generator: ResourceGenerator):
        res = get_generator
        assert res.generate_theme_stylesheet()

    def test_build_package_theme(self, get_generator: ResourceGenerator):
        res = get_generator
        res.build_theme()
        assert len(os.listdir(res.GENERATED)) == 2
        res.package_theme()
        assert not os.path.exists(res.GENERATED)
        assert os.listdir(res.BUILD) != 0

    def test_load_theme_1(self, get_generator: ResourceGenerator, mocker: pytest_mock.MockerFixture):
        with tempfile.TemporaryDirectory() as directory:
            name = 'material_dark'

            mocker.patch("apollo.assets.stylesheets.ASSETS", PurePath(directory))
            mocker.patch("apollo.assets.stylesheets._JINJA", True)
            res = get_generator
            load_theme(self._qt_application, name)
            load_theme(self._qt_application, name)

            theme = PurePath(directory, 'app_themes')
            assert bool(os.path.exists(theme / '__loaded_theme__'))
            assert bool(os.listdir(theme / '__loaded_theme__') == ['icons', 'stylesheet.css'])
            assert bool(os.path.exists(theme / (name + '.zip')))
            assert not bool(os.path.exists(res.BUILD))
            assert not bool(os.path.exists(res.GENERATED))

    def test_load_theme_2(self, get_generator: ResourceGenerator, mocker: pytest_mock.MockerFixture):
        with tempfile.TemporaryDirectory() as directory:
            res = get_generator
            name = 'material_dark'
            mocker.patch("apollo.assets.stylesheets.ASSETS", PurePath(directory))
            mocker.patch("apollo.assets.stylesheets._JINJA", False)
            mocker.patch("apollo.assets.stylesheets.ResourceGenerator.THEMES", PurePath(directory))
            pattern = 'Failed to build theme pack, Jinja is Missing|Theme JSON missing'
            with pytest.warns(UserWarning, match = pattern):
                load_theme(self._qt_application, name)

                theme = PurePath(directory, 'app_themes')
                assert bool(os.path.exists(theme / '__loaded_theme__'))
                assert not bool(os.listdir(theme / '__loaded_theme__'))
                assert not bool(os.path.exists(theme / (name + '.zip')))

    def test_opacity(self):
        from apollo.assets.stylesheets import opacity

        assert opacity("#FFFFFF", 0) == 'rgba({0}, {1}, {2}, {3})'.format(*(255, 255, 255, float(0)))
        assert opacity("#FFFFFF", 0.25) == 'rgba({0}, {1}, {2}, {3})'.format(*(255, 255, 255, 0.25))
        assert opacity("#FFFFFF", 0.5) == 'rgba({0}, {1}, {2}, {3})'.format(*(255, 255, 255, 0.5))
        assert opacity("#FFFFFF", 1) == 'rgba({0}, {1}, {2}, {3})'.format(*(255, 255, 255, float(1)))

    def test_luminosity(self):
        from apollo.assets.stylesheets import luminosity

        assert luminosity("#FFFFFF", 0) == 'rgba({0}, {1}, {2}, {3})'.format(*(255, 255, 255, 1.0))
        assert luminosity("#FFFFFF", 1) == 'rgba({0}, {1}, {2}, {3})'.format(*(255, 255, 255, 1.0))

        assert luminosity("#000000", 0) == 'rgba({0}, {1}, {2}, {3})'.format(*(0, 0, 0, 1.0))
        assert luminosity("#000000", 0.5) == 'rgba({0}, {1}, {2}, {3})'.format(*(127, 127, 127, 1.0))
        assert luminosity("#000000", 1) == 'rgba({0}, {1}, {2}, {3})'.format(*(255, 255, 255, 1.0))

        assert luminosity("#0000FF", 0) == 'rgba({0}, {1}, {2}, {3})'.format(*(0, 0, 255, 1.0))
        assert luminosity("#0000FF", 0.5) == 'rgba({0}, {1}, {2}, {3})'.format(*(127, 127, 255, 1.0))
        assert luminosity("#0000FF", 1) == 'rgba({0}, {1}, {2}, {3})'.format(*(255, 255, 255, 1.0))
