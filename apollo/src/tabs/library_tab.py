import json
import os.path

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.db.models import LibraryModel, PlaylistsModel, Provider, QueueModel
from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo


class LibraryTab:

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.setupUI()

    def setupUI(self):
        # TODO save initial states into a temporary dump
        self.setTableModel()
        self.ui.library_tableview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.ui.library_tableview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.library_tableview.customContextMenuRequested.connect(self.table_ContextMenu)

        self.connectLineEdit()
        self.connectTableView()

    def setTableModel(self):
        self.model = Provider.get_model(LibraryModel)
        self.ui.library_tableview.setModel(self.model)
        self.setHeaderLabels()

    def onModelUpdate(self):
        self.setHeaderLabels()
        Provider.get_model(QueueModel).fetch_records()
        Provider.get_model(QueueModel).TABLE_UPDATE.emit()
        Provider.get_model(PlaylistsModel).fetch_records()
        Provider.get_model(PlaylistsModel).TABLE_UPDATE.emit()

    def setHeaderLabels(self):
        header = self.ui.library_tableview.horizontalHeader()
        for index in range(header.model().columnCount()):
            if header.model().headerData(index, QtCore.Qt.Horizontal) in ["File Id", "File Path"]:
                header.hideSection(index)

    def connectLineEdit(self):
        self.ui.library_tab_lineedit.returnPressed.connect(lambda: (
            self.model.search_table(self.ui.library_tab_lineedit.text()),
            self.setHeaderLabels()
        ))
        self.ui.library_tab_lineedit.textChanged.connect(lambda: (
            self.model.search_table(self.ui.library_tab_lineedit.text()),
            self.setHeaderLabels()
        ))
        self.ui.library_tab_search_pushbutton.pressed.connect(lambda: (
            self.model.search_table(self.ui.library_tab_lineedit.text()),
            self.setHeaderLabels()
        ))

    def connectTableView(self):
        self.ui.library_tableview.doubleClicked.connect(lambda item: (
            Provider.get_model(QueueModel).add_item_toqueue_top(
                self.getRowDataAt(item.row(), ["file_id"])[0][0], self.getRowData(["file_id"])
            )
        ))
        self.model.TABLE_UPDATE.connect(self.onModelUpdate)

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
            rows = set(ModelIndex.row() for ModelIndex in self.ui.library_tableview.selectedIndexes())
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

    def table_ContextMenu(self):
        lv_1 = QtWidgets.QMenu()

        # adds the actions and menu related to Hide section
        lv_1.addAction("Add Folder/File").triggered.connect(lambda: (
            self.add_FoldertoLibrary()
        ))
        lv_1.addAction("Add Selected to Playlist").triggered.connect(lambda: (
            self.add_ToPlaylist()
        ))
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

    def add_FoldertoLibrary(self):
        text, pressed = QtWidgets.QInputDialog.getText(None, "Add Folder/File", "Path:", flags = QtCore.Qt.Dialog)
        if pressed:
            text = os.path.normpath(text)
            self.model.add_itemfrom_FS(text)
            self.setHeaderLabels()

    def add_ToPlaylist(self):
        text, pressed = QtWidgets.QInputDialog.getText(None, "Add To Playlist", "Playlist name:", flags = QtCore.Qt.Dialog)
        if pressed and text != '':
            Provider.get_model(PlaylistsModel).create_playList(text, ids = self.getRowData(["file_id"], rows_selected = True))

    def display_FileInfo(self):
        data = self.get_selected_rowData(['file_id'])
        if len(data) >= 1:
            data = (self.model.get_fileinfo(data.pop()))
            msg_bx = QtWidgets.QMessageBox()
            msg_bx.setWindowTitle("File Info")
            msg_bx.setInformativeText(f"Info About: {data.get('file_name')}")
            msg_bx.setStandardButtons(msg_bx.Ok | msg_bx.Cancel)
            msg_bx.setDefaultButton(msg_bx.Ok)
            msg_bx.setDetailedText(json.dumps(data, indent = 4))
            msg_bx.exec()
