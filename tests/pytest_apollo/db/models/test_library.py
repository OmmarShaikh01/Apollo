import os
from pathlib import PurePath
from typing import Any

import pytest

from apollo.db.database import LibraryManager, RecordSet
from apollo.db.models.library import LibraryModel
from apollo.media import Stream
from apollo.utils import get_logger
from configs import settings
from tests.testing_utils import LIBRARY_TABLE, get_qt_application

cases = "tests.pytest_apollo.models.case_models"
LOGGER = get_logger(__name__)
CONFIG = settings
MEDIA_FOLDER = PurePath(CONFIG.assets_dir, "music_samples")
BENCHMARK = CONFIG.benchmark_formats  # TODO: remove not
MODEL_ROWS, MODEL_COLUMNS = len(LIBRARY_TABLE), len(Stream.TAG_FRAMES)


@pytest.fixture
def model_provider() -> LibraryModel:
    db = LibraryManager()
    with db.connector as connection:
        db.batch_insert(RecordSet(Stream.TAG_FRAMES, LIBRARY_TABLE), 'library', connection)
        db.batch_insert(db.execute("SELECT FILEID FROM library", connection), 'queue', connection)

    model = LibraryModel()
    yield model
    with db.connector as connection:
        db.execute("DELETE FROM library", connection)


# noinspection PyProtectedMember
def check_for_model_start_end(col_index: int, model: LibraryModel, start: Any, end: Any) -> bool:
    for _ in range(int(model._window.global_count / model._window.fetch_limit) + 3):
        model.fetch_data(model.FETCH_DATA_DOWN)
    assert str(model.index(model.rowCount() - 1, col_index).data()) == str(end)

    for _ in range(int(model._window.global_count / model._window.fetch_limit) + 3):
        model.fetch_data(model.FETCH_DATA_UP)
    assert str(model.index(0, col_index).data()) == str(start)

    return bool(model)


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
        from apollo.db.models import ModelProvider
        assert isinstance(ModelProvider.get_model(LibraryModel), LibraryModel)

    def test_init_model_with_data(self, model_provider: LibraryModel):
        model = model_provider
        col_index = len(model.Columns) - 1
        model.sort(col_index)
        assert check_for_model_start_end(col_index, model, 0, 1110)

        model.clear()
        assert not model
