import os

from PySide6 import QtCore
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtSql import QSqlQuery

from apollo.db.database import Connection, LibraryManager, QueryExecutionFailed, QueryBuildFailed
from apollo.utils import threadit


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
    def add_item_fromFS(self, path):
        """
        Scans the filesystem, inserts and updates the model

        Args:
            path (str): path to the directory to scan
        """
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
                ids = tuple(id[0] for id in ids)
            with Connection(self.database.database_file) as CON:
                self.database.exec_query(f"DELETE FROM 'library' WHERE file_id IN {ids}", db = CON, commit = True)
                self.fetch_records()
            self.TABLE_UPDATE.emit()
