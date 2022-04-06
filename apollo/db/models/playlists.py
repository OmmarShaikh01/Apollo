from typing import Optional

from PySide6 import QtCore
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtSql import QSqlQuery

from apollo.db.database import Connection, Database, QueryBuildFailed


class PlaylistsModel(QStandardItemModel):
    TABLE_UPDATE = QtCore.Signal()

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.database = Database()
        self.fields = self.database.playlist_columns

        # TODO: add loaded and all playlists field in config
        self.valid_playlists = ["temp_playlist"]
        self.loadPlaylist(self.valid_playlists[0])

    def loadPlaylist(self, name):
        self.fetchRecords(name)
        self.create_playList(name)
        self.loaded_playlist = name

    def fillHeaderData(self):
        for index, item in enumerate(self.database.library_columns):
            item = str(item).title().replace("_", " ")
            self.setHorizontalHeaderItem(index, QStandardItem(item))

    def fetchRecords(self, name = None):
        if name is None:
            return None
        elif name in self.valid_playlists:
            columns = ", ".join([f"library.{i}" for i in self.database.library_columns])
            with Connection(self.database.database_file) as CONN:
                query = self.database.exec_query(query = f"""
                SELECT {columns} 
                FROM {name} 
                INNER JOIN library ON {name}.file_id = library.file_id
                ORDER BY '{name}.play_order'
                """, db = CONN)
                self.refill_table(query)
                self.loaded_playlist = name
        else:
            return None

    def searchTable(self, text):
        try:
            if text:
                columns = ", ".join([f"library.{i}" for i in self.database.library_columns])
                with Connection(self.database.database_file) as CONN:
                    query = self.database.exec_query(
                        query = f"""
                        SELECT {columns} FROM (
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

    def create_playList(self, name: str = None, ids = None):
        if name is None:
            name = self.loaded_playlist

        table_query = f"""
        CREATE TABLE IF NOT EXISTS "{name}" (        
            "file_id" TEXT NOT NULL,
            "play_order" INTEGER,
            FOREIGN KEY("file_id") REFERENCES "library"("file_id"),
            PRIMARY KEY("play_order")
        );
        """
        if ids is not None:
            with Connection(self.database.database_file) as CON:
                QSqlQuery(table_query, db = CON).exec()
                self.database.batchinsert_data(name, [{'file_id': key[0]} for key in ids], ['file_id'], CON)
            self.fetchRecords(self.loaded_playlist)
        self.TABLE_UPDATE.emit()
