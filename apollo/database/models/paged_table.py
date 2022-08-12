from __future__ import annotations

import dataclasses
import re
from typing import Any, Optional, Union

from PySide6 import QtCore, QtGui, QtSql

from apollo.database import Database, RecordSet
from apollo.utils import get_logger


LOGGER = get_logger(__name__)


@dataclasses.dataclass
class Filter:
    """
    Page Window filter the model uses to filter model data
    """

    query: str = ""  # query to use to filter
    value: list = None  # value to use to filter


# pylint: disable=R0902
@dataclasses.dataclass
class PageWindow:
    """
    Page Window the model uses to fetch and display data
    """

    global_count: int = 0  # Total number of rows in the database
    global_pointer: int = 0  # index of the last row relative to global count

    offset: int = 0  # seeking offset from the top
    fetch_limit: int = 50  # rows to fetch each query
    window_size: int = fetch_limit * 2  # size of each page
    window_max: Any = None  # max value of the last fetch
    window_min: Any = None  # min value of the last fetch

    sort_order: QtCore.Qt.SortOrder = QtCore.Qt.AscendingOrder  # sort order
    sort_col: str = None  # column to sort
    group_col: str = None  # column to group

    # pylint: disable=W0108
    filter: Filter = dataclasses.field(default_factory=lambda: Filter())  # filters the exiting data

    def __bool__(self):
        return not self.global_count == 0

    def reset(self):
        """
        Resets window to default_values
        """
        self.global_count: int = 0
        self.global_pointer: int = 0
        self.offset: int = 0
        self.window_max: Any = None
        self.window_min: Any = None


