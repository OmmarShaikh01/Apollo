import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtSql import QSqlQuery

from apollo.db.library_manager import LibraryManager
from apollo.app.ux_startup import ApolloStartup
from apollo.utils import PlayingQueue, exe_time

# TODO
# saving application state 

# issues
# Menu opens at cursor position need changes

class ApolloTabFunctions(ApolloStartup):
    """
    Interface between all the tabs in Apollo. 
    """
    
    def __init__(self):
        super().__init__()
        self.PlayQueue = PlayingQueue()
    
    
    def Init_SubTabs(self): # works
        self.LoadDB()
        self.MenuBarBindings()
                    
        # initilizes Subtabs
        self.LibraryTab = LibraryTab(self)
        self.NowPlayingTab = NowPlayingTab(self)
        
        
    def LoadDB(self, dbname = None): # works
        """
        Connects to the databse and returns Manager Object to communicate with the DB
        
        :Args:
            dbname: String
                name Of the Db to connect to
                
        :Return: None
        """
        if dbname == None:
            dbname = self.CONF_MANG.Getvalue(path = 'DBNAME')
        self.LibraryManager = LibraryManager(dbname)
        
    def MenuBarBindings(self): 
        """
        Binda all the actions in the menubar to valid functions
        """
        pass       
    
    
    def _BindingLineSearch(self, LEDT, TBV): # works
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
        LEDT.textChanged.connect(lambda : self._BindingLineClear(LEDT, TBV))
    
    
    def _BindingLineClear(self, LEDT, TBV): # works
        """
        Binds the LineEdit Clear to refresh table
        
        :Args:
            LEDT: LineEdit
                LineEdit to take in the search term
            TBV: TableView
                TableView Object to refresh data
                
        :Return: None
        """
        if LEDT.text() == "":
            self.LibraryManager.TableSearch(LEDT, TBV)
    
    
    def _ColumnSelection(self, TBV, Col): # works
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
            List -> [(String)]:
                Returns a list of Indexes
        """
        if isinstance(Col, str):
            Col = self.LibraryManager.db_fields.index(Col) 
        ColCount = TBV.model().columnCount()
        if Col > ColCount:
            return None
        selected = TBV.selectedIndexes()[Col::ColCount]
        return ([index.data() for index in  selected])
        
        
    def _GetSelectionIndexes(self, TBV): # works
        """
        returns all the data at selected Positions in a TBV
        
        :Args:
            TBV: TableView
                Table to get data from
                
        :Return: List[[Columns]]
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
         
         
    def PlayNow(self, TBV): # works
        """
        Clears the Queue whenever new data is added and is indexed Using File_id
        """
        Select = self._ColumnSelection(TBV, "file_id")
        Indexes = self.GetQueueIndexes(Select, Normal = True)
        self.PlayQueue.RemoveElements()
        self.PlayQueue.AddElements(Indexes)
        
        # Refilling Of Data In The NowPlaying Queue
        Queue = self.apollo_TBV_NPQ_maintable
        Queue.setProperty("Order", [])
        self.LibraryManager.Refresh_TableModelData(Queue)
        
        
    def QueueNext(self, TBV):# works
        """
        Adds Data After the Pointer in the Queue whenever new data is ready and is indexed Using File_id
        """
        self.PlayQueue.AddNext(self._ColumnSelection(TBV, "file_id"))
        Select = self.PlayQueue.GetQueue()
        self.GetQueueIndexes(Select, Normal = True)
        
        # Refilling Of Data In The NowPlaying Queue
        Queue = self.apollo_TBV_NPQ_maintable
        Queue.setProperty("Order", Select)        
        self.LibraryManager.Refresh_TableModelData(Queue)
        
        
    def QueueLast(self, TBV):# works
        """
        Adds Data at the end in the Queue whenever new data is ready and is indexed Using File_id
        """
        self.PlayQueue.AddElements(self._ColumnSelection(TBV, "file_id"))
        Select = self.PlayQueue.GetQueue()
        self.GetQueueIndexes(Select, Normal = True)
        
        # Refilling Of Data In The NowPlaying Queue
        Queue = self.apollo_TBV_NPQ_maintable
        Queue.setProperty("Order", Select)        
        self.LibraryManager.Refresh_TableModelData(Queue)
        
        
    def PlayAllShuffled(self, TBV):# works
        """
        Adds Shuffled Data in the Queue whenever new data is ready and is indexed Using File_id
        """
        Select = self._ColumnSelection(TBV, "file_id")
        self.PlayQueue.RemoveElements()
        Indexes = self.GetQueueIndexes(Select, Shuffled = True)
        self.PlayQueue.AddElements(Indexes)
        
        # Refilling Of Data In The NowPlaying Queue
        Queue = self.apollo_TBV_NPQ_maintable
        Queue.setProperty("Order", [])
        self.LibraryManager.Refresh_TableModelData(Queue)
        
        
    def PlayArtist(self, TBV):# works
        """
        Adds Data in the Queue whenever new data is ready and is indexed Using artist
        """
        Select = self._ColumnSelection(TBV, "artist")
        Indexes = self.GetQueueIndexes(Select, Filter = True, FilterField = "artist")        
        self.PlayQueue.AddElements(Indexes)
        
        # Refilling Of Data In The NowPlaying Queue
        Queue = self.apollo_TBV_NPQ_maintable
        Queue.setProperty("Order", [])
        self.LibraryManager.Refresh_TableModelData(Queue)
        
        
    def PlayAlbumNow(self, TBV):# works
        """
        Adds Data in the Queue whenever new data is ready and is indexed Using album
        """
        Select = self._ColumnSelection(TBV, "album")
        self.PlayQueue.RemoveElements()
        Indexes = self.GetQueueIndexes(Select, Filter = True, FilterField = "album")        
        self.PlayQueue.AddElements(Indexes)
        
        # Refilling Of Data In The NowPlaying Queue
        Queue = self.apollo_TBV_NPQ_maintable
        Queue.setProperty("Order", [])
        self.LibraryManager.Refresh_TableModelData(Queue)
        
        
    def QueueAlbumNext(self, TBV):# works
        """
        Adds Data After the Pointer in the Queue whenever new data is ready and is indexed Using album
        """
        Select = self._ColumnSelection(TBV, "album")
        OldIndex = self.PlayQueue.GetQueue()
        NewIndex = self.GetQueueIndexes(Select, Filter = True, FilterField = "album", ID = OldIndex)
        NewIndex = [Keys for Keys in NewIndex if Keys not in OldIndex]
        self.PlayQueue.AddNext(NewIndex)        
        
        # Refilling Of Data In The NowPlaying Queue
        Queue = self.apollo_TBV_NPQ_maintable
        Queue.setProperty("Order", self.PlayQueue.GetQueue())
        self.LibraryManager.Refresh_TableModelData(Queue)
        
        
    def QueueAlbumLast(self, TBV):# works
        """
        Adds Data in the end of the Queue whenever new data is ready and is indexed Using album
        """
        Select = self._ColumnSelection(TBV, "album")
        OldIndex = self.PlayQueue.GetQueue()
        NewIndex = self.GetQueueIndexes(Select, Filter = True, FilterField = "album", ID = OldIndex)
        NewIndex = [Keys for Keys in NewIndex if Keys not in OldIndex]
        self.PlayQueue.AddElements(NewIndex)      
        
        # Refilling Of Data In The NowPlaying Queue
        Queue = self.apollo_TBV_NPQ_maintable
        Queue.setProperty("Order", self.PlayQueue.GetQueue())
        self.LibraryManager.Refresh_TableModelData(Queue)
              
              
    def PlayGenre(self, TBV):# works
        """
        Adds Data in the Queue whenever new data is ready and is indexed Using genre
        """        
        Select = self._ColumnSelection(TBV, "genre")
        self.PlayQueue.RemoveElements()
        Indexes = self.GetQueueIndexes(Select, Filter = True, FilterField = "genre")        
        self.PlayQueue.AddElements(Indexes)
        
        # Refilling Of Data In The NowPlaying Queue
        Queue = self.apollo_TBV_NPQ_maintable
        Queue.setProperty("Order", [])
        self.LibraryManager.Refresh_TableModelData(Queue)
      
      
    def DeleteItem(self, Type, TBV): # Works
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
        Item = self._ColumnSelection(TBV, "file_id")
        Query = QSqlQuery()
        ID = ", ".join([f"'{v}'"for v in Item])
        Query.prepare(f"DELETE FROM {Tname} WHERE file_id IN ({ID})")
        self.LibraryManager.ExeQuery(Query)
        
        if Type == "Delete" and Tname == "library":
            Path = self._ColumnSelection(TBV, "file_path")
            # DeleteAt(Path)
            
        TableModel = TBV.model()
        Index = list(set([index.row() for index in TBV.selectedIndexes()]))
        [TableModel.removeRow(R) for R in Index]
        
    
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
        
        Indexes = self._ColumnSelection(TBV, Field)
        self.LibraryManager.SearchSimilarField(TBV, Field, Indexes)
   
   
    def FilterTable_ByGroups(self, SortTBV, TBV): # works
        """
        Selects similar items from the Grouptable and only diaplays them
        
        :Args:
            TBV: TableView
                TableView to Select data from and Filter Data for
            SortYBV: TableView
                Indexs to use for data filtering
        """        
        Field = SortTBV.property("GROUP_BY")
        Indexes = self._GetSelectionIndexes(SortTBV)
        Indexes = [items[0].strip() for items in Indexes]
        self.LibraryManager.SearchSimilarField(TBV, Field, Indexes)
        
        
