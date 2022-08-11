import os
from pathlib import PurePath
from typing import Any

import pytest
from PySide6 import QtCore
from pytest_mock import MockerFixture

from apollo.db.models.queue import QueueModel
from apollo.media import Stream
from apollo.utils import get_logger
from configs import settings
from tests.pytest_apollo.conftest import clean_temp_dir, copy_mock_data
from tests.testing_utils import LIBRARY_TABLE, get_qt_application


cases = "tests.pytest_apollo.models.case_models"
LOGGER = get_logger(__name__)
CONFIG = settings
MEDIA_FOLDER = PurePath(CONFIG.assets_dir, "music_samples")
BENCHMARK = CONFIG.benchmark_formats  # TODO: remove not
MODEL_ROWS, MODEL_COLUMNS = len(LIBRARY_TABLE), len(["PLAYORDER", *Stream.TAG_FRAMES])


# noinspection PyProtectedMember
@pytest.fixture
def model_provider() -> QueueModel:
    copy_mock_data()
    model = QueueModel()
    yield model
    clean_temp_dir()


# noinspection PyProtectedMember
def check_for_model_start_end(col_index: int, model: QueueModel, start: Any, end: Any) -> bool:
    for _ in range(int(model._window.global_count / model._window.fetch_limit) + 3):
        model.fetch_data(model.FETCH_DATA_DOWN)
    assert str(model.index(model.rowCount() - 1, col_index).data()) == str(end)

    for _ in range(int(model._window.global_count / model._window.fetch_limit) + 3):
        model.fetch_data(model.FETCH_DATA_UP)
    assert str(model.index(0, col_index).data()) == str(start)

    return bool(model)


