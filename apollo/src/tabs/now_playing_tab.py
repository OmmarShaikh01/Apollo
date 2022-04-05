from PySide6 import QtCore, QtWidgets

from apollo.db.models import QueueModel, Provider
from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo


class NowPlayingTab:

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.setupUI()

    def setupUI(self):
        # TODO save initial states into a temporary dump
        self.setTableModel()
        self.ui.queue_listview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.connectLineEdit()
        self.connectTableView()

    def setTableModel(self):
        self.model = Provider.get_model(QueueModel)
        self.ui.queue_listview.setModel(self.model)
        self.ui.queue_listview.setModelColumn(self.model.database.library_columns.index('tracktitle'))

    def connectLineEdit(self):
        self.ui.playlists_tab_lineedit.returnPressed.connect(lambda: (
            self.model.searchTable(self.ui.playlists_tab_lineedit.text())
        ))
        self.ui.playlists_tab_lineedit.textChanged.connect(lambda: (
            self.model.searchTable(self.ui.playlists_tab_lineedit.text())
        ))
        self.ui.library_tab_search_pushbutton.pressed.connect(lambda: (
            self.model.searchTable(self.ui.playlists_tab_lineedit.text())
        ))

    def connectTableView(self):
        self.ui.queue_listview.doubleClicked.connect(lambda item: (
            print(self.getRowData(item.row()))
        ))

    def getRowData(self, index: int) -> list:
        return [self.model.index(index, col).data() for col in range(self.model.columnCount())]
