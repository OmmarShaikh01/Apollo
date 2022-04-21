import datetime
import typing, os
from typing import Optional, Union

from PySide6.QtCore import QRect, QPoint, QSize
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6 import QtCore, QtWidgets, QtGui

from apollo.db.models import QueueModel, Provider
from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo
from apollo.src.playback_bar import PlayBackBar
from apollo.media import Mediafile
from apollo.utils import ROOT


class QueueItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, model: QueueModel) -> None:
        super().__init__()
        self._model = model
        self._page = {}
        self._style = QtWidgets.QApplication.style()
        self.init_default_cover()

    def init_default_cover(self):
        default = (os.path.join(ROOT, 'assets', 'generated', 'theme_custom', 'primary', 'music-note-2.4.svg'))
        data = QIcon(default)
        self.default_cover = data.pixmap(QtCore.QSize(60, 60))

    def sizeHint(self, option: QtWidgets.QStyleOptionViewItem,
                 index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> QtCore.QSize:
        return QtCore.QSize(option.rect.width(), 64)

    def getRowData(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> dict:
        row = index.row()
        fields = self._model.database.library_columns
        return {col: self._model.index(row, fields.index(col)).data() for col in fields}

    def setPageItem(self, key: str, value: typing.Any):
        if len(self._page) > 20:
            del self._page[tuple(self._page.keys())[0]]
        self._page[key] = value

    def getPageItem(self, key: str):
        return self._page.get(key, None)

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem,
              index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> None:
        self.DrawWidget(painter, option, index)

    def DrawWidget(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem,
                   index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> None:
        state = option.state

        if state & self._style.State_Enabled and state & self._style.State_Selected:
            # Selected
            color = (QtGui.QColor(0, 0, 0, int(255 * 1)))
            border = (QtGui.QColor(0, 0, 0, int(255 * 1)))
        elif state & self._style.State_Enabled and state & self._style.State_Active:
            # Normal
            color = (QtGui.QColor(255, 255, 255, int(255 * 0.75)))
            border = (QtGui.QColor(255, 255, 255, int(255 * 0.75)))
        elif state & self._style.State_Enabled:
            # Inactive
            color = (QtGui.QColor(255, 255, 255, int(255 * 0.75)))
            border = (QtGui.QColor(255, 255, 255, int(255 * 0.75)))
        else:
            # Disabled
            color = (QtGui.QColor(255, 255, 255, int(255 * 0.5)))
            border = (QtGui.QColor(255, 255, 255, int(255 * 0.5)))

        painter.setPen(color)
        self._style.drawPrimitive(self._style.PE_PanelItemViewItem, option, painter, option.widget)
        painter.fillRect(option.rect, QtGui.QColor(0, 0, 0, 0))

        # painter.setPen(QtGui.QColor(self._theme.get("text-02")))
        items = self.getRowData(index)
        self.DrawCover(painter, option, items)
        self.DrawTitleLabel(painter, option, items)
        self.DrawArtistLabel(painter, option, items)
        self.DrawBottomLabels(painter, option, items)

        painter.setPen(QtGui.QColor(0, 0, 0, int(255 * 0.5)))
        painter.drawLine(QPoint(0, option.rect.y() + 64), QPoint(option.rect.width(), option.rect.y() + 64))

    def DrawCover(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, item: dict):
        self._style.subElementRect(self._style.SE_ItemViewItemDecoration, option, option.widget)
        rect = option.rect
        temprec = QRect(rect.x() + 2, rect.y() + 2, 60, 60)
        self.setAlbumCoverImage(painter, temprec, item["file_path"])

    def setAlbumCoverImage(self, painter: QtGui.QPainter, rect: QRect, key: str):
        size = QSize(rect.width(), rect.height())
        data = self.getPageItem(key)
        if data is None:
            media = Mediafile(key)
            data = media.Artwork
            if isinstance(data, bytes):
                data = QtGui.QImage().fromData(data).scaled(size)
                painter.drawImage(rect, data)
                self.setPageItem(key, data)
            else:
                painter.drawImage(rect, self.default_cover.toImage())
        elif isinstance(data, QImage):
            painter.drawImage(rect, data)

    def DrawTitleLabel(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, item: dict):
        rect = option.rect
        temprec = QRect(rect.x() + 64, rect.y() + 4, rect.width() - 68, 16)
        painter.drawText(temprec, str(item.get("tracktitle", "")).title())

    def DrawArtistLabel(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, item: dict):
        rect = option.rect
        temprec = QRect(rect.x() + 64, rect.y() + 24, rect.width() - 68, 16)
        painter.drawText(temprec, str(item.get("artist", "")).title())

    def DrawBottomLabels(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, item: dict):
        rect = option.rect
        Width = round((rect.width() - 72) / 3)
        # 1
        temprec = QRect(rect.x() + 64, rect.y() + 44, Width, 16)
        painter.drawText(temprec, str(item.get("album", "")).title())
        # 2
        temprec = QRect(rect.x() + (64 + Width + 4), rect.y() + 44, Width, 16)
        painter.drawText(temprec, str(item.get("genre", "")).title())
        # 3
        temprec = QRect(rect.x() + (64 + Width + 4 + Width + 4), rect.y() + 44, Width - 4, 16)
        _time = ':'.join(str(datetime.timedelta(seconds = eval(item.get("length", "")))).split(".")[0].split(":")[1:])
        painter.drawText(temprec, _time)


class NowPlayingTab:

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.playback_bar_controller = PlayBackBar(ui)
        self.setupUI()

    def setupUI(self):
        # TODO save initial states into a temporary dump
        self.setTableModel()
        self.ui.queue_listview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.connectLineEdit()
        self.connectTableView()

    def setTableModel(self):
        self.model = Provider.get_model(QueueModel)
        self.item_delegate = QueueItemDelegate(self.model)

        self.ui.queue_listview.setModel(self.model)
        self.ui.queue_listview.setModelColumn(self.model.database.library_columns.index('tracktitle'))
        self.ui.queue_listview.setItemDelegate(self.item_delegate)

    def connectLineEdit(self):
        self.ui.queue_tab_lineedit.returnPressed.connect(lambda: (
            self.model.search_table(self.ui.queue_tab_lineedit.text())
        ))
        self.ui.queue_tab_lineedit.textChanged.connect(lambda: (
            self.model.search_table(self.ui.queue_tab_lineedit.text())
        ))
        self.ui.library_tab_search_pushbutton.pressed.connect(lambda: (
            self.model.search_table(self.ui.queue_tab_lineedit.text())
        ))

    def connectTableView(self):
        self.ui.queue_listview.doubleClicked.connect(lambda item: (
            self.playSelected(item.row())
        ))

    def playSelected(self, row_id):
        row = self.getRowData(row_id, ['file_id'])
        self.playback_bar_controller.play_File(row[0])

    def getRowData(self, index, column: str = None) -> list[list]:
        if column is not None:
            column = [self.model.database.library_columns.index(item) for item in column]
        return [self.model.index(index, col).data() for col in column]

    def getRowModelIndex(self, index, column: str = None) -> list[list]:
        if column is not None:
            column = [self.model.database.library_columns.index(item) for item in column]
        return [self.model.index(index, col) for col in [0]]
