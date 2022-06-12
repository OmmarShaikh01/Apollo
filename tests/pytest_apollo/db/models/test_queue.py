import os
from pathlib import PurePath

import pytest

from apollo.db.database import LibraryManager, RecordSet
from apollo.db.models.queue import QueueModel
from apollo.media import Stream
from apollo.utils import get_logger
from configs import settings
from tests.testing_utils import LIBRARY_TABLE, get_qt_application

cases = "tests.pytest_apollo.models.case_models"
LOGGER = get_logger(__name__)
CONFIG = settings
MEDIA_FOLDER = PurePath(CONFIG.assets_dir, "music_samples")
BENCHMARK = CONFIG.benchmark_formats  # TODO: remove not
MODEL_ROWS, MODEL_COLUMNS = len(LIBRARY_TABLE), len(QueueModel.COLUMNS)


@pytest.fixture
def model_provider() -> QueueModel:
    db = LibraryManager()
    with db.connector as connection:
        db.batch_insert(RecordSet(Stream.TAG_FRAMES, LIBRARY_TABLE), 'library', connection)
        db.batch_insert(db.execute("SELECT FILEID FROM library", connection), 'queue', connection)

    model = QueueModel()
    yield model
    with db.connector as connection:
        db.execute("DELETE FROM library", connection)


class Test_QueueModel:
    _qt_application = get_qt_application()

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        if os.path.isfile(CONFIG.db_path):
            os.remove(CONFIG.db_path)
            return None

    def test_provider(self, model_provider: QueueModel):
        from apollo.db.models import Provider
        assert isinstance(Provider.get_model(QueueModel), QueueModel)

    def test_init_model_with_data(self, model_provider: QueueModel):
        model = model_provider
        LOGGER.debug(model)
