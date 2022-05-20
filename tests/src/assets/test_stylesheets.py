import os
import shutil

import pytest
import pytest_mock

from apollo.assets.stylesheets import ResourceGenerator, load_theme, ASSETS
from apollo.utils import get_logger
from configs import settings

CONFIG = settings
LOGGER = get_logger(__name__)


@pytest.fixture
def get_generator() -> ResourceGenerator:
    res = ResourceGenerator(CONFIG.loaded_theme)
    return res


class Test_ResourceGenerator:

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
        res = ResourceGenerator(
            CONFIG.loaded_theme,
            dict.fromkeys([
                "primaryColor", "primaryLightColor", "primaryDarkColor", "secondaryColor",
                "secondaryLightColor", "secondaryDarkColor", 'primaryTextColor', 'secondaryTextColor'
            ])
        )
        assert res.app_theme

        with pytest.raises(FileNotFoundError) as exception:
            res = ResourceGenerator("null_theme")

        with pytest.raises(KeyError) as exception:
            res = ResourceGenerator(
                CONFIG.loaded_theme, dict.fromkeys([
                    "primaryColor", "primaryLightColor", "primaryDarkColor",
                    "secondaryLightColor", "secondaryDarkColor", 'primaryTextColor',
                ])
            )

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
        res.generate_theme_icons(
            res.app_theme['QTCOLOR_PRIMARYLIGHTCOLOR'],
            res.app_theme['QTCOLOR_PRIMARYLIGHTCOLOR'],
            res.app_theme['QTCOLOR_PRIMARYLIGHTCOLOR']
        )
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
