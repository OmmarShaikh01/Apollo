from typing import Optional, Union, overload

import PySide6.QtCore
from PySide6 import QtCore


class PagedSelectionModel(QtCore.QItemSelectionModel):
    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
