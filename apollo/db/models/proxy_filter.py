from typing import Any, Optional

from PySide6 import QtCore, QtSql, QtWidgets, QtGui

from apollo.media.decoders.decode import Stream
from apollo.db.database import RecordSet


class TableFilterModel(QtCore.QSortFilterProxyModel):
    COLUMNS = Stream.TAG_FRAMES

    def __init__(self, source_model: QtGui.QStandardItemModel) -> None:
        super().__init__()
        self.setSourceModel(source_model)

    def __str__(self):
        result = RecordSet(self.COLUMNS)
        result.records = [
            [
                self.index(row_index, col_index).data()
                for col_index in range(self.columnCount())
            ]
            for row_index in range(self.rowCount())
        ]
        return str(result)

    def search(self, search_query: str):
        col_index = -1
        self.setFilterKeyColumn(col_index)
        self.setFilterWildcard(search_query)

    def search_artist(self, search_query: str):
        col_index = self.COLUMNS.index("ARTIST")
        self.setFilterKeyColumn(col_index)
        self.setFilterWildcard(search_query)

    def search_album(self, search_query: str):
        col_index = self.COLUMNS.index("ALBUM")
        self.setFilterKeyColumn(col_index)
        self.setFilterWildcard(search_query)

    def search_genre(self, search_query: str):
        col_index = self.COLUMNS.index("CONTENTTYPE")
        self.setFilterKeyColumn(col_index)
        self.setFilterWildcard(search_query)

    def search_mood(self, search_query: str):
        col_index = self.COLUMNS.index("MOOD")
        self.setFilterKeyColumn(col_index)
        self.setFilterWildcard(search_query)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> Any:
        return self.sourceModel().headerData(section, orientation, role)

    def invalidateFilter(self) -> None:
        self.setFilterWildcard("")
        super().invalidateFilter()
