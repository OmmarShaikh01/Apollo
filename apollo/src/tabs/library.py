import abc
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.db.models import LibraryModel, ModelProvider, QueueModel
from apollo.layout.mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.src.views.delegates import ViewDelegates, set_delegate
from apollo.utils import get_logger
from configs import settings


CONFIG = settings
LOGGER = get_logger(__name__)


class Library_Tab_Interactions(abc.ABC):
    """
    Library_Tab_Interactions
    """

    def __init__(self, ui: Union[Apollo_MainWindow, QtWidgets.QMainWindow]) -> None:
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
            lambda pos: self.cb_context_menu_library_listview(pos)
        )

    def load_states(self):  # pragma: no cover
        """
        loads session states of Apollo
        """

    def save_states(self):  # pragma: no cover
        """
        saves session states of Apollo
        """

    @abc.abstractmethod
    def cb_list_item_clicked(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        ...

    def cb_context_menu_library_listview(self, pos: QtCore.QPoint):
        view = self.UI.library_main_listview
        model: LibraryModel = view.model()
        current_record = model.get_row_atIndex(view.indexAt(pos))
        menu = QtWidgets.QMenu(view)

        menu.addAction("Play Now")  # TODO: Implement Callback
        menu.addAction("Queue Next")  # TODO: Implement Callback
        menu.addAction("Queue Last")  # TODO: Implement Callback
        menu_1 = menu.addMenu("Play More")
        menu_1.addAction("Play All Shuffled")  # TODO: Implement Callback
        artist_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_1.addAction(f'Play Artist "{artist_field}"')  # TODO: Implement Callback
        album_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_1.addAction(f'Play Album "{album_field}"')  # TODO: Implement Callback
        genre_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.MOOD")]
        )
        menu_1.addAction(f'Play Genre "{genre_field}"')  # TODO: Implement Callback
        menu_1_1 = menu_1.addMenu("Output To")
        menu_1_1.addAction(f"Primary Sound Device")  # TODO: Implement Callback
        menu.addSeparator()

        menu.addAction("Edit")  # TODO: Implement Callback
        menu_2 = menu.addMenu("Add to Playlist")
        menu_2.addAction("Add to Current Playlist")  # TODO: Implement Callback
        menu_2.addAction("Add All Shuffled to Playlist")  # TODO: Implement Callback
        artist_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_2.addAction(f'Add Artist "{artist_field}" to Playlist')  # TODO: Implement Callback
        album_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_2.addAction(f'Add Album "{album_field}" to Playlist')  # TODO: Implement Callback
        genre_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.MOOD")]
        )
        menu_2.addAction(f'Add Genre "{genre_field}" to Playlist')  # TODO: Implement Callback

        menu_3 = menu.addMenu("Rating Album")
        menu_3.addAction(f"Set Rating 5.0")  # TODO: Implement Callback
        menu_3.addAction(f"Set Rating 4.5")  # TODO: Implement Callback
        menu_3.addAction(f"Set Rating 4.0")  # TODO: Implement Callback
        menu_3.addAction(f"Set Rating 3.5")  # TODO: Implement Callback
        menu_3.addAction(f"Set Rating 3.0")  # TODO: Implement Callback
        menu_3.addAction(f"Set Rating 2.5")  # TODO: Implement Callback
        menu_3.addAction(f"Set Rating 2.0")  # TODO: Implement Callback
        menu_3.addAction(f"Set Rating 1.5")  # TODO: Implement Callback
        menu_3.addAction(f"Set Rating 1.0")  # TODO: Implement Callback
        menu_3.addAction(f"Set Rating 0.0")  # TODO: Implement Callback

        menu_4 = menu.addMenu("Send To")
        menu_4.addAction(f"Folder (Move)")  # TODO: Implement Callback
        menu_4.addAction(f"Folder (Copy)")  # TODO: Implement Callback
        menu_4.addSeparator()
        menu_4.addAction(f"Format Converter")  # TODO: Implement Callback
        menu_4.addAction(f"File Rescan")  # TODO: Implement Callback

        menu.addAction("Delete")  # TODO: Implement Callback
        menu.addSeparator()

        menu_5 = menu.addMenu("Search")
        artist_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_5.addAction(f'Find Artist "{artist_field}"')  # TODO: Implement Callback
        artist_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.ARTIST")]
        )
        menu_5.addAction(f'Find Similar "{artist_field}"')  # TODO: Implement Callback
        title_field = (
            ""
            if len(current_record.records[0]) == 0
            else current_record.records[0][current_record.fields.index("library.TITLE")]
        )
        menu_5.addAction(f'Find Title "{title_field}"')  # TODO: Implement Callback
        menu_5.addSeparator()
        menu_5.addAction(f"Locate in Library")  # TODO: Implement Callback
        menu_5.addAction(f"Locate in Playlist")  # TODO: Implement Callback
        menu_5.addAction(f"Locate in Explorer")  # TODO: Implement Callback
        menu_5.addAction(f"Locate in Web Browser")  # TODO: Implement Callback

        # Execution
        menu.exec(self.UI.library_main_listview.mapToGlobal(pos))


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

    def bind_models(self, view: QtWidgets.QListView):
        """
        Binds models with Views

        Args:
            view (QtWidgets.QListView): view to bind models to
        """
        view.setModel(self.library_model)

        self.set_model_delegate(view)
        view.verticalScrollbarValueChanged = lambda x: (self.cb_scroll_paging(view, x))
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

    def cb_scroll_paging(self, view: QtWidgets.QListView, value: int):
        """
        On scroll Loader for paged models

        Args:
            view (QtWidgets.QListView): View to get scroll event from
            value (int): Scroll value
        """

        def reset_slider():
            view.verticalScrollbarValueChanged = lambda x: None
            view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))
            view.verticalScrollbarValueChanged = lambda x: (self.cb_scroll_paging(view, x))

        # remeber selection

        if value == view.verticalScrollBar().minimum():
            if self.library_model.fetch_data(self.library_model.FETCH_DATA_UP):
                reset_slider()
        elif value == view.verticalScrollBar().maximum():
            if self.library_model.fetch_data(self.library_model.FETCH_DATA_DOWN):
                reset_slider()

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


class Library_Tab(Library_Tab_Interactions, Library_Tab_Controller):
    """
    Library_Tab
    """

    def __init__(self, ui: Union[Apollo_MainWindow, QtWidgets.QMainWindow]) -> None:
        self.UI = ui
        Library_Tab_Interactions.__init__(self, self.UI)
        Library_Tab_Controller.__init__(self)
        self.bind_models(self.UI.library_main_listview)

    def save_states(self):  # pragma: no cover
        """
        saves session states of Apollo
        """
        Library_Tab_Interactions.save_states(self)
        Library_Tab_Controller.save_states(self)

    def cb_shutdown(self):  # pragma: no cover
        """
        Shutdown callback
        """
        self.save_states()

    def cb_list_item_clicked(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        data = self.library_model.get_row_atIndex(index)
