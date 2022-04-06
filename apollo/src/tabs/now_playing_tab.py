from PySide6 import QtCore, QtWidgets

from apollo.db.models import QueueModel, Provider
from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo
from apollo.src.playback_bar import PlayBackBar


class NowPlayingTab:

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.playback_bar_controller = PlayBackBar(ui)
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
            self.playSelected(item.row())
        ))
        # self.playback_bar_controller.Player.queuePositionChanged = lambda index: (
        #     print(index)
        # )

    def playSelected(self, row_id):
        row = self.getRowData(row_id, ['file_id'])
        self.playback_bar_controller.play_File(row[0])

    def getRowData(self, index, column: str = None) -> list[list]:
        if column is not None:
            column = [self.model.database.library_columns.index(item) for item in column]
        return [self.model.index(index, col).data() for col in column]

    def getRowModelIndex(self, index, column: str = None) -> list[list]:
        if column is not None:
            column = [self.model.database.library_columns.index(item) for item in column]
        return [self.model.index(index, col) for col in [0]]
