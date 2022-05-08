import json
import os
import tempfile

import pytest
from PySide6.QtSql import QSqlQuery

from apollo.db.database import Connection, Database, LibraryManager, QueryBuildFailed, QueryExecutionFailed, RecordSet
from apollo.utils import get_logger
from configs import settings

LOGGER = get_logger(__name__)
CONFIG = settings


# FIXTURES -------------------------------------------------------------------------------------------------------------
@pytest.fixture
def records() -> RecordSet:
    recordset = RecordSet(['col_1', 'col_2', 'col_3'],
                          [['test_1_0', 'test_2_0', 'test_3_0'], ['test_1_1', 'test_2_1', 'test_3_1'],
                           ['test_1_2', 'test_2_2', 'test_3_2'], ['test_1_3', 'test_2_3', 'test_3_3'],
                           ['test_1_4', 'test_2_4', 'test_3_4'], ['test_1_5', 'test_2_5', 'test_3_5'],
                           ['test_1_6', 'test_2_6', 'test_3_6'], ['test_1_7', 'test_2_7', 'test_3_7'],
                           ['test_1_8', 'test_2_8', 'test_3_8'], ['test_1_9', 'test_2_9', 'test_3_9']])
    return recordset


@pytest.fixture
def get_database():
    db = Database()
    return db


@pytest.fixture
def get_filled_database(get_database: Database, records: RecordSet):
    db = get_database
    with db.connector as connection:
        col = records.fields
        db.execute(f'CREATE TABLE IF NOT EXISTS test_table ("{col[0]}" TEXT, "{col[1]}" TEXT, "{col[2]}" TEXT)',
                   connection)
        connection.transaction()
        for row in records.records:
            db.execute(f'INSERT INTO test_table VALUES ("{row[0]}", "{row[1]}", "{row[2]}") ', connection)
        connection.commit()
    return db


@pytest.fixture
def get_library_manager():
    db = LibraryManager()
    return db


@pytest.fixture
def get_filled_library_manager(get_library_manager: Database, records_library_manager: RecordSet):
    db = get_library_manager
    lib, queue = records_library_manager
    with db.connector as connection:
        db.batch_insert(lib, 'library', connection)
        db.batch_insert(queue, 'queue', connection)
    return db


# TESTS ----------------------------------------------------------------------------------------------------------------

class Test_Connection:

    def test_connection_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            with Connection(os.path.join(directory, 'temp.db')) as connection:
                assert connection.isValid()

    def test_connection_is_invalid(self):
        with tempfile.TemporaryDirectory() as directory:
            with pytest.raises(ValueError):
                with Connection(os.path.join(directory, 'temp.txt')) as connection:
                    assert not connection.isValid()

    def test_connection_is_memory(self):
        with Connection(':memory:') as connection:
            assert connection.isValid()


class Test_Database:

    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """

    @classmethod
    def teardown_class(cls):
        """teardown any state that was previously setup with a call to
        setup_class.
        """
        if os.path.isfile(CONFIG.db_path):
            os.remove(CONFIG.db_path)

    def test_database_init(self):
        db = Database()
        assert CONFIG.db_path == db.db_path

    def test_database_connection(self, get_database: Database):
        db = get_database
        with db.connector as connection:
            if connection.isValid() and connection.isOpen():
                assert True
        if connection.isValid() and connection.isOpen():
            assert False

    def test_query_exe_valid(self, get_filled_database: Database, records: RecordSet):
        db = get_filled_database
        with db.connector as connection:
            query = QSqlQuery("SELECT * FROM test_table", connection)
            assert db.execute(query, connection) == records
            assert db.execute("SELECT * FROM test_table", connection) == records

    def test_query_exe_invalid(self, get_database: Database):
        db = get_database
        with db.connector as connection:
            with pytest.raises(QueryBuildFailed):
                query = "SELECT 'SUCCESS'; SELECT 'SUCCESS'"
                db.execute(query, connection)

        with db.connector as connection:
            with pytest.raises(QueryExecutionFailed):
                query = QSqlQuery("SELECT 'SUCCESS'", connection)
                connection.close()
                db.execute(query, connection)

    def test_batch_insert_valid(self, get_database: Database, records: RecordSet):
        db = get_database
        with db.connector as connection:
            col = records.fields
            db.execute(f"DROP TABLE IF EXISTS test_table", connection)
            db.execute(f'CREATE TABLE IF NOT EXISTS test_table ("{col[0]}" TEXT, "{col[1]}" TEXT, "{col[2]}" TEXT)',
                       connection)
            db.batch_insert(records, 'test_table', connection)
            db.batch_insert(records, 'test_table', connection)
            records.records.extend(records.records)
            assert db.execute("SELECT * FROM test_table", connection) == records
            db.execute(f"DROP TABLE IF EXISTS test_table", connection)

    def test_import_export_data(self, get_database):
        db = get_database
        data = dict(
                sql_table_schema = dict(
                        test_table_0 = 'CREATE TABLE test_table_0 ("col_0" TEXT, "col_1" TEXT, "col_2" TEXT)',
                        test_table_1 = 'CREATE TABLE test_table_1 ("col_0" TEXT, "col_1" TEXT, "col_2" TEXT)',
                ),
                test_table_0 = {
                    0: dict(col_0 = 'test_1_0', col_1 = 'test_2_0', col_2 = 'test_3_0'),
                    1: dict(col_0 = 'test_1_1', col_1 = 'test_2_1', col_2 = 'test_3_1'),
                    2: dict(col_0 = 'test_1_2', col_1 = 'test_2_2', col_2 = 'test_3_2'),
                    3: dict(col_0 = 'test_1_3', col_1 = 'test_2_3', col_2 = 'test_3_3'),
                    4: dict(col_0 = 'test_1_4', col_1 = 'test_2_4', col_2 = 'test_3_4'),
                },
                test_table_1 = {
                    0: dict(col_0 = 'test_1_0', col_1 = 'test_2_0', col_2 = 'test_3_0'),
                    1: dict(col_0 = 'test_1_1', col_1 = 'test_2_1', col_2 = 'test_3_1'),
                    2: dict(col_0 = 'test_1_2', col_1 = 'test_2_2', col_2 = 'test_3_2'),
                    3: dict(col_0 = 'test_1_3', col_1 = 'test_2_3', col_2 = 'test_3_3'),
                    4: dict(col_0 = 'test_1_4', col_1 = 'test_2_4', col_2 = 'test_3_4'),
                }
        )
        db.import_data(data)
        assert data == db.export_data()
        with db.connector as connection:
            db.execute(f"DROP TABLE IF EXISTS test_table_0", connection)
            db.execute(f"DROP TABLE IF EXISTS test_table_1", connection)


class Test_LibraryManager:

    @classmethod
    def setup_class(cls): ...

    @classmethod
    def teardown_class(cls):
        if os.path.isfile(CONFIG.db_path):
            os.remove(CONFIG.db_path)

    def test_library_manager(self, get_library_manager: LibraryManager):
        db = get_library_manager
        with db.connector as connection:
            assert db.execute("SELECT * FROM library", connection).fields == db.library_table_columns
            assert db.execute("SELECT * FROM queue", connection).fields == db.queue_table_columns

    def test_scan_directories(self, get_library_manager: LibraryManager):
        db = get_library_manager
        db.scan_directories(os.path.join(CONFIG.assets_dir, 'music_samples'))
