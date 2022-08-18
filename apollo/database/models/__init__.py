from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from apollo.database.models.library import LibraryModel
from apollo.database.models.paged_table import PagedTableModel
from apollo.database.models.queue import QueueModel


class Model_Provider(DeclarativeContainer):
    """
    Model Provider class, creates and returns singleton models
    """

    LibraryModel = Singleton(LibraryModel)
    QueueModel = Singleton(QueueModel)
