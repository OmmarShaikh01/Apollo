import sys

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from apollo.db.library_manager import DataBaseManager
from apollo import exe_time

class SQLTableModel(QtGui.QStandardItemModel):
    """
    Info: Extends the Standard Item Model
    Args: None
    Returns: None
    Errors: None
    """

    def __init__(self):
        """
        Info: Constructor
        Args: None
        Returns: None
        Errors: None
        """
        super().__init__()
        self.DBManager = DataBaseManager()
        self.DB_FIELDS = self.DBManager.db_fields
        self.DB_TABLE = None

    def OrderTable(self, Keys):
        """
        Info: Orders table rows accroding to the keys
        Args:
        Keys: list[String, String]
            -> Kesy to use to sort rows
        Returns: None
        Errors: None
        """
        def FilterData(Row):
            return [QtGui.QStandardItem(str(V)) for V in ResultSet_dict.get(Row)]

        self.removeRows(0, self.rowCount())
        ResultSet = self.DBManager.fetchAll(self.DBManager.ExeQuery(f"SELECT * FROM {self.DB_TABLE}"))

        if len(ResultSet) > 0:
            ResultSet_dict = {Value[0]: Value for Value in ResultSet}
            for Row in Keys:
                self.appendRow(FilterData(Row))

    def Data_atIndex(self, Indexes:[] = None, Rows:[] = None, Columns:[] = None):
        """
        Info: returns all the data at selected Positions in a TBV
        Args:
        TBV: TableView
            Table to get data from
        cols: List[int, int]
        Return: List[[Column, Column, ...]]
        Errors:
        """
        Table = {}

        if Columns == None:
            Columns = list(range(len(self.DB_FIELDS)))

        if Indexes != None:
            for index in Indexes:
                Row = index.row()
                Col = index.column()
                if Col in Columns:
                    if Table.get(Row):
                        Table[Row].append(index.data())
                    else:
                        Table[Row] = [index.data()]

        if Rows != None:
            for Row in Rows:
                for Col in Columns:
                    if Table.get(Row):
                        Table[Row].append(self.index(Row, Col).data())
                    else:
                        Table[Row] = [self.index(Row, Col).data()]

        return list(Table.values())

    def RefreshData(self):
        """
        Info: Refreshing the Tablemodel
        Args: None
        Returns: None
        Errors: None
        """
        self.removeRows(0, self.rowCount())
        self.LoadData(self.DB_TABLE)

    def LoadTable(self, TableName, Header = None):
        """
        Info: Loads the table model with DB values
        Args:
        TableName: string
            -> DB tablename to get data from
        Header: list(string, string)
            -> header names of the table
        Orientation: Qt.Horizontal | Qt.vertical
            -> Orientation of header data
        Returns: None
        Errors: None
        """
        self.DB_TABLE = TableName
        self.LoadData(TableName)
        if Header != None:
            self.LoadHeaderData(Header, Qt.Horizontal)
        else:
            self.LoadHeaderData(self.DB_FIELDS, Qt.Horizontal)

    def LoadData(self, TableName):
        """
        Info: Loads the table model with DB values
        Args:
        TableName: string
            -> DB tablename to get data from
        Returns: None
        Errors: None
        """
        ResultSet = self.DBManager.fetchAll(self.DBManager.ExeQuery(f"SELECT * FROM {TableName}"))
        for Row in ResultSet:
            self.appendRow(list(map(lambda x: QtGui.QStandardItem(str(x)), Row)))

    def LoadHeaderData(self, Header, Orientation = Qt.Horizontal):
        """
        Info: Loads the table model with DB values
        Args:
        Header: list(string, string)
            -> header names of the table
        Orientation: Qt.Horizontal | Qt.vertical
            -> Orientation of header data
        Returns: None
        Errors: None
        """
        for col, data in enumerate(Header):
            self.setHeaderData(col, Orientation, str(data).replace("_", " ").title())

    def SearchMask(self, View, Column = '', QueryString = None):
        """
        Info: Searches the query string and applies the mast where the data matches the query
        Args:
        QueryString: String
            -> Data to searh for
        View: QtTableVIew
            -> View to apply mask to

        Returns: None
        Errors: None
        """
        if QueryString != None:
            Text = QueryString.strip()
        else:
            Text = (self.Data_atIndex(View, [self.DB_FIELDS.index(Column)])[0])

        if Text != "":
            Query = self.DBManager.ExeQuery(f"""
            SELECT file_id FROM {self.DB_TABLE}
            WHERE
            album LIKE '%{Text}%'
            OR albumartist LIKE '%{Text}%'
            OR artist LIKE '%{Text}%'
            OR author LIKE '%{Text}%'
            OR composer LIKE '%{Text}%'
            OR performer LIKE '%{Text}%'
            OR title LIKE '%{Text}%'
            OR lower(album) LIKE '%{Text}%'
            OR lower(albumartist) LIKE '%{Text}%'
            OR lower(artist) LIKE '%{Text}%'
            OR lower(author) LIKE '%{Text}%'
            OR lower(composer) LIKE '%{Text}%'
            OR lower(performer) LIKE '%{Text}%'
            OR lower(title) LIKE '%{Text}%'
            """)
            ResultSet = self.DBManager.fetchAll(Query)
            for Row in range(self.rowCount()):
                if self.index(Row, 0).data() in ResultSet:
                    View.showRow(Row)
                else:
                    View.hideRow(Row)
        else:
            [View.showRow(Row) for Row in range(View.model().rowCount())]

    def RemoveItem(self, SelectedIndexes):
        """
        Info: Removes Item From Model
        Args:
        View: QtTableView
            -> View to delete data from
        Returns: None
        Errors:
        1. Rows are not deleted when deleting more than 5000 rows
        """

        if self.DB_TABLE == "library":
            selectedID = self.Data_atIndex(Indexes = SelectedIndexes, Columns = [0])
            selectedID = ", ".join([f"'{v}'"for v in selectedID])
            self.DBManager.ExeQuery(f"DELETE FROM {self.DB_TABLE} WHERE file_id IN ({selectedID})")
            self.RefreshData()
            Paths = self.Data_atIndex(SelectedIndexes, [self.DB_FIELDS.index("file_path")])
        else:
            selectedID = set([index.row() for index in SelectedIndexes.selectedIndexes()])
            if len(selectedID) == self.rowCount():
                self.removeRows(0, self.rowCount())
            else:
                OFFSET = 0
                for R in selectedID:
                    self.removeRow(R - OFFSET)
                    OFFSET += 1


class ApolloDataProvider:
    """"""

    def __init__(self):
        """Constructor"""
        self.DataModels = {}

    def AddModel(self, DataModel, Key):
        self.DataModels[Key] = DataModel

    def GetModel(self, Key):
        if (Key in self.DataModels.keys()):
            return self.DataModels.get(Key)
        else:
            raise NotImplementedError()
