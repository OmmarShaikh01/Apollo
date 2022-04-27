import enum
import os

from PySide6 import QtCore
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtSql import QSqlQuery

from apollo.db.database import Connection, LibraryManager, QueryBuildFailed, QueryExecutionFailed
from apollo.utils import add_to_config, get_configparser, get_logger, threadit, write_config
from apollo.media import Mediafile

LOGGER = get_logger(__name__)


class LibraryModel(QStandardItemModel):
    """
    Model for library table
    """
    TABLE_UPDATE = QtCore.Signal()

    def __init__(self, parent: QtCore.QObject = None) -> None:
        """
        Constructor

        Args:
            parent (QtCore.QObject): parent object for the model.
        """
        super().__init__(parent)
        self.database = LibraryManager()
        self.fields = self.database.library_columns
        self.fetch_records()

        self.TABLE_UPDATE.connect(lambda: self.fetch_records())

    def fill_headerdata(self):
        """fills the header data for the loaded model with DB column headers"""
        for index, item in enumerate(self.fields):
            item = str(item).title().replace("_", " ")
            self.setHorizontalHeaderItem(index, QStandardItem(item))

    def fetch_records(self):
        """fetches data from the database into the model"""
        columns = ", ".join([f"{i}" for i in self.fields])
        with Connection(self.database.database_file) as CONN:
            query = self.database.exec_query(query = f"SELECT {columns} FROM library", db = CONN)
            self.fill_table(query)

    def fill_table(self, query: QSqlQuery):
        """
        Fetches the data from the query and fills the model

        Args:
            query (QSqlQuery): query to fetch data from and fill model with
        """
        self.clear()
        self.fill_headerdata()
        for index, row in enumerate(self.database.fetch_all(query, lambda x: QStandardItem(str(x)))):
            self.appendRow(row)

    def search_table(self, text: str):
        """
        Queries the table and filters the loaded models data

        Args:
            text (str): string to search for in tracktitle, artist, album, file_name columns
        """
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
                    self.fill_table(query)
            except QueryBuildFailed:
                self.fetch_records()
        else:
            self.fetch_records()

    def get_fileinfo(self, file_id: str) -> dict:
        """
        fetches the file tags from the database into a dict
        Args:
            file_id:

        Returns:
            dict: file info metadata
        """
        columns = ", ".join([f"{i}" for i in self.fields])
        query = f"SELECT {columns} FROM library WHERE file_id LIKE '%{file_id}%' LIMIT 1"
        with Connection(self.database.database_file) as CONN:
            query = self.database.exec_query(query, db = CONN)
            return {index: row for index, row in zip(self.fields, self.database.fetch_all(query, lambda x: str(x))[0])}

    @threadit
    def add_item_fromFS(self, path: [str, list[str]]):
        """
        Scans the filesystem, inserts and updates the model

        Args:
            path (str): path to the directory to scan
        """

        def scan_path(file_path: str):
            if os.path.isdir(file_path):
                self.database.scan_directory(file_path)
                self.add_dir_to_watcher(file_path)
                LOGGER.info(f"Scanned {file_path}")
            elif os.path.isfile(file_path):
                self.database.scan_file(file_path)
                LOGGER.info(f"Scanned {file_path}")
            else:
                pass

        try:
            if isinstance(path, list):
                for item in path:
                    scan_path(item)
            elif isinstance(path, str):
                scan_path(path)
            else:
                pass

        except QueryExecutionFailed:
            self.TABLE_UPDATE.emit()
            return None
        finally:
            self.TABLE_UPDATE.emit()

    def delete_item_fromFS(self, ids: list[str]):
        """
        Deletes items from the filesystem

        Args:
            ids (list[str]): file ids of the files to be removed
        """
        if len(ids) > 0:
            if len(ids) == 1:
                ids = f"('{ids[0][0]}')"
            else:
                ids = tuple(_id[0] for _id in ids)
            with Connection(self.database.database_file) as CON:
                self.database.exec_query(f"DELETE FROM 'library' WHERE file_id IN {ids}", db = CON, commit = True)
                self.fetch_records()
            self.TABLE_UPDATE.emit()

    # noinspection PyMethodMayBeStatic
    def add_dir_to_watcher(self, path: str):
        config = get_configparser()
        add_to_config('WATCHER/FILES', path, config)
        add_to_config('WATCHER/MONITOR', path, config)
        write_config(config)

    def fetch_file_info(self, path: str) -> dict:
        if Mediafile.isSupported(path):
            media = Mediafile(path)
            if media.SynthTags['file_id']:
                return media.SynthTags

    def reload_tags(self, path: str):
        if Mediafile.isSupported(path):
            media = Mediafile(path)
            if not media.SynthTags['file_id']:
                return None

            tags = media.SynthTags
            _id = tags['file_id']
            placeholders = ", ".join("=".join((v, '?')) for v in tags.keys())
            query = f"""
            UPDATE 'library'
            SET {placeholders}
            WHERE library.file_id LIKE '{_id}'
            """
            with Connection(self.database.database_file) as CON:
                query = QSqlQuery(query, CON)
                [query.bindValue(k, v) for k, v in enumerate(tags.values())]
                self.database.exec_query(query, CON)

            for row in range(self.rowCount()):
                if self.item(row, 0) == _id:
                    self.insertRow(row, list(map(lambda x: QStandardItem(str(x)), tags)))
