import enum
from typing import Optional

from PySide6 import QtWidgets

from apollo.src.views.delegates.track_delegate_mid import TrackDelegate_Mid
from apollo.src.views.delegates.track_delegate_small import TrackDelegate_Small
from apollo.src.views.delegates.track_delegate_small_queue import TrackDelegate_Small_Queue


class ViewDelegates(enum.Enum):
    TrackDelegate_Small = "TrackDelegate_Small"
    TrackDelegate_Small_Queue = "TrackDelegate_Small_Queue"
    TrackDelegate_Mid = "TrackDelegate_Mid"

    AlbumDelegate_Large = "AlbumDelegate_Large"
    ArtistDelegate_Large = "ArtistDelegate_Large"


def set_delegate(view: QtWidgets.QAbstractItemView, delegate: Optional[ViewDelegates] = None):
    if delegate is None:
        view.setItemDelegate(QtWidgets.QStyledItemDelegate())

    elif delegate.name == "TrackDelegate_Small":
        view.setItemDelegate(TrackDelegate_Small())

    elif delegate.name == "TrackDelegate_Mid":
        view.setItemDelegate(TrackDelegate_Mid())

    elif delegate.name == "TrackDelegate_Small_Queue":
        view.setItemDelegate(TrackDelegate_Small_Queue())

    else:
        return None
