from __future__ import annotations

import dataclasses
import re
from typing import Any, Optional

from PySide6 import QtCore, QtGui, QtSql

from apollo.db.database import Database, RecordSet
from apollo.utils import get_logger

LOGGER = get_logger(__name__)


@dataclasses.dataclass
class Filter:
    query: str = ''
    value: list = None


@dataclasses.dataclass
class PageWindow:

    global_count: int = 0
    global_pointer: int = 0

    offset: int = 0
    fetch_limit: int = 50
    window_size: int = fetch_limit * 2
    window_max: Any = None
    window_min: Any = None

    sort_order: QtCore.Qt.SortOrder = None
    sort_col: str = None
    filter: Filter = dataclasses.field(default_factory = lambda: Filter())

    def __bool__(self):
        return not (self.global_count == 0)

    def reset(self):
        self.global_count: int = 0
        self.global_pointer: int = 0
        self.offset: int = 0
        self.window_max: Any = None
        self.window_min: Any = None


class PagedTableModel(QtGui.QStandardItemModel):
    FETCH_SCROLL_DOWN = 0
    FETCH_SCROLL_UP = 1

    def __init__(self, table_name: str):
        super().__init__()
        self._table_name = table_name
        self._db = Database()
        self._window = PageWindow()
        self.set_global_row_count()

    def __bool__(self):
        return not (self.rowCount() == 0)

    def __str__(self):
        return str(
            RecordSet(
                self.Columns,
                [[self.index(r, c).data() for c in range(self.columnCount())] for r in range(self.rowCount())]
            )
        )

    def set_global_row_count(self):
        window = self._window
        with self._db.connector as connection:
            if window.filter.query == '':
                result = self._db.execute(f'SELECT COUNT("__rowid__") FROM ({self.SelectQuery})', connection)
            else:
                query = f'SELECT COUNT("__rowid__") FROM ({self.SelectQuery} WHERE {window.filter.query})'
                query = QtSql.QSqlQuery(query, connection)
                for index, item in enumerate(window.filter.value):
                    query.bindValue(index, item)
                result = self._db.execute(query, connection)
        window.global_count = result.records[0][0]

    def clear(self) -> None:
        self._window.reset()
        self.set_global_row_count()
        super().clear()

    def sort(self, column: int, order: Optional[QtCore.Qt.SortOrder] = QtCore.Qt.AscendingOrder):
        self._window.sort_col = self.Columns[column]
        self._window.sort_order = order
        super().sort(column, order)
        self.clear()
        self.fetch_data(self.FETCH_SCROLL_DOWN)

    def fetch_data(self, direction: int) -> bool:
        if self._window.sort_order is None and self._window.sort_col is None:
            self._window.sort_order = QtCore.Qt.AscendingOrder
            self._window.sort_col = self.Columns[0]

        limit = self._window.fetch_limit
        sort = 'ASC' if self._window.sort_order is QtCore.Qt.AscendingOrder else 'DESC'
        sort_col = self._window.sort_col

        if self._window.window_max is None and self._window.window_min is None:
            SELECT = self.SelectQuery
            WHERE = f'WHERE ({self._window.filter.query})'
            ORDER = f'ORDER BY {sort_col} {sort} LIMIT {limit}'
            with self._db.connector as connection:
                if self._window.filter.value is not None and self._window.filter.query:  # ENABLES FILTERING
                    query = QtSql.QSqlQuery(' '.join([SELECT, WHERE, ORDER]), connection)
                    for index, item in enumerate(self._window.filter.value):
                        query.bindValue(index, item)
                else:
                    query = QtSql.QSqlQuery(' '.join([SELECT, ORDER]), connection)
                result = self._db.execute(query, connection)
            if result:
                self.populate(result, direction)
                return True
            else:
                return False

        if direction == self.FETCH_SCROLL_DOWN:  # ON SCROLL DOWN
            SELECT = self.SelectQuery
            ORDER = f'ORDER BY {sort_col} {sort} LIMIT {limit}'
            with self._db.connector as connection:
                if self._window.filter.value is not None and self._window.filter.query:  # ENABLES FILTERING
                    WHERE = f'WHERE {sort_col} > ? AND ({self._window.filter.query})'
                    query = QtSql.QSqlQuery(' '.join([SELECT, WHERE, ORDER]), connection)
                    query.bindValue(0, self._window.window_max)
                    for index, item in enumerate(self._window.filter.value):
                        query.bindValue(index + 1, item)
                else:
                    WHERE = f'WHERE {sort_col} > ?'
                    query = QtSql.QSqlQuery(' '.join([SELECT, WHERE, ORDER]), connection)
                    query.bindValue(0, self._window.window_max)
                result = self._db.execute(query, connection)
            if result:
                self.populate(result, direction)
                return True
            else:
                return False

        if direction == self.FETCH_SCROLL_UP:  # ON SCROLL UP
            SELECT = self.SelectQuery
            ORDER = f'ORDER BY {sort_col} {sort} LIMIT {self.Offset}, {limit}'
            with self._db.connector as connection:
                if self._window.filter.value is not None and self._window.filter.query:  # ENABLES FILTERING
                    WHERE = f'WHERE {sort_col} < ? AND ({self._window.filter.query})'
                    query = QtSql.QSqlQuery(' '.join([SELECT, WHERE, ORDER]), connection)
                    query.bindValue(0, self._window.window_min)
                    for index, item in enumerate(self._window.filter.value):
                        query.bindValue(index + 1, item)
                else:
                    WHERE = f'WHERE {sort_col} < ?'
                    query = QtSql.QSqlQuery(' '.join([SELECT, WHERE, ORDER]), connection)
                    query.bindValue(0, self._window.window_min)
                result = self._db.execute(query, connection)
            if result:
                self.populate(result, direction)
                return True
            else:
                return False

    def populate(self, data: RecordSet, direction: int):

        def get_row(_row: list):
            return [QtGui.QStandardItem(str(x)) for x in _row]

        row_index = 0
        if direction == self.FETCH_SCROLL_UP:  # ON SCROLL UP
            self.beginResetModel()
            for row_index, row in enumerate(data.records[::-1]):
                self.insertRow(0, get_row(row))
                if len(data.records) == 1:
                    LOGGER.critical(data)
                if self.rowCount() > self._window.window_size:
                    self.removeRow(self.rowCount() - 1)

            self._window.global_pointer -= row_index
            self.update_offset(direction)
            self._window.window_min = data.records[0][self.Columns.index(self._window.sort_col)]
            self._window.window_max = data.records[-1][self.Columns.index(self._window.sort_col)]
            self.endResetModel()

        if direction == self.FETCH_SCROLL_DOWN:  # ON SCROLL UP
            self.beginResetModel()
            for row_index, row in enumerate(data.records):
                self.appendRow(get_row(row))
                if self.rowCount() > self._window.window_size:
                    self.removeRow(0)

            self._window.global_pointer += row_index
            self.update_offset(direction)
            self._window.window_min = data.records[0][self.Columns.index(self._window.sort_col)]
            self._window.window_max = data.records[-1][self.Columns.index(self._window.sort_col)]
            self.endResetModel()

    # noinspection PyAttributeOutsideInit
    @property
    def Offset(self) -> int:
        offset = self._window.offset * self._window.fetch_limit
        if (offset - self._window.window_size) > 0:
            return offset - self._window.window_size
        else:
            return 0

    # noinspection PyAttributeOutsideInit
    def update_offset(self, direction: int):
        if self.rowCount() == self._window.window_size:
            if direction == self.FETCH_SCROLL_DOWN:
                if 0 <= self._window.offset:
                    self._window.offset += 1
            if direction == self.FETCH_SCROLL_UP:
                if 0 < self._window.offset:
                    self._window.offset -= 1

    def clear_filter(self):
        self._window.filter.query = f''
        self._window.filter.value = None
        self.clear()
        self.fetch_data(self.FETCH_SCROLL_DOWN)

    def set_filter(self, col_index: int, search_query: str):
        if col_index == -1:
            cols = list(
                filter(
                    lambda item: re.match(r'.*\.(TITLE|FILENAME|ARTIST|ALBUM)$', str(item)),
                    self.Columns
                )
            )
            self._window.filter.query = ' OR '.join([f"{col_index} LIKE ?" for col_index in cols])
            self._window.filter.value = [f"%{search_query}%" for _ in cols]
        else:
            self._window.filter.query = f"{self.Columns[col_index]} LIKE ?"
            self._window.filter.value = [f"%{search_query}%"]

        self.clear()
        self.fetch_data(self.FETCH_SCROLL_DOWN)

    @property
    def SelectQuery(self) -> str:
        raise NotImplementedError

    @property
    def Columns(self) -> list:
        raise NotImplementedError
