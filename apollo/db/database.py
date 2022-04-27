import os
import random
from types import TracebackType
from typing import Callable, Union

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from apollo.media import Mediafile
from apollo.utils import threadit, get_logger, get_configparser

CONFIG = get_configparser()
LOGGER = get_logger(__name__)

class DBStructureError(Exception):
    """Raised when DB Tables or relations are not present"""
    __module__ = "Database"


class QueryBuildFailed(Exception):
    """Raised when Query build fails"""
    __module__ = "Database"


class QueryExecutionFailed(Exception):
    """Raised when execution fails"""
    __module__ = "Database"


class Connection:
    """ Connector used execute queries """

    def __init__(self, db_path: str, commit: bool = True):
        """
        Constructor

        Args:
            db_path (str): database file path to connect
            commit (bool): autocommit of commits on exit
        """
        super().__init__()
        self.database = self.connect(db_path)
        self.name = str(random.random())
        self.autocommit = commit

    def __enter__(self) -> QSqlDatabase:
        """
        Returns:
            QSqlDatabase: a connection object used to execute queries
        """
        self.db_driver = QSqlDatabase.addDatabase("QSQLITE", self.name)
        self.db_driver.setDatabaseName(self.database)
        if self.db_driver.open() and self.db_driver.isValid() and self.db_driver.isOpen():
            self.db_driver.exec("PRAGMA foreign_keys=ON")
            return self.db_driver
        else:
            raise ConnectionError(self.database)

    def __exit__(self, exc_type: BaseException, value: BaseException, traceback: TracebackType):
        """
        Args:
            exc_type (BaseException): Exception type
            value (BaseException): Exception Value
            traceback (TracebackType): Traceback stack
        """
        if hasattr(self, "db_driver"):
            if self.autocommit:
                self.db_driver.commit()
            del self.db_driver
        if any([exc_type, value, traceback]):
            print(f"Type: {exc_type}\nValue: {value}\nTraceback:\n{traceback}")
        QSqlDatabase.removeDatabase(self.name)

    @staticmethod
    def connect(db_path: str) -> str:
        """
        Connection validator used to connect to a database

        Args:
            db_path (str): database path

        Returns:
            str: if the connection file is valid, otherwise None
        """
        if (db_path == ":memory:") or os.path.splitext(db_path)[1] == ".db":
            return db_path
        else:
            raise ValueError(db_path)


