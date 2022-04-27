import os.path
import typing
from typing import Optional

from PySide6 import QtCore
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtSql import QSqlQuery

import apollo.utils
from apollo.db.database import Connection, Database, QueryBuildFailed
from apollo.utils import get_configparser, write_config

CONFIG = get_configparser()


class PlaylistsModel(QStandardItemModel):
    """Model for playlist table"""
    TABLE_UPDATE = QtCore.Signal()

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        """
        Constructor

        Args:
            parent (QtCore.QObject): parent object for the model.
        """
        super().__init__(parent)
        self.database = Database()
        self.fields = self.database.playlist_columns

        self.valid_playlists = list(CONFIG['PLAYLISTS'].keys())
        self.loaded_playlist = ''
        self.load_playlist(CONFIG['GLOBALS']["loaded_playlist"])

    def load_playlist(self, name: str):
        """
        load playlist into the model

        Args:
            name (str): name of the playlist to load
        """
        if name:
            self.fetch_records(name)
            self.create_playList(name)
            CONFIG['GLOBALS']["loaded_playlist"] = name
            self.loaded_playlist = name
            write_config(CONFIG)

    def fill_headerdata(self):
        """fills the header data for the loaded model with DB column headers"""
        for index, item in enumerate(self.database.library_columns):
            item = str(item).title().replace("_", " ")
            self.setHorizontalHeaderItem(index, QStandardItem(item))

    def fetch_records(self, name: str = None):
        """
        fetches data from the database into the model

        Args:
            name (str): name of the playlist to load
        """
        if name in self.valid_playlists and name is not None:
            columns = ", ".join([f"library.{i}" for i in self.database.library_columns])
            with Connection(self.database.database_file) as CONN:
                query = self.database.exec_query(query = f"""
                        SELECT {columns} 
                        FROM {name} 
                        INNER JOIN library ON {name}.file_id = library.file_id
                        ORDER BY '{name}.play_order'
                        """, db = CONN)
                self.fill_table(query)
                self.loaded_playlist = name

    def search_table(self, text: str):
        """
        Queries the table and filters the loaded models data

        Args:
            text (str): string to search for in tracktitle, artist, album, file_name columns
        """
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
                    self.fill_table(query)
            else:
                self.fetch_records()
        except QueryBuildFailed:
            self.fetch_records()

    def fill_table(self, query: QSqlQuery):
        """
        Fetches the data from the query and fills the model

        Args:
            query (QSqlQuery): query to fetch data from and fill model with
        """
        self.clear()
        self.fill_headerdata()
        for row in self.database.fetch_all(query, lambda x: QStandardItem(str(x))):
            self.appendRow(row)

    @apollo.utils.threadit
    def create_playList(self, ids: list[str], name: str = None):
        """
        creates a playlist from file_ids

        Args:
            name (str): name of the playlist to create
            ids (list[str]): list of files ids to add to the playlist
        """
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
                self.add_playlist_toconfig(name)
            if name == self.loaded_playlist:
                self.fetch_records(name)
            elif self.loaded_playlist == "":
                self.load_playlist(name)
            self.TABLE_UPDATE.emit()

    def delete_item_fromDB(self, ids: list[str]):
        """
        Deletes items from the playlist

        Args:
            ids (list[str]): file ids of the files to be removed from the playlist
        """
        if len(ids) > 0:
            if len(ids) == 1:
                ids = f"('{ids[0][0]}')"
            else:
                ids = tuple(id[0] for id in ids)
            with Connection(self.database.database_file) as CON:
                self.database.exec_query(f"DELETE FROM '{self.loaded_playlist}' WHERE file_id IN {ids}",
                                         db = CON, commit = True)
                self.fetch_records()
            self.TABLE_UPDATE.emit()

    def add_playlist_toconfig(self, name: str):
        """
        Adds the playlist name to the list of available playlist

        Args:
            name (str): name of the playlist to add
        """
        playlist = CONFIG['PLAYLISTS']
        if name not in playlist:
            CONFIG['PLAYLISTS'][name] = ''
            write_config(CONFIG)
