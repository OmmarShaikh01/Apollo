

import unittest, datetime, os, sys
sys.path.append(os.path.split(os.path.abspath(__file__))[0].rsplit("\\", 2)[0])

from PyQt5 import QtWidgets, QtCore, QtGui

from apollo.db.library_manager import LibraryManager


class TestSuit_main:
    """"""
    def __init__(self):
        # initialize the test suite
        self.Loader = unittest.TestLoader()
        self.Suite  = unittest.TestSuite()

    def AddTest(self, TestClass):
        # add tests to the test suite
        self.Suite.addTest(self.Loader.loadTestsFromTestCase(TestClass))

    def Run(self, Exe = True, QT = False):
        if QT:
            self.QtApp = QtWidgets.QApplication([])
        if Exe:
            # initialize a runner, pass it your suite and run it
            Runner = unittest.TextTestRunner(verbosity = 1)
            Result = Runner.run(self.Suite)
            return 1
        else:
            return 0

class TesterObjects:
    """Generates Objects and Values Required to Perform Tests"""

    def __init__(self): ...

    @classmethod
    def Gen_TableModel(cls, size = (20, 20)):
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

    @classmethod
    def Gen_TableView(cls, size = (20, 20)):
        TableView = QtWidgets.QTableView()

        # sets Selection Mode
        TableView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        # sets Model to the given view
        RawTable, TableModel = cls.Gen_TableModel(size = size)
        TableView.setModel(TableModel)

        # sets header lables to the given view
        header = TableView.horizontalHeader().model()
        Labels = list(range(header.columnCount()))
        for col, data in enumerate(Labels):
            header.setHeaderData(col, QtCore.Qt.Horizontal, str(data).replace("_", " ").title())


        return (RawTable, TableView)

    @classmethod
    def Gen_TableView_fromData(cls, DataTable: dict):
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

    @classmethod
    def Gen_DbTable_Data(cls, rows = 20):
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
