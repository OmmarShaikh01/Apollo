"""
DEV NOTES
"""
from __future__ import annotations

import copy
import dataclasses
import os
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import PurePath
from types import TracebackType
from typing import Any, Union

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from apollo.media import Mediafile
from apollo.utils import ApolloWarning, get_logger
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
    """Connector used execute queries"""

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
        if any([exc_type, value, traceback]):  # pragma: no cover
            LOGGER.error(f"Type: {exc_type}\nValue: {value}\nTraceback:\n{traceback}")
        self.commit()
        self.close()
        QSqlDatabase.removeDatabase(self.name)

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
    records: list[list] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_json(json: dict) -> RecordSet:
        """
        To create a RecordSet object from a json dict

        Args:
            json: dict to use for the record set creation

        Returns:
            RecordSet: populated record set
        """
        records = RecordSet(
            list(json[list(json.keys())[0]].keys()), [list(row.values()) for row in json.values()]
        )
        return records

    def __bool__(self):
        return len(self.records) != 0

    def __str__(self) -> str:  # pragma: no cover
        def str_converter(item: Any):
            if item:
                return str(item)
            else:
                return str(None)

        if self:
            HEADER = " | ".join(str(item) for item in self.fields)
            SEP = "-" * len(HEADER)
            DATA = "\n".join(" | ".join(map(str_converter, row)) for row in self.records)
            return f"\n{SEP}\n{HEADER}\n{SEP}\n{DATA}\n{SEP}\n"
        else:
            return f"\n----\nEMPTY\n----\nEMPTY\n----\n"


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
        self.init_structure()

    def init_structure(self):
        """
        Creates the Tables For Apollo
        """
        cols = []
        for K, V in Mediafile.TAG_FRAMES_FIELDS:
            if K == "FILEID":
                cols.append(f"{K} {V} PRIMARY KEY ON CONFLICT IGNORE")
            elif K in ["FILEPATH", "FILENAME", "FILESIZE", "FILEEXT"]:
                cols.append(f"{K} {V} NOT NULL")
            else:
                cols.append(f"{K} {V}")

        library_table = f"""
        CREATE TABLE IF NOT EXISTS library (
            {str(", ").join(cols)}
        )
        """

        queue_table = """
        CREATE TABLE IF NOT EXISTS queue (
            FILEID    STRING  REFERENCES library (FILEID) ON DELETE CASCADE ON UPDATE CASCADE,
            PLAYORDER INTEGER PRIMARY KEY
        )
        """
        with self.connector as connection:
            self.execute(library_table, connection)
            self.execute(queue_table, connection)

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

        def _dedent_query(query_str: str):  # pragma: no cover
            lines = query_str.splitlines()
            return "\n".join(line.lstrip() for line in lines)

        if records:
            columns = ", ".join(records.fields)
            placeholders = ", ".join(["?" for _ in records.fields])
            query = QSqlQuery(
                f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})", db=conn
            )
            for col in range(len(records.fields)):
                query.bindValue(
                    col, [records.records[row][col] for row in range(len(records.records))]
                )

            LOGGER.debug(f"Batch Insert into: {table}")
            LOGGER.critical(records)
            conn.transaction()
            if not query.execBatch():  # pragma: no cover
                connection_info = str(conn)
                msg = (
                    f"\nError: {(query.lastError().text())}"
                    f"\nQuery: {_dedent_query(query.lastQuery())}"
                    f"\nConnection: {connection_info}"
                )
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

        connection_info = str(conn)
        if isinstance(query, str):
            query_str = query
            query = QSqlQuery(db=conn)
            if not query.prepare(query_str):
                raise QueryBuildFailed(f"{connection_info}\n{query_str}")

        query_executed = query.exec()
        if query_executed:
            LOGGER.debug(f"Executed: {_dedent_query(query.executedQuery())}")
        else:
            msg = (
                f"\nExe: {query_executed}"
                f"\nError: {(query.lastError().text())}"
                f"\nQuery: {_dedent_query(query.lastQuery())}"
                f"\nQueryValues: {_dedent_query(str(query.boundValues()))}"
                f"\nConnection: {connection_info}"
            )
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
            result = self.execute(
                "SELECT tbl_name, sql FROM sqlite_schema WHERE sql IS NOT NULL", connection
            ).records
            export["sql_table_schema"] = {item[0]: item[1] for item in result}
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
    """
    Library Manager, Manages all media files indexed by Apollo
    """

    library_table_columns = Mediafile.TAG_FRAMES
    queue_table_columns = ["FILEID", "PLAYORDER"]

    def __init__(self, path: str = None):
        """
        Constructor

        Args:
            path (str): Database Path
        """
        super().__init__(path)
        self._dirs_watched = []  # TODO: Save To config

    def add_dir_to_watcher(self, path: PurePath):
        """
        Adds Directories to files monitor

        Args:
            path (PurePath): Directory Path
        """
        if len(self._dirs_watched) == 0:
            self._dirs_watched.append(path)
        else:
            if path.parent in self._dirs_watched:

                ApolloWarning(f"Skipped {path} parent directory exists")
            elif path in [_path.parent for _path in self._dirs_watched]:
                if all([(path / str(item)) in self._dirs_watched for item in os.listdir(path)]):
                    self._dirs_watched.append(path)
                    for file in os.listdir(path):
                        self._dirs_watched.pop(self._dirs_watched.index(path / str(file)))
            elif path not in self._dirs_watched:
                self._dirs_watched.append(path)
            else:

                ApolloWarning(f"Skipped {path}, is not monitored")

    def scan_directories(self, path: Union[list[PurePath, str], str, PurePath]):
        """
        Scans a directory Recursively

        Args:
            path Union[list[PurePath, str], str, PurePath]: Paths to the directory
        """
        if isinstance(path, str):
            path = [PurePath(path)]

        if not isinstance(path, list):
            path = [path]

        if isinstance(path, list):
            path = [item if not isinstance(item, str) else PurePath(item) for item in path]

        paths = []
        for item in path:
            LOGGER.info(f"Scanning directory: {item}")
            self.add_dir_to_watcher(item)
            for dirct, subdirs, files in os.walk(item):
                paths.extend([PurePath(dirct, file) for file in files])
        self.scan_files(paths)

    def scan_files(self, path: Union[list[PurePath, str], str, PurePath]):
        """
        Scans files

        Args:
            path Union[list[PurePath, str], str, PurePath]: Paths to the files
        """

        def exe(_path: list):
            try:
                files_scanned = []
                for file_path in _path:
                    if Mediafile.isSupported(file_path):
                        mediafile = Mediafile(file_path)
                        if mediafile:
                            files_scanned.append(list(mediafile.Records.values()))
                        else:
                            ApolloWarning(f"Skipped {file_path}")
                    else:
                        ApolloWarning(f"Skipped {file_path}")
                if len(files_scanned) > 0:  # pragma: no cover
                    records = RecordSet(Mediafile.TAG_FRAMES, files_scanned)
                    with self.connector as connection:
                        self.batch_insert(records, "library", connection)
                else:
                    ApolloWarning(f"Skipped {len(_path)} Files")
            except Exception as e:
                LOGGER.error(f"Type: {e}\nValue: {e.__cause__}\nTraceback:\n{traceback.print_tb()}")

        if isinstance(path, str):
            path = [PurePath(path)]

        if not isinstance(path, list):
            path = [path]

        if isinstance(path, list):
            path = [item if not isinstance(item, str) else PurePath(item) for item in path]

        part = 250
        if len(path) <= part:
            exe(path)
        else:
            cuts = int(round(len(path) / part, 0))
            with ThreadPoolExecutor(max_workers=8) as executor:
                thread = 0
                start, end = 0, part
                for cut in range(cuts):
                    executor.submit(exe, (path[start:end]))
                    if (cut + 1) > cuts:
                        start, end = start + part, end + part
                        thread += 1
                    else:
                        executor.submit(exe, (path[end:]))
                        thread += 1
                        break
                LOGGER.debug(thread)

    def get_library_stats(self) -> RecordSet:
        """
        Get Vital Stats of the library Table

        Returns:
            RecordSet: Library Table Stats
        """
        with self.connector as connection:
            records = self.execute(
                """
            SELECT 
                count(FILEID) as TRACKS,
                SUM(FILESIZE) as BYTESIZE,
                round(SUM(SONGLEN), 4) as PLAYLEN,
                (SELECT count(ARTIST) FROM library GROUP BY ARTIST) as ARTIST,
                (SELECT count(ALBUM) FROM library GROUP BY ALBUM) as ALBUM
            FROM library 
            """,
                connection,
            )
        return records

    def rescan_files(self):
        """
        Rescans Files present in the library Table
        """
        with self.connector as connection:
            recordset = self.execute("SELECT FILEPATH FROM library", connection)
        self.scan_files([item[0] for item in recordset.records])

    def rescan_folders(self):
        """
        Rescans Directories that are monitored
        """
        self.scan_directories(self._dirs_watched)
