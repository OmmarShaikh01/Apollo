import os, re, sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtSql import QSqlQuery

from apollo.app.apollo_ux import ApolloUX
from apollo.utils import PlayingQueue, exe_time
from apollo.db.library_manager import LibraryManager
from apollo.app.library_tab import LibraryTab
from apollo.app.nowplaying_tab import NowPlayingTab
from apollo.dsp.dsp_main import ApolloDSP

# Issues
# 1. menu over tablestats update only when hovered

# TODO
# 1. all searches and filters use hide anad unhide function rather than updating the model


########################################################################################################################
# Base Utils
########################################################################################################################
class ApolloUtility_Functions(ApolloUX):

    def __init__(self):
        super().__init__()
        self.PlayQueue = PlayingQueue()

    def MenuBarBindings(self):
        """
        Binda all the actions in the menubar to valid functions
        """
        pass


    def LoadDB(self, dbname = None): # works
        """
        Connects to the databse and returns Manager Object to communicate with the DB

        :Args:
            dbname: String
                name Of the Db to connect to

        :Return: None
        """
        if dbname == None:
            dbname = self.CONF_MANG.Getvalue(path = 'CURRENT_DB')
            dbname = self.CONF_MANG.Getvalue(path = f'MONITERED_DB/{dbname}/db_loc')
        self.LibraryManager = LibraryManager(dbname)


    def HeaderActionsBinding(self, index, Model, Header): # works
        """
        Creates all the actions and checkboxes for the related header section at given index

        :Args:
            index: Int
                index of rhe given header section
            Model: QStandardItemModel
                Model of the given table
            Header: QHeaderView
                header view of the given table

        :Return:
            QAction
        """
        def HeaderHide(Index, Action, Header): # works
            """
            Binds all the actions with the hiding and showing functions

            :Args:
                index: Int
                    index of rhe given header section
                Action: QAction
                    Action to set check and uncheck state
                Header: QHeaderView
                    header view of the given table
            """
            if not (Header.isSectionHidden(Index)):
                Action.setChecked(False)
                Header.hideSection(Index)
            else:
                Action.setChecked(True)
                Header.showSection(Index)

        Action = QtWidgets.QAction(Model.headerData(index, 1))
        Action.setCheckable(True)
        if (Header.isSectionHidden(index)):
            Action.setChecked(False)
        else:
            Action.setChecked(True)
        Action.triggered.connect(lambda: HeaderHide(index, Action, Header))
        return Action

    def ColumnSelection(self, TBV, Col): # works
        """
        Gets Data from the slected items from the QTableView and
        returns data of the requested column

        :Args:
            TBV: TableView
                Table to get data from
            Col: String
                Column name to get data from
            Col: Int
                Column index to get data from

        :Return:
            List -> List[Row, Row, ...]
                Returns a list of Indexes
        """
        if isinstance(Col, str):
            Col = self.LibraryManager.db_fields.index(Col)
        ColCount = TBV.model().columnCount()
        if Col > ColCount:
            return None
        selected = TBV.selectedIndexes()[Col::ColCount]
        return ([index.data() for index in  selected])

    def GetSelectionIndexes(self, TBV): # works
        """
        returns all the data at selected Positions in a TBV

        :Args:
            TBV: TableView
                Table to get data from

        :Return: List[[Column, Column, ...]]
            Returns all the data that is selected as a Listed of rows and columns
        """
        selected = TBV.selectedIndexes()
        Table = {}
        for index in selected:
            Row = index.row()
            if Table.get(Row):
                Table[Row].append(index.data())
            else:
                Table[Row] = [index.data()]

        return list(Table.values())