class Database:
    """
    Database class for all database queries and methods
    """
    library_columns = [
        "file_id",
        "file_name",
        "file_path",
        "tracktitle",
        "artist",
        "album",
        "albumartist",
        "composer",
        "tracknumber",
        "totaltracks",
        "discnumber",
        "totaldiscs",
        "genre",
        "year",
        "compilation",
        "lyrics",
        "isrc",
        "comment",
        "artwork",
        "bitrate",
        "codec",
        "length",
        "channels",
        "bitspersample",
        "samplerate",
        "rating",
        "isLiked",
        "play_count"
    ]
    playlist_columns = ["file_id", "order"]
    queue_columns = ["file_id", "order"]

    def __init__(self) -> None:
        self.database_file = CONFIG["GLOBALS"]["database_location"]
        self.init_structure()

    def init_structure(self):
        """
        Initializes all the database tables and relations
        """
        table_query_library = """
        CREATE TABLE IF NOT EXISTS "library" (
            "file_id"	TEXT NOT NULL,
            "file_name"	TEXT NOT NULL,
            "file_path"	TEXT NOT NULL,
            "tracktitle"	TEXT,
            "artist"	TEXT,
            "album"	TEXT,
            "albumartist"	TEXT,
            "composer"	TEXT,
            "tracknumber"	TEXT,
            "totaltracks"	TEXT,
            "discnumber"	TEXT,
            "totaldiscs"	TEXT,
            "genre"	TEXT,
            "year"	TEXT,
            "compilation"	TEXT,
            "lyrics"	TEXT,
            "isrc"	TEXT,
            "comment"	TEXT,
            "artwork"	TEXT,
            "bitrate"	TEXT,
            "codec"	TEXT,
            "length"	TEXT,
            "channels"	TEXT,
            "bitspersample"	TEXT,
            "samplerate"	TEXT,
            "rating"	INTEGER  DEFAULT 0,
            "isLiked"	INTEGER  DEFAULT 0,
            "play_count"	INTEGER  DEFAULT 0,
            PRIMARY KEY("file_id")
        );
        """
        table_query_queue = """
        CREATE TABLE IF NOT EXISTS "queue" (
            "file_id" TEXT NOT NULL,
            "play_order" INTEGER,
            FOREIGN KEY("file_id") REFERENCES "library"("file_id"),
            PRIMARY KEY("play_order")
        );
        """
        with Connection(self.database_file) as CON:
            self.exec_query(table_query_library, db = CON).exec()
            self.exec_query(table_query_queue, db = CON).exec()
            del CON

    def exec_query(self, query: Union[str, QSqlQuery], db: QSqlDatabase, commit: bool = True):
        """
        Creates a connection to the DB that is linked to the main class

        Args:
            query (str): query string used for execution
            db (QSqlDatabase): Connection used to execute queries on
            commit (bool): autocommit flag, commits the query after execution

        Returns:
            QSqlQuery: executed query, with the fetched data
        """
        if isinstance(query, str):
            query_str = query
            query = QSqlQuery(db = db)
            if not query.prepare(query_str):
                connection_info = (str(db))
                LOGGER.error(f"{connection_info}: {query_str}")
                raise QueryBuildFailed(f"{connection_info}\n{query_str}")

        # executes the given query
        query_executed = query.exec()
        log_msg = ''.join(part.strip() for part in str(query.lastQuery()).splitlines())
        LOGGER.info(f"Executed: {log_msg}")

        if commit:
            db.commit()

        if not query_executed:
            connection_info = (str(db))
            msg = f"\nEXE: {query_executed}" \
                  f"\nERROR: {(query.lastError().text())}" \
                  f"\nQuery: {query.lastQuery()}" \
                  f"\nConnection: {connection_info}"
            LOGGER.error(f"FAILED: {log_msg}")
            raise QueryExecutionFailed(msg)
        else:
            return query

    def fetch_all(self, query: QSqlQuery, to_obj: Callable = None, fltr_column: Union[list[int], int] = None) -> list[list[any]]:
        """
        fetches data from te executed query

        Args:
            query (QSqlQuery): query to get data from
            to_obj (Callable): a callable(x: string) used to box string type to any
            fltr_column: filtering the columns to output

        Returns:
            list[list[any]]: table of the fetched data
        """
        if fltr_column is None:
            fltr_column = [query.record().count()]
        if isinstance(fltr_column, int):
            fltr_column = [fltr_column]

        data = []
        if len(fltr_column) == 1:
            fltr_column = range(fltr_column[0])
            if to_obj:
                while query.next():
                    data.append([to_obj(query.value(C)) for C in fltr_column])
            else:
                while query.next():
                    data.append([query.value(C) for C in fltr_column])
        else:
            if to_obj:
                while query.next():
                    data.append([to_obj(query.value(C)) for C in fltr_column])
            else:
                while query.next():
                    data.append([query.value(C) for C in fltr_column])
        return data

    def insert_Metadata(self, metadata: dict, keys: list, connection: QSqlDatabase = None):
        """
        Inserts Music metadata into the library database

        Args:
            metadata (dict): metadata dict
            keys (list): fields list
            connection (QSqlDatabase): database connection
        """
        def internal_call(con: QSqlDatabase):
            columns = ", ".join([f"'{i}'" for i in keys])
            placeholders = ", ".join(["?" for i in keys])
            query = QSqlQuery(f"INSERT OR IGNORE INTO library ({columns}) VALUES ({placeholders})", db = con)
            [query.bindValue(index, metadata[key]) for index, key in enumerate(keys)]
            if query.exec():
                con.commit()
            else:
                connection_info = (str(con))
                msg = f"\nERROR: {(query.lastError().text())}" \
                      f"\nQuery: {query.lastQuery()}" \
                      f"\nConnection: {connection_info}"
                raise QueryExecutionFailed(msg)

        if connection is None:
            with Connection(self.database_file) as connection:
                internal_call(connection)
        else:
            internal_call(connection)

    def batchinsert_data(self, table: str, data: list, keys: list, connection: QSqlDatabase = None):
        """
        Inserts data into the table

        Args:
            table (str): table to fill data into
            data (list): data to be inserted into the table
            keys (list): fields list
            connection (QSqlDatabase): database connection
        """
        def internal_call(con):
            self.exec_query(query = "PRAGMA journal_mode = MEMORY", db = con)
            con.transaction()
            columns = ", ".join([f"'{i}'" for i in keys])
            placeholders = ", ".join(["?" for i in keys])
            query = QSqlQuery(f"INSERT OR IGNORE INTO {table} ({columns}) VALUES ({placeholders})", db = con)
            for key in keys:
                query.addBindValue([value[key] for value in data])
            if query.execBatch():
                con.commit()
                self.exec_query(query = "PRAGMA journal_mode = WAL", db = con)
            else:
                connection_info = (str(con))
                msg = f"\nERROR: {(query.lastError().text())}" \
                      f"\nQuery: {query.lastQuery()}" \
                      f"\nConnection: {connection_info}"
                raise QueryExecutionFailed(msg)

        if connection is None:
            with Connection(self.database_file) as connection:
                internal_call(connection)
        else:
            internal_call(connection)


class LibraryManager(Database):

    def __init__(self) -> None:
        super().__init__()

    def loaded_directories(self):
        """
        Returns the directories the files are being loaded from

        Returns:
            list[list[str]]: directories the files are being loaded from
        """
        query = r"""
        SELECT  rtrim(replace(file_path, file_name, ''), '\') AS 'directory' 
        FROM library 
        GROUP BY 'directory'
        """
        with Connection(self.database_file) as connection:
            return self.fetch_all(self.exec_query(query, db = connection))

    def scan_directory(self, directory: str):
        """
        Starts a recursive scan of the directory and inserts the metadata into the file

        Args:
            directory (str): directory to scan files from
        """
        if not os.path.isdir(directory):
            return None

        scanned_files = []
        for dirct, subdirs, files in os.walk(directory):
            for file in files:
                path = (os.path.normpath(os.path.join(dirct, file)))
                if Mediafile.isSupported(path):
                    mediafile = Mediafile(path)
                    if mediafile.SynthTags['file_id']:
                        scanned_files.append(mediafile.SynthTags)
        self.batchinsert_data('library', scanned_files, Mediafile.tags_fields)

    def scan_file(self, path: str):
        """
        Starts a scan of the file and inserts the metadata into the library

        Args:
            path (str): file to scan and insert into library
        """
        if not os.path.isfile(path):
            return None

        if Mediafile.isSupported(path):
            mediafile = Mediafile(path)
            if mediafile.SynthTags['file_id']:
                self.insert_Metadata(mediafile.SynthTags, Mediafile.tags_fields)


if __name__ == '__main__':
    manager = LibraryManager()
    manager.scan_file(r"D:\Music\fold_2\topntch.mp3")
