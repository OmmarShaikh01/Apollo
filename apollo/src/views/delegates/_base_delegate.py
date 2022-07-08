import copy
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.assets import AppIcons, AppTheme


class CustomItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        self._palette = copy.deepcopy(AppTheme)
        self._style = QtWidgets.QApplication.style()

        self._default_cover = QtGui.QPixmap(AppIcons.MUSIC_NOTE.primary)
        self._cover_cache = {}

        super().__init__(parent)

    def get_cover_from_cache(self, fid: str) -> QtGui.QPixmap:
        return self._cover_cache.get(fid, self._default_cover)

    def set_cover_to_cache(self, fid: str, data: QtGui.QPixmap):
        if 0 <= len(self._cover_cache.keys()) < 50:
            self._cover_cache[fid] = data
        else:
            self._cover_cache.popitem()

    def get_widget(
        self,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> QtWidgets.QWidget:
        raise NotImplementedError

    def draw_widget(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ) -> None:
        raise NotImplementedError

    def editorEvent(
        self,
        event: QtCore.QEvent,
        model: QtCore.QAbstractItemModel,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ) -> bool:
        return False
