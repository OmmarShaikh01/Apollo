"""
DEV NOTES

TODO: Document code
TODO: Write unit tests
"""
from __future__ import annotations

import copy
import dataclasses
import os
import uuid
from pathlib import PurePath
from types import TracebackType
from typing import Union

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from apollo.media import Mediafile
from apollo.utils import get_logger
from configs import settings

CONFIG = settings
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


class Connection(QSqlDatabase):
    """ Connector used execute queries """

    def __init__(self, db_path: str):
        """
        Constructor

        Args:
            db_path (str): database file path to connect
        """
        self.database = self.is_valid_db(db_path)
        self.name = str(uuid.uuid4())
        super().__init__("QSQLITE")
        self.addDatabase("QSQLITE", self.name)
        self.setDatabaseName(str(self.database))

    def __enter__(self) -> QSqlDatabase:
        """
        Returns:
            QSqlDatabase: a connection object used to execute queries
        """
        LOGGER.debug(f"Connected {self.database} <{self.name}>")
        if self.open() and self.isValid() and self.isOpen():
            self.exec("PRAGMA foreign_keys=ON")
            return self
        else:
            raise ConnectionError(self.database)

    def __exit__(self, exc_type: BaseException, value: BaseException, traceback: TracebackType):
        """
        Args:
            exc_type (BaseException): Exception type
            value (BaseException): Exception Value
            traceback (TracebackType): Traceback stack
        """
        if any([exc_type, value, traceback]):
            print(f"Type: {exc_type}\nValue: {value}\nTraceback:\n{traceback}")
        self.commit()
        self.close()
        QSqlDatabase.removeDatabase(self.name)
        LOGGER.debug(f"Disconnected {self.database} <{self.name}>")

    @staticmethod
    def is_valid_db(db_path: Union[str, PurePath]) -> Union[str, PurePath]:
        """
        Connection validator used to connect to a database

        Args:
            db_path (Union[str, PurePath]): database path

        Returns:
            Union[str, PurePath]: if the connection file is valid, otherwise None

        Raises:
              ValueError: when database file is invalid
        """
        if db_path == ":memory:":
            return db_path
        elif os.path.splitext(db_path)[1] == ".db":
            if isinstance(db_path, str):
                db_path = PurePath(db_path)
            return db_path
        else:
            raise ValueError(db_path)


@dataclasses.dataclass
class RecordSet:
    """
    Dataclass for the Record ser return when a query is executed
    """
    fields: list
    records: list[list] = dataclasses.field(default_factory = list)

    @staticmethod
    def from_json(json: dict) -> RecordSet:
        """
        To create a RecordSet object from a json dict

        Args:
            json: dict to use for the record set creation

        Returns:
            RecordSet: populated record set
        """
        records = RecordSet(list(json[list(json.keys())[0]].keys()), [list(row.values()) for row in json.values()])
        return records

    def __bool__(self):
        return not (len(self.fields) == 0 and len(self.records) == 0)

    def __str__(self) -> str:
        if self:
            HEADER = " | ".join(item for item in self.fields)
            SEP = "-" * len(HEADER)
            DATA = "\n".join(" | ".join(sub_item for sub_item in item) for item in self.records)
            return f"{SEP}\n{HEADER}\n{SEP}\n{DATA}\n{SEP}"
        else:
            return f"----\nEMPTY\n----\nEMPTY\n----"


