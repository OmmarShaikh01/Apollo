import os
import uuid
from pathlib import PurePath

import pytest
import pytest_mock
from PySide6 import QtWidgets

from apollo.db.database import LibraryManager
from apollo.db.models.library import LibraryModel
from apollo.utils import get_logger
from configs import settings
from tests.testing_utils import get_qt_application

cases = "tests.pytest_apollo.models.case_models"
LOGGER = get_logger(__name__)
CONFIG = settings
MEDIA_FOLDER = PurePath(CONFIG.assets_dir, "music_samples")
BENCHMARK = CONFIG.benchmark_formats  # TODO: remove not
MODEL_ROWS, MODEL_COLUMNS = 10, len(LibraryManager.library_table_columns)


@pytest.fixture
def model_provider(mocker: pytest_mock.MockerFixture) -> LibraryModel:
    db = LibraryManager()
    file_path = [MEDIA_FOLDER / 'mp3' / "example_48000H_2C_TAGGED.mp3" for _ in range(MODEL_ROWS)]
    mocker.patch.multiple("apollo.media.decoders.Stream", __abstractmethods__ = set(),
                          _file_id = lambda x: str(uuid.uuid4()))
    db.scan_files(file_path)
    model = LibraryModel()
    yield model
    with db.connector as connection:
        db.execute("DELETE FROM library", connection)


class Test_LibraryModel:
    _qt_application = get_qt_application()

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        if os.path.isfile(CONFIG.db_path):
            os.remove(CONFIG.db_path)
            return None

    def test_provider(self):
        from apollo.db.models import Provider
        assert isinstance(Provider.get_model(LibraryModel), LibraryModel)

    def test_init_model_with_data(self, model_provider: LibraryModel):
        model = model_provider
        assert (model.rowCount()) == MODEL_ROWS
        assert (model.columnCount()) == MODEL_COLUMNS
        assert all([
            model.horizontalHeaderItem(col_index).text() == col
            for col_index, col in enumerate(LibraryManager.library_table_columns)
        ])
        LOGGER.debug(model)

        with model.database.connector as connection:
            model.database.execute("DELETE FROM library", connection)
        model.load_data()
        assert (model.rowCount()) == 0
        assert (model.columnCount()) == MODEL_COLUMNS
        assert all([
            model.horizontalHeaderItem(col_index).text() == col
            for col_index, col in enumerate(LibraryManager.library_table_columns)
        ])
        LOGGER.debug(model)
