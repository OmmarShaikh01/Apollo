import datetime
import os.path
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem

from apollo.assets.app_themes import AppIcons
from apollo.db.models import QueueModel
from apollo.media import Mediafile
from apollo.src.views.delegates._base_delegate import CustomItemDelegate
from apollo.utils import get_logger


LOGGER = get_logger(__name__)


class TrackDelegate_Mid(CustomItemDelegate):
    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ) -> None:
        self.draw_widget(painter, option, index)

    def sizeHint(
        self,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ) -> QtCore.QSize:
        # noinspection PyUnresolvedReferences
        w, h = option.rect.width(), 72
        return QtCore.QSize(w, h)

    # noinspection PyUnresolvedReferences
    def draw_widget(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ) -> None:
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
            widget.setProperty("STATE", "SELECTED")
        elif state & self._style.State_Enabled and state & self._style.State_Active:
            # Normal
            widget.setProperty("STATE", "DEFAULT")
        elif state & self._style.State_Enabled:
            # Inactive
            widget.setProperty("STATE", "DEFAULT")
        else:
            # Disabled
            widget.setProperty("STATE", "DEFAULT")

        widget.style().unpolish(widget)
        widget.style().polish(widget)

        # renders onto view
        widget.render(s_painter, QtCore.QPoint(0, 0), widget.rect())
        painter.drawPixmap(option.rect.topLeft(), pixmap)
        s_painter.end()

        painter.restore()

    def get_widget(
        self,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> QtWidgets.QWidget:
        # widget creation
        TrackDelegate_Mid_Frame = QFrame(None)
        TrackDelegate_Mid_Frame.setObjectName("TrackDelegate_Mid_Frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TrackDelegate_Mid_Frame.sizePolicy().hasHeightForWidth())
        TrackDelegate_Mid_Frame.setSizePolicy(sizePolicy)
        TrackDelegate_Mid_Frame.setMinimumSize(QSize(0, 72))
        TrackDelegate_Mid_Frame.setMaximumSize(QSize(16777215, 72))
        TrackDelegate_Mid_Frame.setFrameShape(QFrame.StyledPanel)
        TrackDelegate_Mid_Frame.setFrameShadow(QFrame.Raised)
        horizontalLayout_2 = QHBoxLayout(TrackDelegate_Mid_Frame)
        horizontalLayout_2.setSpacing(8)
        horizontalLayout_2.setObjectName("horizontalLayout_2")
        horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        TrackDelegate_Mid_Cover_pixmap = QLabel(TrackDelegate_Mid_Frame)
        TrackDelegate_Mid_Cover_pixmap.setObjectName("TrackDelegate_Mid_Cover_pixmap")
        TrackDelegate_Mid_Cover_pixmap.setMinimumSize(QSize(64, 64))
        TrackDelegate_Mid_Cover_pixmap.setMaximumSize(QSize(64, 64))
        TrackDelegate_Mid_Cover_pixmap.setAlignment(Qt.AlignCenter)

        horizontalLayout_2.addWidget(TrackDelegate_Mid_Cover_pixmap)

        frame_2 = QFrame(TrackDelegate_Mid_Frame)
        frame_2.setObjectName("frame_2")
        sizePolicy.setHeightForWidth(frame_2.sizePolicy().hasHeightForWidth())
        frame_2.setSizePolicy(sizePolicy)
        frame_2.setFrameShape(QFrame.NoFrame)
        frame_2.setFrameShadow(QFrame.Raised)
        gridLayout = QGridLayout(frame_2)
        gridLayout.setSpacing(2)
        gridLayout.setObjectName("gridLayout")
        gridLayout.setContentsMargins(0, 0, 0, 0)
        TrackDelegate_Mid_title_label = QLabel(frame_2)
        TrackDelegate_Mid_title_label.setObjectName("TrackDelegate_Mid_title_label")
        sizePolicy.setHeightForWidth(TrackDelegate_Mid_title_label.sizePolicy().hasHeightForWidth())
        TrackDelegate_Mid_title_label.setSizePolicy(sizePolicy)
        TrackDelegate_Mid_title_label.setMinimumSize(QSize(0, 24))
        TrackDelegate_Mid_title_label.setMaximumSize(QSize(16777215, 24))

        gridLayout.addWidget(TrackDelegate_Mid_title_label, 0, 0, 1, 1)

        TrackDelegate_Mid_album_label = QLabel(frame_2)
        TrackDelegate_Mid_album_label.setObjectName("TrackDelegate_Mid_album_label")
        sizePolicy.setHeightForWidth(TrackDelegate_Mid_album_label.sizePolicy().hasHeightForWidth())
        TrackDelegate_Mid_album_label.setSizePolicy(sizePolicy)
        TrackDelegate_Mid_album_label.setMinimumSize(QSize(0, 24))
        TrackDelegate_Mid_album_label.setMaximumSize(QSize(16777215, 24))

        gridLayout.addWidget(TrackDelegate_Mid_album_label, 0, 1, 1, 1)

        frame_3 = QFrame(frame_2)
        frame_3.setObjectName("frame_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(frame_3.sizePolicy().hasHeightForWidth())
        frame_3.setSizePolicy(sizePolicy1)
        frame_3.setFrameShape(QFrame.NoFrame)
        frame_3.setFrameShadow(QFrame.Raised)
        gridLayout_2 = QGridLayout(frame_3)
        gridLayout_2.setSpacing(2)
        gridLayout_2.setObjectName("gridLayout_2")
        gridLayout_2.setContentsMargins(0, 0, 0, 0)
        TrackDelegate_Mid_misc1_label = QLabel(frame_3)
        TrackDelegate_Mid_misc1_label.setObjectName("TrackDelegate_Mid_misc1_label")
        TrackDelegate_Mid_misc1_label.setMinimumSize(QSize(0, 0))
        TrackDelegate_Mid_misc1_label.setMaximumSize(QSize(16777215, 16777215))

        gridLayout_2.addWidget(TrackDelegate_Mid_misc1_label, 1, 0, 1, 1)

        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        gridLayout_2.addItem(horizontalSpacer, 1, 3, 1, 1)

        TrackDelegate_Mid_misc3_label = QLabel(frame_3)
        TrackDelegate_Mid_misc3_label.setObjectName("TrackDelegate_Mid_misc3_label")
        TrackDelegate_Mid_misc3_label.setMinimumSize(QSize(0, 0))
        TrackDelegate_Mid_misc3_label.setMaximumSize(QSize(16777215, 16777215))

        gridLayout_2.addWidget(TrackDelegate_Mid_misc3_label, 1, 2, 1, 1)

        TrackDelegate_Mid_misc2_label = QLabel(frame_3)
        TrackDelegate_Mid_misc2_label.setObjectName("TrackDelegate_Mid_misc2_label")
        TrackDelegate_Mid_misc2_label.setMinimumSize(QSize(0, 0))
        TrackDelegate_Mid_misc2_label.setMaximumSize(QSize(16777215, 16777215))

        gridLayout_2.addWidget(TrackDelegate_Mid_misc2_label, 1, 1, 1, 1)

        TrackDelegate_Mid_artist_label = QLabel(frame_3)
        TrackDelegate_Mid_artist_label.setObjectName("TrackDelegate_Mid_artist_label")
        sizePolicy1.setHeightForWidth(
            TrackDelegate_Mid_artist_label.sizePolicy().hasHeightForWidth()
        )
        TrackDelegate_Mid_artist_label.setSizePolicy(sizePolicy1)

        gridLayout_2.addWidget(TrackDelegate_Mid_artist_label, 0, 0, 1, 3)

        gridLayout.addWidget(frame_3, 1, 0, 1, 1)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        gridLayout.addItem(verticalSpacer, 1, 1, 1, 1)

        horizontalLayout_2.addWidget(frame_2)

        TrackDelegate_Mid_isLiked_pixmap = QLabel(TrackDelegate_Mid_Frame)
        TrackDelegate_Mid_isLiked_pixmap.setObjectName("TrackDelegate_Mid_isLiked_pixmap")
        TrackDelegate_Mid_isLiked_pixmap.setMinimumSize(QSize(32, 0))
        TrackDelegate_Mid_isLiked_pixmap.setMaximumSize(QSize(32, 16777215))

        horizontalLayout_2.addWidget(TrackDelegate_Mid_isLiked_pixmap)

        TrackDelegate_Mid_time_label = QLabel(TrackDelegate_Mid_Frame)
        TrackDelegate_Mid_time_label.setObjectName("TrackDelegate_Mid_time_label")
        TrackDelegate_Mid_time_label.setMinimumSize(QSize(64, 0))
        TrackDelegate_Mid_time_label.setMaximumSize(QSize(64, 16777215))
        TrackDelegate_Mid_time_label.setAlignment(Qt.AlignCenter)

        horizontalLayout_2.addWidget(TrackDelegate_Mid_time_label)

        # widget set data
        self._widget_set_data(
            index,
            **dict(
                TrackDelegate_Mid_Cover_Pixmap=TrackDelegate_Mid_Cover_pixmap,
                TrackDelegate_Mid_isLiked_Pixmap=TrackDelegate_Mid_isLiked_pixmap,
                TrackDelegate_Mid_title_label=TrackDelegate_Mid_title_label,
                TrackDelegate_Mid_artist_label=TrackDelegate_Mid_artist_label,
                TrackDelegate_Mid_time_label=TrackDelegate_Mid_time_label,
                TrackDelegate_Mid_album_label=TrackDelegate_Mid_album_label,
                TrackDelegate_Mid_misc1_label=TrackDelegate_Mid_misc1_label,
                TrackDelegate_Mid_misc2_label=TrackDelegate_Mid_misc2_label,
                TrackDelegate_Mid_misc3_label=TrackDelegate_Mid_misc3_label,
            ),
        )

        return TrackDelegate_Mid_Frame

    # noinspection PyMethodMayBeStatic
    def _widget_set_data(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex], **kwargs
    ):
        TrackDelegate_Mid_Cover_Pixmap = kwargs["TrackDelegate_Mid_Cover_Pixmap"]
        TrackDelegate_Mid_isLiked_Pixmap = kwargs["TrackDelegate_Mid_isLiked_Pixmap"]
        TrackDelegate_Mid_title_label = kwargs["TrackDelegate_Mid_title_label"]
        TrackDelegate_Mid_artist_label = kwargs["TrackDelegate_Mid_artist_label"]
        TrackDelegate_Mid_time_label = kwargs["TrackDelegate_Mid_time_label"]
        TrackDelegate_Mid_album_label = kwargs["TrackDelegate_Mid_album_label"]
        TrackDelegate_Mid_misc1_label = kwargs["TrackDelegate_Mid_misc1_label"]
        TrackDelegate_Mid_misc2_label = kwargs["TrackDelegate_Mid_misc2_label"]
        TrackDelegate_Mid_misc3_label = kwargs["TrackDelegate_Mid_misc3_label"]

        # widget set data
        TrackDelegate_Mid_Cover_Pixmap.setText("")
        self.set_cover_img(TrackDelegate_Mid_Cover_Pixmap, index)

        TrackDelegate_Mid_isLiked_Pixmap.setText("")
        rating = float(index.model().index(index.row(), 71).data())
        if rating == 5:
            pixmap = QtGui.QPixmap(AppIcons.FAVORITE_FILLED.primary)
            pixmap = pixmap.scaled(QtCore.QSize(32, 32), mode=Qt.SmoothTransformation)
            TrackDelegate_Mid_isLiked_Pixmap.setPixmap(pixmap)
        else:
            pixmap = QtGui.QPixmap(AppIcons.FAVORITE.primary)
            pixmap = pixmap.scaled(QtCore.QSize(32, 32), mode=Qt.SmoothTransformation)
            TrackDelegate_Mid_isLiked_Pixmap.setPixmap(pixmap)

        TrackDelegate_Mid_title_label.setText(str(index.model().index(index.row(), 6).data()))
        TrackDelegate_Mid_artist_label.setText(str(index.model().index(index.row(), 8).data()))
        TrackDelegate_Mid_album_label.setText(str(index.model().index(index.row(), 16).data()))

        TrackDelegate_Mid_misc1_label.setText(str(index.model().index(index.row(), 73).data()))
        TrackDelegate_Mid_misc2_label.setText(str(index.model().index(index.row(), 74).data()))
        TrackDelegate_Mid_misc3_label.setText(str(index.model().index(index.row(), 75).data()))

        song_len = datetime.timedelta(seconds=float(index.model().index(index.row(), 34).data()))
        TrackDelegate_Mid_time_label.setText(str(song_len))

    def set_cover_img(
        self,
        widget: QtWidgets.QLabel,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ):
        current_index_id = index.model().index(index.row(), 0).data()
        if current_index_id not in self._cover_cache.keys():
            current_index_path = index.model().index(index.row(), 1).data()
            if os.path.exists(current_index_path) and Mediafile.isSupported(current_index_path):
                # noinspection PyUnresolvedReferences
                data = Mediafile(current_index_path).Artwork[0].data
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                pixmap = pixmap.scaled(widget.size(), mode=Qt.SmoothTransformation)
                widget.setPixmap(pixmap)
                self.set_cover_to_cache(current_index_id, pixmap)
                return None

        pixmap = self.get_cover_from_cache(current_index_id)
        if pixmap.size() != widget.size():
            pixmap = pixmap.scaled(widget.size(), mode=Qt.SmoothTransformation)
        widget.setPixmap(pixmap)
