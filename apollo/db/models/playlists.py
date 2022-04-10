import os.path
import typing
from typing import Optional

from PySide6 import QtCore
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtSql import QSqlQuery

import apollo.utils
from apollo.db.database import Connection, Database, QueryBuildFailed
from apollo.utils import getConfigParser, writeConfig

CONFIG = getConfigParser()


class PlaylistsModel(QStandardItemModel):
    TABLE_UPDATE = QtCore.Signal()

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.database = Database()
        self.fields = self.database.playlist_columns

        # TODO: add loaded and all playlists field in config
        self.valid_playlists = eval(CONFIG['DEFAULT']["playlists"])
        self.loaded_playlist = ''
        self.loadPlaylist(CONFIG['DEFAULT']["loaded_playlist"])

    def loadPlaylist(self, name: typing.AnyStr):
        if name:
            self.fetchRecords(name)
            self.create_playList(name)
            CONFIG['DEFAULT']["loaded_playlist"] = name
            self.loaded_playlist = name
            writeConfig(CONFIG)

    def fillHeaderData(self):
        for index, item in enumerate(self.database.library_columns):
            item = str(item).title().replace("_", " ")
            self.setHorizontalHeaderItem(index, QStandardItem(item))

    def fetchRecords(self, name: typing.AnyStr = None):
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

    def searchTable(self, text: typing.AnyStr):
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

    def refill_table(self, query: QSqlQuery):
        self.clear()
        self.fillHeaderData()
        for row in self.database.fetch_all(query, lambda x: QStandardItem(str(x))):
            self.appendRow(row)

    @apollo.utils.threadit
    @apollo.utils.timeit
    def create_playList(self, name: typing.AnyStr = None, ids: typing.List = None):
        if name is None:
            name = self.loaded_playlist
        if ids is None:
            ids = []

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
                self.database.exec_query(table_query, db = CON)
                self.database.batchinsert_data(name, [{'file_id': key[0]} for key in ids], ['file_id'], CON)
                self.addPlaylistToConfig(name)
            if name == self.loaded_playlist:
                self.fetchRecords(name)
            elif self.loaded_playlist == "":
                self.loadPlaylist(name)
            self.TABLE_UPDATE.emit()

    def delete_ItemfromDB(self, ids: typing.List):
        if ids is None:
            ids = []
        if len(ids) > 0:
            if len(ids) == 1:
                ids = f"('{ids[0][0]}')"
            else:
                ids = tuple(id[0] for id in ids)
            with Connection(self.database.database_file) as CON:
                self.database.exec_query(f"""DELETE FROM '{self.loaded_playlist}' WHERE file_id IN {ids}""",
                                         db = CON, commit = True)
                self.fetchRecords()
            self.TABLE_UPDATE.emit()

    def addPlaylistToConfig(self, name: typing.AnyStr):
        playlist = eval(CONFIG['DEFAULT']["playlists"])
        if name not in playlist:
            playlist.append(name)
            CONFIG['DEFAULT']["playlists"] = str(playlist)
            writeConfig(CONFIG)
