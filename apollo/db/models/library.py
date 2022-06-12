from apollo.db.database import LibraryManager
from apollo.db.models.paged_table import PagedTableModel


class LibraryModel(PagedTableModel):

    def __init__(self) -> None:
        super().__init__('library')
        self._db = LibraryManager()
        self.prefetch(self.FETCH_SCROLL_DOWN)

    @property
    def SelectQuery(self) -> str:
        cols = ", ".join(self.COLUMNS)
        return f'SELECT {cols} FROM library'
