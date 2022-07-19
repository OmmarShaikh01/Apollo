import abc
from typing import Optional, Union

from PySide6 import QtCore, QtWidgets

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
            lambda index: self.call_on_list_item_clicked(index)
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
    def call_on_list_item_clicked(
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

    def bind_models(self, view: QtWidgets.QListView):
        """
        Binds models with Views

        Args:
            view (QtWidgets.QListView): view to bind models to
        """
        view.setModel(self.library_model)
        self.set_model_delegate(view)
        view.verticalScrollbarValueChanged = lambda x: (self.call_on_scroll_paging(view, x))
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

    def call_on_scroll_paging(self, view: QtWidgets.QListView, value: int):
        """
        On scroll Loader for paged models

        Args:
            view (QtWidgets.QListView): View to get scroll event from
            value (int): Scroll value
        """

        def reset_slider():
            view.verticalScrollbarValueChanged = lambda x: None
            view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))
            view.verticalScrollbarValueChanged = lambda x: (self.call_on_scroll_paging(view, x))

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

    def call_on_shutdown(self):  # pragma: no cover
        """
        Shutdown callback
        """
        self.save_states()

    def call_on_list_item_clicked(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        data = self.library_model.get_row_atIndex(index)
