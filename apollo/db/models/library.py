from typing import Optional
import os, threading

from PySide6 import QtCore
from PySide6.QtGui import QStandardItem, QStandardItemModel

from apollo.db.database import Connection, Database, QueryBuildFailed, LibraryManager


def threadit(method):
    def exe(*args, **kwargs):
        thread = threading.Thread(target = lambda: (method(*args, **kwargs)))
        thread.start()
    return exe


class LibraryModel(QStandardItemModel):
    TABLE_UPDATE = QtCore.Signal()

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.database = LibraryManager()
        self.fields = self.database.library_columns
        self.fetchRecords()
        self.connectSignals()

    def connectSignals(self):
        self.TABLE_UPDATE.connect(lambda: self.fetchRecords())

    def fillHeaderData(self):
        for index, item in enumerate(self.fields):
            item = str(item).title().replace("_", " ")
            self.setHorizontalHeaderItem(index, QStandardItem(item))

    def fetchRecords(self):
        columns = ", ".join([f"{i}" for i in self.fields])
        with Connection(self.database.database_file) as CONN:
            query = self.database.exec_query(query = f"SELECT {columns} FROM library", db = CONN)
            self.refill_table(query)

    def searchTable(self, text):
        if text:
            try:
                columns = ", ".join([f"{i}" for i in self.fields])
                with Connection(self.database.database_file) as CONN:
                    query = self.database.exec_query(
                            query = f"""
                        SELECT {columns} FROM library 
                        WHERE 
                        tracktitle LIKE '%{text}%' OR
                        artist LIKE '%{text}%' OR
                        album LIKE '%{text}%' OR
                        file_name LIKE '%{text}%' 
                        """,
                            db = CONN
                    )
                    self.refill_table(query)
            except QueryBuildFailed:
                self.fetchRecords()
        else:
            self.fetchRecords()

    def refill_table(self, query):
        self.clear()
        self.fillHeaderData()
        for index, row in enumerate(self.database.fetch_all(query, lambda x: QStandardItem(str(x)))):
            self.appendRow(row)

    def getFileInfo(self, file_id: str):
        columns = ", ".join([f"{i}" for i in self.fields])
        query = f"SELECT {columns} FROM library LIMIT 1"
        with Connection(self.database.database_file) as CONN:
            query = self.database.exec_query(query, db = CONN)
            info = {index: row for index, row in zip(self.fields, self.database.fetch_all(query, lambda x: str(x))[0])}
        return info

    @threadit
    def add_ItemFormFS(self, path):
        try:
            if os.path.isdir(path):
                self.database.scan_directory(path)
            elif os.path.isfile(path):
                self.database.scan_file(path)
            else:
                pass
        except QueryExecutionFailed:
            self.TABLE_UPDATE.emit()
            return None
        finally:
            self.TABLE_UPDATE.emit()
