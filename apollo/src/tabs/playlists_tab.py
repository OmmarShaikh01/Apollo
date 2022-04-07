from PySide6 import QtCore, QtWidgets

from apollo.db.models import PlaylistsModel, Provider
from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo
from apollo.utils import getConfigParser

CONFIG = getConfigParser()


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
        self.connectAddedPlaylistButton()

    def setTableModel(self):
        self.model = Provider.get_model(PlaylistsModel)
        self.ui.playlists_tableview.setModel(self.model)
        self.setHeaderLabels()

    def setHeaderLabels(self):
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

    def connectAddedPlaylistButton(self):
        self.ui.playlists_tab_menu_pushbutton.pressed.connect(lambda: (
            self.avaliablePLaylists_ContextMenu()
        ))

    def avaliablePLaylists_ContextMenu(self):
        lv_1 = QtWidgets.QMenu()
        playlists = eval(CONFIG['DEFAULT']["playlists"])
        menu_action = (lambda name: lv_1.addAction(name).triggered.connect(lambda: (
            self.model.loadPlaylist(name), self.setHeaderLabels()
        )))
        for item in playlists:
            menu_action(str(item))
        # Execution
        cursor = self.ui.playlists_tab_menu_pushbutton.mapToGlobal(QtCore.QPoint(0, 0))
        print(cursor)
        cursor.setY(cursor.y() - (len(playlists) * 32))
        print(cursor)
        lv_1.exec(cursor)

    def connectTableView(self):
        self.ui.playlists_tableview.doubleClicked.connect(lambda item: (
            print(self.getRowData(item.row()))
        ))

    def getRowData(self, index: int) -> list:
        return [self.model.index(index, col).data() for col in range(self.model.columnCount())]
