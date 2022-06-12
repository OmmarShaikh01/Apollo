import os
from pathlib import PurePath

import pytest
import pytest_mock

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
MODEL_ROWS, MODEL_COLUMNS = len(LIBRARY_TABLE), len(LibraryManager.library_table_columns)


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

    @pytest.mark.skip
    def test_provider(self):
        from apollo.db.models import Provider
        assert isinstance(Provider.get_model(LibraryModel), LibraryModel)

    @pytest.mark.skip
    def test_init_model_with_data(self, model_provider: LibraryModel):
        model = model_provider
        assert model.rowCount() == model._window.fetch_limit

    def test_prefetch_scroll(self, model_provider: LibraryModel, mocker: pytest_mock.MockerFixture):
        model = model_provider
        test_column = 'FILEPATH'
        with model._db.connector as conn:
            result = model._db.execute(f'SELECT {test_column} FROM library ORDER BY {test_column} ASC', conn)
        model._window.fetch_limit = 10
        model._window.window_size = 20
        model.sort(model.COLUMNS.index(f'{test_column}'))

        model.clear()
        offset = 0
        for _ in range(11):
            model.prefetch(model.FETCH_SCROLL_DOWN)
            data = [model.index(row, model.COLUMNS.index(test_column)).data() for row in range(model.rowCount())]
            if model.rowCount() == 10:
                assert all([x == [y] for x, y in zip(result.records[0:(offset + model._window.fetch_limit)], data)])
            elif model.rowCount() == 20:
                assert all([x == [y] for x, y in zip(result.records[offset:offset + 20], data)])
                offset = (offset + model._window.fetch_limit)
            else:
                assert False
            LOGGER.debug(('FETCH_SCROLL_DOWN', data))

        for _ in range(11):
            model.prefetch(model.FETCH_SCROLL_UP)
            data = [model.index(row, model.COLUMNS.index(test_column)).data() for row in range(model.rowCount())]
            if model.rowCount() == 20 and 0 < offset:
                assert all([x == [y] for x, y in zip(result.records[(offset - 20):offset], data)])
                offset = (offset - model._window.fetch_limit)
            elif model.rowCount() == 20:
                all([x == [y] for x, y in zip(result.records[0:model._window.window_size], data)])
            else:
                assert False
            LOGGER.debug(('FETCH_SCROLL_UP', data))
