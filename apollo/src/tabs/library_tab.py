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
        header = self.ui.library_tableview.horizontalHeader()
        for index in range(header.model().columnCount()):
            if header.model().headerData(index, QtCore.Qt.Horizontal) in ["File Id", "File Path"]:
                header.hideSection(index)

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

    def get_selected_rowData(self, column: str = None) -> list[list]:
        rows = set(ModelIndex.row() for ModelIndex in self.ui.library_tableview.selectedIndexes())
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

    def get_all_rowData(self, column: str = None) -> list[list]:
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
            (Provider.get_model(PlaylistsModel).create_playList('temp_playlist', ids = self.get_selected_rowData(["file_id"])))
        ))
        lv_1.addAction("File Info").triggered.connect(lambda: (
            self.display_FileInfo()
        ))
        lv_1.addSeparator()
        lv_1.addAction("Play All").triggered.connect(lambda: (
            (Provider.get_model(QueueModel).create_playList("queue", self.get_all_rowData(["file_id"])))
        ))
        lv_1.addAction("Play Selected").triggered.connect(lambda: (
            (Provider.get_model(QueueModel).create_playList("queue", self.get_selected_rowData(["file_id"])))
        ))
        lv_1.addSeparator()
        lv_1.addAction("Delete Selected")
        lv_1.addAction("Delete Selected Physically")

        # Execution
        cursor = QtGui.QCursor()
        lv_1.exec(cursor.pos())

    def add_FoldertoLibrary(self):
        text, pressed = QtWidgets.QInputDialog.getText(None, "input dialog", "Is this ok?", flags = QtCore.Qt.Dialog)
        if pressed:
            text = os.path.normpath(text)
            self.model.add_ItemFormFS(text)

    def display_FileInfo(self):
        data = self.get_selected_rowData(['file_id'])
        if len(data) >= 1:
            data = (self.model.getFileInfo(data.pop()))
            msg_bx = QtWidgets.QMessageBox()
            msg_bx.setWindowTitle("File Info")
            msg_bx.setInformativeText(f"Info About: {data.get('file_name')}")
            msg_bx.setStandardButtons(msg_bx.Ok | msg_bx.Cancel)
            msg_bx.setDefaultButton(msg_bx.Ok)
            msg_bx.setDetailedText(json.dumps(data, indent = 4))
            msg_bx.exec()
