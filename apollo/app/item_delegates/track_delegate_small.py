import datetime
import os.path
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from apollo.app.item_delegates._base_delegate import CustomItemDelegate
from apollo.assets.app_themes import AppIcons
from apollo.media import Mediafile
from apollo.utils import get_logger


LOGGER = get_logger(__name__)


class TrackDelegate_Small(CustomItemDelegate):
    """
    Delegate class to display in Library List view
    """

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ) -> None:
        """
        Paint event invoked each time a draw call is invoked

        Args:
            painter (QtGui.QPainter): Parent widget painter
            option (QtWidgets.QStyleOptionViewItem): widget style options
            index (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): Current item index
        """
        self.draw_widget(painter, option, index)

    # pylint: disable=W0613
    def sizeHint(
        self,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ) -> QtCore.QSize:
        """
        Args:
            option (QtWidgets.QStyleOptionViewItem): widget style options
            index (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): Current item index

        Returns:
            QtCore.QSize: Qt widets size hint, that defines the display size
        """
        # noinspection PyUnresolvedReferences
        w, h = option.rect.width(), 48
        return QtCore.QSize(w, h)

    # noinspection PyUnresolvedReferences
    def draw_widget(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ) -> None:
        """
        Draws the delegate widget

        Args:
            painter (QtGui.QPainter): Parent widget painter
            option (QtWidgets.QStyleOptionViewItem): widget style options
            index (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): Current item index
        """
        pixmap = QtGui.QPixmap(option.rect.width(), option.rect.height())
        painter.save()

        # Draws widget into delegate
        s_painter = QtGui.QPainter(pixmap)
        widget = self.get_widget(option, index, option.widget)

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

    # pylint: disable=R0914,R0915
    def get_widget(
        self,
        option: QtWidgets.QStyleOptionViewItem,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> QtWidgets.QWidget:
        """
        Returns Widget to paint inplace of delegate

        Args:
            option (QtWidgets.QStyleOptionViewItem): widget style options
            index (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): Current item index
            parent (Optional[QtWidgets.QWidget]): Parent widget

        Returns:
            QtWidgets.QWidget: Widget to paint inplace of delegate
        """
        # widget creation
        TrackDelegate_Small_Frame = QtWidgets.QFrame(None)
        TrackDelegate_Small_Frame.setObjectName("TrackDelegate_Small_Frame")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TrackDelegate_Small_Frame.sizePolicy().hasHeightForWidth())
        TrackDelegate_Small_Frame.setSizePolicy(sizePolicy)
        TrackDelegate_Small_Frame.setMinimumSize(QtCore.QSize(0, 48))
        TrackDelegate_Small_Frame.setMaximumSize(QtCore.QSize(16777215, 48))
        TrackDelegate_Small_Frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        gridLayout_2 = QtWidgets.QGridLayout(TrackDelegate_Small_Frame)
        gridLayout_2.setObjectName("gridLayout_2")
        gridLayout_2.setHorizontalSpacing(6)
        gridLayout_2.setContentsMargins(2, 2, 2, 2)
        TrackDelegate_Small_album_label = QtWidgets.QLabel(TrackDelegate_Small_Frame)
        TrackDelegate_Small_album_label.setObjectName("TrackDelegate_Small_album_label")
        TrackDelegate_Small_album_label.setMinimumSize(QtCore.QSize(0, 40))
        TrackDelegate_Small_album_label.setMaximumSize(QtCore.QSize(16777215, 40))
        TrackDelegate_Small_album_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_album_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        gridLayout_2.addWidget(TrackDelegate_Small_album_label, 0, 3, 1, 1)

        TrackDelegate_Small_Cover_Pixmap = QtWidgets.QLabel(TrackDelegate_Small_Frame)
        TrackDelegate_Small_Cover_Pixmap.setObjectName("TrackDelegate_Small_Cover_Pixmap")
        TrackDelegate_Small_Cover_Pixmap.setMinimumSize(QtCore.QSize(40, 40))
        TrackDelegate_Small_Cover_Pixmap.setMaximumSize(QtCore.QSize(40, 40))
        TrackDelegate_Small_Cover_Pixmap.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_Cover_Pixmap.setAlignment(Qt.AlignCenter)

        gridLayout_2.addWidget(TrackDelegate_Small_Cover_Pixmap, 0, 1, 1, 1)

        TrackDelegate_Small_time_label = QtWidgets.QLabel(TrackDelegate_Small_Frame)
        TrackDelegate_Small_time_label.setObjectName("TrackDelegate_Small_time_label")
        TrackDelegate_Small_time_label.setMinimumSize(QtCore.QSize(64, 40))
        TrackDelegate_Small_time_label.setMaximumSize(QtCore.QSize(64, 40))
        TrackDelegate_Small_time_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_time_label.setAlignment(Qt.AlignCenter)

        gridLayout_2.addWidget(TrackDelegate_Small_time_label, 0, 5, 1, 1)

        TrackDelegate_Small_isLiked_Pixmap = QtWidgets.QLabel(TrackDelegate_Small_Frame)
        TrackDelegate_Small_isLiked_Pixmap.setObjectName("TrackDelegate_Small_isLiked_Pixmap")
        TrackDelegate_Small_isLiked_Pixmap.setMinimumSize(QtCore.QSize(24, 40))
        TrackDelegate_Small_isLiked_Pixmap.setMaximumSize(QtCore.QSize(24, 40))
        TrackDelegate_Small_isLiked_Pixmap.setFrameShape(QtWidgets.QFrame.NoFrame)

        gridLayout_2.addWidget(TrackDelegate_Small_isLiked_Pixmap, 0, 4, 1, 1)

        frame_2 = QtWidgets.QFrame(TrackDelegate_Small_Frame)
        frame_2.setObjectName("frame_2")
        frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        verticalLayout = QtWidgets.QVBoxLayout(frame_2)
        verticalLayout.setSpacing(0)
        verticalLayout.setObjectName("verticalLayout")
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        TrackDelegate_Small_title_label = QtWidgets.QLabel(frame_2)
        TrackDelegate_Small_title_label.setObjectName("TrackDelegate_Small_title_label")
        TrackDelegate_Small_title_label.setMinimumSize(QtCore.QSize(0, 24))
        TrackDelegate_Small_title_label.setMaximumSize(QtCore.QSize(16777215, 24))
        TrackDelegate_Small_title_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_title_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        verticalLayout.addWidget(TrackDelegate_Small_title_label)

        TrackDelegate_Small_artist_label = QtWidgets.QLabel(frame_2)
        TrackDelegate_Small_artist_label.setObjectName("TrackDelegate_Small_artist_label")
        TrackDelegate_Small_artist_label.setMinimumSize(QtCore.QSize(0, 16))
        TrackDelegate_Small_artist_label.setMaximumSize(QtCore.QSize(16777215, 16))
        TrackDelegate_Small_artist_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        TrackDelegate_Small_artist_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        verticalLayout.addWidget(TrackDelegate_Small_artist_label)

        gridLayout_2.addWidget(frame_2, 0, 2, 1, 1)

        gridLayout_2.setColumnStretch(2, 1)
        gridLayout_2.setColumnStretch(3, 1)

        # noinspection PyUnresolvedReferences
        TrackDelegate_Small_Frame.setGeometry(option.rect)
        TrackDelegate_Small_title_label.setFixedWidth(int(parent.width() * 0.5))
        TrackDelegate_Small_album_label.setFixedWidth(int(parent.width() * 0.2))

        # widget set data
        self._widget_set_data(
            index,
            **dict(
                TrackDelegate_Small_Cover_Pixmap=TrackDelegate_Small_Cover_Pixmap,
                TrackDelegate_Small_isLiked_Pixmap=TrackDelegate_Small_isLiked_Pixmap,
                TrackDelegate_Small_title_label=TrackDelegate_Small_title_label,
                TrackDelegate_Small_artist_label=TrackDelegate_Small_artist_label,
                TrackDelegate_Small_time_label=TrackDelegate_Small_time_label,
                TrackDelegate_Small_album_label=TrackDelegate_Small_album_label,
            ),
        )

        return TrackDelegate_Small_Frame

    # noinspection PyMethodMayBeStatic
    def _widget_set_data(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex], **kwargs
    ):
        """
        Sets relevant data passed in from kwargs to the widget

        Args:
            index (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): current item index
            **kwargs: data to set into the widget
        """
        TrackDelegate_Small_Cover_Pixmap = kwargs["TrackDelegate_Small_Cover_Pixmap"]
        TrackDelegate_Small_isLiked_Pixmap = kwargs["TrackDelegate_Small_isLiked_Pixmap"]
        TrackDelegate_Small_title_label = kwargs["TrackDelegate_Small_title_label"]
        TrackDelegate_Small_artist_label = kwargs["TrackDelegate_Small_artist_label"]
        TrackDelegate_Small_time_label = kwargs["TrackDelegate_Small_time_label"]
        TrackDelegate_Small_album_label = kwargs["TrackDelegate_Small_album_label"]

        # widget set data
        TrackDelegate_Small_Cover_Pixmap.setText("")
        self.set_cover_img(TrackDelegate_Small_Cover_Pixmap, index)

        TrackDelegate_Small_isLiked_Pixmap.setText("")
        rating = float(index.model().index(index.row(), 71).data())
        if rating == 5:
            pixmap = QtGui.QPixmap(AppIcons.FAVORITE_FILLED.primary)
            pixmap = pixmap.scaled(QtCore.QSize(24, 24), mode=Qt.SmoothTransformation)
            TrackDelegate_Small_isLiked_Pixmap.setPixmap(pixmap)
        else:
            pixmap = QtGui.QPixmap(AppIcons.FAVORITE.primary)
            pixmap = pixmap.scaled(QtCore.QSize(24, 24), mode=Qt.SmoothTransformation)
            TrackDelegate_Small_isLiked_Pixmap.setPixmap(pixmap)

        self.elide_text(
            TrackDelegate_Small_title_label, str(index.model().index(index.row(), 6).data())
        )
        self.elide_text(
            TrackDelegate_Small_artist_label, str(index.model().index(index.row(), 8).data())
        )
        self.elide_text(
            TrackDelegate_Small_album_label, str(index.model().index(index.row(), 16).data())
        )

        song_len = datetime.timedelta(seconds=float(index.model().index(index.row(), 34).data()))
        TrackDelegate_Small_time_label.setText(str(song_len).split(".", maxsplit=1)[0])

    def set_cover_img(
        self,
        widget: QtWidgets.QLabel,
        index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
    ):
        """
        Sets A cover image to a Display

        Args:
            widget (QtWidgets.QLabel): Parent widget to set image to
            index (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): current item index
        """
        current_index_id = index.model().index(index.row(), 0).data()
        if current_index_id not in self._cover_cache:
            current_index_path = index.model().index(index.row(), 1).data()
            if os.path.exists(current_index_path) and Mediafile.isSupported(current_index_path):
                # noinspection PyUnresolvedReferences
                data = Mediafile(current_index_path).Artwork[0].data
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                pixmap = pixmap.scaled(widget.size(), mode=Qt.SmoothTransformation)
                widget.setPixmap(pixmap)
                self.set_cover_to_cache(current_index_id, pixmap)
            else:
                pixmap = self.DEFAULT_COVER_ART.scaled(widget.size(), mode=Qt.SmoothTransformation)
                widget.setPixmap(pixmap)
        elif current_index_id in self._cover_cache:
            pixmap = self.get_cover_from_cache(current_index_id)
            if pixmap.size() != widget.size():
                pixmap = pixmap.scaled(widget.size(), mode=Qt.SmoothTransformation)
            widget.setPixmap(pixmap)
