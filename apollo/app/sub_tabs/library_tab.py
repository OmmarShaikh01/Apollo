"""
KNOWN BUGS:
1. Cant select delegates on the view when first launch
    Replication: Launch Apollo > Select at the end of List Item
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.app.item_delegates import ViewDelegates, set_delegate
from apollo.database.models import Model_Provider
from apollo.utils import Apollo_Generic_View, get_logger
from configs import settings as CONFIG


if TYPE_CHECKING:
    from apollo.app.main import Apollo_MainWindow_UI

LOGGER = get_logger(__name__)


class Library_Tab(Apollo_Generic_View):
    """
    Library Tab
    """

    _DELEGATE_TYPE = CONFIG.get(
        "APOLLO.LIBRARY_TAB.DELEGATE_TYPE", str(ViewDelegates.TrackDelegate_Small.value)
    )

    def __init__(self, ui: Apollo_MainWindow_UI):
        self.UI = ui
        self.MODEL_PROVIDER = Model_Provider

        self.setup_conections()
        self.setup_defaults()

    def setup_conections(self):
        self.UI.library_main_listview.doubleClicked.connect(
            lambda index: self._cb_list_item_clicked(index)
        )
        self.UI.library_main_listview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.UI.library_main_listview.customContextMenuRequested.connect(
            lambda pos: self._cb_context_menu_library_listview(pos)
        )

    def setup_defaults(self):
        self._bind_model()
        self.set_model_delegate(self._DELEGATE_TYPE)

    def save_states(self):
        CONFIG["APOLLO.LIBRARY_TAB.DELEGATE_TYPE"] = self._DELEGATE_TYPE

    # pylint: disable=C0415
    def _bind_model(self):
        """
        Binds models with Views
        """
        from apollo.assets import AppTheme
        from apollo.assets.stylesheets import luminosity

        view = self.UI.library_main_listview
        model = self.MODEL_PROVIDER.LibraryModel()

        view.viewport().setStyleSheet(
            f"background-color: {luminosity(AppTheme['QTCOLOR_PRIMARYDARKCOLOR'], 0.125)}"
        )
        view.setModel(model)
        # noinspection PyUnresolvedReferences
        view.verticalScrollBar().valueChanged.connect(lambda x: (self._cb_scroll_paging(x)))
        model.fetch_data(model.FETCH_DATA_DOWN)

    def set_model_delegate(self, _type: Optional[ViewDelegates, str] = None):
        """
        Binds models with Views
        Args:
            _type (Optional[ViewDelegates]): Delegate type to use
        """
        if isinstance(_type, str):
            if _type.upper() == "TRACKDELEGATE_SMALL":
                _type = ViewDelegates.TrackDelegate_Small
            elif _type.upper() == "TRACKDELEGATE_MID":
                _type = ViewDelegates.TrackDelegate_Mid
            elif _type.upper() == "TRACKDELEGATE_SMALL_QUEUE":
                _type = ViewDelegates.TrackDelegate_Small_Queue

        elif _type is None:
            _type = ViewDelegates.TrackDelegate_Small
            if self._DELEGATE_TYPE == ViewDelegates.TrackDelegate_Mid.name:
                _type = ViewDelegates.TrackDelegate_Mid

        set_delegate(self.UI.library_main_listview, _type)
        self._DELEGATE_TYPE = _type.name

    def _cb_scroll_paging(self, value: int):
        """
        On scroll Loader for paged models
        Args:
            value (int): Scroll value
        """
        view = self.UI.library_main_listview
        model = self.MODEL_PROVIDER.LibraryModel()

        def reset_slider():
            view.verticalScrollBar().valueChanged.connect(lambda x: None)
            view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))
            view.verticalScrollBar().valueChanged.connect(lambda x: (self._cb_scroll_paging(x)))

        if value == view.verticalScrollBar().minimum():
            if model.fetch_data(model.FETCH_DATA_UP):
                reset_slider()
        elif value == view.verticalScrollBar().maximum():
            if model.fetch_data(model.FETCH_DATA_DOWN):
                reset_slider()

    def _cb_context_menu_library_listview(self, pos: QtCore.QPoint):
        """
        Handles Context menu request

        Args:
            pos (Qtcore.QPoint): Pos to draw menu at
        """

        def get_field(col: str) -> str:
            """
            Get field of the selected row

            Args:
                col (str): column name

            Returns:
                str: data that is at column
            """
            value = (
                ""
                if len(current_record.records[0]) == 0
                else current_record.records[0][current_record.fields.index(col)]
            )
            max_len = 20
            value = f"{value[:max_len]}..." if len(value) > max_len else value
            value = f"'{value}'" if value else ""
            return value

        view = self.UI.library_main_listview
        model = self.MODEL_PROVIDER.LibraryModel()
        current_record = model.get_row_atIndex(view.indexAt(pos))
        menu = QtWidgets.QMenu(view)

        # Menu Defination
        menu.addAction("Play Now", self._cb_play_now)
        menu.addAction("Queue Next", self._cb_queue_next)
        menu.addAction("Queue Last", self._cb_queue_last)
        menu_1 = menu.addMenu("Play More")
        menu_1.addAction(
            f"Play Artist {get_field('library.ARTIST')}",
            lambda: (self._cb_play_artist(view.indexAt(pos))),
        )
        menu_1.addAction(
            f"Play Album {get_field('library.ALBUM')}",
            lambda: (self._cb_play_album(view.indexAt(pos))),
        )
        menu_1.addAction(
            f"Play Genre {get_field('library.MOOD')}",
            lambda: (self._cb_play_genre(view.indexAt(pos))),
        )
        menu_1.addAction("Play Shuffled", self._cb_play_shuffled)
        menu_1.addAction("Play All Shuffled", self._cb_play_all_shuffled)
        menu.addSeparator()

        menu_2 = menu.addMenu("Set Rating")
        menu_2.addAction("Set Rating 0.0", lambda: self._cb_update_track_rating(0))
        menu_2.addAction("Set Rating 1.0", lambda: self._cb_update_track_rating(1))
        menu_2.addAction("Set Rating 2.0", lambda: self._cb_update_track_rating(2))
        menu_2.addAction("Set Rating 3.0", lambda: self._cb_update_track_rating(3))
        menu_2.addAction("Set Rating 4.0", lambda: self._cb_update_track_rating(4))
        menu_2.addAction("Set Rating 5.0", lambda: self._cb_update_track_rating(5))

        menu.addSeparator()
        menu_3 = menu.addMenu("Search")
        menu_3.addAction(
            "Locate in Explorer",
            lambda: self._cb_locate_in_explorer(view.indexAt(pos)),
        )
        menu_3.addAction(
            "Locate in Web Browser",
            lambda: self._cb_locate_in_web_browser(view.indexAt(pos)),
        )

        # Execution
        menu.exec(QtGui.QCursor.pos())

    def _cb_list_item_clicked(self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        """
        Plays item on double click

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1:
            self.MODEL_PROVIDER.QueueModel().play_now([data])
            self.play_top_track()

    def cb_on_search_query(self, query: str):
        """
        Filter model using search query

        Args:
            query (str): filter query
        """
        self.MODEL_PROVIDER.LibraryModel().set_filter(query)

    def _cb_play_now(self):
        """
        Plays selected tracks
        """
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.MODEL_PROVIDER.QueueModel().play_now(data)
            self.play_top_track()

    def _cb_queue_next(self):
        """
        Queues selected tracks after current track
        """
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.MODEL_PROVIDER.QueueModel().queue_next(data)
            self.play_top_track()

    def _cb_queue_last(self):
        """
        Queues selected tracks at the end of the queue
        """
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.MODEL_PROVIDER.QueueModel().queue_last(data)
            self.play_top_track()

    def _cb_play_artist(self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        """
        Plays selected track, using artist

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1:
            self.MODEL_PROVIDER.QueueModel().play_artist(data)
            self.play_top_track()

    def _cb_play_album(self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        """
        Plays selected track, using album

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1:
            self.MODEL_PROVIDER.QueueModel().play_album(data)
            self.play_top_track()

    def _cb_play_genre(self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        """
        Plays selected track, using genre

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1:
            self.MODEL_PROVIDER.QueueModel().play_genre(data)
            self.play_top_track()

    def _cb_play_shuffled(self):
        """
        Plays selected tracks, as shuffled
        """
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.MODEL_PROVIDER.QueueModel().play_shuffled(data)
            self.play_top_track()

    def _cb_play_all_shuffled(self):
        """
        Plays selected tracks, as all shuffled
        """
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.MODEL_PROVIDER.QueueModel().play_shuffled()
            self.play_top_track()

    def _cb_update_track_rating(self, rating: float):
        """
        Updates the rating information of selected tracks

        Args:
            rating (float): rating information
        """
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.MODEL_PROVIDER.LibraryModel().update_track_rating(rating, data)

    def _cb_find_artist(self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        """
        Locates track in Library Table, using artist

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1 and data.data():
            self.MODEL_PROVIDER.LibraryModel().search_artist(data.data())

    def _cb_find_similar(self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        """
        Locates track in Library Table, using media similarity

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1 and data.data():
            self.MODEL_PROVIDER.LibraryModel().set_filter(data.data())

    def _cb_find_title(self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        """
        Locates track in Library Table, using title

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1 and data.data():
            self.MODEL_PROVIDER.LibraryModel().search_title(data.data())

    # pylint: disable=W0511
    def _cb_locate_in_explorer(self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        """
        Locates track in Windows file explorer

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1:
            # TODO: Implementation
            LOGGER.info("Implementation Required")

    # pylint: disable=W0511
    def _cb_locate_in_web_browser(
        self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        """
        Locates track using a web query

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1:
            # TODO: Implementation
            LOGGER.info("Implementation Required")

    def play_top_track(self):
        """
        Starts Playing the top Track from the Queue
        """
        model = self.MODEL_PROVIDER.QueueModel()
        model.CURRENT_FILE_ID = model.index(0, 1).data()
        self.UI.queue_main_listview.repaint()
        self.SIGNALS.PlayTrackSignal.emit(model.CURRENT_FILE_ID)
