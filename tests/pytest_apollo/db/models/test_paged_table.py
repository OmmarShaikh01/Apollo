from typing import Any

import pytest

from apollo.db.database import LibraryManager, RecordSet
from apollo.db.models import PagedTableModel
from apollo.media import Stream
from apollo.utils import get_logger
from tests.testing_utils import LIBRARY_TABLE

LOGGER = get_logger(__name__)


class MockPagedTableModel(PagedTableModel):

    def __init__(self, table_name: str):
        super().__init__(table_name)

    @property
    def SelectQuery(self) -> str:
        cols = ', '.join(self.Columns)
        return f'SELECT {cols} FROM library'

    @property
    def Columns(self) -> list:
        cols = [f'library.{i}' for i in Stream.TAG_FRAMES]
        return cols


@pytest.fixture
def model_provider() -> MockPagedTableModel:
    db = LibraryManager()
    with db.connector as connection:
        db.batch_insert(RecordSet(Stream.TAG_FRAMES, LIBRARY_TABLE), 'library', connection)
        db.batch_insert(db.execute("SELECT FILEID FROM library", connection), 'queue', connection)

    model = MockPagedTableModel('library')
    yield model
    with db.connector as connection:
        db.execute("DELETE FROM library", connection)
        db.execute("DELETE FROM queue", connection)


# noinspection PyProtectedMember
def check_for_model_start_end(col_index: int, model: MockPagedTableModel, start: Any, end: Any) -> bool:
    for _ in range(int(model._window.global_count / model._window.fetch_limit) + 3):
        model.fetch_data(model.FETCH_SCROLL_DOWN)
    assert str(model.index(model.rowCount() - 1, col_index).data()) == str(end)

    for _ in range(int(model._window.global_count / model._window.fetch_limit) + 3):
        model.fetch_data(model.FETCH_SCROLL_UP)
    assert str(model.index(0, col_index).data()) == str(start)

    return bool(model)


class Test_PagedTable:

    def test_init(self, model_provider: MockPagedTableModel):
        model = MockPagedTableModel('library')
        col_index = len(model.Columns) - 1
        model.sort(col_index)
        assert check_for_model_start_end(col_index, model, 0, 1110)

        model.clear()
        assert not model

    def test_sorted_scroll(self, model_provider: MockPagedTableModel):
        model = model_provider
        col_index = model.Columns.index('library.FILEPATH')
        model.sort(col_index)
        assert check_for_model_start_end(col_index, model, 'TESTING_FILEPATH_0', 'TESTING_FILEPATH_999')

        model.clear()
        assert not model

    def test_filtered_scroll(self, model_provider: MockPagedTableModel):
        model = model_provider
        col_index = model.Columns.index('library.FILEPATH')
        model.sort(col_index)
        assert check_for_model_start_end(col_index, model, 'TESTING_FILEPATH_0', 'TESTING_FILEPATH_999')
        model.set_filter(-1, 'TESTING_FILENAME_0')
        assert check_for_model_start_end(col_index, model, 'TESTING_FILEPATH_0', 'TESTING_FILEPATH_0')

        model.clear()
        assert not model
