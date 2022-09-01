import enum
from typing import Optional

from PySide6 import QtWidgets

from apollo.app.item_delegates.track_delegate_mid import TrackDelegate_Mid
from apollo.app.item_delegates.track_delegate_small import TrackDelegate_Small
from apollo.app.item_delegates.track_delegate_small_queue import TrackDelegate_Small_Queue


class ViewDelegates(enum.Enum):
    """
    Enum Class for delegates
    """

    TrackDelegate_Small = "TRACKDELEGATE_SMALL"
    TrackDelegate_Small_Queue = "TRACKDELEGATE_SMALL_QUEUE"
    TrackDelegate_Mid = "TRACKDELEGATE_MID"

    AlbumDelegate_Large = "ALBUMDELEGATE_LARGE"
    ArtistDelegate_Large = "ARTISTDELEGATE_LARGE"


def set_delegate(view: QtWidgets.QAbstractItemView, delegate: Optional[ViewDelegates] = None):
    """
    Delegate setter for views

    Args:
        view (QtWidgets.QAbstractItemView): Parent View
        delegate (Optional[ViewDelegates]): Delegate Type
    """
    if delegate is None:
        view.setItemDelegate(QtWidgets.QStyledItemDelegate())

    elif delegate.value == "TRACKDELEGATE_SMALL":
        view.setItemDelegate(TrackDelegate_Small())

    elif delegate.value == "TRACKDELEGATE_MID":
        view.setItemDelegate(TrackDelegate_Mid())

    elif delegate.value == "TRACKDELEGATE_SMALL_QUEUE":
        view.setItemDelegate(TrackDelegate_Small_Queue())
