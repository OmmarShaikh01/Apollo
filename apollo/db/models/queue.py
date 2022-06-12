from apollo.db.database import Database
from apollo.db.models.paged_table import PagedTableModel


class QueueModel(PagedTableModel):

    def __init__(self) -> None:
        super().__init__('queue')
        self._db = Database()

    @property
    def SelectQuery(self) -> str:
        cols = ", ".join(map(lambda x: f'library.{x}', self.COLUMNS))
        query = f"SELECT {cols} FROM queue INNER JOIN library ON queue.FILEID = library.FILEID ORDER BY queue.PLAYORDER"
        return query
