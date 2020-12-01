from PyQt5 import QtWidgets, QtGui, QtCore

from apollo.db.library_manager import LibraryManager
from apollo.app.ux_startup import ApolloStartup
from apollo.utils import PlayingQueue, exe_time

class ApolloTabFunctions(ApolloStartup):
    """
    Interface between all the tabs in Apollo. 
    """
    
    def __init__(self):
        super().__init__()
        self.PlayQueue = PlayingQueue()
    
    def Init_SubTabs(self):
        self.LibraryTab = LibraryTab(self)
        self.NowPlayingTab = NowPlayingTab(self)
        
    def LoadDB(self, dbname = None): # works
        """
        Connects to the databse and returns Manager Object to communicate with
        """
        if dbname == None:
            dbname = self.CONF_MANG.Getvalue(path = 'DBNAME')
        self.LIB_MANG = LibraryManager(dbname)
        
        
    def _BindingLineSearch(self, LEDT, TBV): # works
        """Binds the LineEdit text to a search term and searches in DB and refreshes table"""
        LEDT.returnPressed.connect(lambda: self.LIB_MANG.TableSearch(LEDT, TBV))
        LEDT.textChanged.connect(lambda : self._BindingLineClear(LEDT, TBV))
    
    
    def _BindingLineClear(self, LEDT, TBV): # works
        """Binds the LineEdit Clear to refresh table"""
        if LEDT.text() == "":
            self.LIB_MANG.TableSearch(LEDT, TBV)
    
    
    def _ColumnSelection(self, TBV, Col): # works
        """
        Gets Data from the slected items from the QTableView and
        returns data of the requested column
        
        :Args:
            TBV: TableView
                Table to get data from
            Col: String
                Column to get data from
        """
        if isinstance(Col, str):
            Col = self.LIB_MANG.db_fields.index(Col) 
        ColCount = TBV.model().columnCount()
        
        if Col > ColCount:
            return None
        
        selected = TBV.selectedIndexes()[Col::ColCount]
        
        return ([index.data() for index in  selected])
        
        
    def _GetSelectionIndexes(self, TBV): # works
        """
        returns all th data at selected Positions in a TBV
        
        :Args:
            TBV: TableView
                Table to get data from
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
   
    def GetQueueIndexes(self, Data, **kwargs): # needs test
        """
        Refreshes the NowPlaying Table with Updated Values
        """
        Indexes = None
        if kwargs.get("Filter") != None:
            Field = kwargs.get("FilterField")
            Indexes = self.LIB_MANG.CreateView("nowplaying", Selector = Data,
                                               Filter = True, FilterField = str(Field), ID = kwargs.get("ID"))
        if kwargs.get("Shuffled") != None:
            Indexes = self.LIB_MANG.CreateView("nowplaying", Selector = Data, Shuffled = True, FilterField = "file_id")
        if kwargs.get("Normal") != None:
            Indexes = self.LIB_MANG.CreateView("nowplaying", Selector = Data, Normal = True, FilterField = "file_id")
        return Indexes
        
    def PlayNow(self, TBV): # works
        Select = self._ColumnSelection(TBV, "file_id")
        Indexes = self.GetQueueIndexes(Select, Normal = True)
        self.PlayQueue.RemoveElements()
        self.PlayQueue.AddElements(Indexes)
        TBV.setProperty("Order", [])
        
    def QueueNext(self, TBV): 
        self.PlayQueue.AddNext(self._ColumnSelection(TBV, "file_id"))
        Select = self.PlayQueue.GetQueue()
        self.GetQueueIndexes(Select, Normal = True)
        TBV.setProperty("Order", Select)        
        
    def QueueLast(self, TBV): 
        self.PlayQueue.AddElements(self._ColumnSelection(TBV, "file_id"))
        Select = self.PlayQueue.GetQueue()
        self.GetQueueIndexes(Select, Normal = True)
        TBV.setProperty("Order", Select)        
                
    def PlayAllShuffled(self, TBV): 
        Select = self._ColumnSelection(TBV, "file_id")
        self.PlayQueue.RemoveElements()
        Indexes = self.GetQueueIndexes(Select, Shuffled = True)
        self.PlayQueue.AddElements(Indexes)
        TBV.setProperty("Order", [])
        
    def PlayArtist(self, TBV): 
        Select = self._ColumnSelection(TBV, "artist")
        Indexes = self.GetQueueIndexes(Select, Filter = True, FilterField = "artist")        
        self.PlayQueue.AddElements(Indexes)
        TBV.setProperty("Order", [])
        
    def PlayAlbumNow(self, TBV): 
        Select = self._ColumnSelection(TBV, "album")
        self.PlayQueue.RemoveElements()
        Indexes = self.GetQueueIndexes(Select, Filter = True, FilterField = "album")        
        self.PlayQueue.AddElements(Indexes)
        TBV.setProperty("Order", [])
        
    def QueueAlbumNext(self, TBV): 
        Select = self._ColumnSelection(TBV, "album")
        OldIndex = self.PlayQueue.GetQueue()
        NewIndex = self.GetQueueIndexes(Select, Filter = True, FilterField = "album", ID = OldIndex)
        NewIndex = [Keys for Keys in NewIndex if Keys not in OldIndex]
        self.PlayQueue.AddNext(NewIndex)        
        TBV.setProperty("Order", self.PlayQueue.GetQueue())
        
    def QueueAlbumLast(self, TBV): 
        Select = self._ColumnSelection(TBV, "album")
        OldIndex = self.PlayQueue.GetQueue()
        NewIndex = self.GetQueueIndexes(Select, Filter = True, FilterField = "album", ID = OldIndex)
        NewIndex = [Keys for Keys in NewIndex if Keys not in OldIndex]
        self.PlayQueue.AddElements(NewIndex)      
        TBV.setProperty("Order", self.PlayQueue.GetQueue())
      
    def PlayGenre(self, TBV): 
        Select = self._ColumnSelection(TBV, "genre")
        self.PlayQueue.RemoveElements()
        Indexes = self.GetQueueIndexes(Select, Filter = True, FilterField = "genre")        
        self.PlayQueue.AddElements(Indexes)
        TBV.setProperty("Order", [])
        
    
class LibraryTab:
    
    def __init__(self, UI = None):
        if UI != None:
            self.UI = UI
        else:
            self.UI = ApolloTabFunctions()
        
        self.AssignObjects()
        self.Init_TableModel("library")
        self.ElementsBindings()
        
    def AssignObjects(self):
        """
        Assigns UI Objects TO Operate Upon
        """
        self.MainTable = self.UI.apollo_TBV_LBT_maintable
        self.MainSearch = self.UI.apollo_LEDT_LBT_main_search
        self.GroupTable = self.UI.apollo_TBV_LBT_grouptable
        self.GroupSearch = self.UI.apollo_LEDT_LBT_groupsearch
        
    def Init_TableModel(self, tablename):
        """
        initilizes table with database values
        """
        self.UI.LIB_MANG.SetTableModle(tablename, self.MainTable, self.UI.LIB_MANG.db_fields)
        self.MainTable.setProperty("DB_Table", tablename)
        self.MainTable.setProperty("DB_Columns", self.UI.LIB_MANG.db_fields)
        self.MainTable.setProperty("Order", [])
      
    def ElementsBindings(self):
        """
        Binds and connects UI Signals to internal functions.
        """
        self.UI._BindingLineSearch(self.UI.apollo_LEDT_LBT_main_search, self.MainTable)
        self.MainTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.MainTable.customContextMenuRequested.connect(self.ContextMenu_MainTable)
        self.UI.apollo_PSB_LBT_addtrack.pressed.connect(lambda: print(self.UI.PlayQueue))

    def ContextMenu_MainTable(self):
        """
        Context menu Bindings for the Library Tab MainTable
        """
        
        # Main Menu
        lv_1 = QtWidgets.QMenu()
        
        (lv_1).addAction("Play Now").triggered.connect(lambda: self.UI._PlayNow(TBV = self.MainTable))
        (lv_1).addAction("Queue Next").triggered.connect(lambda: self.UI._QueueNext(TBV = self.MainTable))
        (lv_1).addAction("Queue Last").triggered.connect(lambda: self.UI._QueueLast(TBV = self.MainTable))
        
        # Play More Menu
        lv_1_1 = (lv_1).addMenu("Play More >")
        (lv_1_1).addAction("Try On Auto-DJ")
        (lv_1_1).addSeparator() # ----------------------------------------------
        
        (lv_1_1).addMenu("Output To >")
        (lv_1_1).addSeparator() # ----------------------------------------------
        
        (lv_1_1).addAction("Play Shuffled").triggered.connect(lambda: self.UI._PlayAll_Shuffled(TBV = self.MainTable))
        (lv_1_1).addSeparator() # ----------------------------------------------
        
        (lv_1_1).addAction("Play Artist").triggered.connect(lambda: self.UI._PlayArtist(TBV = self.MainTable))
        (lv_1_1).addAction("Play Similar")
        (lv_1_1).addSeparator() # ----------------------------------------------
        
        (lv_1_1).addAction("Play Album Now").triggered.connect(lambda: self.UI._PlayAlbumNow(TBV = self.MainTable))
        (lv_1_1).addAction("Queue Album Next")
        (lv_1_1).addAction("Queue Album Last")
        (lv_1_1).addSeparator() # ----------------------------------------------
        
        (lv_1_1).addAction("Play Genre")        
        (lv_1).addSeparator() # ------------------------------------------------
        
        # Edit Action
        (lv_1).addAction("Edit")

        # Ratings Menu
        lv_1_2 = (lv_1).addMenu("Rating >")
        
        # Add To Playlist Menu
        lv_1_3 = (lv_1).addMenu("Add To Playlist >")
        
        # Send To Menu
        lv_1_4 = (lv_1).addMenu("Send To >")
        
        # Delete Action
        (lv_1).addAction("Delete")
        (lv_1).addSeparator() # ------------------------------------------------

        # Search Menu
        lv_1_5 = (lv_1).addMenu("Search >")
        lv_1_5.addAction("Search Similar Artist")
        lv_1_5.addAction("Search Similar Album")
        lv_1_5.addAction("Search Similar Genre")
        (lv_1_5).addSeparator() # ----------------------------------------------
        
        
        lv_1_5.addAction("Open In Browser")
        lv_1_5.addAction("Locate In Explorer")
        
        # Execution        
        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos()) 
        
      
class NowPlayingTab:
    ## Issues
    # 1. Columns are sorted and Dont remain As a Queue, 
    #    Database Internally Sorts them
    
    
    def __init__(self, UI):
        if UI != None:
            self.UI = UI
        else:
            self.UI = ApolloTabFunctions()
            
        self.Init_TableModel("nowplaying")
        self.ElementsBindings()
            
    def Init_TableModel(self, tablename):
        """
        initilizes table with a QStandardItemModel
        """
        self.UI.LIB_MANG.SetTableModle(tablename, self.UI.apollo_TBV_NPQ_maintable, self.UI.LIB_MANG.db_fields)
        self.UI.apollo_TBV_NPQ_maintable.setSortingEnabled(False)
        self.UI.apollo_TBV_NPQ_maintable.setProperty("DB_Table", tablename)
        self.UI.apollo_TBV_NPQ_maintable.setProperty("DB_Columns", self.UI.LIB_MANG.db_fields)
        self.UI.apollo_TBV_NPQ_maintable.setProperty("Order", [])
        
        
    def ElementsBindings(self):
        """
        Binds and connects UI Signals to internal functions.
        """    
        self.UI._BindingLineSearch(self.UI.apollo_LEDT_NPQ_main_search, self.UI.apollo_TBV_NPQ_maintable)
 
 
    def ShuffleQueueTable(self):
        """
        Refreshes the NowPlaying Table with Updated Values
        """
        data = self.UI.PlayQueue.GetQueue()
        self.UI.LIB_MANG.CreateView("nowplaying", "file_id", data, Shuffled = True)
        self.UI.apollo_TBV_NPQ_maintable.setProperty("Order", [])
        TableModel = self.UI.LIB_MANG.Refresh_TableModelData(self.UI.apollo_TBV_NPQ_maintable)
        self.UI.PlayQueue.RemoveElements()
        indexes = [TableModel.item(row).text() for row in range(TableModel.rowCount())]
        self.UI.PlayQueue.AddElements(indexes)
        
                
    def FilterQueueTable(self, Field, Data):
        """
        Filters Out the fields and returns file_id of those fields
        
        >>> NowPlayingTab.FilterQueueTable("artist",[1,b,c])
        
        :Args:
        Field: String
            Field to use for 
        Data: List
            Data fields used for selection
        """
        self.UI.LIB_MANG.CreateView("nowplaying", Field, Data, Filter = True)
        self.UI.LIB_MANG.Refresh_TableModelData(self.UI.apollo_TBV_NPQ_maintable)
        Model = self.UI.apollo_TBV_NPQ_maintable.model()
        Indexs = []
        for Row in range(Model.rowCount()):
            Indexs.append(Model.index(Row, 0).data())
        return Indexs
        
if __name__ == "__main__":
    from apollo.app.apollo_exe import ApolloExecute
    app = ApolloExecute()
    app.Execute()

