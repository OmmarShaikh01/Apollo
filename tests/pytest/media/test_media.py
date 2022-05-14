import os

import pytest

from apollo.media import Mediafile
from apollo.utils import get_logger
from configs import settings

LOGGER = get_logger(__name__)
CONFIG = settings


class Test_Mediafile:

    def test_init(self):
        for dirct, subdirs, files in os.walk(os.path.join(CONFIG.assets_dir, "music_samples")):
            for file in files:
                _path = (os.path.normpath(os.path.join(dirct, file)))
                if Mediafile.isSupported(_path):
                    media_file = Mediafile(_path)
                    assert media_file.Info['file_ext'] == os.path.splitext(_path)[1]
                else:
                    LOGGER.debug(f"SKIPPED: {_path}")

    def test_init_invalid(self):
        with pytest.raises(NotImplementedError):
            file = Mediafile("test_file.ext_false")