########################################################################################################################
# Search & Selection Utils
########################################################################################################################
class SearchSelection_Utils(ApolloUtility_Functions):
    """"""

    def __init__(self):
        """Constructor"""
        super().__init__()


    def SetGroupMarkers(self, TBV, Field, SortTBV): # works
        """
        Set the field Pointers for the Group Table that can Be used to Filter the MainTable

        :Args:
            TBV: TableView
                Main Table
            Field: String
                Fields that are acceptable
                ["artist", "album", "genre", "albumartist", "folder"]
                Field To select Indexs From
            SortTBV: TableVIew
                Sort/Group Table
        """
        Field = "file_path" if Field == "folder" else Field
        TableName = TBV.property("DB_Table")

        Query = self.LibraryManager.ExeQuery(f"""
        SELECT DISTINCT {Field}
        FROM {TableName}
        WHERE  ({Field} NOT IN ("", " "))
        ORDER BY {Field}
        """)

        Row = 0
        TableModel = QtGui.QStandardItemModel()

        if Field == "file_path":
            FilePath = []
        while Query.next():
            if Field == "file_path":
                item = os.path.split(Query.value(0))[0]
                if item not in FilePath:
                    FilePath.append(item)
                    item = QtGui.QStandardItem(str(f"    {item}")) # adds an 4 space offset to an item
                    item.setTextAlignment(QtCore.Qt.AlignJustify)
                    TableModel.setItem(Row, item)
                    Row += 1
            else:
                item = (Query.value(0))
                item = QtGui.QStandardItem(str(f"    {item}")) # adds an 4 space offset to an item
                item.setTextAlignment(QtCore.Qt.AlignJustify)
                TableModel.setItem(Row, item)
                Row += 1

        SortTBV.setProperty("GROUP_BY", Field)
        SortTBV.horizontalHeader().setStretchLastSection(True)
        SortTBV.setModel(TableModel)

    def SearchSimilarField(self, TBV, Field): # works
        """
        Selects similar items from the table and only diaplays them

        :Args:
            TBV: TableView
                TableView to Select data from and Filter Data for
            Field: String
                Field to use for data filtering
        """

        Indexes = self.ColumnSelection(TBV, Field)
        self.LibraryManager.SearchSimilarField(TBV, Field, Indexes)

    def FilterTable_ByGroups(self, SortTBV, TBV): # Works
        #  no tests, is similar to SearchSimilarField just uses values from group table to apply a filter
        """
        Selects similar items from the Grouptable and only diaplays them

        :Args:
            TBV: TableView
                TableView to Select data from and Filter Data for
            SortYBV: TableView
                Indexs to use for data filtering
        """
        Field = SortTBV.property("GROUP_BY")
        Indexes = self.GetSelectionIndexes(SortTBV)
        Indexes = [items[0].strip() for items in Indexes]
        self.LibraryManager.SearchSimilarField(TBV, Field, Indexes)

    def SearchGroupTable(self, LEDT = QtWidgets.QLineEdit, TBV = QtWidgets.QTableView, ColLimit = 1):
        Model = TBV.model()
        Search = LEDT.text()

        if Search == "":
            for Row in range(Model.rowCount()):
                TBV.showRow(Row)
        else:
            for Col in range(ColLimit):
                for Row in range(Model.rowCount()):
                    data = Model.index(Row, Col).data()
                    Query = [(re.search(f".*{Search}.*", data)),
                             (re.search(f".*{Search.upper()}.*", data)),
                             (re.search(f".*{Search.lower()}.*", data)),
                             (re.search(f".*{Search.title()}.*", data))]
                    if any(Query):
                        TBV.showRow(Row)
                    else:
                        TBV.hideRow(Row)

    def BindingLineSearch(self, LEDT, TBV): # is a Method Binding function, needs no tests
        """
        Binds the LineEdit text to a search term and searches in DB and refreshes table

        :Args:
            LEDT: LineEdit
                LineEdit to take in the search term
            TBV: TableView
                TableView Object to refresh data

        :Return: None
        """
        LEDT.returnPressed.connect(lambda: self.LibraryManager.TableSearch(LEDT, TBV))
        LEDT.textChanged.connect(lambda: self.LibraryManager.TableSearch(LEDT, TBV))

    def GetQueueIndexes(self, Data, **kwargs): # Just Routes Functions no test needed
        """
        Refreshes the NowPlaying Table with Updated Values

        :Args:
            Data: List
                list of Items used as selectors
            FilterField: String
                Field colum to use as key
            ID: List
                File_id as a secondary key
            Filter: Bool
                Filter switch
            Shuffled: Bool
                Shuffle Switch
            Normal: Bool
                Normal Switch

        :Return:
            Indexes: list
                items indexed
        """
        Indexes = None
        if kwargs.get("Filter") != None:
            Field = kwargs.get("FilterField")
            Indexes = self.LibraryManager.CreateView("nowplaying",
                                                     Selector = Data,
                                                     Filter = True,
                                                     FilterField = str(Field),
                                                     ID = kwargs.get("ID"))
        if kwargs.get("Shuffled") != None:
            Indexes = self.LibraryManager.CreateView("nowplaying",
                                                     Selector = Data,
                                                     Shuffled = True,
                                                     FilterField = "file_id")
        if kwargs.get("Normal") != None:
            Indexes = self.LibraryManager.CreateView("nowplaying",
                                                     Selector = Data,
                                                     Normal = True,
                                                     FilterField = "file_id")
        return Indexes

