import random
import random
import uuid
from pathlib import PurePath

import pytest
from PySide6 import QtGui

from apollo.db.database import LibraryManager
from apollo.db.models.proxy_filter import TableFilterModel
from apollo.media.decoders.decode import Stream
from apollo.utils import get_logger
from configs import settings
from tests.testing_utils import get_qt_application

cases = "tests.pytest_apollo.models.case_models"
LOGGER = get_logger(__name__)
CONFIG = settings
MEDIA_FOLDER = PurePath(CONFIG.assets_dir, "music_samples")
BENCHMARK = CONFIG.benchmark_formats  # TODO: remove not
MODEL_ROWS, MODEL_COLUMNS = 100, len(LibraryManager.library_table_columns)


@pytest.fixture
def temporary_item_model() -> QtGui.QStandardItemModel:
    model = QtGui.QStandardItemModel()
    for col_index, col in enumerate(Stream.TAG_FRAMES):
        model.setHorizontalHeaderItem(col_index, QtGui.QStandardItem(str(col)))

    for row_index in range(MODEL_ROWS):
        for col_index, (col, _type) in enumerate(Stream.TAG_FRAMES_FIELDS):
            if col == "FILEID":
                model.setItem(row_index, col_index, QtGui.QStandardItem(str(uuid.uuid4())))
            elif _type == "STRING":
                model.setItem(row_index, col_index, QtGui.QStandardItem(f"TESTING_{col}_{row_index}"))
            elif _type == "INTEGER":
                model.setItem(row_index, col_index, QtGui.QStandardItem(str(random.randint(0, 100))))
            else:
                continue
    return model


@pytest.fixture
def get_init_filter_model(temporary_item_model) -> TableFilterModel:
    model = temporary_item_model
    filter_model = TableFilterModel(model)
    return filter_model


@pytest.mark.skip
class Test_LibraryProxyFilter:
    _qt_application = get_qt_application()

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        return None

    def test_init(self, temporary_item_model):
        model = temporary_item_model
        filter_model = TableFilterModel(model)
        assert model.rowCount() == MODEL_ROWS

    def test_search(self, get_init_filter_model: TableFilterModel):
        model = get_init_filter_model
        assert model.rowCount() == MODEL_ROWS

        model.search("TESTING_ARTIST_1")
        LOGGER.debug(f"FILTERED{model}")
        assert model.rowCount() == 1
        actual = model.index(0, model.COLUMNS.index("ARTIST")).data()
        assert actual == "TESTING_ARTIST_1"

        model.invalidateFilter()
        LOGGER.debug(f"FILTERED cleared{model}")
        assert model.rowCount() == MODEL_ROWS

    def test_search_artist(self, get_init_filter_model: TableFilterModel):
        model = get_init_filter_model
        assert model.rowCount() == MODEL_ROWS

        model.search_artist("TESTING_ARTIST_1")
        LOGGER.debug(f"FILTERED{model}")
        assert model.rowCount() == 1
        actual = model.index(0, model.COLUMNS.index("ARTIST")).data()
        assert actual == "TESTING_ARTIST_1"

        model.invalidateFilter()
        LOGGER.debug(f"FILTERED cleared{model}")
        assert model.rowCount() == MODEL_ROWS

    def test_search_album(self, get_init_filter_model: TableFilterModel):
        model = get_init_filter_model
        assert model.rowCount() == MODEL_ROWS

        model.search_album("TESTING_ALBUM_1")
        LOGGER.debug(f"FILTERED{model}")
        assert model.rowCount() == 1
        actual = model.index(0, model.COLUMNS.index("ALBUM")).data()
        assert actual == "TESTING_ALBUM_1"

        model.invalidateFilter()
        LOGGER.debug(f"FILTERED cleared{model}")
        assert model.rowCount() == MODEL_ROWS

    def test_search_genre(self, get_init_filter_model: TableFilterModel):
        model = get_init_filter_model
        assert model.rowCount() == MODEL_ROWS

        model.search_genre("TESTING_CONTENTTYPE_1")
        LOGGER.debug(f"FILTERED{model}")
        assert model.rowCount() == 1
        actual = model.index(0, model.COLUMNS.index("CONTENTTYPE")).data()
        assert actual == "TESTING_CONTENTTYPE_1"

        model.invalidateFilter()
        LOGGER.debug(f"FILTERED cleared{model}")
        assert model.rowCount() == MODEL_ROWS

    def test_search_mood(self, get_init_filter_model: TableFilterModel):
        model = get_init_filter_model
        assert model.rowCount() == MODEL_ROWS

        model.search_mood("TESTING_MOOD_1")
        LOGGER.debug(f"FILTERED{model}")
        assert model.rowCount() == 1
        actual = model.index(0, model.COLUMNS.index("MOOD")).data()
        assert actual == "TESTING_MOOD_1"

        model.invalidateFilter()
        LOGGER.debug(f"FILTERED cleared{model}")
        assert model.rowCount() == MODEL_ROWS
