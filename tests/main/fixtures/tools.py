import datetime
import os
import pytest

from PySide6.QtSql import QSqlQuery
from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

from apollo.db import DataBaseManager, FileManager, LibraryManager
from apollo.db import DBStructureError, QueryBuildFailed, QueryExecutionFailed

@pytest.fixture
def Gen_TableModel(size = (20, 20)):
    """
    Generates a TableModel and RawList
    """
    TableModel = QtGui.QStandardItemModel()
    RawTable = []

    for Row in range(size[0]):
        RawTable.append([])
        for Col in range(size[1]):
            Item = f"{Row}X{Col}"
            TableModel.setItem(Row, Col, QtGui.QStandardItem(str(Item)))
            RawTable[Row].append(Item)

    return (RawTable, TableModel)

@pytest.fixture
def Gen_TableView(size = (20, 20)):
    TableView = QtWidgets.QTableView()

    # sets Selection Mode
    TableView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

    # sets Model to the given view
    RawTable, TableModel = Gen_TableModel(size = size)
    TableView.setModel(TableModel)

    # sets header lables to the given view
    header = TableView.horizontalHeader().model()
    Labels = list(range(header.columnCount()))
    for col, data in enumerate(Labels):
        header.setHeaderData(col, QtCore.Qt.Horizontal, str(data).replace("_", " ").title())


    return (RawTable, TableView)

@pytest.fixture
def Gen_TableView_fromData(DataTable: dict):
    TableView = QtWidgets.QTableView()
    TableModel = QtGui.QStandardItemModel()
    for COLID, Column in enumerate(DataTable.values()):
        for ROWID, value in enumerate(Column):
            TableModel.setItem(ROWID, COLID, QtGui.QStandardItem(str(value)))
    TableView.setModel(TableModel)

    # sets Selection Mode
    TableView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
    # sets header lables to the given view
    header = TableView.horizontalHeader().model()
    Labels = list(range(header.columnCount()))
    for col, data in enumerate(Labels):
        header.setHeaderData(col, QtCore.Qt.Horizontal, str(data).replace("_", " ").title())

    return TableView

@pytest.fixture
def Gen_DbTable_Data(rows = 20):
    # data insertion into library table
    DataTable = {}
    for fields in LibraryManager().db_fields:
        if fields in ["discnumber", "channels"]:
            data = [Row for Row in range(rows)]
        else:
            if fields == "filesize":
                data = [f"1024" for Row in range(rows)]
            elif fields == "length":
                data = datetime.timedelta(seconds = 60)
                data = [f"{data}" for Row in range(rows)]
            else:
                data = [f"{fields}X{Row}" for Row in range(rows)]
        DataTable[fields] = data
    return DataTable

@pytest.fixture
def DBManager():
    Manager = DataBaseManager()
    Manager.connect(":memory:")
    return Manager

@pytest.fixture
def DBManager_Filled(Gen_DbTable_Data):
    Manager = DataBaseManager()
    Manager.connect(":memory:")
    Manager.BatchInsert_Metadata(Gen_DbTable_Data)
    return Manager

@pytest.fixture
def LibraryManager_connected():
    Manager = LibraryManager(":memory:")
    return Manager

@pytest.fixture
def TempFilled_DB(Gen_DbTable_Data):
    Manager = DataBaseManager()
    Data = Gen_DbTable_Data
    Manager.connect(r".\testing_tools\test_files\temp.db")
    if os.path.isfile(r".\testing_tools\test_files\temp.db"):
        Manager.BatchInsert_Metadata(Data)
    return (Manager, Data)

def del_TempFilled_DB():
    if os.path.isfile(r".\testing_tools\test_files\temp.db"):
        os.remove(r".\testing_tools\test_files\temp.db")
