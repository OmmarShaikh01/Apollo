from apollo.db.database import LibraryManager
from apollo.db.models.paged_table import PagedTableModel
from apollo.media import Stream


class LibraryModel(PagedTableModel):
    PRIVATE_FIELDS = ['FILEID', 'FILEPATH', 'FILENAME', 'FILESIZE', 'FILEEXT']

    def __init__(self) -> None:
        super().__init__('library')
        self._db = LibraryManager()

    @property
    def SelectQuery(self) -> str:
        cols = ', '.join(self.Columns)
        return f'SELECT {cols} FROM library'

    @property
    def Columns(self) -> list:
        cols = [f'library.{i}' for i in Stream.TAG_FRAMES]
        return cols

    def search_album(self, query: str):
        self.clear_filter()
        col_index = self.Columns.index('library.ALBUM')
        self.set_filter(col_index, query)

    def search_artist(self, query: str):
        self.clear_filter()
        col_index = self.Columns.index('library.ARTIST')
        self.set_filter(col_index, query)

    def search_title(self, query: str):
        self.clear_filter()
        col_index = self.Columns.index('library.TITLE')
        self.set_filter(col_index, query)

    def search_filename(self, query: str):
        self.clear_filter()
        col_index = self.Columns.index('library.FILENAME')
        self.set_filter(col_index, query)
