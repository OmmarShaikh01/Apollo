from __future__ import annotations

from typing import TYPE_CHECKING, Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.app.item_delegates import ViewDelegates, set_delegate
from apollo.database.models import Model_Provider
from apollo.utils import Apollo_Generic_View, get_logger


if TYPE_CHECKING:
    from apollo.app.main import Apollo_MainWindow_UI

LOGGER = get_logger(__name__)


# disable linting warnings because local imports are defined on runtime
# pylint: disable=C0415
class Now_Playing_Tab(Apollo_Generic_View):
    """
    Now Playing Tab
    """

    def __init__(self, ui: Apollo_MainWindow_UI):
        self.UI = ui
        self.MODEL_PROVIDER = Model_Provider

        self.setup_conections()
        self.setup_defaults()

    def setup_conections(self):
        self.UI.queue_main_listview.doubleClicked.connect(
            lambda index: self._cb_list_item_clicked(index)
        )
        self.UI.queue_main_listview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.UI.queue_main_listview.customContextMenuRequested.connect(
            lambda pos: self._cb_context_menu_library_listview(pos)
        )

    def setup_defaults(self):
        self._bind_model()
        set_delegate(self.UI.queue_main_listview, ViewDelegates.TrackDelegate_Small_Queue)

    def save_states(self):
        pass

    def _bind_model(self):
        """
        Binds models with Views
        """
        from apollo.assets import AppTheme
        from apollo.assets.stylesheets import luminosity

        view = self.UI.queue_main_listview
        model = self.MODEL_PROVIDER.QueueModel()

        view.viewport().setStyleSheet(
            f"background-color: {luminosity(AppTheme['QTCOLOR_PRIMARYDARKCOLOR'], 0.125)}"
        )
        view.setModel(model)
        # noinspection PyUnresolvedReferences
        view.verticalScrollBar().valueChanged.connect(lambda x: (self._cb_scroll_paging(x)))
        model.fetch_data(model.FETCH_DATA_DOWN)

    def _cb_scroll_paging(self, value: int):
        """
        On scroll Loader for paged models
        Args:
            value (int): Scroll value
        """
        view = self.UI.queue_main_listview
        model = self.MODEL_PROVIDER.QueueModel()

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

    def _cb_list_item_clicked(self, data: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]):
        """
        Plays item on double click

        Args:
            data (Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]): query data
        """
        if data.row() != -1:
            data = self.MODEL_PROVIDER.QueueModel().index(data.row(), 1).data()
            self.MODEL_PROVIDER.QueueModel().CURRENT_FILE_ID = data
            self.UI.queue_main_listview.repaint()
            self.SIGNALS.PlayTrackSignal.emit(self.MODEL_PROVIDER.QueueModel().CURRENT_FILE_ID)

    # pylint: disable=W0612
    def _cb_context_menu_library_listview(self, pos: QtCore.QPoint):
        """
        Handles Context menu request

        Args:
            pos (Qtcore.QPoint): Pos to draw menu at
        """
        view = self.UI.queue_main_listview
        model = self.MODEL_PROVIDER.QueueModel()
        current_record = model.get_row_atIndex(view.indexAt(pos))
        menu = QtWidgets.QMenu(view)

        # Execution
        menu.exec(QtGui.QCursor.pos())

    def cb_on_search_query(self, query: str):
        """
        Filter model using search query

        Args:
            query (str): filter query
        """
        self.MODEL_PROVIDER.QueueModel().set_filter(query)
