import abc

from PySide6 import QtWidgets

from apollo.db.models import LibraryModel, ModelProvider, QueueModel
from apollo.layout.mainwindow import Ui_MainWindow as Apollo
from apollo.src.views.delegates import ViewDelegates, set_delegate


class Library_Tab_Interactions(abc.ABC):

    def __init__(self, ui: Apollo) -> None:
        self.ui = ui
        self.setup_interactions()
        self.setup_defaults()

    def setup_interactions(self):
        pass

    def setup_defaults(self):
        pass


class Library_Tab_Controller:

    def __init__(self) -> None:
        self.library_model = ModelProvider.get_model(LibraryModel)
        self.queue_model = ModelProvider.get_model(QueueModel)

    def bind_models(self, view: QtWidgets.QAbstractItemView):
        view.setModel(self.library_model)
        set_delegate(view, ViewDelegates.TrackDelegate_Small)
        view.verticalScrollbarValueChanged = lambda x: (self.scroll_paging(view, x))
        self.library_model.fetch_data(self.library_model.FETCH_SCROLL_DOWN)

    def scroll_paging(self, view: QtWidgets.QAbstractItemView, value: int):
        if value == view.verticalScrollBar().minimum():
            if self.library_model.fetch_data(self.library_model.FETCH_SCROLL_UP):
                view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))
        if value == view.verticalScrollBar().maximum():
            if self.library_model.fetch_data(self.library_model.FETCH_SCROLL_DOWN):
                view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))


class Library_Tab(Library_Tab_Interactions, Library_Tab_Controller):  # TODO: Documentation

    def __init__(self, ui: Apollo) -> None:
        Library_Tab_Interactions.__init__(self, ui)
        Library_Tab_Controller.__init__(self)
        self.bind_models(self.ui.library_main_listview)
