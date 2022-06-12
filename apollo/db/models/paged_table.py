from __future__ import annotations

import dataclasses
from typing import Any, Optional

from PySide6 import QtCore, QtGui, QtSql

from apollo.db.database import Database, RecordSet
from apollo.media import Stream
from apollo.utils import get_logger

LOGGER = get_logger(__name__)


@dataclasses.dataclass
class PageWindow:
    global_max: Any = None
    global_min: Any = None
    window_max: Any = None
    window_min: Any = None
    window_size: int = 500
    fetch_limit: int = 100
    sort_order: QtCore.Qt.SortOrder = None
    sort_col: str = None


class PagedTableModel(QtGui.QStandardItemModel):
    FETCH_SCROLL_DOWN = 0
    FETCH_SCROLL_UP = 1
    COLUMNS = Stream.TAG_FRAMES
    PRIVATE_FIELDS = ['FILEID', 'FILEPATH', 'FILENAME', 'FILESIZE', 'FILEEXT']

    def __init__(self, table_name: str):
        super().__init__()
        self._table_name = table_name
        self._db = Database()
        self._window = PageWindow()

    def __str__(self):
        result = RecordSet(self.COLUMNS)
        result.records = [
            [
                self.item(row_index, col_index).text() for col_index in range(self.columnCount())
            ] for row_index in range(self.rowCount())
        ]
        return str(result)

    def fill_header_data(self):
        for col_index, col in enumerate(self.COLUMNS):
            self.setHorizontalHeaderItem(col_index, QtGui.QStandardItem(str(col)))

    def prefetch(self, direction: int):
        limit = self._window.fetch_limit
        query = None
        order = ''

        if self._window.sort_order is None and self._window.sort_col is None:
            self._window.sort_order = QtCore.Qt.AscendingOrder
            self._window.sort_col = "FILEID"
        sort = 'ASC' if self._window.sort_order is QtCore.Qt.AscendingOrder else 'DESC'
        sort_col = self._window.sort_col

        with self._db.connector as connection:
            if self._window.window_max is not None and self._window.window_min is not None:
                if direction == self.FETCH_SCROLL_DOWN:  # ON SCROLL DOWN
                    query = f"{self.SelectQuery} WHERE {sort_col} > ? ORDER BY {sort_col} {sort} LIMIT {limit}"
                    query = QtSql.QSqlQuery(query, connection)
                    query.bindValue(0, self._window.window_max)
                if direction == self.FETCH_SCROLL_UP:  # ON SCROLL UP
                    query = f"{self.SelectQuery} WHERE {sort_col} < ? ORDER BY {sort_col} {sort} LIMIT {self.Offset}, {limit}"
                    query = QtSql.QSqlQuery(query, connection)
                    query.bindValue(0, self._window.window_min)
            else:
                query = QtSql.QSqlQuery(f"{self.SelectQuery} ORDER BY {sort_col} {sort} LIMIT {limit}", connection)

            result = self._db.execute(query, connection)
            if result:
                self._window.window_min = result.records[0][result.fields.index(sort_col)]
                self._window.window_max = result.records[-1][result.fields.index(sort_col)]
                self.populate(result.records, direction)
                self.update_offset(direction)

    def populate(self, data: list[list], direction: int):

        def get_row(_row: list):
            return list(map(lambda x: QtGui.QStandardItem(str(x)), _row))

        if direction == self.FETCH_SCROLL_UP:  # ON SCROLL DOWN
            for row_index, row in enumerate(data[::-1]):
                if self.rowCount() < self._window.window_size:
                    self.insertRow(0, get_row(row))
                else:
                    self.removeRow(self.rowCount() - 1)
                    self.insertRow(0, get_row(row))
        if direction == self.FETCH_SCROLL_DOWN:  # ON SCROLL UP
            for row_index, row in enumerate(data):
                if self.rowCount() < self._window.window_size:
                    self.appendRow(get_row(row))
                else:
                    self.removeRow(0)
                    self.appendRow(get_row(row))

    def sort(self, column: int, order: Optional[QtCore.Qt.SortOrder] = QtCore.Qt.AscendingOrder):
        self._window.sort_col = self.COLUMNS[column]
        self._window.sort_order = order
        super().sort(column, order)

    @property
    def SelectQuery(self) -> str:
        raise NotImplementedError()

    # noinspection PyAttributeOutsideInit
    @property
    def Offset(self) -> int:
        if not hasattr(self, '_offset'):
            self._offset = 0
        offset = self._offset * self._window.fetch_limit
        if (offset - self._window.window_size) > 0:
            return offset - self._window.window_size
        else:
            return 0

    # noinspection PyAttributeOutsideInit
    def update_offset(self, direction: int):
        if not hasattr(self, '_offset'):
            self._offset = 0

        if self.rowCount() == self._window.window_size:
            if direction == self.FETCH_SCROLL_DOWN:
                if 0 <= self._offset:
                    self._offset += 1
            if direction == self.FETCH_SCROLL_UP:
                if 0 < self._offset:
                    self._offset -= 1

            LOGGER.info(self._offset)
