import copy
import os
import configparser
import random
import typing
from typing import Union, Callable

from PySide6.QtSql import QSqlQuery, QSqlDatabase

from apollo.media import Mediafile

PARENT_ROOT = (os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
config = configparser.ConfigParser()
config.read(os.path.join(PARENT_ROOT, '.ini'))


class DBStructureError(Exception):
    __module__ = "LibraryManager"


class QueryBuildFailed(Exception):
    __module__ = "LibraryManager"


class QueryExecutionFailed(Exception):
    __module__ = "LibraryManager"


class Connection:

    def __init__(self, db_name: str, commit: bool = True):
        super().__init__()
        self.database = self.connect(db_name)
        self.autocommit = commit

    def __enter__(self):
        self.db_driver = QSqlDatabase.addDatabase("QSQLITE", str(random.random()))
        self.db_driver.setDatabaseName(self.database)
        if self.db_driver.open() and self.db_driver.isValid() and self.db_driver.isOpen():
            return self.db_driver
        else:
            raise ConnectionError(self.database)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if hasattr(self, "db_driver"):
            self.db_driver.commit()
            del self.db_driver
        if any([exc_type, exc_value, exc_traceback]):
            print(f"exc_type: {exc_type}\nexc_value: {exc_value}\nexc_traceback: {exc_traceback}")
        QSqlDatabase.removeDatabase(str(random.random()))

    @staticmethod
    def connect(db_name: str):
        if (db_name == ":memory:") or os.path.splitext(db_name)[1] == ".db":
            return db_name
        else:
            raise ConnectionError()


class Database:
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
        "isLiked"
    ]
    playlist_columns = ["file_id", "order"]
    queue_columns = ["file_id", "order"]

    def __init__(self) -> None:
        self.database_file = config["DATABASE"]["file_location"]
        self.initilize_structure()

    def initilize_structure(self):
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
            "isLiked"	INTEGER  DEFAULT 0,
            PRIMARY KEY("file_id")
        );
        """
        table_query_queue = """
        CREATE TABLE IF NOT EXISTS "queue" (
            "file_id" TEXT NOT NULL,
            "order" INTEGER,
            FOREIGN KEY("file_id") REFERENCES "library"("file_id"),
            PRIMARY KEY("order")
        );
        """
        with Connection(self.database_file) as CON:
            QSqlQuery(table_query_library, db = CON).exec()
            QSqlQuery(table_query_queue, db = CON).exec()
            del CON

    def batchinsert_Metadata(self, metadata: dict, keys: list, connection: Connection = None):

        def internal_call(CON, keys, metadata):
            CON.transaction()
            self.exec_query(query = "PRAGMA journal_mode = MEMORY", db = CON)
            columns = ", ".join([f"'{i}'" for i in keys])
            placeholders = ", ".join(["?" for i in keys])
            query = QSqlQuery(f"INSERT OR IGNORE INTO library ({columns}) VALUES ({placeholders})", db = CON)
            for key in keys:
                query.addBindValue([value[key] for value in metadata])
            if query.execBatch():
                self.exec_query(query = "PRAGMA journal_mode = WAL", db = CON)
                CON.commit()
            else:
                msg = f"ERROR: {(query.lastError().text())}\nQuery: {query.lastQuery()}"
                self.exec_query(query = "PRAGMA journal_mode = WAL", db = CON)
                raise QueryExecutionFailed(msg)

        if connection is None:
            with Connection(self.database_file) as CON:
                internal_call(CON, keys, metadata)
        else:
            internal_call(connection, keys, metadata)

    def batchinsert_data(self, table: str, data: dict, keys: list, connection: Connection = None):

        def internal_call(CON, keys, data):
            CON.transaction()
            self.exec_query(query = "PRAGMA journal_mode = MEMORY", db = CON)
            columns = ", ".join([f"'{i}'" for i in keys])
            placeholders = ", ".join(["?" for i in keys])
            query = QSqlQuery(f"INSERT OR IGNORE INTO {table} ({columns}) VALUES ({placeholders})", db = CON)
            for key in keys:
                query.addBindValue([value[key] for value in data])
            if query.execBatch():
                self.exec_query(query = "PRAGMA journal_mode = WAL", db = CON)
                CON.commit()
            else:
                msg = f"ERROR: {(query.lastError().text())}\nQuery: {query.lastQuery()}"
                self.exec_query(query = "PRAGMA journal_mode = WAL", db = CON)
                raise QueryExecutionFailed(msg)

        if connection is None:
            with Connection(self.database_file) as CON:
                internal_call(CON, keys, data)
        else:
            internal_call(connection, keys, data)

    def exec_query(self, query: str, db: Connection, column: Union[int, None] = None, commit: bool = True):
        # creates a connection to the DB that is linked to the main class
        if isinstance(query, str):
            query_str = query
            query = QSqlQuery(db = db)
            if not query.prepare(query_str):
                connection_info = (str(db))
                raise QueryBuildFailed(f"{connection_info}\n{query_str}")

        # executes the given query
        query_executed = query.exec()
        if not query_executed:
            connection_info = (str(db))
            msg = f"""
                EXE: {query_executed}
                ERROR: {(query.lastError().text())}
                Query: {query.lastQuery()}
                Connection: {connection_info}
                """
            raise QueryExecutionFailed(msg)
        else:
            return query

    def fetch_all(self, query: QSqlQuery, to: Callable = None, column: Union[int, None] = None):
        data = []

        if column is None:
            column = query.record().count()

        if column == 1:
            if to:
                while query.next():
                    data.append(to(query.value(0)))
            else:
                while query.next():
                    data.append(query.value(0))
        else:
            if to:
                while query.next():
                    data.append([to(query.value(C)) for C in range(column)])
            else:
                while query.next():
                    data.append([query.value(C) for C in range(column)])
        return data


class LibraryManager(Database):

    def __init__(self) -> None:
        super().__init__()

    def scan_directory(self, directiory: str):
        if not os.path.isdir(directiory):
            return None

        scanned_files = []
        for dir, subdirs, files in os.walk(directiory):
            for file in files:
                path = (os.path.normpath(os.path.join(dir, file)))
                if Mediafile.isSupported(path):
                    mediafile = Mediafile(path)
                    if mediafile.SynthTags['file_id']:
                        scanned_files.append(mediafile.SynthTags)
        self.batchinsert_Metadata(scanned_files, Mediafile.tags_fields)


if __name__ == '__main__':
    import dotenv

    dotenv.load_dotenv(os.path.join(PARENT_ROOT, 'development.env'))
    manager = LibraryManager()
    manager.scan_directory(r"D:\Music")
