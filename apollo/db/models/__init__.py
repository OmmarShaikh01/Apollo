from typing import Union

from apollo.db.models.library import LibraryModel
from apollo.db.models.paged_table import PagedTableModel
from apollo.db.models.queue import QueueModel
from apollo.db.models.selection_model import PagedSelectionModel


class _Provider:
    """
    Model Provider class, creates and returns singleton models
    """

    def __init__(self) -> None:
        self.LibraryModel = None
        self.QueueModel = None

    def get_model(
        self, _type: Union[LibraryModel, QueueModel]
    ) -> Union[LibraryModel, QueueModel, None]:
        """
        Returns Model Singleton

        Args:
            _type (Union[LibraryModel, QueueModel]):

        Returns:
            Union[LibraryModel, QueueModel, None]
        """
        if _type is LibraryModel:
            if self.LibraryModel is None:
                self.LibraryModel = LibraryModel()
            return self.LibraryModel

        if _type is QueueModel:
            if self.QueueModel is None:
                self.QueueModel = QueueModel()
            return self.QueueModel

        return None


ModelProvider = _Provider()
