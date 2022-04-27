import enum
from typing import Optional

from PySide6 import QtCore
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtSql import QSqlQuery

from apollo.db.database import Connection, Database, QueryBuildFailed
from apollo.utils import threadit, get_logger, get_configparser

LOGGER = get_logger(__name__)
CONFIG = get_configparser()


class QueueModel(QStandardItemModel):
    """Model for queue table"""

    class PlayType(enum.Enum):
        ALL = 0
        ARTIST = 1
        GENRE = 2

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
        # TODO: add loaded and all playlists field in config
        self.loaded_playlist = 'queue'
        self.fetch_records()

    def fill_headerdata(self):
        """fills the header data for the loaded model with DB column headers"""
        for index, item in enumerate(self.database.library_columns):
            item = str(item).title().replace("_", " ")
            self.setHorizontalHeaderItem(index, QStandardItem(item))

    def fetch_records(self):
        """fetches data from the database into the model"""
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
            self.fill_table(query)

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

    def fill_table(self, query):
        """
        Fetches the data from the query and fills the model

        Args:
            query (QSqlQuery): query to fetch data from and fill model with
        """
        self.clear()
        self.fill_headerdata()
        for row in self.database.fetch_all(query, lambda x: QStandardItem(str(x))):
            self.appendRow(row)

    @threadit
    def create_playList(self, ids: list[str], _type: PlayType = PlayType.ALL):
        """
        creates a queue from file_ids

        Args:
            ids (list[str]): list of files ids to add to the playlist
            _type (PlayType): Type of selection method used to create the queue
        """
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
        if len(ids) > 0:
            with Connection(self.database.database_file) as CON:
                self.database.exec_query(table_drop, db = CON)
                self.database.exec_query(table_query, db = CON)

                if _type == self.PlayType.ALL:
                    self.database.batchinsert_data(name, [{'file_id': key[0]} for key in ids], ['file_id'], CON)
                else:
                    if len(ids) == 1:
                        ids = f"('{ids[0][0]}')"
                    else:
                        ids = tuple(id[0] for id in ids)

                    if _type == self.PlayType.ARTIST:
                        selector_query = f"""
                        INSERT INTO queue (file_id)
                        SELECT library.file_id 
                        FROM library 
                        WHERE library.artist
                        IN (
                            SELECT library.artist 
                            FROM library 
                            WHERE file_id 
                            IN {ids}
                        )
                        """
                        CON.transaction()
                        self.database.exec_query(selector_query, CON)
                    elif _type == self.PlayType.GENRE:
                        ids = tuple([key[0] for key in ids])
                        selector_query = f"""
                        INSERT INTO queue (file_id)
                        SELECT library.file_id 
                        FROM library 
                        WHERE library.genre 
                        IN (
                            SELECT library.genre 
                            FROM library 
                            WHERE file_id 
                            IN {ids}
                        )
                        """
                        CON.transaction()
                        self.database.exec_query(selector_query, CON)
                    else:
                        pass
            self.fetch_records()
            self.TABLE_UPDATE.emit()

    @threadit
    def add_item_toqueue_top(self, first: str, remaining: list[[str]]):
        """
        creates a queue from the file ids provided

        Args:
            first (str): first item to start the queue from
            remaining (list[[str]]): remaining file ids to add to the queue
        """
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
        primary_insert = f"""INSERT INTO "{name}" ('file_id') VALUES ('{first}')"""
        if len(remaining) > 0:
            with Connection(self.database.database_file) as CON:
                self.database.exec_query(table_drop, db = CON)
                self.database.exec_query(table_query, db = CON)
                self.database.exec_query(primary_insert, db = CON)
                self.database.batchinsert_data(name, [{'file_id': key} for key in remaining], ['file_id'], CON)
            self.fetch_records()
            self.TABLE_UPDATE.emit()
