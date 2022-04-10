from typing import Optional

from PySide6 import QtCore
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtSql import QSqlQuery

import apollo.utils
from apollo.db.database import Connection, Database, QueryBuildFailed


class QueueModel(QStandardItemModel):
    TABLE_UPDATE = QtCore.Signal()

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.database = Database()
        self.fields = self.database.playlist_columns
        # TODO: add loaded and all playlists field in config
        self.loaded_playlist = 'queue'
        self.fetchRecords()

    def fillHeaderData(self):
        for index, item in enumerate(self.database.library_columns):
            item = str(item).title().replace("_", " ")
            self.setHorizontalHeaderItem(index, QStandardItem(item))

    def fetchRecords(self):
        name = self.loaded_playlist
        columns = ", ".join([f"library.{i}" for i in self.database.library_columns])
        with Connection(self.database.database_file) as CONN:
            query = self.database.exec_query(
                query = f"""
                SELECT {columns}
                FROM {name} 
                INNER JOIN library ON {name}.file_id = library.file_id
                ORDER BY '{name}.play_order'
                """, db = CONN)
            self.refill_table(query)

    def searchTable(self, text):
        try:
            if text:
                name = self.loaded_playlist
                columns = ", ".join([f"library.{i}" for i in self.database.library_columns])
                with Connection(self.database.database_file) as CONN:
                    query = self.database.exec_query(
                        query = f"""
                        SELECT * FROM (
                            SELECT {columns}
                            FROM {name} 
                            INNER JOIN library ON {name}.file_id = library.file_id
                            ORDER BY '{name}.play_order'
                        ) 
                        WHERE 
                        tracktitle LIKE '%{text}%' OR
                        artist LIKE '%{text}%' OR
                        album LIKE '%{text}%' OR
                        file_name LIKE '%{text}%' 
                        """,
                        db = CONN
                    )
                    self.refill_table(query)
            else:
                self.fetchRecords()
        except QueryBuildFailed:
            self.fetchRecords()

    def refill_table(self, query):
        self.clear()
        self.fillHeaderData()
        for row in self.database.fetch_all(query, lambda x: QStandardItem(str(x))):
            self.appendRow(row)

    @apollo.utils.threadit
    def create_playList(self, name: str = None, ids = None):
        if name is None:
            name = self.loaded_playlist
        if ids is None:
            ids = []

        table_drop = f"""DROP TABLE IF EXISTS "{name}" """
        table_query = f"""
        CREATE TABLE IF NOT EXISTS "{name}" (        
            "file_id" TEXT NOT NULL,
            "play_order" INTEGER,
            FOREIGN KEY("file_id") REFERENCES "library"("file_id") ON DELETE CASCADE,
            PRIMARY KEY("play_order")
        );
        """
        if len(ids) > 0:
            with Connection(self.database.database_file) as CON:
                self.database.exec_query(table_drop, db = CON)
                self.database.exec_query(table_query, db = CON)
                self.database.batchinsert_data(name, [{'file_id': key[0]} for key in ids], ['file_id'], CON)
            self.fetchRecords()
            self.TABLE_UPDATE.emit()

    @apollo.utils.threadit
    def addItemToQueueTop(self, first: str, remaining: list[[str]]):
        if first in [" ", "", None]:
            return False
        remaining = [item[0] for item in remaining if item[0] != first]
        name = self.loaded_playlist
        table_drop = f"""DROP TABLE IF EXISTS "{name}" """
        table_query = f"""
        CREATE TABLE IF NOT EXISTS "{name}" (        
            "file_id" TEXT NOT NULL,
            "play_order" INTEGER,
            FOREIGN KEY("file_id") REFERENCES "library"("file_id") ON DELETE CASCADE,
            PRIMARY KEY("play_order")
        );
        """
        primary_insert = (f"""INSERT INTO "{name}" ('file_id') VALUES ('{first}')""")
        if len(remaining) > 0:
            with Connection(self.database.database_file) as CON:
                self.database.exec_query(table_drop, db = CON)
                self.database.exec_query(table_query, db = CON)
                self.database.exec_query(primary_insert, db = CON)
                self.database.batchinsert_data(name, [{'file_id': key} for key in remaining], ['file_id'], CON)
            self.fetchRecords()
            self.TABLE_UPDATE.emit()
