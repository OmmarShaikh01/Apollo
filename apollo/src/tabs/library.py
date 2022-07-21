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
        menu = QtWidgets.QMenu()

        menu.addAction("Play Now")
        menu.addAction("Queue Next")
        menu.addAction("Queue Last")
        menu_1 = menu.addMenu("Play More")
        menu_1.addAction("Play All Tracks Shuffled")
        menu_1.addSeparator()
        menu_1.addAction("Play Artist")
        menu_1.addAction("Play Similar")
        menu_1.addSeparator()
        menu_1.addAction("Play Genre")
        menu.addSeparator()

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
