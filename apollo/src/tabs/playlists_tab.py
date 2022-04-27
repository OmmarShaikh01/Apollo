from PySide6 import QtCore, QtGui, QtWidgets

from apollo.db.models import LibraryModel, PlaylistsModel, Provider, QueueModel
from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo
from apollo.utils import ApolloSignal, get_configparser, get_logger

LOGGER = get_logger(__name__)
CONFIG = get_configparser()


class PlaylistTab:
    SHUTDOWN = ApolloSignal()

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.setupUI()

    def setupUI(self):
        # TODO save initial states into a temporary dump
        self.setTableModel()
        self.ui.playlists_tableview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.ui.playlists_tableview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.playlists_tableview.customContextMenuRequested.connect(self.table_ContextMenu)

        self.connectLineEdit()
        self.connectTableView()
        self.connectAddedPlaylistButton()
        self.SHUTDOWN.connect(self.shutdown)

    def shutdown(self):
        LOGGER.info('SHUTDOWN')

    def setTableModel(self):
        self.model = Provider.get_model(PlaylistsModel)
        self.ui.playlists_tableview.setModel(self.model)
        self.setHeaderLabels()
        self.model.TABLE_UPDATE.connect(self.onModelUpdate)

    def onModelUpdate(self):
        self.setHeaderLabels()

    def setHeaderLabels(self):
        header = self.ui.playlists_tableview.horizontalHeader()
        for index in range(header.model().columnCount()):
            if header.model().headerData(index, QtCore.Qt.Horizontal) in ["File Id", "File Path"]:
                header.hideSection(index)

    def connectLineEdit(self):
        self.ui.playlists_tab_lineedit.returnPressed.connect(lambda: (
            self.model.search_table(self.ui.playlists_tab_lineedit.text()),
            self.setHeaderLabels()
        ))
        self.ui.playlists_tab_lineedit.textChanged.connect(lambda: (
            self.model.search_table(self.ui.playlists_tab_lineedit.text()),
            self.setHeaderLabels()
        ))
        self.ui.library_tab_search_pushbutton.pressed.connect(lambda: (
            self.model.search_table(self.ui.playlists_tab_lineedit.text()),
            self.setHeaderLabels()
        ))

    def connectAddedPlaylistButton(self):
        self.ui.playlists_tab_menu_pushbutton.pressed.connect(lambda: (
            self.avaliablePLaylists_ContextMenu()
        ))

    def avaliablePLaylists_ContextMenu(self):
        CONFIG = get_configparser()
        lv_1 = QtWidgets.QMenu()
        playlists = eval(CONFIG['DEFAULT']["playlists"])
        menu_action = (lambda name: lv_1.addAction(name).triggered.connect(lambda: (
            self.model.load_playlist(name), self.setHeaderLabels()
        )))
        for item in playlists:
            menu_action(str(item))
        # Execution
        cursor = self.ui.playlists_tab_menu_pushbutton.mapToGlobal(QtCore.QPoint(0, 0))
        cursor.setY(cursor.y() - (len(playlists) * 32))
        lv_1.exec(cursor)

    def table_ContextMenu(self):
        lv_1 = QtWidgets.QMenu()

        # adds the actions and menu related to Hide section
        lv_1.addAction("File Info").triggered.connect(lambda: (
            self.display_FileInfo()
        ))
        lv_1.addSeparator()
        lv_1.addAction("Play All").triggered.connect(lambda: (
            Provider.get_model(QueueModel).create_playList("queue", self.getRowData(["file_id"]))
        ))
        lv_1.addAction("Play Selected").triggered.connect(lambda: (
            Provider.get_model(QueueModel).create_playList("queue", self.getRowData(["file_id"], rows_selected = True))
        ))
        lv_1.addSeparator()
        lv_1.addAction("Delete Selected").triggered.connect(lambda: (
            self.model.delete_item_fromFS(self.getRowData(["file_id"], rows_selected = True))
        ))
        lv_1.addAction("Delete Selected Physically")

        # Execution
        cursor = QtGui.QCursor()
        lv_1.exec(cursor.pos())

    def connectTableView(self):
        self.ui.playlists_tableview.doubleClicked.connect(lambda item: (
            Provider.get_model(QueueModel).add_item_toqueue_top(
                    self.getRowDataAt(item.row(), ["file_id"])[0][0], self.getRowData(["file_id"])
            )
        ))

    def getRowDataAt(self, index: int, column: list[str] = None) -> list:
        if column is not None:
            column = [self.model.fields.index(item) for item in column]

        row = []
        column_data = []
        for col_index in range(self.model.columnCount()):
            if column is None:
                column_data.append(data)
            else:
                if col_index in column:
                    column_data.append(self.model.index(index, col_index).data())
        row.append(column_data)
        return row

    def getRowData(self, column: str = None, rows_selected: bool = False) -> list[list]:
        if rows_selected:
            rows = set(ModelIndex.row() for ModelIndex in self.ui.playlists_tableview.selectedIndexes())
        else:
            rows = set(range(self.model.rowCount()))

        if column is not None:
            column = [self.model.fields.index(item) for item in column]

        table = []
        column_data = []
        for row_index in rows:
            for col_index in range(self.model.columnCount()):
                if column is None:
                    column_data.append(data)
                else:
                    if col_index in column:
                        column_data.append(self.model.index(row_index, col_index).data())
            table.append(column_data)
            column_data = []
        return table

    def display_FileInfo(self):
        data = self.getRowData(['file_id'])
        if len(data) >= 1:
            data = (self.model.get_fileinfo(data.pop()))
            msg_bx = QtWidgets.QMessageBox()
            msg_bx.setWindowTitle("File Info")
            msg_bx.setInformativeText(f"Info About: {data.get('file_name')}")
            msg_bx.setStandardButtons(msg_bx.Ok | msg_bx.Cancel)
            msg_bx.setDefaultButton(msg_bx.Ok)
            msg_bx.setDetailedText(json.dumps(data, indent = 4))
            msg_bx.exec()