class Database:
    """
    Database class for all database queries and methods
    """

    def __init__(self, path: str = None):
        """
        Constructor

        Args:
            path: path to the db file
        """
        self.db_path = Connection.is_valid_db(path) if path is not None else CONFIG.db_path
        LOGGER.info(f"Database Connected: {self.db_path}")

    @staticmethod
    def batch_insert(records: RecordSet, table: str, conn: Connection):
        """
        Batch executor tha performs an insert transaction

        Args:
            records (RecordSet): Records to insert into
            table (str): table name
            conn (Connection): db connection

        Raises:
            QueryExecutionFailed: when a query fails to execute
        """
        def _dedent_query(query_str: str):
            lines = query_str.splitlines()
            return "\n".join(line.lstrip() for line in lines)

        if records:
            columns = ", ".join(records.fields)
            placeholders = ", ".join(["?" for _ in records.fields])
            query = QSqlQuery(f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})", db = conn)
            for col in range(len(records.fields)):
                query.bindValue(col, [records.records[row][col] for row in range(len(records.records))])

            LOGGER.debug(f"Batch Insert into: {table}")
            conn.transaction()
            if not query.execBatch():
                connection_info = (str(conn))
                msg = f"\nError: {(query.lastError().text())}" \
                      f"\nQuery: {_dedent_query(query.lastQuery())}" \
                      f"\nConnection: {connection_info}"
                conn.rollback()
                raise QueryExecutionFailed(msg)
            conn.commit()

    @staticmethod
    def execute(query: Union[str, QSqlQuery], conn: Connection) -> RecordSet:
        """
        Executes a given query

        Args:
            query (Union[str, QSqlQuery]): query to execute
            conn (Connection): db connection

        Returns:
            RecordSet: result of the executed query

        Raises:
            QueryBuildFailed: when a prepared query fails to build
            QueryExecutionFailed: when a query fails to execute
        """
        def _dedent_query(query_str: str):
            lines = query_str.splitlines()
            return "\n".join(line.lstrip() for line in lines)

        connection_info = (str(conn))
        if isinstance(query, str):
            query_str = query
            query = QSqlQuery(db = conn)
            if not query.prepare(query_str):
                raise QueryBuildFailed(f"{connection_info}\n{query_str}")

        query_executed = query.exec()
        if query_executed:
            LOGGER.debug(f"Executed: {_dedent_query(query.lastQuery())}")
        else:
            msg = f"\nExe: {query_executed}" \
                  f"\nError: {(query.lastError().text())}" \
                  f"\nQuery: {_dedent_query(query.lastQuery())}" \
                  f"\nConnection: {connection_info}"
            raise QueryExecutionFailed(msg)

        record = query.record()
        keys = [record.fieldName(idx) for idx in range(record.count())]
        data = []
        while query.next():
            data.append([query.value(idx) for idx in keys])
        return RecordSet(keys, data)

    def import_data(self, records: dict):
        """
        Import a db that has been exported using Database class export method

        Args:
            records: dict that holds the db structure
        """
        records = copy.deepcopy(records)
        with self.connector as connection:
            for name, sql in records.pop("sql_table_schema").items():
                self.execute(sql, connection)
            for table_name, table_data in records.items():
                table_records = RecordSet.from_json(table_data)
                self.batch_insert(table_records, table_name, connection)

    def export_data(self) -> dict:
        """
        Export th db structure and data into a json representation

        Returns:
            dict:  json representation
        """
        export = {}
        with self.connector as connection:
            result = self.execute("SELECT tbl_name, sql FROM sqlite_schema WHERE sql IS NOT NULL", connection).records
            export['sql_table_schema'] = {item[0]: item[1] for item in result}
            for item in result:
                table_name = item[0]
                table_result = self.execute(f"SELECT * FROM {table_name}", connection)
                table_result = {
                    index: {k: v for k, v in zip(table_result.fields, row)}
                    for index, row in enumerate(table_result.records)
                }
                export[table_name] = table_result
        return export

    # noinspection PyTypeChecker
    @property
    def connector(self) -> Connection:
        """
        DB base cursor used to execute queries

        Returns:
            Connection: DB cursor
        """
        conn = Connection(self.db_path)
        return conn


class LibraryManager(Database):
    library_table_columns = [
        "file_id", "file_path", "file_name", "file_size", "file_ext", "track_title", "artist", "album",
        "album_artist", "composer", "track_number", "total_tracks", "disc_number", "total_discs", "genre",
        "year", "compilation", "lyrics", "isrc", "comment", "artwork", "bitrate", "codec", "play_length",
        "channels", "bits_per_sample", "samplerate", "liked", "play_count", "rating",
    ]
    queue_table_columns = ["file_id", "play_order"]

    def __init__(self, path: str = None):
        super().__init__(path)
        self.init_structure()

    def init_structure(self):
        library_table = """
        CREATE TABLE IF NOT EXISTS library (
            -- Syntehtic tags        
            file_id         STRING  PRIMARY KEY ON CONFLICT IGNORE,
            file_path       STRING  NOT NULL,
            file_name       STRING  NOT NULL,
            file_size       INTEGER NOT NULL,
            file_ext        STRING  NOT NULL,
            
            -- Actual tags
            track_title     STRING,
            artist          STRING,
            album           STRING,
            album_artist    STRING,
            composer        STRING,
            track_number    STRING,
            total_tracks    STRING,
            disc_number     STRING,
            total_discs     STRING,
            genre           STRING,
            year            STRING,
            compilation     STRING,
            lyrics          STRING,
            isrc            STRING,
            comment         STRING,
            
            -- File info
            artwork         BOOLEAN,
            bitrate         STRING,
            codec           STRING,            
            play_length     FLOAT,
            channels        INTEGER,
            bits_per_sample INTEGER,
            samplerate      INTEGER,
            
            -- User generated tags
            liked           BOOLEAN DEFAULT FALSE,
            play_count      INTEGER NOT NULL DEFAULT 0,
            rating          INTEGER NOT NULL DEFAULT 0
        )
        """
        queue_table = """
        CREATE TABLE IF NOT EXISTS queue (
            file_id    STRING  REFERENCES library (file_id) ON DELETE CASCADE ON UPDATE CASCADE,
            play_order INTEGER PRIMARY KEY
        )
        """
        with self.connector as connection:
            self.execute(library_table, connection)
            self.execute(queue_table, connection)

    def scan_directories(self, path: Union[list[PurePath, str], str, PurePath]):

        def scan_directory(dir_path: str, connection: Connection):
            files_scanned = []
            mediafile = None
            for dirct, subdirs, files in os.walk(dir_path):
                for file in files:
                    _path = (os.path.normpath(os.path.join(dirct, file)))
                    if Mediafile.isSupported(_path):
                        mediafile = Mediafile(_path)
                        # TODO:
                        # if mediafile.SynthTags['file_id'] and float(mediafile.Tags['length']) < 3600:
                        #     files_scanned.append(list(mediafile.SynthTags.values()))
                        files_scanned.append(list(mediafile.SynthTags.values()))
            if mediafile is not None and len(files_scanned) > 0:
                records = RecordSet(list(mediafile.SynthTags.keys()), files_scanned)
                self.batch_insert(records, 'library', connection)

        if isinstance(path, str):
            path = PurePath(path)

        if not isinstance(path, list):
            path = [path]

        with self.connector as connection:
            for item in path:
                LOGGER.info(f"Scanning directory: {item}")
                scan_directory(str(item), connection)

    def scan_files(self, path: Union[list[str], str]): ...

