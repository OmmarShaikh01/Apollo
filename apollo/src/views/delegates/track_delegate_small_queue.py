import datetime
import os.path
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from apollo.db.models import QueueModel
from apollo.media import Mediafile
from apollo.src.views.delegates._base_delegate import CustomItemDelegate
from apollo.utils import get_logger

LOGGER = get_logger(__name__)


class TrackDelegate_Small_Queue(CustomItemDelegate):

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem,
              index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> None:
        self.draw_widget(painter, option, index)

    def sizeHint(self, option: QtWidgets.QStyleOptionViewItem,
                 index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> QtCore.QSize:
        # noinspection PyUnresolvedReferences
        w, h = option.rect.width(), 48
        return QtCore.QSize(w, h)

    # noinspection PyUnresolvedReferences
    def draw_widget(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem,
                    index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> None:
        pixmap = QtGui.QPixmap(option.rect.width(), option.rect.height())
        painter.save()

        # Draws widget into delegate
        s_painter = QtGui.QPainter(pixmap)
        widget = self.get_widget(option, index, option.widget)
        widget.setGeometry(option.rect)

        # Checks state
        state = option.state
        if state & self._style.State_Enabled and state & self._style.State_Selected:
            # Selected
            widget.setProperty('STATE', 'SELECTED')
        elif state & self._style.State_Enabled and state & self._style.State_Active:
            # Normal
            widget.setProperty('STATE', 'DEFAULT')
        elif state & self._style.State_Enabled:
            # Inactive
            widget.setProperty('STATE', 'DEFAULT')
        else:
            # Disabled
            widget.setProperty('STATE', 'DEFAULT')

        current_index_id = index.model().index(index.row(), 1).data()
        if QueueModel.CURRENT_FILE_ID is not None and QueueModel.CURRENT_FILE_ID == current_index_id:
            widget.setProperty('STATE', 'IS_PLAYING')

        widget.style().unpolish(widget)
        widget.style().polish(widget)

        # renders onto view
        widget.render(s_painter, QtCore.QPoint(0, 0), widget.rect())
        painter.drawPixmap(option.rect.topLeft(), pixmap)
        s_painter.end()

        painter.restore()

    def get_widget(self, option: QtWidgets.QStyleOptionViewItem,
                   index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
                   parent: Optional[QtWidgets.QWidget] = None) -> QtWidgets.QWidget:
        TrackDelegate_Small_Queue_Frame = QtWidgets.QFrame(None)
        TrackDelegate_Small_Queue_Frame.setObjectName(u"TrackDelegate_Small_Queue_Frame")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TrackDelegate_Small_Queue_Frame.sizePolicy().hasHeightForWidth())
        TrackDelegate_Small_Queue_Frame.setSizePolicy(sizePolicy)
        TrackDelegate_Small_Queue_Frame.setMinimumSize(QtCore.QSize(0, 48))
        TrackDelegate_Small_Queue_Frame.setMaximumSize(QtCore.QSize(16777215, 48))
        TrackDelegate_Small_Queue_Frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_Queue_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        gridLayout_2 = QtWidgets.QGridLayout(TrackDelegate_Small_Queue_Frame)
        gridLayout_2.setObjectName(u"gridLayout_2")
        gridLayout_2.setHorizontalSpacing(6)
        gridLayout_2.setContentsMargins(2, 1, 2, 1)
        TrackDelegate_Small_Queue_Cover_pixmap = QtWidgets.QLabel(TrackDelegate_Small_Queue_Frame)
        TrackDelegate_Small_Queue_Cover_pixmap.setObjectName(u"TrackDelegate_Small_Queue_Cover_pixmap")
        TrackDelegate_Small_Queue_Cover_pixmap.setMinimumSize(QtCore.QSize(40, 40))
        TrackDelegate_Small_Queue_Cover_pixmap.setMaximumSize(QtCore.QSize(40, 40))
        TrackDelegate_Small_Queue_Cover_pixmap.setFrameShape(QtWidgets.QFrame.NoFrame)

        gridLayout_2.addWidget(TrackDelegate_Small_Queue_Cover_pixmap, 0, 1, 1, 1)

        TrackDelegate_Small_Queue_time_label = QtWidgets.QLabel(TrackDelegate_Small_Queue_Frame)
        TrackDelegate_Small_Queue_time_label.setObjectName(u"TrackDelegate_Small_Queue_time_label")
        TrackDelegate_Small_Queue_time_label.setMinimumSize(QtCore.QSize(56, 40))
        TrackDelegate_Small_Queue_time_label.setMaximumSize(QtCore.QSize(56, 40))
        TrackDelegate_Small_Queue_time_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_Queue_time_label.setAlignment(Qt.AlignCenter)

        gridLayout_2.addWidget(TrackDelegate_Small_Queue_time_label, 0, 3, 1, 1)

        frame_2 = QtWidgets.QFrame(TrackDelegate_Small_Queue_Frame)
        frame_2.setObjectName(u"frame_2")
        frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        verticalLayout = QtWidgets.QVBoxLayout(frame_2)
        verticalLayout.setSpacing(0)
        verticalLayout.setObjectName(u"verticalLayout")
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        TrackDelegate_Small_Queue_title_label = QtWidgets.QLabel(frame_2)
        TrackDelegate_Small_Queue_title_label.setObjectName(u"TrackDelegate_Small_Queue_title_label")
        TrackDelegate_Small_Queue_title_label.setMinimumSize(QtCore.QSize(0, 14))
        TrackDelegate_Small_Queue_title_label.setMaximumSize(QtCore.QSize(16777215, 14))
        TrackDelegate_Small_Queue_title_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_Queue_title_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        verticalLayout.addWidget(TrackDelegate_Small_Queue_title_label)

        TrackDelegate_Small_Queue_artist_label = QtWidgets.QLabel(frame_2)
        TrackDelegate_Small_Queue_artist_label.setObjectName(u"TrackDelegate_Small_Queue_artist_label")
        TrackDelegate_Small_Queue_artist_label.setMinimumSize(QtCore.QSize(0, 14))
        TrackDelegate_Small_Queue_artist_label.setMaximumSize(QtCore.QSize(16777215, 14))
        TrackDelegate_Small_Queue_artist_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_Queue_artist_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        verticalLayout.addWidget(TrackDelegate_Small_Queue_artist_label)

        TrackDelegate_Small_Queue_album_label = QtWidgets.QLabel(frame_2)
        TrackDelegate_Small_Queue_album_label.setObjectName(u"TrackDelegate_Small_Queue_album_label")
        TrackDelegate_Small_Queue_album_label.setMinimumSize(QtCore.QSize(0, 14))
        TrackDelegate_Small_Queue_album_label.setMaximumSize(QtCore.QSize(16777215, 14))
        TrackDelegate_Small_Queue_album_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_Queue_album_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        verticalLayout.addWidget(TrackDelegate_Small_Queue_album_label)

        gridLayout_2.addWidget(frame_2, 0, 2, 1, 1, Qt.AlignVCenter)

        TrackDelegate_Small_Queue_number_label = QtWidgets.QLabel(TrackDelegate_Small_Queue_Frame)
        TrackDelegate_Small_Queue_number_label.setObjectName(u"TrackDelegate_Small_Queue_number_label")
        TrackDelegate_Small_Queue_number_label.setMinimumSize(QtCore.QSize(32, 40))
        TrackDelegate_Small_Queue_number_label.setMaximumSize(QtCore.QSize(32, 40))
        TrackDelegate_Small_Queue_number_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_Queue_number_label.setAlignment(Qt.AlignCenter)

        gridLayout_2.addWidget(TrackDelegate_Small_Queue_number_label, 0, 0, 1, 1)

        # noinspection PyUnresolvedReferences
        if option.widget.width() <= 320:
            TrackDelegate_Small_Queue_number_label.hide()

        # widget set data
        self._widget_set_data(index, **dict(
            TrackDelegate_Small_Queue_Cover_pixmap = TrackDelegate_Small_Queue_Cover_pixmap,
            TrackDelegate_Small_Queue_time_label = TrackDelegate_Small_Queue_time_label,
            TrackDelegate_Small_Queue_title_label = TrackDelegate_Small_Queue_title_label,
            TrackDelegate_Small_Queue_artist_label = TrackDelegate_Small_Queue_artist_label,
            TrackDelegate_Small_Queue_album_label = TrackDelegate_Small_Queue_album_label,
            TrackDelegate_Small_Queue_number_label = TrackDelegate_Small_Queue_number_label
        ))

        return TrackDelegate_Small_Queue_Frame

    # noinspection PyMethodMayBeStatic
    def _widget_set_data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex], **kwargs):
        TrackDelegate_Small_Queue_Cover_pixmap = kwargs['TrackDelegate_Small_Queue_Cover_pixmap']
        TrackDelegate_Small_Queue_time_label = kwargs['TrackDelegate_Small_Queue_time_label']
        TrackDelegate_Small_Queue_title_label = kwargs['TrackDelegate_Small_Queue_title_label']
        TrackDelegate_Small_Queue_artist_label = kwargs['TrackDelegate_Small_Queue_artist_label']
        TrackDelegate_Small_Queue_album_label = kwargs['TrackDelegate_Small_Queue_album_label']
        TrackDelegate_Small_Queue_number_label = kwargs['TrackDelegate_Small_Queue_number_label']

        # widget set data
        TrackDelegate_Small_Queue_Cover_pixmap.setText("")
        self.set_cover_img(TrackDelegate_Small_Queue_Cover_pixmap, index)

        TrackDelegate_Small_Queue_title_label.setText(str(index.model().index(index.row(), 7).data()))
        TrackDelegate_Small_Queue_artist_label.setText(str(index.model().index(index.row(), 8).data()))
        TrackDelegate_Small_Queue_album_label.setText(str(index.model().index(index.row(), 17).data()))

        song_len = datetime.timedelta(seconds = float(index.model().index(index.row(), 35).data()))
        TrackDelegate_Small_Queue_time_label.setText(str(song_len))

        TrackDelegate_Small_Queue_number_label.setText(str(index.model().index(index.row(), 0).data()))

    def set_cover_img(self, widget: QtWidgets.QLabel, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        current_index_id = index.model().index(index.row(), 1).data()
        if current_index_id not in self._cover_cache.keys():
            current_index_path = index.model().index(index.row(), 2).data()
            if os.path.exists(current_index_path) and Mediafile.isSupported(current_index_path):
                # noinspection PyUnresolvedReferences
                data = Mediafile(current_index_path).Artwork[0].data
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                pixmap = pixmap.scaled(widget.size(), mode = Qt.SmoothTransformation)
                widget.setPixmap(pixmap)
                self.set_cover_to_cache(current_index_id, pixmap)
                return None

        pixmap = self.get_cover_from_cache(current_index_id)
        if pixmap.size() != widget.size():
            pixmap = pixmap.scaled(widget.size(), mode = Qt.SmoothTransformation)
        widget.setPixmap(pixmap)