class Test_QueueModel:
    SELECT_QUERY = "SELECT library.FILEID FROM library ORDER BY library.FILEPATH"

    _qt_application = get_qt_application()

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        if os.path.isfile(CONFIG.db_path):
            os.remove(CONFIG.db_path)
            return None

    def test_provider(self, model_provider: QueueModel):
        from apollo.db.models import ModelProvider

        assert isinstance(ModelProvider.get_model(QueueModel), QueueModel)

    def test_init_model_with_data(self, model_provider: QueueModel):
        model = model_provider
        LOGGER.info(model._window)
        col_index = len(model.Columns) - 1
        model.sort(col_index)
        assert check_for_model_start_end(col_index, model, 0, 1110)

        model.clear()
        assert not model

    def test_play_now(self, model_provider: QueueModel, mocker: MockerFixture):
        def get_model_index(_id: str):
            index = mocker.MagicMock(spec=["data"])
            index.data.return_value = _id
            return index

        model = model_provider
        with model._db.connector as conn:
            model._db.execute("DELETE FROM queue", conn)
            model.play_now(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 1",
                            conn,
                        ).records,
                    )
                )
            )
            EXPECTED = [
                "TESTING_FILEPATH_0",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

            model.play_now(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10",
                            conn,
                        ).records,
                    )
                )
            )
            EXPECTED = [
                "TESTING_FILEPATH_0",
                "TESTING_FILEPATH_1",
                "TESTING_FILEPATH_10",
                "TESTING_FILEPATH_100",
                "TESTING_FILEPATH_1000",
                "TESTING_FILEPATH_1001",
                "TESTING_FILEPATH_1002",
                "TESTING_FILEPATH_1003",
                "TESTING_FILEPATH_1004",
                "TESTING_FILEPATH_1005",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

            model.play_now(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10",
                            conn,
                        ).records,
                    )
                )
            )
            EXPECTED = [
                "TESTING_FILEPATH_0",
                "TESTING_FILEPATH_1",
                "TESTING_FILEPATH_10",
                "TESTING_FILEPATH_100",
                "TESTING_FILEPATH_1000",
                "TESTING_FILEPATH_1001",
                "TESTING_FILEPATH_1002",
                "TESTING_FILEPATH_1003",
                "TESTING_FILEPATH_1004",
                "TESTING_FILEPATH_1005",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

            model.play_now(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10, 10",
                            conn,
                        ).records,
                    )
                )
            )
            EXPECTED = [
                "TESTING_FILEPATH_1006",
                "TESTING_FILEPATH_1007",
                "TESTING_FILEPATH_1008",
                "TESTING_FILEPATH_1009",
                "TESTING_FILEPATH_101",
                "TESTING_FILEPATH_1010",
                "TESTING_FILEPATH_1011",
                "TESTING_FILEPATH_1012",
                "TESTING_FILEPATH_1013",
                "TESTING_FILEPATH_1014",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

    def test_queue_next(self, model_provider: QueueModel, mocker: MockerFixture):
        def get_model_index(_id: str):
            index = mocker.MagicMock(spec=["data"])
            index.data.return_value = _id
            return index

        model = model_provider
        with model._db.connector as conn:
            model._db.execute("DELETE FROM queue", conn)
            model.play_now(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10",
                            conn,
                        ).records,
                    )
                )
            )
            model.queue_next(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10, 10",
                            conn,
                        ).records,
                    )
                ),
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 5, 1",
                            conn,
                        ).records,
                    )
                )[0],
            )
            EXPECTED = [
                "TESTING_FILEPATH_0",
                "TESTING_FILEPATH_1",
                "TESTING_FILEPATH_10",
                "TESTING_FILEPATH_100",
                "TESTING_FILEPATH_1000",
                "TESTING_FILEPATH_1006",
                "TESTING_FILEPATH_1007",
                "TESTING_FILEPATH_1008",
                "TESTING_FILEPATH_1009",
                "TESTING_FILEPATH_101",
                "TESTING_FILEPATH_1010",
                "TESTING_FILEPATH_1011",
                "TESTING_FILEPATH_1012",
                "TESTING_FILEPATH_1013",
                "TESTING_FILEPATH_1014",
                "TESTING_FILEPATH_1001",
                "TESTING_FILEPATH_1002",
                "TESTING_FILEPATH_1003",
                "TESTING_FILEPATH_1004",
                "TESTING_FILEPATH_1005",
            ]

            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

        with model._db.connector as conn:
            model._db.execute("DELETE FROM queue", conn)
            model.play_now(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10",
                            conn,
                        ).records,
                    )
                )
            )
            model.queue_next(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10, 10",
                            conn,
                        ).records,
                    )
                ),
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 1",
                            conn,
                        ).records,
                    )
                )[0],
            )
            EXPECTED = [
                "TESTING_FILEPATH_0",
                "TESTING_FILEPATH_1006",
                "TESTING_FILEPATH_1007",
                "TESTING_FILEPATH_1008",
                "TESTING_FILEPATH_1009",
                "TESTING_FILEPATH_101",
                "TESTING_FILEPATH_1010",
                "TESTING_FILEPATH_1011",
                "TESTING_FILEPATH_1012",
                "TESTING_FILEPATH_1013",
                "TESTING_FILEPATH_1014",
                "TESTING_FILEPATH_1",
                "TESTING_FILEPATH_10",
                "TESTING_FILEPATH_100",
                "TESTING_FILEPATH_1000",
                "TESTING_FILEPATH_1001",
                "TESTING_FILEPATH_1002",
                "TESTING_FILEPATH_1003",
                "TESTING_FILEPATH_1004",
                "TESTING_FILEPATH_1005",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

        with model._db.connector as conn:
            model._db.execute("DELETE FROM queue", conn)
            model.play_now(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10",
                            conn,
                        ).records,
                    )
                )
            )
            model.queue_next(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10, 10",
                            conn,
                        ).records,
                    )
                ),
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 9, 1",
                            conn,
                        ).records,
                    )
                )[0],
            )

            EXPECTED = [
                "TESTING_FILEPATH_0",
                "TESTING_FILEPATH_1",
                "TESTING_FILEPATH_10",
                "TESTING_FILEPATH_100",
                "TESTING_FILEPATH_1000",
                "TESTING_FILEPATH_1001",
                "TESTING_FILEPATH_1002",
                "TESTING_FILEPATH_1003",
                "TESTING_FILEPATH_1004",
                "TESTING_FILEPATH_1005",
                "TESTING_FILEPATH_1006",
                "TESTING_FILEPATH_1007",
                "TESTING_FILEPATH_1008",
                "TESTING_FILEPATH_1009",
                "TESTING_FILEPATH_101",
                "TESTING_FILEPATH_1010",
                "TESTING_FILEPATH_1011",
                "TESTING_FILEPATH_1012",
                "TESTING_FILEPATH_1013",
                "TESTING_FILEPATH_1014",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

        with model._db.connector as conn:
            model._db.execute("DELETE FROM queue", conn)
            model.queue_next(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10",
                            conn,
                        ).records,
                    )
                ),
            )

            EXPECTED = [
                "TESTING_FILEPATH_0",
                "TESTING_FILEPATH_1",
                "TESTING_FILEPATH_10",
                "TESTING_FILEPATH_100",
                "TESTING_FILEPATH_1000",
                "TESTING_FILEPATH_1001",
                "TESTING_FILEPATH_1002",
                "TESTING_FILEPATH_1003",
                "TESTING_FILEPATH_1004",
                "TESTING_FILEPATH_1005",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )
            model.queue_next(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10, 10",
                            conn,
                        ).records,
                    )
                )
            )

            EXPECTED = [
                "TESTING_FILEPATH_0",
                "TESTING_FILEPATH_1",
                "TESTING_FILEPATH_10",
                "TESTING_FILEPATH_100",
                "TESTING_FILEPATH_1000",
                "TESTING_FILEPATH_1001",
                "TESTING_FILEPATH_1002",
                "TESTING_FILEPATH_1003",
                "TESTING_FILEPATH_1004",
                "TESTING_FILEPATH_1005",
                "TESTING_FILEPATH_1006",
                "TESTING_FILEPATH_1007",
                "TESTING_FILEPATH_1008",
                "TESTING_FILEPATH_1009",
                "TESTING_FILEPATH_101",
                "TESTING_FILEPATH_1010",
                "TESTING_FILEPATH_1011",
                "TESTING_FILEPATH_1012",
                "TESTING_FILEPATH_1013",
                "TESTING_FILEPATH_1014",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

        with model._db.connector as conn:
            model._db.execute("DELETE FROM queue", conn)
            model.queue_last(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10",
                            conn,
                        ).records,
                    )
                ),
            )

            EXPECTED = [
                "TESTING_FILEPATH_0",
                "TESTING_FILEPATH_1",
                "TESTING_FILEPATH_10",
                "TESTING_FILEPATH_100",
                "TESTING_FILEPATH_1000",
                "TESTING_FILEPATH_1001",
                "TESTING_FILEPATH_1002",
                "TESTING_FILEPATH_1003",
                "TESTING_FILEPATH_1004",
                "TESTING_FILEPATH_1005",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

            model.queue_last(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10, 10",
                            conn,
                        ).records,
                    )
                )
            )

            EXPECTED = [
                "TESTING_FILEPATH_0",
                "TESTING_FILEPATH_1",
                "TESTING_FILEPATH_10",
                "TESTING_FILEPATH_100",
                "TESTING_FILEPATH_1000",
                "TESTING_FILEPATH_1001",
                "TESTING_FILEPATH_1002",
                "TESTING_FILEPATH_1003",
                "TESTING_FILEPATH_1004",
                "TESTING_FILEPATH_1005",
                "TESTING_FILEPATH_1006",
                "TESTING_FILEPATH_1007",
                "TESTING_FILEPATH_1008",
                "TESTING_FILEPATH_1009",
                "TESTING_FILEPATH_101",
                "TESTING_FILEPATH_1010",
                "TESTING_FILEPATH_1011",
                "TESTING_FILEPATH_1012",
                "TESTING_FILEPATH_1013",
                "TESTING_FILEPATH_1014",
            ]
            assert all(
                (
                    model.index(r, 2).data() == exp
                    for r, exp in zip(range(model.rowCount()), EXPECTED)
                )
            )

    def test_play_artist(self, model_provider: QueueModel, mocker: MockerFixture):
        def get_model_index(_id: str):
            index = mocker.MagicMock(spec=["data"])
            index.data.return_value = _id
            return index

        model = model_provider
        with model._db.connector as conn:
            model.play_artist(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 1",
                            conn,
                        ).records,
                    )
                )[0]
            )
        EXPECTED = ["TESTING_FILEPATH_0"]
        assert all(
            (model.index(r, 2).data() == exp for r, exp in zip(range(model.rowCount()), EXPECTED))
        )

    def test_play_album(self, model_provider: QueueModel, mocker: MockerFixture):
        def get_model_index(_id: str):
            index = mocker.MagicMock(spec=["data"])
            index.data.return_value = _id
            return index

        model = model_provider
        with model._db.connector as conn:
            model.play_album(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 1",
                            conn,
                        ).records,
                    )
                )[0]
            )
        EXPECTED = ["TESTING_FILEPATH_0"]
        assert all(
            (model.index(r, 2).data() == exp for r, exp in zip(range(model.rowCount()), EXPECTED))
        )

    def test_play_genre(self, model_provider: QueueModel, mocker: MockerFixture):
        def get_model_index(_id: str):
            index = mocker.MagicMock(spec=["data"])
            index.data.return_value = _id
            return index

        model = model_provider
        with model._db.connector as conn:
            model.play_genre(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 1",
                            conn,
                        ).records,
                    )
                )[0]
            )
        EXPECTED = ["TESTING_FILEPATH_0"]
        assert all(
            (model.index(r, 2).data() == exp for r, exp in zip(range(model.rowCount()), EXPECTED))
        )

    def test_play_shuffled(self, model_provider: QueueModel, mocker: MockerFixture):
        def get_model_index(_id: str):
            index = mocker.MagicMock(spec=["data"])
            index.data.return_value = _id
            return index

        model = model_provider
        with model._db.connector as conn:
            model.play_shuffled(
                list(
                    map(
                        lambda x: get_model_index(x[0]),
                        model._db.execute(
                            f"{self.SELECT_QUERY} LIMIT 10",
                            conn,
                        ).records,
                    )
                )
            )
        EXPECTED = [
            "TESTING_FILEPATH_0",
            "TESTING_FILEPATH_1",
            "TESTING_FILEPATH_10",
            "TESTING_FILEPATH_100",
            "TESTING_FILEPATH_1000",
            "TESTING_FILEPATH_1001",
            "TESTING_FILEPATH_1002",
            "TESTING_FILEPATH_1003",
            "TESTING_FILEPATH_1004",
            "TESTING_FILEPATH_1005",
        ]
        assert all((model.index(r, 2).data() in EXPECTED for r in range(model.rowCount())))
