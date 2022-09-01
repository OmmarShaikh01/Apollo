from typing import Optional

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from apollo.database.db import Database
from apollo.database.models.library import LibraryModel
from apollo.database.models.paged_table import PagedTableModel
from apollo.database.models.queue import QueueModel


def _cb_modifided_db_data_signal(table: Optional[str] = None):
    """
    Handles change events for DB data

    Args:
        table (Optional[str]): table model to refresh
    """
    if table is None:
        Model_Provider.LibraryModel().refresh()
        Model_Provider.QueueModel().refresh()
    elif table.upper() == "LIBRARY":
        Model_Provider.LibraryModel().refresh()
    elif table.upper() == "QUEUE":
        Model_Provider.QueueModel().refresh()


class Model_Provider(DeclarativeContainer):
    """
    Model Provider class, creates and returns singleton models
    """

    LibraryModel = Singleton(LibraryModel)
    QueueModel = Singleton(QueueModel)
    Database().ModifidedDBData_Signal.connect(_cb_modifided_db_data_signal)