# class LibraryManager(Database):
#
#     def __init__(self) -> None:
#         super().__init__()
#
#     def scan_directory(self, directory: str):
#         """
#         Starts a recursive scan of the directory and inserts the metadata into the file
#
#         Args:
#             directory (str): directory to scan files from
#         """
#         if not os.path.isdir(directory):
#             return None
#
#         scanned_files = []
#         for dirct, subdirs, files in os.walk(directory):
#             for file in files:
#                 path = (os.path.normpath(os.path.join(dirct, file)))
#                 if Mediafile.isSupported(path):
#                     mediafile = Mediafile(path)
#                     if mediafile.SynthTags['file_id'] and float(mediafile.Tags['length']) < 3600:
#                         scanned_files.append(mediafile.SynthTags)
#         self.batchinsert_data('library', scanned_files, Mediafile.tags_fields)
#
#     def scan_file(self, path: str):
#         """
#         Starts a scan of the file and inserts the metadata into the library
#
#         Args:
#             path (str): file to scan and insert into library
#         """
#         if not os.path.isfile(path):
#             return None
#
#         if Mediafile.isSupported(path):
#             mediafile = Mediafile(path)
#             if mediafile.SynthTags['file_id'] and float(mediafile.Tags['length']) < 3600:
#                 self.insert_Metadata(mediafile.SynthTags, Mediafile.tags_fields)
#
#     def refresh_library(self):
#         """
#         Starts a scan of all the files loades in the library model and refreshes the metadata
#         """
#         delete_queue = []
#         insert_queue = []
#         with Connection(self.database_file) as connection:
#             files = self.fetch_all(self.exec_query('SELECT library.file_path from library', connection))
#             for file in files:
#                 path = (os.path.normpath(file[0]))
#                 if not os.path.isfile(path):
#                     delete_queue.append(path)
#                 elif Mediafile.isSupported(path):
#                     mediafile = Mediafile(path)
#                     if mediafile.SynthTags['file_id'] and float(mediafile.Tags['length']) < 3600:
#                         insert_queue.append(mediafile.SynthTags)
#                 else:
#                     continue
#             self.delete_items('file_path', delete_queue, connection)
#             if len(insert_queue) > 0:
#                 self.batchinsert_data('library', insert_queue, Mediafile.tags_fields, connection)
#
#     def delete_items(self, field: str, delete_items: list[str], connection: QSqlDatabase = None):
#         if len(delete_items) > 0:
#             if len(delete_items) == 1:
#                 str_delete_queue = f"('{delete_items[0]}')"
#             else:
#                 str_delete_queue = tuple(_id for _id in delete_items)
#         else:
#             return None
#
#         if connection is None:
#             with Connection(self.database_file) as connection:
#                 self.exec_query(f'DELETE FROM library WHERE library.{field} IN {str_delete_queue}', connection)
#         else:
#             self.exec_query(f'DELETE FROM library WHERE library.{field} IN {str_delete_queue}', connection)
#         self.DATABASE_MODIFIED.emit()
