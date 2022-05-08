import os
from typing import Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.db.models import LibraryModel, Provider, QueueModel
from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo
from apollo.utils import ApolloSignal, get_configparser, get_logger

LOGGER = get_logger(__name__)
CONFIG = get_configparser()


def placeholder(*args, **kwargs):
    print(args, kwargs)


class LibraryTab:
    """
    Library tab controller, manages all the UX related functions.
    """
    SHUTDOWN = ApolloSignal()

    def __init__(self, ui: Union[Apollo, QtWidgets.QMainWindow]) -> None:
        """
        Constructor

        Args:
            ui (Apollo): Apollo UI Mainwindow
        """
        super().__init__()
        self.ui = ui
        self.init_viewmodels()
        self.setupUI()

    def setupUI(self):
        """
        Sets up tu UI and connects all the functions and signals
        """
        self.SHUTDOWN.connect(self.shutdown)
        self.connectLineEdit()
        self.connectTableView()

        # call startup after all objects are created and started up
        self.startup()

    def shutdown(self):
        """On application shutdown calls all the destructors and saves session state"""
        LOGGER.info('SHUTDOWN')

    def startup(self):
        """On application startup calls all the constructor and loads session state"""
        LOGGER.info('STARTUP')

    # noinspection PyAttributeOutsideInit
    def init_viewmodels(self):
        """initializes the model for the main tableview"""
        self.main_model = Provider.get_model(LibraryModel)
        self.queue_model = Provider.get_model(QueueModel)
        # TODO:
        # self.playlist_model = Provider.get_model(PlaylistsModel)

        self.ui.library_tableview.setModel(self.main_model)
        self.ui.library_tableview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.library_tableview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.library_tableview.customContextMenuRequested.connect(self.table_ContextMenu)
        self.setHeaderLabels()

    def setHeaderLabels(self):
        """sets up the header view for the primary tableview"""
        header = self.ui.library_tableview.horizontalHeader()
        for index in range(header.model().columnCount()):
            item = header.model().headerData(index, QtCore.Qt.Horizontal)
            if str(item).lower().replace(" ", "_") in ['file_id', 'file_path']:
                header.hideSection(index)

    def onModelUpdate(self):
        self.setHeaderLabels()
        self.queue_model.fetch_records()
        self.queue_model.TABLE_UPDATE.emit()
        # TODO:
        # self.playlist_model.fetch_records()
        # self.playlist_model.TABLE_UPDATE.emit()

    def connectLineEdit(self):
        """connects callbacks to the line edit"""

        def query_model():
            """
            queries and filters the library model for any str from the line_edit
            """
            self.main_model.search_table(self.ui.library_tab_lineedit.text()),
            self.setHeaderLabels()

        self.ui.library_tab_lineedit.returnPressed.connect(query_model)
        self.ui.library_tab_lineedit.textChanged.connect(query_model)
        self.ui.library_tab_search_pushbutton.pressed.connect(query_model)

    def connectTableView(self):
        """connects callbacks to the table view"""

        # is triggerd when an item is double-clicked
        self.ui.library_tableview.doubleClicked.connect(lambda item: (
            placeholder(  # TODO
                first = self.getRowDataAt(item.row(), ["file_id"])[0][0],
                remaining = self.getRowData(["file_id"], rows_selected = False)
            )
        ))

        # connects the database table signal
        self.main_model.TABLE_UPDATE.connect(self.onModelUpdate)

    def getRowDataAt(self, index: int, column: list[str] = None) -> list[list]:
        """
        Gets row data at given index

        Args:
            index (int): index of the row to fetch data from
            column (list[str]): columns to get data for

        Returns:
            list[list]: returns data
        """
        if column is not None:
            column = [self.main_model.fields.index(item) for item in column]

        row = []
        column_data = []
        for col_index in range(self.main_model.columnCount()):
            if column is None:
                column_data.append(self.main_model.index(index, col_index).data())
            else:
                if col_index in column:
                    column_data.append(self.main_model.index(index, col_index).data())
        row.append(column_data)
        return row

    def getRowData(self, column: list[str] = None, rows_selected: bool = True) -> list[list]:
        """
        Gets row data in a table format

        Args:
            column (list[str]): columns to get data for
            rows_selected (bool): to get only selected rows

        Returns:
            list[list]: returns data
        """
        if rows_selected:
            rows = set(ModelIndex.row() for ModelIndex in self.ui.library_tableview.selectedIndexes())
        else:
            rows = set(range(self.main_model.rowCount()))

        if column is not None:
            column = [self.main_model.fields.index(item) for item in column]

        table = []
        column_data = []
        for row_index in rows:
            for col_index in range(self.main_model.columnCount()):
                if column is None:
                    column_data.append(self.main_model.index(row_index, col_index).data())
                else:
                    if col_index in column:
                        column_data.append(self.main_model.index(row_index, col_index).data())
            table.append(column_data)
            column_data = []
        return table

    # noinspection PyUnresolvedReferences
    def table_ContextMenu(self):
        """
        Context menu for the main table view
        """
        lv_1 = QtWidgets.QMenu()

        # adds the actions and menu
        lv_1.addAction("Play all").triggered.connect(
            lambda: self.queue_model.create_playList(
                    ids = self.getRowData(column = ['file_id'], rows_selected = False),
                    _type = self.queue_model.PlayType.ALL
            )
        )
        lv_1_1 = lv_1.addMenu("Play More")
        lv_1_1.addAction("Play selected files").triggered.connect(
            lambda: self.queue_model.create_playList(
                    ids = self.getRowData(column = ['file_id']),
                    _type = self.queue_model.PlayType.ALL
            )
        )
        lv_1_1.addAction("Play similar artist").triggered.connect(
            lambda: self.queue_model.create_playList(
                    ids = self.getRowData(column = ['file_id']),
                    _type = self.queue_model.PlayType.ARTIST
            )
        )
        lv_1_1.addAction("Play similar genre").triggered.connect(
            lambda: self.queue_model.create_playList(
                    ids = self.getRowData(column = ['file_id']),
                    _type = self.queue_model.PlayType.GENRE
            )
        )
        lv_1.addSeparator()

        lv_1.addAction("Add files").triggered.connect(self.launch_explorer_files)
        lv_1.addAction("Add folder").triggered.connect(self.launch_explorer_directory)
        lv_1.addAction("Add files to playlist").triggered.connect(
            lambda: placeholder(items = self.getRowData(column = ['file_id']))  # TODO
        )
        lv_1.addSeparator()

        lv_1.addAction("File info").triggered.connect(lambda: (
            row := self.ui.library_tableview.selectedIndexes()[0].row(),
            file_info := self.main_model.fetch_file_info(self.getRowDataAt(row, column = ['file_path'])[0][0]),
            self.display_file_info(file_info)
        ))
        lv_1.addAction("Open File location").triggered.connect(lambda: (
            row := self.ui.library_tableview.selectedIndexes()[0].row(),
            self.open_file_path(self.getRowDataAt(row, column = ['file_path'])[0][0])
        ))
        lv_1.addAction("Reload tags for selected").triggered.connect(lambda: (
            row := self.ui.library_tableview.selectedIndexes()[0].row(),
            self.main_model.reload_tags(self.getRowDataAt(row, column = ['file_path'])[0][0])
        ))
        lv_1.addSeparator()

        lv_1_2 = lv_1.addMenu("User rating")
        lv_1_2.addAction("0").triggered.connect(
            lambda: self.main_model.modify_rating(ids = self.getRowData(column = ['file_id']), rating = 0)
        )
        lv_1_2.addAction("1").triggered.connect(
            lambda: self.main_model.modify_rating(ids = self.getRowData(column = ['file_id']), rating = 1)
        )
        lv_1_2.addAction("2").triggered.connect(
            lambda: self.main_model.modify_rating(ids = self.getRowData(column = ['file_id']), rating = 2)
        )
        lv_1_2.addAction("3").triggered.connect(
            lambda: self.main_model.modify_rating(ids = self.getRowData(column = ['file_id']), rating = 3)
        )
        lv_1_2.addAction("4").triggered.connect(
            lambda: self.main_model.modify_rating(ids = self.getRowData(column = ['file_id']), rating = 4)
        )
        lv_1_2.addAction("5").triggered.connect(
            lambda: self.main_model.modify_rating(ids = self.getRowData(column = ['file_id']), rating = 5)
        )
        lv_1.addSeparator()

        lv_1.addAction("Delete from library").triggered.connect(
            lambda: self.del_file_path(self.getRowData(column = ['file_id', 'file_path']))
        )
        lv_1.addAction("Physically delete file").triggered.connect(
            lambda: self.del_file_path(self.getRowData(column = ['file_id', 'file_path']), True)
        )
        lv_1.addSeparator()

        lv_1.addAction("Refresh library").triggered.connect(self.main_model.refresh_table)
        lv_1.addAction("Statistics").triggered.connect(self.display_table_stats)

        # Execution
        cursor = QtGui.QCursor()
        lv_1.exec(cursor.pos())

    def launch_explorer_directory(self):
        """
        open a file explorer in directory only mode
        """
        files = QtWidgets.QFileDialog.getExistingDirectoryUrl(parent = self.ui,
                                                              caption = "Add folders to library")
        if files:
            self.main_model.add_item_fromFS(files.toLocalFile())

    def launch_explorer_files(self):
        """
        open a file explorer in files mode
        """
        files, _ = QtWidgets.QFileDialog.getOpenFileUrls(parent = self.ui,
                                                         caption = "Add folders to library")
        if files:
            files = [file.toLocalFile() for file in files]
            self.main_model.add_item_fromFS(files)

    def display_file_info(self, info: dict):
        placeholder(info = info)

    def display_table_stats(self):
        stats = self.main_model.fetch_table_stats()
        placeholder(**stats)

    # noinspection PyMethodMayBeStatic
    def open_file_path(self, path: str):
        """
        opens file directory in explorer

        Args:
            path (str): location of the file
        """
        os.startfile(os.path.dirname(os.path.realpath(path)), 'explore')

    def del_file_path(self, paths: list[list[str]], physically: bool = False):
        """
        deletes file from library and/or physically

        Args:
            paths (list[str]): location of the file
            physically (bool): true deletes file physically
        """
        # TODO: check for detete item bugs
        pass
