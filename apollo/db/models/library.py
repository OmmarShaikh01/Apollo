from typing import Optional

import PySide6.QtCore
from PySide6 import QtCore, QtSql, QtWidgets, QtGui

from apollo.db.database import LibraryManager, RecordSet
from apollo.media.decoders.decode import Stream


class LibraryModel(QtGui.QStandardItemModel):
    COLUMNS = Stream.TAG_FRAMES
    PRIVATE_FIELDS = ['FILEID', 'FILEPATH', 'FILENAME', 'FILESIZE', 'FILEEXT']

    def __init__(self) -> None:
        super().__init__()
        self.database = LibraryManager()
        self.load_data()

    def __str__(self):
        result = RecordSet(self.COLUMNS)
        result.records = [
            [
                self.item(row_index, col_index).text()
                for col_index in range(self.columnCount())
            ]
            for row_index in range(self.rowCount())
        ]
        return str(result)

    def load_data(self):
        with self.database.connector as connection:
            cols = ", ".join(self.database.library_table_columns)
            result = self.database.execute(f'SELECT {cols} FROM library', connection)
        self.clear()
        for col_index, col in enumerate(self.database.library_table_columns):
            self.setHorizontalHeaderItem(col_index, QtGui.QStandardItem(str(col)))
        if len(result.records) > 0:
            for row_index, row in enumerate(result.records):
                self.insertRow(row_index, list(map(lambda x: QtGui.QStandardItem(str(x)), row)))
