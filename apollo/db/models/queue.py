from typing import Optional

import PySide6.QtCore
from PySide6 import QtGui

from apollo.media.decoders.decode import Stream
from apollo.db.database import Database, RecordSet


class QueueModel(QtGui.QStandardItemModel):
    COLUMNS = Stream.TAG_FRAMES
    PRIVATE_FIELDS = ['FILEID', 'FILEPATH', 'FILENAME', 'FILESIZE', 'FILEEXT']

    def __init__(self) -> None:
        super().__init__()
        self.database = Database()
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
            cols = ", ".join(map(lambda x: f'library.{x}', self.COLUMNS))
            query = f"SELECT {cols} FROM queue INNER JOIN library ON queue.FILEID = library.FILEID ORDER BY queue.PLAYORDER"
            result = self.database.execute(query, connection)
        self.clear()
        for col_index, col in enumerate(self.COLUMNS):
            self.setHorizontalHeaderItem(col_index, QtGui.QStandardItem(str(col)))
        if len(result.records) > 0:
            for row_index, row in enumerate(result.records):
                self.insertRow(row_index, list(map(lambda x: QtGui.QStandardItem(str(x)), row)))
