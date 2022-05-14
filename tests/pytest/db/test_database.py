import os
import timeit
import tempfile
from pathlib import PurePath

import pytest
import pytest_cases
from PySide6.QtSql import QSqlQuery

from apollo.db.database import Connection, Database, LibraryManager, QueryBuildFailed, QueryExecutionFailed, RecordSet
from apollo.utils import get_logger
from configs import settings
from tests.pytest.utils_for_tests import IDGen

cases = "tests.pytest.db.case_db"
LOGGER = get_logger(__name__)
CONFIG = settings
MEDIA_FOLDER = PurePath(CONFIG.assets_dir, "music_samples")
BENCHMARK = CONFIG.benchmark_formats  # TODO: remove not


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
        with Connection(CONFIG.db_path) as connection:
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

    @pytest_cases.parametrize_with_cases('data', cases = cases, prefix = 'import_json_data', ids = IDGen)
    def test_import_export_data(self, get_database: Database, data: dict):
        db = get_database
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
            assert all([a == b for a, b in
                        zip(db.execute("SELECT * FROM library", connection).fields, db.library_table_columns)])
            assert all([a == b for a, b in
                        zip(db.execute("SELECT * FROM queue", connection).fields, db.queue_table_columns)])

    @pytest_cases.parametrize('path', [MEDIA_FOLDER, MEDIA_FOLDER.as_posix(), [MEDIA_FOLDER, MEDIA_FOLDER]])
    def test_scan_directories(self, get_library_manager: LibraryManager, path):
        db = get_library_manager
        db.scan_directories(path)
        with db.connector as connection:
            records = db.execute("SELECT * FROM library", connection)
            LOGGER.debug(records)
            assert records.fields
            db.execute("DELETE FROM library", connection)

    @pytest_cases.parametrize_with_cases('file_path', cases = cases, prefix = 'file_tagged_mp3', ids = IDGen)
    def test_scan_files(self, get_library_manager: LibraryManager, file_path):
        db = get_library_manager
        db.scan_files(file_path)
        with db.connector as connection:
            records = db.execute("SELECT * FROM library", connection)
            LOGGER.debug(records)
            assert records.fields
            db.execute("DELETE FROM library", connection)

    @pytest.mark.skipif(not BENCHMARK, reason = f"Benchmarking: {BENCHMARK}")
    def test_benchmark_scanning(self, get_library_manager: LibraryManager):
        db = get_library_manager
        file_path = [MEDIA_FOLDER / 'mp3' / "example_48000H_2C_TAGGED.mp3" for _ in range(1000)]
        LOGGER.info("RUNTIME: {run}".format(run = timeit.timeit(lambda: db.scan_files(file_path), number = 5)))
        with db.connector as connection:
            records = db.execute("SELECT * FROM library", connection)
            LOGGER.debug(records)
            assert records.fields
            db.execute("DELETE FROM library", connection)

    def test_add_dir_to_watcher(self, get_library_manager: LibraryManager):
        db = get_library_manager
        with tempfile.TemporaryDirectory() as directory:
            ROOT = PurePath(directory, "ROOT")
            os.mkdir(ROOT)
            ROOT_1 = PurePath(directory, "ROOT", "ROOT_1")
            os.mkdir(ROOT_1)
            ROOT_2 = PurePath(directory, "ROOT", "ROOT_2")
            os.mkdir(ROOT_2)
            ROOT_3 = PurePath(directory, "ROOT", "ROOT_3")
            os.mkdir(ROOT_3)
            ROOT_1_1 = PurePath(directory, "ROOT", "ROOT_1", "ROOT_1_1")
            os.mkdir(ROOT_1_1)
            ROOT_1_2 = PurePath(directory, "ROOT", "ROOT_1", "ROOT_1_2")
            os.mkdir(ROOT_1_2)
            ROOT_1_3 = PurePath(directory, "ROOT", "ROOT_1", "ROOT_1_3")
            os.mkdir(ROOT_1_3)
            ROOT_1_4 = PurePath(directory, "ROOT", "ROOT_1", "ROOT_1_4")
            os.mkdir(ROOT_1_4)
            ROOT_2_1 = PurePath(directory, "ROOT", "ROOT_2", "ROOT_2_1")
            os.mkdir(ROOT_2_1)
            ROOT_2_2 = PurePath(directory, "ROOT", "ROOT_2", "ROOT_2_2")
            os.mkdir(ROOT_2_2)
            ROOT_2_3 = PurePath(directory, "ROOT", "ROOT_2", "ROOT_2_3")
            os.mkdir(ROOT_2_3)
            ROOT_2_4 = PurePath(directory, "ROOT", "ROOT_2", "ROOT_2_4")
            os.mkdir(ROOT_2_4)
            ROOT_3_1 = PurePath(directory, "ROOT", "ROOT_3", "ROOT_3_1")
            os.mkdir(ROOT_3_1)
            ROOT_3_2 = PurePath(directory, "ROOT", "ROOT_3", "ROOT_3_2")
            os.mkdir(ROOT_3_2)
            ROOT_3_2_1 = PurePath(directory, "ROOT", "ROOT_3", "ROOT_3_2", "ROOT_3_2_1")
            os.mkdir(ROOT_3_2)
            ROOT_3_2_2 = PurePath(directory, "ROOT", "ROOT_3", "ROOT_3_2", "ROOT_3_2_2")
            os.mkdir(ROOT_3_2)
            ROOT_3_3 = PurePath(directory, "ROOT", "ROOT_3", "ROOT_3_3")
            os.mkdir(ROOT_3_3)
            ROOT_3_4 = PurePath(directory, "ROOT", "ROOT_3", "ROOT_3_4")
            os.mkdir(ROOT_3_4)

            db.add_dir_to_watcher(ROOT_1)
            db.add_dir_to_watcher(ROOT_1_1)
            db.add_dir_to_watcher(ROOT_1_2)
            assert all([True if (a in [ROOT_1, ROOT_1_1, ROOT_1_2]) else False for a in db._dirs_watched])
            db.add_dir_to_watcher(ROOT_1_3)
            db.add_dir_to_watcher(ROOT_1_4)
            assert db._dirs_watched == [ROOT_1]

            db.add_dir_to_watcher(ROOT_2_1)
            db.add_dir_to_watcher(ROOT_2_2)
            exp = [ROOT_1, ROOT_2_1, ROOT_2_2, ROOT_2_3, ROOT_2_4]
            assert all([True if (a in exp) else False for a in db._dirs_watched])
            db.add_dir_to_watcher(ROOT_2_3)
            db.add_dir_to_watcher(ROOT_2_4)
            db.add_dir_to_watcher(ROOT_2)
            exp = [ROOT_1, ROOT_2]
            assert all([True if (a in exp) else False for a in db._dirs_watched])

            db.add_dir_to_watcher(ROOT_3_1)
            db.add_dir_to_watcher(ROOT_3_2)
            db.add_dir_to_watcher(ROOT_3_2_1)
            db.add_dir_to_watcher(ROOT_3_3)
            db.add_dir_to_watcher(ROOT_3_4)
            exp = [ROOT_1, ROOT_2, ROOT_3_1, ROOT_3_2, ROOT_3_3, ROOT_3_4, ROOT_3_2_1]
            assert all([True if (a in exp) else False for a in db._dirs_watched])
            db.add_dir_to_watcher(ROOT_3_2_2)
            exp = [ROOT_1, ROOT_2, ROOT_3]
            assert all([True if (a in exp) else False for a in db._dirs_watched])
            db.add_dir_to_watcher(ROOT_3)
            assert db._dirs_watched == [ROOT_1, ROOT_2, ROOT_3]

            db.add_dir_to_watcher(ROOT)
            assert db._dirs_watched == [ROOT]