class LibraryTab:
    
    
    def __init__(self, UI = None):
        if UI != None:
            self.UI = UI
        else:
            self.UI = ApolloTabFunctions()
        
        self.LibraryManager = self.UI.LibraryManager
        self.AssignObjects()
        self.Init_MainTableModel("library")
        self.Init_GroupTable()
        self.ElementsBindings()
        
        
    def AssignObjects(self):
        """
        Assigns UI Objects TO Operate Upon
        """
        self.MainTable = self.UI.apollo_TBV_LBT_maintable
        self.MainSearch = self.UI.apollo_LEDT_LBT_main_search
        self.GroupTable = self.UI.apollo_TBV_LBT_grouptable
        self.GroupSearch = self.UI.apollo_LEDT_LBT_groupsearch
        
     
    def Init_MainTableModel(self, tablename):
        """
        initilizes table with database values
        """
        self.LibraryManager.SetTableModle(tablename, self.MainTable, self.LibraryManager.db_fields)
        self.MainTable.setProperty("DB_Table", tablename)
        self.MainTable.setProperty("DB_Columns", self.LibraryManager.db_fields)
        self.MainTable.setProperty("Order", [])
            
           
    def Init_GroupTable(self):
        """
        Initilizes the Grouping table with Selectors
        """
        Field = self.UI.CONF_MANG.Getvalue(path = "LIBRARY_GROUPORDER")
        self.UI.SetGroupMarkers(self.MainTable, Field, self.GroupTable)
        self.UI.apollo_TLB_LBT_grouptool.setText(f"Group By {Field.title().replace('_', ' ')}")
        
        
    def ElementsBindings(self):
        """
        Binds and connects UI Signals to internal functions.
        """
        self.UI._BindingLineSearch(self.UI.apollo_LEDT_LBT_main_search, self.MainTable)
        self.MainTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.MainTable.customContextMenuRequested.connect(self.ContextMenu_MainTable)
        
        self.MainTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.MainTable.customContextMenuRequested.connect(self.ContextMenu_MainTable)
        
        self.UI.apollo_TLB_LBT_grouptool.setMenu(self.ContextMenu_GroupTable())
        
        
        self.UI.apollo_TBV_LBT_grouptable.doubleClicked.connect(lambda: self.UI.FilterTable_ByGroups(\
            self.UI.apollo_TBV_LBT_grouptable,                                                                                           
            self.UI.apollo_TBV_LBT_maintable))      
        self.UI.apollo_PSB_LBT_addtrack.pressed.connect(lambda: print(self.UI.PlayQueue))
        
        
    def ContextMenu_MainTable(self):
        """
        Context menu Bindings for the Library Tab MainTable
        """
        def BindMenuActions(Element, Name, Method = lambda: ""):
            (Element).addAction(f"{Name}").triggered.connect(Method)
            
        
        # Main Menu
        lv_1 = QtWidgets.QMenu()
        
        BindMenuActions(lv_1, "Play Now", lambda: self.UI.PlayNow(TBV = self.MainTable))
        BindMenuActions(lv_1, "Queue Next", lambda: self.UI.QueueNext(TBV = self.MainTable))
        BindMenuActions(lv_1, "Queue Last", lambda: self.UI.QueueLast(TBV = self.MainTable))
        
        # Play More Menu
        lv_1_1 = (lv_1).addMenu("Play More >")
        BindMenuActions(lv_1_1, "Try On Auto-DJ")
        (lv_1_1).addSeparator()
        
        (lv_1_1).addMenu("Output To >")
        (lv_1_1).addSeparator()
        
        BindMenuActions(lv_1_1, "Play Shuffled", lambda: self.UI.PlayAllShuffled(TBV = self.MainTable))
        (lv_1_1).addSeparator()
        
        BindMenuActions(lv_1_1, "Play Artist", lambda: self.UI.PlayArtist(TBV = self.MainTable))
        BindMenuActions(lv_1_1, "Play Similar")
        (lv_1_1).addSeparator()
        
        BindMenuActions(lv_1_1, "Play Album Now", lambda: self.UI.PlayAlbumNow(TBV = self.MainTable))
        BindMenuActions(lv_1_1, "Queue Album Next", lambda: self.UI.QueueAlbumNext(TBV = self.MainTable))
        BindMenuActions(lv_1_1, "Queue Album Last", lambda: self.UI.QueueAlbumLast(TBV = self.MainTable))
        (lv_1_1).addSeparator()
        
        BindMenuActions(lv_1_1, "Play Genre", lambda: self.UI.PlayGenre(TBV = self.MainTable))       
        (lv_1).addSeparator()
        
        # Edit Action
        BindMenuActions(lv_1, "Edit")

        # Ratings Menu
        lv_1_2 = (lv_1).addMenu("Rating >")
        
        # Add To Playlist Menu
        lv_1_3 = (lv_1).addMenu("Add To Playlist >")
        
        # Send To Menu
        lv_1_4 = (lv_1).addMenu("Send To >")
        
        # Delete Action
        BindMenuActions(lv_1, "Delete", lambda: self.UI.DeleteItem("Delete", self.MainTable))
        BindMenuActions(lv_1, "Remove", lambda: self.UI.DeleteItem("Remove", self.MainTable))
        (lv_1).addSeparator()

        # Search Menu
        lv_1_5 = (lv_1).addMenu("Search >")
        BindMenuActions(lv_1_5, "Search Similar Artist", lambda:self.UI.SearchSimilarField(self.MainTable,"artist"))
        BindMenuActions(lv_1_5, "Search Similar Album", lambda:self.UI.SearchSimilarField(self.MainTable,"album"))
        BindMenuActions(lv_1_5, "Search Similar Genre", lambda:self.UI.SearchSimilarField(self.MainTable,"genre"))
        (lv_1_5).addSeparator()
        BindMenuActions(lv_1_5, "Open In Browser")
        BindMenuActions(lv_1_5, "Locate In Explorer")
        
        # Execution        
        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos())
        
        
    def ContextMenu_GroupTable(self):
        """
        Context menu Bindings for the Library Tab GrourTable
        
        :Return: QMenu
        """
        def BindMenuActions(Element, Name, Method = lambda: ""):
            (Element).addAction(f"{Name}").triggered.connect(Method)
        
        
        # Main Menu
        lv_1 = QtWidgets.QMenu()
        lv_1.aboutToShow.connect(lambda: lv_1.setMinimumWidth(self.UI.apollo_TLB_LBT_grouptool.width()))
        
        BindMenuActions(lv_1, "Group By Artist", lambda:(\
                        self.UI.SetGroupMarkers(self.MainTable, "artist", self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Artist")))
        
        BindMenuActions(lv_1, "Group By Album", lambda :(\
                        self.UI.SetGroupMarkers(self.MainTable, "album", self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Album")))
        
        BindMenuActions(lv_1, "Group By Album Artist", lambda:(\
                        self.UI.SetGroupMarkers(self.MainTable, "albumartist", self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Album Artist")))
        
        BindMenuActions(lv_1, "Group By Genre", lambda :(\
                        self.UI.SetGroupMarkers(self.MainTable, "genre", self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Genre")))
        
        BindMenuActions(lv_1, "Group By Folder", lambda: (\
                        self.UI.SetGroupMarkers(self.MainTable,  "file_path",  self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Folder")))
        
        return lv_1     
        
   
class NowPlayingTab:
    ## Issues
    
    def __init__(self, UI):
        if UI != None:
            self.UI = UI
        else:
            self.UI = ApolloTabFunctions()
            
        self.LibraryManager = self.UI.LibraryManager
        self.Init_TableModel("nowplaying")
        self.ElementsBindings()
            
    def Init_TableModel(self, tablename):
        """
        initilizes table with a QStandardItemModel
        """
        self.LibraryManager.SetTableModle(tablename,
                                             self.UI.apollo_TBV_NPQ_maintable,
                                             self.LibraryManager.db_fields)
        self.UI.apollo_TBV_NPQ_maintable.setSortingEnabled(False)
        self.UI.apollo_TBV_NPQ_maintable.setProperty("DB_Table", tablename)
        self.UI.apollo_TBV_NPQ_maintable.setProperty("DB_Columns", self.LibraryManager.db_fields)
        self.UI.apollo_TBV_NPQ_maintable.setProperty("Order", [])
        
        
    def ElementsBindings(self):
        """
        Binds and connects UI Signals to internal functions.
        """    
        self.UI._BindingLineSearch(self.UI.apollo_LEDT_NPQ_main_search, self.UI.apollo_TBV_NPQ_maintable)
 
        
if __name__ == "__main__":
    from apollo.app.apollo_exe import ApolloExecute
    app = ApolloExecute()
    app.Execute()