class PagedTableModel(QtGui.QStandardItemModel):
    """
    Paginated table model that interfaces with SQLITE DB
    """

    FETCH_DATA_DOWN = 0
    FETCH_DATA_UP = 1

    def __init__(self, table_name: str, database: Database):
        super().__init__()
        self._table_name = table_name
        self._db = database
        self._window = PageWindow(sort_col=self.Columns[0])
        self.set_global_row_count()

    def __bool__(self):
        return not self.rowCount() == 0

    def __str__(self):
        return str(
            RecordSet(
                self.Columns,
                [
                    [self.index(r, c).data() for c in range(self.columnCount())]
                    for r in range(self.rowCount())
                ],
            )
        )

    def set_global_row_count(self):
        """
        Sets the global row count for the database table
        """
        window = self._window
        with self._db.connector as connection:
            if window.filter.query == "":
                result = self._db.execute(
                    f'SELECT COUNT("__rowid__") FROM ({self.SelectQuery})', connection
                )
            else:
                query = f"""
                    SELECT COUNT("__rowid__")
                    FROM ({self.SelectQuery} 
                    WHERE {window.filter.query})
                """
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
        self.fetch_data(self.FETCH_DATA_DOWN)

    def group(self, column: int):
        """
        Groups the displayed model data

        Args:
            column: Column to use for grouping
        """
        self._window.group_col = self.Columns[column]
        self.clear()
        self.fetch_data(self.FETCH_DATA_DOWN)

    def fetch_data(self, direction: int) -> bool:
        """
        Fetches data on scroll event

        Args:
            direction (int): Scroll Direction

        Returns:
            bool: if fetch was successful returns True, otherwise Flase
        """
        SELECT = self.SelectQuery
        LIMIT = self._window.fetch_limit
        SORT_COL = self._window.sort_col
        SORT = "ASC" if self._window.sort_order is QtCore.Qt.AscendingOrder else "DESC"
        GROUP = f"GROUP BY {self._window.group_col}" if self._window.group_col is not None else ""
        FILTERING = bool(self._window.filter.value is not None and self._window.filter.query)
        RESULT = None

        if self._window.window_max is None and self._window.window_min is None:
            WHERE = f"WHERE ({self._window.filter.query})" if self._window.filter.query else ""
            ORDER = f"ORDER BY {SORT_COL} {SORT} LIMIT {LIMIT}"
            with self._db.connector as connection:
                if FILTERING:  # ENABLES FILTERING
                    query = QtSql.QSqlQuery(" ".join([SELECT, WHERE, GROUP, ORDER]), connection)
                    for index, item in enumerate(self._window.filter.value):
                        query.bindValue(index, item)
                else:
                    query = QtSql.QSqlQuery(" ".join([SELECT, WHERE, GROUP, ORDER]), connection)
                RESULT = self._db.execute(query, connection)

        elif direction == self.FETCH_DATA_DOWN:  # ON SCROLL DOWN
            ORDER = f"ORDER BY {SORT_COL} {SORT} LIMIT {LIMIT}"
            with self._db.connector as connection:
                if FILTERING:  # ENABLES FILTERING
                    WHERE = f"WHERE {SORT_COL} > ? AND ({self._window.filter.query})"
                    query = QtSql.QSqlQuery(" ".join([SELECT, WHERE, GROUP, ORDER]), connection)
                    query.bindValue(0, self._window.window_max)
                    for index, item in enumerate(self._window.filter.value):
                        query.bindValue(index + 1, item)
                else:
                    WHERE = f"WHERE {SORT_COL} > ?"
                    query = QtSql.QSqlQuery(" ".join([SELECT, WHERE, GROUP, ORDER]), connection)
                    query.bindValue(0, self._window.window_max)
                RESULT = self._db.execute(query, connection)

        elif direction == self.FETCH_DATA_UP:  # ON SCROLL UP
            ORDER = f"ORDER BY {SORT_COL} {SORT} LIMIT {self.Offset}, {LIMIT}"
            with self._db.connector as connection:
                if FILTERING:  # ENABLES FILTERING
                    WHERE = f"WHERE {SORT_COL} < ? AND ({self._window.filter.query})"
                    query = QtSql.QSqlQuery(" ".join([SELECT, WHERE, GROUP, ORDER]), connection)
                    query.bindValue(0, self._window.window_min)
                    for index, item in enumerate(self._window.filter.value):
                        query.bindValue(index + 1, item)
                else:
                    WHERE = f"WHERE {SORT_COL} < ?"
                    query = QtSql.QSqlQuery(" ".join([SELECT, WHERE, GROUP, ORDER]), connection)
                    query.bindValue(0, self._window.window_min)
                RESULT = self._db.execute(query, connection)

        if RESULT:
            self.populate(RESULT, direction)
            return True
        return False

    def populate(self, data: RecordSet, direction: int):
        """
        Populates te model using the fetched data

        Args:
            data (RecordSet): Data to populate model with
            direction (int): Scroll Direction
        """

        def get_row(_row: list):
            return [QtGui.QStandardItem(str(x)) for x in _row]

        # ON SCROLL DOWN
        if (
            direction == self.FETCH_DATA_DOWN
            and self._window.global_pointer <= self._window.global_count
        ):
            self._window.global_pointer += len(data.records)
            self.beginResetModel()
            for row in data.records:
                self.appendRow(get_row(row))
                if self.rowCount() > self._window.window_size:
                    self.removeRow(0)
            self.endResetModel()

            self.update_offset(direction)
            self.update_min_max(data)
            return None

        # ON SCROLL UP
        if direction == self.FETCH_DATA_UP and self._window.global_pointer >= 0:
            self._window.global_pointer -= len(data.records)
            self.beginResetModel()
            for row in data.records[::-1]:
                self.insertRow(0, get_row(row))
                if self.rowCount() > self._window.window_size:
                    self.removeRow(self.rowCount() - 1)
            self.endResetModel()

            self.update_offset(direction)
            self.update_min_max(data)
            return None

    def update_min_max(self, data: RecordSet):
        """
        Update the Min and max of the Data table

        Args:
            data (RecordSet): Data recently fetched
        """
        data = data.records[0][self.Columns.index(self._window.sort_col)]
        if isinstance(data, str):
            self._window.window_min = str(
                self.index(0, self.Columns.index(self._window.sort_col)).data()
            )
            self._window.window_max = str(
                self.index(self.rowCount() - 1, self.Columns.index(self._window.sort_col)).data()
            )
        if isinstance(data, float):
            self._window.window_min = float(
                self.index(0, self.Columns.index(self._window.sort_col)).data()
            )
            self._window.window_max = float(
                self.index(self.rowCount() - 1, self.Columns.index(self._window.sort_col)).data()
            )
        if isinstance(data, int):
            self._window.window_min = int(
                self.index(0, self.Columns.index(self._window.sort_col)).data()
            )
            self._window.window_max = int(
                self.index(self.rowCount() - 1, self.Columns.index(self._window.sort_col)).data()
            )

    # noinspection PyAttributeOutsideInit
    @property
    def Offset(self) -> int:
        """
        returns the offset of the limit function to fetch rows from

        Returns:
            int: offset of the limit function to fetch rows from
        """
        offset = self._window.offset * self._window.fetch_limit
        if (offset - self._window.window_size) > 0:
            return offset - self._window.window_size
        return 0

    # noinspection PyAttributeOutsideInit
    def update_offset(self, direction: int):
        """
        updates the offset of the limit function to fetch rows from
        """
        if self.rowCount() == self._window.window_size:
            if direction == self.FETCH_DATA_DOWN:
                if 0 <= self._window.offset:
                    self._window.offset += 1
            if direction == self.FETCH_DATA_UP:
                if 0 < self._window.offset:
                    self._window.offset -= 1

    def clear_filter(self):
        """
        Clears the applied filter to the currently displayed model
        """
        self._window.filter.query = ""
        self._window.filter.value = None
        self.clear()
        self.fetch_data(self.FETCH_DATA_DOWN)

    def clear_grouping(self):
        """
        Clears the applied grouping to the currently displayed model
        """
        self._window.group_col = None
        self.clear()
        self.fetch_data(self.FETCH_DATA_DOWN)

    def set_filter(self, search_query: str, col_index: int = -1):
        """
        Sets the filter to the model

        Args:
            col_index (int): Column to filter
            search_query (str): term to search for
        """
        if col_index == -1:
            cols = list(
                filter(
                    lambda item: re.match(r".*\.(TITLE|FILENAME|ARTIST|ALBUM)$", str(item)),
                    self.Columns,
                )
            )
            self._window.filter.query = " OR ".join([f"{col_index} LIKE ?" for col_index in cols])
            self._window.filter.value = [f"%{search_query}%" for _ in cols]
        else:
            self._window.filter.query = f"{self.Columns[col_index]} LIKE ?"
            self._window.filter.value = [f"%{search_query}%"]

        self.clear()
        self.fetch_data(self.FETCH_DATA_DOWN)

    def get_row_atIndex(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ) -> RecordSet:
        """
        Fetches Row Data at index

        Args:
            index (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): Row index to get data

        Returns:
            RecordSet: row data at given index
        """
        row_index = index.row()
        if row_index != -1:
            return RecordSet(
                self.Columns,
                [
                    [
                        self.index(row_index, col_index).data()
                        for col_index in range(self.columnCount())
                    ]
                ],
            )
        return RecordSet(self.Columns, [[]])

    @property
    def SelectQuery(self) -> str:
        """
        Rows Select query to use

        Returns:
            str: select query the model uses
        """
        raise NotImplementedError

    @property
    def Columns(self) -> list[str]:
        """
        Columns the model displays

        Returns:
            list[str]: Columns the model displays
        """
        raise NotImplementedError