########################################################################################################################
# Queue Utils
########################################################################################################################
class Queue_Utils(SearchSelection_Utils):
    """"""

    def __init__(self):
        """Constructor"""
        super().__init__()


    def Refill_QueueTable(self, QueueTBV = None, Order = []): # Untested
        """
        Refilling Of Data In The NowPlaying Queue

        :Args:
            Order: List
                order to arrnage data items in
        """
        if QueueTBV == None:
            return None

        QueueTBV = self.apollo_TBV_NPQ_maintable
        QueueTBV.setProperty("Order", Order)
        self.LibraryManager.Refresh_TableModelData(QueueTBV)

    def DeleteItem(self, Type, TBV): # Untested
        """
        Delets the File from the database and filesystem
        OR
        Removes the File from the database

        :Args:
            Type: String
                Delete or Remove
            TBV: TableView
        """

        Tname = TBV.property("DB_Table")
        Item = self.ColumnSelection(TBV, "file_id")
        Query = QSqlQuery()
        ID = ", ".join([f"'{v}'"for v in Item])
        Query.prepare(f"DELETE FROM {Tname} WHERE file_id IN ({ID})")
        self.LibraryManager.ExeQuery(Query)

        if Type == "Delete" and Tname == "library":
            Path = self.ColumnSelection(TBV, "file_path")
            # DeleteAt(Path)

        TableModel = TBV.model()
        Index = list(set([index.row() for index in TBV.selectedIndexes()]))
        [TableModel.removeRow(R) for R in Index]


    def PlayNow(self, TBV, QueueTBV = None): # Works
        """
        Clears the Queue whenever new data is added and is indexed Using File_id

        :Args:
            TBV: TableView
                Tableview to use to get data items from
        """
        Select = self.ColumnSelection(TBV, "file_id")
        self.GetQueueIndexes(Select, Normal = True)
        self.PlayQueue.RemoveElements()
        self.PlayQueue.AddElements(Select)
        self.Refill_QueueTable(QueueTBV = QueueTBV, Order = Select)


    def QueueNext(self, TBV, QueueTBV = None): # Works
        """
        Adds Data After the Pointer in the Queue whenever new data is ready and is indexed Using File_id

        :Args:
            TBV: TableView
                Tableview to use to get data items from
        """
        Queue = self.PlayQueue.GetQueue()
        Select = list(filter(lambda x: x not in Queue, self.ColumnSelection(TBV, "file_id")))
        self.PlayQueue.AddNext(Select)
        Queue = self.PlayQueue.GetQueue()
        self.GetQueueIndexes(Queue, Normal = True)
        self.Refill_QueueTable(QueueTBV = QueueTBV, Order = Queue)


    def QueueLast(self, TBV, QueueTBV = None): # Works
        """
        Adds Data at the end in the Queue whenever new data is ready and is indexed Using File_id

        :Args:
            TBV: TableView
                Tableview to use to get data items from
        """
        Queue = self.PlayQueue.GetQueue()
        Select = list(filter(lambda x: x not in Queue, self.ColumnSelection(TBV, "file_id")))
        self.PlayQueue.AddElements(Select)
        Queue = self.PlayQueue.GetQueue()
        self.GetQueueIndexes(Queue, Normal = True)
        self.Refill_QueueTable(QueueTBV = QueueTBV, Order = Queue)


    def PlayAllShuffled(self, TBV, QueueTBV = None): # Works
        """
        Adds Shuffled Data in the Queue whenever new data is ready and is indexed Using File_id

        :Args:
            TBV: TableView
                Tableview to use to get data items from
        """
        Select = self.ColumnSelection(TBV, "file_id")
        self.PlayQueue.RemoveElements()
        Indexes = self.GetQueueIndexes(Select, Shuffled = True)
        self.PlayQueue.AddElements(Indexes)
        self.Refill_QueueTable(QueueTBV = QueueTBV)

    def PlayArtist(self, TBV, QueueTBV = None): # Works
        """
        Adds Data in the Queue whenever new data is ready and is indexed Using artist

        :Args:
            TBV: TableView
                Tableview to use to get data items from
        """
        Select = self.ColumnSelection(TBV, "artist")
        Indexes = self.GetQueueIndexes(Select, Filter = True, FilterField = "artist")
        self.PlayQueue.AddElements(Indexes)
        self.Refill_QueueTable(QueueTBV = QueueTBV)

    def PlayAlbumNow(self, TBV, QueueTBV = None): # Works
        """
        Adds Data in the Queue whenever new data is ready and is indexed Using album

        :Args:
            TBV: TableView
                Tableview to use to get data items from
        """
        Select = self.ColumnSelection(TBV, "album")
        self.PlayQueue.RemoveElements()
        Indexes = self.GetQueueIndexes(Select, Filter = True, FilterField = "album")
        self.PlayQueue.AddElements(Indexes)
        self.Refill_QueueTable(QueueTBV = QueueTBV)

    def PlayGenre(self, TBV, QueueTBV = None): # Works
        """
        Adds Data in the Queue whenever new data is ready and is indexed Using genre

        :Args:
            TBV: TableView
                Tableview to use to get data items from
        """
        Select = self.ColumnSelection(TBV, "genre")
        self.PlayQueue.RemoveElements()
        Indexes = self.GetQueueIndexes(Select, Filter = True, FilterField = "genre")
        self.PlayQueue.AddElements(Indexes)
        self.Refill_QueueTable(QueueTBV = QueueTBV)

    def QueueAlbumNext(self, TBV, QueueTBV = None): # Works
        """
        Adds Data After the Pointer in the Queue whenever new data is ready and is indexed Using album

        :Args:
            TBV: TableView
                Tableview to use to get data items from
        """
        Select = self.ColumnSelection(TBV, "album")
        OldIndex = self.PlayQueue.GetQueue()
        NewIndex = self.GetQueueIndexes(Select, Filter = True, FilterField = "album", ID = OldIndex)
        NewIndex = [Keys for Keys in NewIndex if Keys not in OldIndex]
        self.PlayQueue.AddNext(NewIndex)
        self.Refill_QueueTable(QueueTBV = QueueTBV, Order = self.PlayQueue.GetQueue())

    def QueueAlbumLast(self, TBV, QueueTBV = None): # Works
        """
        Adds Data in the end of the Queue whenever new data is ready and is indexed Using album

        :Args:
            TBV: TableView
                Tableview to use to get data items from
        """
        Select = self.ColumnSelection(TBV, "album")
        OldIndex = self.PlayQueue.GetQueue()
        NewIndex = self.GetQueueIndexes(Select, Filter = True, FilterField = "album", ID = OldIndex)
        NewIndex = [Keys for Keys in NewIndex if Keys not in OldIndex]
        self.PlayQueue.AddElements(NewIndex)
        self.Refill_QueueTable(QueueTBV = QueueTBV, Order = self.PlayQueue.GetQueue())


