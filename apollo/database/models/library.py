from typing import Union

from PySide6 import QtCore

from apollo.database import LibraryManager
from apollo.database.models.paged_table import PagedTableModel
from apollo.media import Stream
from apollo.utils import get_logger

LOGGER = get_logger(__name__)


class LibraryModel(PagedTableModel):
    """
    Library Paged Table Model
    """

    PRIVATE_FIELDS = ["FILEID", "FILEPATH", "FILENAME", "FILESIZE", "FILEEXT"]

    def __init__(self) -> None:
        super().__init__("library", LibraryManager())

    @property
    def SelectQuery(self) -> str:
        cols = ", ".join(self.Columns)
        return f"SELECT {cols} FROM library"

    @property
    def Columns(self) -> list:
        cols = [f"library.{i}" for i in Stream.TAG_FRAMES]
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

    def fetch_track_info(self, fid: str):
        """
        Fetches track information from the library

        Args:
            fid (str): File id

        Returns:
            Recordset: Fetched info for the track
        """
        with self._db.connector as conn:
            cols = ", ".join(self.Columns)
            data = self._db.execute(
                f"SELECT {cols} FROM library where library.FILEID = '{fid}'", conn
            )
        return data

    def update_track_rating(
        self,
        rating: Union[int, float],
        indexes: list[Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]]
    ):
        if 0 <= rating <= 5:
            indexes = list(map(lambda x: f"'{x.data()}'", indexes))
            with self._db.connector as conn:
                query = f"UPDATE library SET POPULARIMETER = {rating} WHERE FILEID IN ({', '.join(indexes)})"
                self._db.execute(query, conn)

    def update_current_track_rating(
        self,
        rating: Union[int, float],
        fid: str
    ):
        if 0 <= rating <= 5 and fid:
            with self._db.connector as conn:
                query = f"UPDATE library SET POPULARIMETER = {rating} WHERE FILEID IN ('{fid}')"
                self._db.execute(query, conn)
