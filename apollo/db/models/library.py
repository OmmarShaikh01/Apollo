from typing import Optional

import PySide6.QtCore
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtSql import QSqlQuery, QSqlDatabase

from apollo.db.database import Database, Connection, QueryBuildFailed
from apollo.media import Mediafile


class LibraryModel(QStandardItemModel):

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.database = Database()
        self.fields = self.database.library_columns
        self.fetchRecords()

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
        for row in self.database.fetch_all(query, lambda x: QStandardItem(str(x))):
            self.appendRow(row)
