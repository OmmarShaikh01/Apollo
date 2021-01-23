import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtSql import QSqlQuery

################################################################################
# LibraryTab
################################################################################

class LibraryTab:
    
    def __init__(self, UI):
        if UI != None:
            self.UI = UI
        else:
            from apollo.app.apollo_TabBindings import ApolloTabBindings
            self.UI = ApolloTabBindings()
            
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
        self.MainTable.setProperty("DB_Table", tablename)
        self.MainTable.setProperty("DB_Columns", self.LibraryManager.db_fields)
        self.MainTable.setProperty("Order", [])        
        
        self.LibraryManager.SetTableModle(tablename, self.MainTable, self.LibraryManager.db_fields)
           
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
        
        self.UI.BindingLineSearch(self.UI.apollo_LEDT_LBT_main_search, self.MainTable)
        
        # group table Queries Functions
        self.UI.apollo_LEDT_LBT_groupsearch.returnPressed.connect(lambda: \
        self.UI.SearchGroupTable(self.UI.apollo_LEDT_LBT_groupsearch, self.UI.apollo_TBV_LBT_grouptable))
        
        self.UI.apollo_LEDT_LBT_groupsearch.textChanged.connect(lambda: \
        self.UI.SearchGroupTable(self.UI.apollo_LEDT_LBT_groupsearch, self.UI.apollo_TBV_LBT_grouptable))
        
        self.UI.apollo_TBV_LBT_grouptable.doubleClicked.connect(lambda: self.UI.FilterTable_ByGroups(\
            self.UI.apollo_TBV_LBT_grouptable,                                                                                           
            self.UI.apollo_TBV_LBT_maintable)) 
    
        Header = self.MainTable.horizontalHeader()
        Header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        Header.customContextMenuRequested.connect(self.ContextMenu_HeaderMenu)        
        
        self.UI.apollo_TLB_LBT_grouptool.setMenu(self.ContextMenu_GroupTable())
        self.UI.apollo_TLB_LBT_main.setMenu(self.ContextMenu_MainGroupMenu())        
        
        self.MainTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.MainTable.customContextMenuRequested.connect(self.ContextMenu_MainTable)
        
        
