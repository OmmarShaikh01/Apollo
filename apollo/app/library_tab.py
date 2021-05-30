import sys

from PySide6 import QtWidgets, QtGui, QtCore 
from PySide6.QtCore import Qt

from apollo.db.library_manager import DataBaseManager
from apollo.utils import exe_time
from apollo.app.dataproviders import SQLTableModel


class LibraryTab:
    """
    Info: LIbrary Tab class
    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self, UI):
        """
        Info: Constructor
        Args: None
        Returns: None
        Errors: None
        """
        ### Development code not production code will cause bugs if not removed
        if UI != None:
            self.UI = UI
        else:
            from apollo.app.mainapp_ux import ApolloMain
            self.UI = ApolloMain()
        ###
        self.DataProvider = self.UI.DataProvider
        self.PlayingQueue = self.DataProvider.GetModel("nowplaying_model")
        self.Init_DataModels()
        self.MiscFunctionBinding()

    def Init_DataModels(self):
        self.MainView = self.UI.LDT_TBV_maintable
        self.MainModel = SQLTableModel()
        self.MainModel.LoadTable("library", self.MainModel.DB_FIELDS, Qt.Horizontal)
        self.DataProvider.AddModel(self.MainModel, "library_model")
        self.MainView.setModel(self.MainModel)
        self.MainView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.MainView.customContextMenuRequested.connect(self.ContextMenu_MainTable)

    def MiscFunctionBinding(self):
        self.UI.LBT_LEDT_mainsearch.textChanged.connect(lambda x: self.MainModel.SearchMask(self.MainView, QueryString = x))

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

        BindMenuActions(lv_1, "Play Now", lambda: self.PlayingQueue.PlayNow(self.MainView))
        BindMenuActions(lv_1, "Queue Next", lambda: self.PlayingQueue.QueueNext(self.MainView))
        BindMenuActions(lv_1, "Queue Last", lambda: self.PlayingQueue.QueueLast(self.MainView))

        # Play More Menu
        lv_1_1 = (lv_1).addMenu("Play More")
        BindMenuActions(lv_1_1, "Try On Auto-DJ @")
        (lv_1_1).addSeparator()

        (lv_1_1).addMenu("Output To @")
        (lv_1_1).addSeparator()

        BindMenuActions(lv_1_1, "Play Shuffled", lambda: self.PlayingQueue.PlayShuffled(self.MainView))
        BindMenuActions(lv_1_1, "Play Artist", lambda: self.PlayingQueue.PlayArtist(self.MainView))
        BindMenuActions(lv_1_1, "Play Album Now", lambda: self.PlayingQueue.PlayAlbum(self.MainView))
        BindMenuActions(lv_1_1, "Play Genre", lambda: self.PlayingQueue.PlayGenre(self.MainView))
        (lv_1).addSeparator()

        # Edit Action
        BindMenuActions(lv_1, "Edit @")

        # Ratings Menu
        lv_1_2 = (lv_1).addMenu("Rating")
        BindMenuActions(lv_1_2, "0   stars", lambda: print(1))
        BindMenuActions(lv_1_2, "1   stars", lambda: print(1))
        BindMenuActions(lv_1_2, "1.5 stars", lambda: print(1))
        BindMenuActions(lv_1_2, "2   stars", lambda: print(1))
        BindMenuActions(lv_1_2, "2.5 stars", lambda: print(1))  
        BindMenuActions(lv_1_2, "3   stars", lambda: print(1))
        BindMenuActions(lv_1_2, "3.5 stars", lambda: print(1))
        BindMenuActions(lv_1_2, "4   stars", lambda: print(1))
        BindMenuActions(lv_1_2, "4.5 stars", lambda: print(1))
        BindMenuActions(lv_1_2, "5   stars", lambda: print(1))



        # Add To Playlist Menu
        lv_1_3 = (lv_1).addMenu("Add To Playlist @")

        # Send To Menu
        lv_1_4 = (lv_1).addMenu("Send To @")

        # Delete Action
        BindMenuActions(lv_1, "Delete", lambda: self.MainModel.DeleteItem(self.MainView))
        BindMenuActions(lv_1, "Remove", lambda: self.MainModel.RemoveItem(self.MainView))
        (lv_1).addSeparator()

        # Search Menu
        lv_1_5 = (lv_1).addMenu("Search")
        BindMenuActions(lv_1_5, "Search Similar Artist", lambda: self.MainModel.SearchMask(self.MainView, "artist"))
        BindMenuActions(lv_1_5, "Search Similar Album", lambda: self.MainModel.SearchMask(self.MainView, "album"))
        BindMenuActions(lv_1_5, "Search Similar Genre", lambda: self.MainModel.SearchMask(self.MainView, "genre"))
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
                        self.UI.SetGroupMarkers(self.MainTable, "artist", self.GroupTable)))

        BindMenuActions(GroupBy_menu, "Group By Album", lambda :(\
                        self.UI.SetGroupMarkers(self.MainTable, "album", self.GroupTable)))

        BindMenuActions(GroupBy_menu, "Group By Album Artist", lambda:(\
                        self.UI.SetGroupMarkers(self.MainTable, "albumartist", self.GroupTable)))

        BindMenuActions(GroupBy_menu, "Group By Genre", lambda :(\
                        self.UI.SetGroupMarkers(self.MainTable, "genre", self.GroupTable)))

        BindMenuActions(GroupBy_menu, "Group By Folder", lambda: (\
                        self.UI.SetGroupMarkers(self.MainTable,  "file_path",  self.GroupTable)))

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
    from apollo.app.mainapp import ApolloExecute
    from apollo.plugins.app_theme import Theme

    Theme().LoadAppIcons("GRAY_100")
    app = ApolloExecute()
    app.Execute()
