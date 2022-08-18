import random
from typing import Optional, Union

from PySide6 import QtCore

from apollo.database import Database, RecordSet
from apollo.database.models.paged_table import PagedTableModel
from apollo.media import Stream
from apollo.utils import get_logger

LOGGER = get_logger(__name__)


class QueueModel(PagedTableModel):
    """
    Queue Paged Table Model
    """

    CURRENT_FILE_ID = None
    PRIVATE_FIELDS = ["PLAYORDER", "FILEID", "FILEPATH", "FILENAME", "FILESIZE", "FILEEXT"]

    def __init__(self) -> None:
        super().__init__("queue", Database())

    @property
    def SelectQuery(self) -> str:
        cols = ", ".join(self.Columns)
        return f"SELECT {cols} FROM queue INNER JOIN library ON queue.FILEID = library.FILEID"

    @property
    def Columns(self) -> list:
        cols = ["queue.PLAYORDER", *[f"library.{i}" for i in Stream.TAG_FRAMES]]
        return cols

    def search_album(self, query: str):
        """
        Searches Query in album Column

        Args:
            query (str): term to search for
        """
        self.clear_filter()
        col_index = self.Columns.index("library.ALBUM")
        self.set_filter(query, col_index)

    def search_artist(self, query: str):
        """
        Searches Query in artist Column

        Args:
            query (str): term to search for
        """
        self.clear_filter()
        col_index = self.Columns.index("library.ARTIST")
        self.set_filter(query, col_index)

    def search_title(self, query: str):
        """
        Searches Query in title Column

        Args:
            query (str): term to search for
        """
        self.clear_filter()
        col_index = self.Columns.index("library.TITLE")
        self.set_filter(query, col_index)

    def search_filename(self, query: str):
        """
        Searches Query in filename Column

        Args:
            query (str): term to search for
        """
        self.clear_filter()
        col_index = self.Columns.index("library.FILENAME")
        self.set_filter(query, col_index)

    def insert_into_queue(
        self, indexes: list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]]
    ):
        # pylint: disable=C0301
        """
        Inserts the given indexes into the queue table

        Args:
            indexes (list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]]): Items to add to the queue
        """
        cols = ["PLAYORDER", "FILEID"]
        records = [[i, d] for i, d in enumerate(indexes)]
        with self._db.connector as conn:
            self._db.batch_insert(RecordSet(cols, records), "queue", conn)
        self.clear()
        self.fetch_data(self.FETCH_DATA_DOWN)

    def play_now(self, indexes: list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]]):
        # pylint: disable=C0301
        """
        Adds selected index to the top of the playing queue

        Args:
            indexes list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]]: Items to add to the queue
        """
        indexes = list(map(lambda x: x.data(), indexes))
        with self._db.connector as conn:
            self._db.execute("DELETE FROM queue", conn)

        self.insert_into_queue(indexes)

    def queue_next(
        self,
        indexes: list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]],
    ):
        # pylint: disable=C0301
        """
        Queues items after the currently playing item

        Args:
            indexes (list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]]): Indexes to queue
        """
        indexes = list(map(lambda x: x.data(), indexes))
        with self._db.connector as conn:
            data = list(
                map(
                    lambda x: x[0], self._db.execute("SELECT queue.FILEID FROM queue", conn).records
                )
            )

        if len(data) != 0 and self.CURRENT_FILE_ID is not None:
            current_index = self.CURRENT_FILE_ID
            pos = data.index(current_index)
            if pos == 0:
                indexes = [data[0], *indexes, *data[(pos + 1):]]
            elif pos == (len(data) - 1):
                indexes = [*data, *indexes]
            else:
                indexes = [*data[0:pos + 1], *indexes, *data[pos + 1:]]

        self.insert_into_queue(indexes)

    def queue_last(
        self,
        indexes: list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]],
    ):
        # pylint: disable=C0301
        """
        Queues items at the end

        Args:
            indexes (list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]]): Indexes to queue
        """
        indexes = list(map(lambda x: x.data(), indexes))
        with self._db.connector as conn:
            data = list(
                map(
                    lambda x: x[0], self._db.execute("SELECT queue.FILEID FROM queue", conn).records
                )
            )

        if len(data) != 0:
            indexes = [*data, *indexes]

        self.insert_into_queue(indexes)

    def play_artist(
        self,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ):
        # pylint: disable=C0301
        """
        Adds items with similar artist to the queue

        Args:
            index Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]: Index to use to extract artist from
        """
        index = index.data()
        with self._db.connector as conn:
            self._db.execute("DELETE FROM queue", conn)
            data = list(
                map(
                    lambda x: x[0],
                    self._db.execute(
                        f"SELECT library.ARTIST FROM library WHERE library.FILEID = '{index}' LIMIT 1",
                        conn,
                    ).records,
                )
            )[0]
            data = list(
                map(
                    lambda x: x[0],
                    self._db.execute(
                        f"SELECT library.FILEID FROM library WHERE library.ARTIST LIKE '%{data}%'",
                        conn,
                    ).records,
                )
            )

        if data:
            self.insert_into_queue(data)

    def play_album(
        self,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ):
        # pylint: disable=C0301
        """
        Adds items with similar album to the queue

        Args:
            index Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]: Index to use to extract album from
        """
        index = index.data()
        with self._db.connector as conn:
            self._db.execute("DELETE FROM queue", conn)
            data = list(
                map(
                    lambda x: x[0],
                    self._db.execute(
                        f"SELECT library.ALBUM FROM library WHERE library.FILEID = '{index}' LIMIT 1",
                        conn,
                    ).records,
                )
            )[0]
            data = list(
                map(
                    lambda x: x[0],
                    self._db.execute(
                        f"SELECT library.FILEID FROM library WHERE library.ALBUM LIKE '%{data}%'",
                        conn,
                    ).records,
                )
            )

        if data:
            self.insert_into_queue(data)

    def play_genre(
        self,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ):
        # pylint: disable=C0301
        """
        Adds items with similar genre to the queue

        Args:
            index Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]: Index to use to extract genre from
        """
        index = index.data()
        with self._db.connector as conn:
            self._db.execute("DELETE FROM queue", conn)
            data = list(
                map(
                    lambda x: x[0],
                    self._db.execute(
                        f"SELECT library.MOOD FROM library WHERE library.FILEID = '{index}' LIMIT 1",
                        conn,
                    ).records,
                )
            )[0]
            data = list(
                map(
                    lambda x: x[0],
                    self._db.execute(
                        f"SELECT library.FILEID FROM library WHERE library.MOOD LIKE '%{data}%'",
                        conn,
                    ).records,
                )
            )

        if data:
            self.insert_into_queue(data)

    def play_shuffled(
        self,
        indexes: Optional[list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]]] = None,
    ):
        # pylint: disable=C0301
        """
        Adds selected indexes to the playing queue (shuffled)

        Args:
            indexes Optional[list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]]]: Items to add to the queue
        """
        if indexes is not None:
            indexes = list(map(lambda x: x.data(), indexes))

        with self._db.connector as conn:
            self._db.execute("DELETE FROM queue", conn)
            if indexes is None:
                indexes = list(
                    map(
                        lambda x: x[0],
                        self._db.execute(
                            "SELECT library.FILEID from library",
                            conn,
                        ).records,
                    )
                )

        random.shuffle(indexes)
        self.insert_into_queue(indexes)
