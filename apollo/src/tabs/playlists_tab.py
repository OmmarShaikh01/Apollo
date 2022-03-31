from PySide6 import QtCore, QtWidgets

from apollo.db.models import PlaylistsModel, Provider
from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo


class PlaylistTab:

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.setupUI()

    def setupUI(self):
        # TODO save initial states into a temporary dump
        self.setTableModel()
        self.ui.playlists_tableview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.connectLineEdit()
        self.connectTableView()

    def setTableModel(self):
        self.model = Provider.get_model(PlaylistsModel)
        self.ui.playlists_tableview.setModel(self.model)
        header = self.ui.playlists_tableview.horizontalHeader()
        for index in range(header.model().columnCount()):
            if header.model().headerData(index, QtCore.Qt.Horizontal) in ["File Id", "File Path"]:
                header.hideSection(index)

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
        self.ui.playlists_tableview.doubleClicked.connect(lambda item: (
            print(self.getRowData(item.row()))
        ))

    def getRowData(self, index: int) -> list:
        return [self.model.index(index, col).data() for col in range(self.model.columnCount())]
