from PySide6 import QtWidgets
import pytest
import os
import sys

from apollo.app.dataproviders import SQLTableModel
from apollo.db import DataBaseManager
from tests.main.fixtures import Gen_DbTable_Data, del_TempFilled_DB, TempFilled_DB

@pytest.fixture
def getSQLModel(TempFilled_DB):
    Manager, Data = TempFilled_DB
    Table = [[str(C[R]) for C in Data.values()] for R in range(len(Data["album"]))]
    Model = SQLTableModel()
    Model.LoadTable("library")
    return (Model, Manager, Table)

#### Tests ####################################################################
class Test_SQLTableModel:

    @classmethod
    def setup_class(cls):
        App = QtWidgets.QApplication()

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        del_TempFilled_DB()

    def test_SQlTable_load(self, TempFilled_DB):
        Manager, Table = TempFilled_DB
        Table = [[str(C[R]) for C in Table.values()] for R in range(len(Table["album"]))]

        Model = SQLTableModel()
        Model.LoadTable("library")
        Data = Model.Data_atIndex(Rows = list(range(20)))
        assert Data == Table

        Manager.close_connection() #clean up

    def test_SQlTable_index(self, getSQLModel):
        (Model, Manager, Table) = getSQLModel

        assert [Table[1]] == Model.Data_atIndex(Rows = [1])
        assert [Table[1][5:10]] == Model.Data_atIndex(Rows = [1], Columns = list(range(5,10)))
        Manager.close_connection() #clean up

    def test_SQlTable_selectedindex(self, getSQLModel):
        (Model, Manager, Table) = getSQLModel

        View = QtWidgets.QTableView()
        View.setModel(Model)
        View.selectAll()
        assert Table == Model.Data_atIndex(View.selectedIndexes())

        Manager.close_connection() #clean up


