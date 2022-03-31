from PySide6 import QtWidgets

from apollo.db.models.library import LibraryModel
from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo


class NowPlayingTab:

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        # self.setupUI()

    def setupUI(self):
        # TODO save initial states into a temporary dump
        self.model = LibraryModel()

        self.ui.library_tableview.setModel(self.model)
        self.ui.playlists_tableview.setModel(self.model)
        self.ui.library_tableview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.connectLineEdit()
        self.connectTableView()

    def connectLineEdit(self):
        self.ui.library_tab_lineedit.returnPressed.connect(lambda: (
            self.model.searchTable(self.ui.library_tab_lineedit.text())
        ))
        self.ui.library_tab_lineedit.textChanged.connect(lambda: (
            self.model.searchTable(self.ui.library_tab_lineedit.text())
        ))
        self.ui.library_tab_search_pushbutton.pressed.connect(lambda: (
            self.model.searchTable(self.ui.library_tab_lineedit.text())
        ))

    def connectTableView(self):
        self.ui.library_tableview.doubleClicked.connect(lambda item: (
            print(self.getRowData(item.row()))
        ))

    def getRowData(self, index: int) -> list:
        return [self.model.index(index, col).data() for col in range(self.model.columnCount())]
