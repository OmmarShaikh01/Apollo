import abc
from typing import Optional

from PySide6 import QtWidgets

from apollo.db.models import LibraryModel, ModelProvider, QueueModel
from apollo.layout.mainwindow import Ui_MainWindow as Apollo
from apollo.src.views.delegates import ViewDelegates, set_delegate
from apollo.utils import get_logger
from configs import settings


CONFIG = settings
LOGGER = get_logger(__name__)


class Library_Tab_Interactions(abc.ABC):
    """
    Library_Tab_Interactions
    """

    def __init__(self, ui: Apollo) -> None:
        """
        Constructor

        Args:
            ui (Apollo): UI objects
        """
        self.ui = ui
        self.setup_interactions()
        self.setup_defaults()

    def setup_interactions(self):
        """
        Sets up interactions
        """

    def setup_defaults(self):
        """
        Sets up default states
        """
        pass

    def save_states(self):
        """
        saves session states of Apollo
        """
        pass

    @abc.abstractmethod
    def call_on_shutdown(self):
        ...


class Library_Tab_Controller:
    """
    Library_Tab_Controller
    """

    _DELEGATE_TYPE = CONFIG.get(
        "APOLLO.LIBRARY_TAB.DELEGATE_TYPE", ViewDelegates.TrackDelegate_Mid.name
    )

    def __init__(self) -> None:
        """
        Constructor
        """
        self.library_model = ModelProvider.get_model(LibraryModel)
        self.queue_model = ModelProvider.get_model(QueueModel)

    def bind_models(self, view: QtWidgets.QAbstractItemView):
        """
        Binds models with Views

        Args:
            view (QtWidgets.QAbstractItemView): view to bind models to
        """
        view.setModel(self.library_model)
        self.set_model_delegate(view)
        view.verticalScrollbarValueChanged = lambda x: (self.scroll_paging(view, x))
        self.library_model.fetch_data(self.library_model.FETCH_DATA_DOWN)

    def set_model_delegate(
        self, view: QtWidgets.QAbstractItemView, _type: Optional[ViewDelegates] = None
    ):
        """
        Binds models with Views

        Args:
            view (QtWidgets.QAbstractItemView): view to bind models to
            _type (Optional[ViewDelegates]): Delegate type to use
        """
        if _type is not None:
            set_delegate(view, _type)
            self._DELEGATE_TYPE = _type.name
        else:
            if self._DELEGATE_TYPE == "TrackDelegate_Small":
                set_delegate(view, ViewDelegates.TrackDelegate_Small)
            elif self._DELEGATE_TYPE == "TrackDelegate_Mid":
                set_delegate(view, ViewDelegates.TrackDelegate_Mid)
            else:
                return None

    def scroll_paging(self, view: QtWidgets.QAbstractItemView, value: int):
        """
        On scroll Loader for paged models

        Args:
            view (QtWidgets.QAbstractItemView): View to get scroll event from
            value (int): Scroll value
        """
        if value == view.verticalScrollBar().minimum():
            if self.library_model.fetch_data(self.library_model.FETCH_DATA_UP):
                view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))
        if value == view.verticalScrollBar().maximum():
            if self.library_model.fetch_data(self.library_model.FETCH_DATA_DOWN):
                view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))

    def save_states(self):
        """
        saves session states of Apollo
        """
        CONFIG["APOLLO.LIBRARY_TAB.DELEGATE_TYPE"] = self._DELEGATE_TYPE


class Library_Tab(Library_Tab_Interactions, Library_Tab_Controller):  # TODO: Documentation
    """
    Library_Tab
    """

    def __init__(self, ui: Apollo) -> None:
        Library_Tab_Interactions.__init__(self, ui)
        Library_Tab_Controller.__init__(self)
        self.bind_models(self.ui.library_main_listview)

    def shutdown(self):
        """
        Shutdown callback
        """
        self.call_on_shutdown()
        Library_Tab_Interactions.save_states(self)
        Library_Tab_Controller.save_states(self)

    def call_on_shutdown(self):
        """
        Shutdown callback
        """
        LOGGER.debug("SHUTDOWN")

    def call_on_search(self):
        if self.ui.main_tabs_stack_widget.currentIndex() == 0:
            self.library_model.set_filter(self.ui.search_lineEdit.text())

    def call_on_clear_search(self):
        if self.ui.main_tabs_stack_widget.currentIndex() == 0:
            self.library_model.clear_filter()