########################################################################################################################
# Files Utils
########################################################################################################################
class Files_Utils(Queue_Utils):
    """"""

    def __init__(self):
        """Constructor"""
        super().__init__()

    def SetFileRatings(self, Amount, TBV: QtWidgets.QTableView): # Untested
        """
        Sets the file rating for the track in the DB and TableModel

        :Args:
            Amount: Int
                Amount used to set the rating to
            TBV: QtWidgets.QTableView
                Table to get FileId from
        """

        FileId = self.ColumnSelection(TBV, Col = "file_id")
        ID = ", ".join([f"'{v}'"for v in FileId])

        Query = QSqlQuery(f"""
        UPDATE {TBV.property("DB_Table")}
        SET rating = {Amount}
        WHERE file_id IN ({ID})
        """)
        if self.LibraryManager.ExeQuery(Query):
            Model = TBV.model()
            for Row in range(Model.rowCount()):
                if (Model.index(Row, self.LibraryManager.db_fields.index("file_id")).data() in FileId):
                    Model.setItem(Row, self.LibraryManager.db_fields.index("rating"), QtGui.QStandardItem(str(Amount)))

########################################################################################################################
# Main Bindings
########################################################################################################################
class ApolloTabBindings(Files_Utils):
    """"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.Init_SubTabs()

    def Init_SubTabs(self): # works
        self.LoadDB()

        # initilizes Subtabs
        self.LibraryTab = LibraryTab(self)
        self.NowPlayingTab = NowPlayingTab(self)
        self.AudioToolsTab = ApolloDSP(UI = self)

if __name__ == "__main__":
    from apollo.app.apollo_main import ApolloExecute
    app = ApolloExecute()
    app.Execute()