########################################################################################################################
# Context Menus
########################################################################################################################        
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
        lv_1_1 = (lv_1).addMenu("Play More")
        BindMenuActions(lv_1_1, "Try On Auto-DJ @")
        (lv_1_1).addSeparator()
        
        (lv_1_1).addMenu("Output To @")
        (lv_1_1).addSeparator()
        
        BindMenuActions(lv_1_1, "Play Shuffled", lambda: self.UI.PlayAllShuffled(TBV = self.MainTable))
        (lv_1_1).addSeparator()
        
        BindMenuActions(lv_1_1, "Play Artist", lambda: self.UI.PlayArtist(TBV = self.MainTable))
        BindMenuActions(lv_1_1, "Play Similar @")
        (lv_1_1).addSeparator()
        
        BindMenuActions(lv_1_1, "Play Album Now", lambda: self.UI.PlayAlbumNow(TBV = self.MainTable))
        BindMenuActions(lv_1_1, "Queue Album Next", lambda: self.UI.QueueAlbumNext(TBV = self.MainTable))
        BindMenuActions(lv_1_1, "Queue Album Last", lambda: self.UI.QueueAlbumLast(TBV = self.MainTable))
        (lv_1_1).addSeparator()
        
        BindMenuActions(lv_1_1, "Play Genre", lambda: self.UI.PlayGenre(TBV = self.MainTable))       
        (lv_1).addSeparator()
        
        # Edit Action
        BindMenuActions(lv_1, "Edit @")

        # Ratings Menu
        lv_1_2 = (lv_1).addMenu("Rating @")
        
        # Add To Playlist Menu
        lv_1_3 = (lv_1).addMenu("Add To Playlist @")
        
        # Send To Menu
        lv_1_4 = (lv_1).addMenu("Send To @")
        
        # Delete Action
        BindMenuActions(lv_1, "Delete", lambda: self.UI.DeleteItem("Delete", self.MainTable))
        BindMenuActions(lv_1, "Remove", lambda: self.UI.DeleteItem("Remove", self.MainTable))
        (lv_1).addSeparator()

        # Search Menu
        lv_1_5 = (lv_1).addMenu("Search")
        BindMenuActions(lv_1_5, "Search Similar Artist", lambda:self.UI.SearchSimilarField(self.MainTable,"artist"))
        BindMenuActions(lv_1_5, "Search Similar Album", lambda:self.UI.SearchSimilarField(self.MainTable,"album"))
        BindMenuActions(lv_1_5, "Search Similar Genre", lambda:self.UI.SearchSimilarField(self.MainTable,"genre"))
        (lv_1_5).addSeparator()
        BindMenuActions(lv_1_5, "Open In Browser @")
        BindMenuActions(lv_1_5, "Locate In Explorer @")
        
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
        
        # GroupBy Menu
        GroupBy_menu = lv_1.addMenu("Group By")
        BindMenuActions(GroupBy_menu, "Group By Artist", lambda:(\
                        self.UI.SetGroupMarkers(self.MainTable, "artist", self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Artist")))
        
        BindMenuActions(GroupBy_menu, "Group By Album", lambda :(\
                        self.UI.SetGroupMarkers(self.MainTable, "album", self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Album")))
        
        BindMenuActions(GroupBy_menu, "Group By Album Artist", lambda:(\
                        self.UI.SetGroupMarkers(self.MainTable, "albumartist", self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Album Artist")))
        
        BindMenuActions(GroupBy_menu, "Group By Genre", lambda :(\
                        self.UI.SetGroupMarkers(self.MainTable, "genre", self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Genre")))
        
        BindMenuActions(GroupBy_menu, "Group By Folder", lambda: (\
                        self.UI.SetGroupMarkers(self.MainTable,  "file_path",  self.GroupTable),
                        self.UI.apollo_TLB_LBT_grouptool.setText("Group By Folder")))
        
        lv_1.addSeparator()
        BindMenuActions(GroupBy_menu, "Group None", lambda: (self.UI.LibraryManager.ClearView_Masks(self.MainTable)))
        
        return lv_1
        
    def ContextMenu_MainGroupMenu(self):               
        # Main Menu
        lv_1 = QtWidgets.QMenu()
        lv_1.aboutToShow.connect(lambda: lv_1.setMinimumWidth(self.UI.apollo_TLB_LBT_grouptool.width()))
        
        # Stats Menu
        StatsMenu = lv_1.addMenu("Table Stats")
        Tablename = self.MainTable.property("DB_Table")

        ## Stats Menu -> TableSize_act
        TableSize_act = QtWidgets.QAction(f"Size: {self.LibraryManager.TableSize(Tablename)} Gb", StatsMenu)
        TableSize_act.hovered.connect(lambda:TableSize_act.setText(f"Size: {self.LibraryManager.TableSize(Tablename)} Gb"))
        StatsMenu.addAction(TableSize_act)
        ## Stats Menu -> TablePlaytime_act
        TablePlaytime_act = QtWidgets.QAction(f"PlayTime: {self.LibraryManager.TablePlaytime(Tablename)}", StatsMenu)
        TablePlaytime_act.hovered.connect(lambda: TablePlaytime_act.setText(f"PlayTime: {self.LibraryManager.TablePlaytime(Tablename)}"))
        StatsMenu.addAction(TablePlaytime_act)
        ## Stats Menu -> TableAlbumcount_act
        TableAlbumcount_act = QtWidgets.QAction(f"Album Count: {self.LibraryManager.TableAlbumcount(Tablename)}", StatsMenu)
        TableAlbumcount_act.hovered.connect(lambda: TableAlbumcount_act.setText(f"Album Count: {self.LibraryManager.TableAlbumcount(Tablename)}"))
        StatsMenu.addAction(TableAlbumcount_act)
        ## Stats Menu -> TableArtistcount_act
        TableArtistcount_act = QtWidgets.QAction(f"Artist Count: {self.LibraryManager.TableArtistcount(Tablename)}", StatsMenu)
        TableArtistcount_act.hovered.connect(lambda: TableArtistcount_act.setText(f"Artist Count: {self.LibraryManager.TableArtistcount(Tablename)}"))
        StatsMenu.addAction(TableArtistcount_act)
        ## Stats Menu -> TableTrackcount_act
        TableTrackcount_act = QtWidgets.QAction(f"Track Count: {self.LibraryManager.TableTrackcount(Tablename)}", StatsMenu)
        TableTrackcount_act.hovered.connect(lambda: TableTrackcount_act.setText(f"Track Count: {self.LibraryManager.TableTrackcount(Tablename)}"))
        StatsMenu.addAction(TableTrackcount_act)        
                
        return lv_1
        
            
    def ContextMenu_HeaderMenu(self):
        """
        Context menu Bindings for the Library Tab Header Functions
        
        :Return: None
        """        
        # Main Menu
        lv_1 = QtWidgets.QMenu()
         
        # adds the actions and menu related to Hide section 
        Model = self.MainTable.model()
        Header = self.MainTable.horizontalHeader()
        Actions = [(self.UI.HeaderActionsBinding(index, Model, Header)) for index in range(Model.columnCount())]
        lv_1.addMenu("Hide Section").addActions(Actions)
                
        # Execution        
        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos())
    

if __name__ == "__main__":
    from apollo.app.apollo_main import ApolloExecute
    app = ApolloExecute()
    app.Execute()
