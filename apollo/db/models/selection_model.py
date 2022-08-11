from typing import Optional

from PySide6 import QtCore


class PagedSelectionModel(QtCore.QItemSelectionModel):
    """
    Model for tracking selection for paged models
    """
