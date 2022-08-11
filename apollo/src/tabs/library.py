import abc
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.assets import AppTheme
from apollo.assets.stylesheets import luminosity
from apollo.db.models import LibraryModel, ModelProvider, QueueModel
from apollo.layout.mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.src.views.delegates import ViewDelegates, set_delegate
from apollo.utils import Apollo_Main_UI_TypeStub, get_logger
from configs import settings


CONFIG = settings
LOGGER = get_logger(__name__)


class Library_Tab_Interactions(abc.ABC):
    """
    Library_Tab_Interactions
    """

    def __init__(self, ui: Apollo_Main_UI_TypeStub) -> None:
        """
        Constructor

        Args:
            ui (Union[Apollo_MainWindow, QtWidgets.QMainWindow]): UI objects
        """
        self.UI = ui
        self.setup_interactions()
        self.load_states()

    def setup_interactions(self):  # pragma: no cover
        """
        Sets up interactions
        """
        self.UI.library_main_listview.doubleClicked.connect(
            lambda index: self.cb_list_item_clicked(index)
        )
        self.UI.library_main_listview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.UI.library_main_listview.customContextMenuRequested.connect(
            lambda pos: self._cb_context_menu_library_listview(pos)
        )

    def load_states(self):  # pragma: no cover
        """
        loads session states of Apollo
        """

    def save_states(self):  # pragma: no cover
        """
        saves session states of Apollo
        """

    def _cb_context_menu_library_listview(self, pos: QtCore.QPoint):
        view = self.UI.library_main_listview
        model: LibraryModel = view.model()
        current_record = model.get_row_atIndex(view.indexAt(pos))
        menu = QtWidgets.QMenu(view)

        menu.addAction("Play Now", self.cb_play_now)
        menu.addAction("Queue Next", self.cb_queue_next)
        menu.addAction("Queue Last", self.cb_queue_last)
        menu_1 = menu.addMenu("Play More")
        menu_1.addAction("Play All Shuffled", self.cb_play_all_shuffled)
        artist_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_1.addAction(
            f'Play Artist "{artist_field}"', lambda: self.cb_play_artist(view.indexAt(pos))
        )
        album_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_1.addAction(
            f'Play Album "{album_field}"', lambda: self.cb_play_album(view.indexAt(pos))
        )
        genre_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.MOOD")]
        )
        menu_1.addAction(
            f'Play Genre "{genre_field}"', lambda: self.cb_play_genre(view.indexAt(pos))
        )
        menu_1_1 = menu_1.addMenu("Output To")
        menu_1_1.addAction(f"Primary Sound Device", self.cb_primary_sound_device)
        menu.addSeparator()

        menu.addAction("Edit", lambda: self.cb_edit(view.indexAt(pos)))
        menu_2 = menu.addMenu("Add to Playlist")
        menu_2.addAction("Add to Current Playlist", self.cb_add_to_current_playlist)
        menu_2.addAction("Add All Shuffled to Playlist", self.cb_add_all_shuffled_to_playlist)
        artist_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_2.addAction(
            f'Add Artist "{artist_field}" to Playlist',
            lambda: self.cb_add_artist_to_playlist(view.indexAt(pos)),
        )
        album_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_2.addAction(
            f'Add Album "{album_field}" to Playlist',
            lambda: self.cb_add_album_to_playlist(view.indexAt(pos)),
        )
        genre_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.MOOD")]
        )
        menu_2.addAction(
            f'Add Genre "{genre_field}" to Playlist',
            lambda: self.cb_add_genre_to_playlist(view.indexAt(pos)),
        )

        menu_3 = menu.addMenu("Rating Album")
        menu_3.addAction(f"Set Rating 5.0", lambda: self.cb_set_rating(5.0))
        menu_3.addAction(f"Set Rating 4.5", lambda: self.cb_set_rating(4.5))
        menu_3.addAction(f"Set Rating 4.0", lambda: self.cb_set_rating(4.0))
        menu_3.addAction(f"Set Rating 3.5", lambda: self.cb_set_rating(3.5))
        menu_3.addAction(f"Set Rating 3.0", lambda: self.cb_set_rating(3.0))
        menu_3.addAction(f"Set Rating 2.5", lambda: self.cb_set_rating(2.5))
        menu_3.addAction(f"Set Rating 2.0", lambda: self.cb_set_rating(2.0))
        menu_3.addAction(f"Set Rating 1.5", lambda: self.cb_set_rating(1.5))
        menu_3.addAction(f"Set Rating 1.0", lambda: self.cb_set_rating(1.0))
        menu_3.addAction(f"Set Rating 0.0", lambda: self.cb_set_rating(0))

        menu_4 = menu.addMenu("Send To")
        menu_4.addAction(f"Folder (Move)", self.cb_folder_move)
        menu_4.addAction(f"Folder (Copy)", self.cb_folder_copy)
        menu_4.addSeparator()
        menu_4.addAction(f"Format Converter", lambda: self.cb_format_converter(view.indexAt(pos)))
        menu_4.addAction(f"File Rescan", self.cb_file_rescan)

        menu.addAction("Delete", self.cb_delete)
        menu.addSeparator()

        menu_5 = menu.addMenu("Search")
        artist_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_5.addAction(
            f'Find Artist "{artist_field}"', lambda: self.cb_find_artist(view.indexAt(pos))
        )
        artist_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_5.addAction(
            f'Find Similar "{artist_field}"', lambda: self.cb_find_similar(view.indexAt(pos))
        )
        title_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.TITLE")]
        )
        menu_5.addAction(
            f'Find Title "{title_field}"', lambda: self.cb_find_title(view.indexAt(pos))
        )
        menu_5.addSeparator()
        menu_5.addAction(f"Locate in Library", lambda: self.cb_locate_in_library(view.indexAt(pos)))
        menu_5.addAction(
            f"Locate in Playlist", lambda: self.cb_locate_in_playlist(view.indexAt(pos))
        )
        menu_5.addAction(
            f"Locate in Explorer", lambda: self.cb_locate_in_explorer(view.indexAt(pos))
        )
        menu_5.addAction(
            f"Locate in Web Browser", lambda: self.cb_locate_in_web_browser(view.indexAt(pos))
        )

        # Execution
        menu.exec(QtGui.QCursor.pos())

    @abc.abstractmethod
    def cb_list_item_clicked(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_play_now(self):
        ...

    @abc.abstractmethod
    def cb_queue_next(self):
        ...

    @abc.abstractmethod
    def cb_queue_last(self):
        ...

    @abc.abstractmethod
    def cb_play_all_shuffled(self):
        ...

    @abc.abstractmethod
    def cb_play_artist(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_play_album(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_play_genre(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_primary_sound_device(self):
        ...

    @abc.abstractmethod
    def cb_edit(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_add_to_current_playlist(self):
        ...

    @abc.abstractmethod
    def cb_add_all_shuffled_to_playlist(self):
        ...

    @abc.abstractmethod
    def cb_add_artist_to_playlist(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        ...

    @abc.abstractmethod
    def cb_add_album_to_playlist(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        ...

    @abc.abstractmethod
    def cb_add_genre_to_playlist(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        ...

    @abc.abstractmethod
    def cb_set_rating(self, rating: float):
        ...

    @abc.abstractmethod
    def cb_folder_move(self):
        ...

    @abc.abstractmethod
    def cb_folder_copy(self):
        ...

    @abc.abstractmethod
    def cb_format_converter(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_file_rescan(self):
        ...

    @abc.abstractmethod
    def cb_delete(self):
        ...

    @abc.abstractmethod
    def cb_find_artist(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_find_similar(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_find_title(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_locate_in_library(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_locate_in_playlist(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_locate_in_explorer(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    @abc.abstractmethod
    def cb_locate_in_web_browser(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        ...


class Library_Tab_Controller:
    """
    Library_Tab_Controller
    """

    _DELEGATE_TYPE: str = str(ViewDelegates.TrackDelegate_Small.name)

    def __init__(self) -> None:
        """
        Constructor
        """
        self.load_states()
        self.library_model = ModelProvider.get_model(LibraryModel)
        self.queue_model = ModelProvider.get_model(QueueModel)

        self._SELECTION = []

    def bind_models(self, view: QtWidgets.QListView):
        """
        Binds models with Views

        Args:
            view (QtWidgets.QListView): view to bind models to
        """
        view.viewport().setStyleSheet(
            f"background-color: {luminosity(AppTheme['QTCOLOR_PRIMARYDARKCOLOR'], 0.125)}"
        )
        view.setModel(self.library_model)
        self.set_model_delegate(view)
        # noinspection PyUnresolvedReferences
        view.verticalScrollBar().valueChanged.connect(lambda x: (self._cb_scroll_paging(view, x)))
        self.library_model.fetch_data(self.library_model.FETCH_DATA_DOWN)

    def set_model_delegate(self, view: QtWidgets.QListView, _type: Optional[ViewDelegates] = None):
        """
        Binds models with Views

        Args:
            view (QtWidgets.QListView): view to bind models to
            _type (Optional[ViewDelegates]): Delegate type to use
        """
        if _type is None:
            _type = ViewDelegates.TrackDelegate_Small
            if self._DELEGATE_TYPE == ViewDelegates.TrackDelegate_Mid.name:
                _type = ViewDelegates.TrackDelegate_Mid

        set_delegate(view, _type)
        self._DELEGATE_TYPE = _type.name

    def save_states(self):  # pragma: no cover
        """
        saves session states of Apollo
        """
        CONFIG["APOLLO.LIBRARY_TAB.DELEGATE_TYPE"] = self._DELEGATE_TYPE

    def load_states(self):  # pragma: no cover
        """
        loads session states of Apollo
        """
        self._DELEGATE_TYPE = CONFIG.get(
            "APOLLO.LIBRARY_TAB.DELEGATE_TYPE", str(ViewDelegates.TrackDelegate_Small.name)
        )

    def _cb_scroll_paging(self, view: QtWidgets.QListView, value: int):
        """
        On scroll Loader for paged models

        Args:
            view (QtWidgets.QListView): View to get scroll event from
            value (int): Scroll value
        """

        def reset_slider():
            view.verticalScrollbarValueChanged = lambda x: None
            view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))
            view.verticalScrollbarValueChanged = lambda x: (self._cb_scroll_paging(view, x))

        if value == view.verticalScrollBar().minimum():
            if self.library_model.fetch_data(self.library_model.FETCH_DATA_UP):
                reset_slider()
        elif value == view.verticalScrollBar().maximum():
            if self.library_model.fetch_data(self.library_model.FETCH_DATA_DOWN):
                reset_slider()


class Library_Tab(Library_Tab_Interactions, Library_Tab_Controller):
    """
    Library_Tab
    """

    def __init__(self, ui: Apollo_Main_UI_TypeStub) -> None:
        self.UI = ui
        Library_Tab_Interactions.__init__(self, self.UI)
        Library_Tab_Controller.__init__(self)
        self.bind_models(self.UI.library_main_listview)

    def save_states(self):  # pragma: no cover
        """
        Shutdown callback
        """
        Library_Tab_Interactions.save_states(self)
        Library_Tab_Controller.save_states(self)

    def cb_list_item_clicked(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            self.queue_model.CURRENT_FILE_ID = data.data()
            self.UI.queue_main_listview.repaint()
            self.queue_model.play_now([data])
            self.UI.SIGNALS.PlayTrackSignal.emit(self.queue_model.CURRENT_FILE_ID)

    def cb_play_now(self):
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.queue_model.play_now(data)

    def cb_queue_next(self):
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.queue_model.queue_next(data)  # Add support for current selected index

    def cb_queue_last(self):
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.queue_model.queue_last(data)

    def cb_play_all_shuffled(self):
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            self.queue_model.play_shuffled(data)

    def cb_play_artist(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            self.queue_model.play_artist(data)

    def cb_play_album(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            self.queue_model.play_album(data)

    def cb_play_genre(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            self.queue_model.play_genre(data)

    def cb_primary_sound_device(self):
        print("cb_primary_sound_device")

    def cb_edit(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            print("cb_edit", data)

    def cb_add_to_current_playlist(self):
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            print("cb_add_to_current_playlist", data)

    def cb_add_all_shuffled_to_playlist(self):
        self.UI.library_main_listview.selectAll()
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            print("cb_add_all_shuffled_to_playlist", data)

    def cb_add_artist_to_playlist(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        data = index
        if data.row() != -1:
            print("cb_add_artist_to_playlist", data)

    def cb_add_album_to_playlist(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        data = index
        if data.row() != -1:
            print("cb_add_album_to_playlist", data)

    def cb_add_genre_to_playlist(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        data = index
        if data.row() != -1:
            print("cb_add_genre_to_playlist", data)

    def cb_set_rating(self, rating: float):
        data = self.UI.library_main_listview.selectionModel().selectedRows(0)
        if data:
            print("cb_set_rating", rating)

    def cb_folder_move(self):
        print("cb_folder_move")

    def cb_folder_copy(self):
        print("cb_folder_copy")

    def cb_format_converter(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            print("cb_format_converter", data)

    def cb_file_rescan(self):
        print("cb_file_rescan")

    def cb_delete(self):
        print("cb_delete")

    def cb_find_artist(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            print("cb_find_artist", data)

    def cb_find_similar(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            print("cb_find_similar", data)

    def cb_find_title(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            print("cb_find_title", data)

    def cb_locate_in_library(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            print("cb_locate_in_library", data)

    def cb_locate_in_playlist(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            print("cb_locate_in_playlist", data)

    def cb_locate_in_explorer(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = index
        if data.row() != -1:
            print("cb_locate_in_explorer", data)

    def cb_locate_in_web_browser(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        data = index
        if data.row() != -1:
            print("cb_locate_in_web_browser", data)
