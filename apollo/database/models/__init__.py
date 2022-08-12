from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from apollo.database import Database, LibraryManager
from apollo.database.models.library import LibraryModel
from apollo.database.models.queue import QueueModel
from apollo.database.models.paged_table import PagedTableModel


class Model_Provider(DeclarativeContainer):
    """
    Model Provider class, creates and returns singleton models
    """

    _LibraryModel = Singleton(LibraryModel, database=LibraryManager)
    _QueueModel = Singleton(QueueModel, database=Database)

    @property
    def LibraryModel(self) -> LibraryModel:
        """
        Property getter

        Returns:
            LibraryModel: Returns LibraryModel model
        """
        return self._LibraryModel()

    @property
    def QueueModel(self) -> QueueModel:
        """
        Property getter

        Returns:
            QueueModel: Returns QueueModel model
        """
        return self._QueueModel()
