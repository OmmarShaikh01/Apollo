import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtSql import QSqlQuery   

class TrackItemWidget(QtWidgets.QWidget):# unfinished
    """"""
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        
        self.DBFIELDS = ["file_id", "path_id","file_name","file_path","album",
                         "albumartist","artist","author","bpm","compilation",
                         "composer","conductor","date","discnumber","discsubtitle",
                         "encodedby","genre","language","length","filesize",
                         "lyricist","media","mood","organization","originaldate",
                         "performer","releasecountry","replaygain_gain","replaygain_peak",
                         "title","tracknumber","version","website","album_gain",
                         "bitrate","bitrate_mode","channels","encoder_info","encoder_settings",
                         "frame_offset","layer","mode","padding","protected","sample_rate",
                         "track_gain","track_peak", "rating", "playcount"]
        
        self.setupUi(self)
        if kwargs.get("Data"):
            self.setData(kwargs.get("Data"))

    def setData(self, Data):
        self.TrackItem_LAB_artist.setText(Data[self.DBFIELDS.index("artist")])
        self.TrackItem_LAB_bitrate.setText(Data[self.DBFIELDS.index("bitrate_mode")])
        self.TrackItem_LAB_genre.setText(Data[self.DBFIELDS.index("genre")])
        self.TrackItem_LAB_length.setText(Data[self.DBFIELDS.index("length")])
        self.TrackItem_LAB_size.setText(Data[self.DBFIELDS.index("filesize")])
        self.TrackItem_LAB_title.setText(Data[self.DBFIELDS.index("title")])        
    
    def setupUi(self, TrackItem_WDG):
        TrackItem_WDG.setObjectName("TrackItem_WDG")
        TrackItem_WDG.resize(475, 96)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TrackItem_WDG.sizePolicy().hasHeightForWidth())
        TrackItem_WDG.setSizePolicy(sizePolicy)
        TrackItem_WDG.setMinimumSize(QtCore.QSize(256, 96))
        self.gridLayout = QtWidgets.QGridLayout(TrackItem_WDG)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.TrackItem_PIXLB = QtWidgets.QLabel(TrackItem_WDG)
        self.TrackItem_PIXLB.setMinimumSize(QtCore.QSize(94, 94))
        self.TrackItem_PIXLB.setObjectName("TrackItem_PIXLB")
        self.gridLayout.addWidget(self.TrackItem_PIXLB, 0, 0, 3, 1)
        self.TrackItem_LAB_artist = QtWidgets.QLabel(TrackItem_WDG)
        self.TrackItem_LAB_artist.setMinimumSize(QtCore.QSize(0, 0))
        self.TrackItem_LAB_artist.setObjectName("TrackItem_LAB_artist")
        self.gridLayout.addWidget(self.TrackItem_LAB_artist, 0, 1, 1, 4)
        self.TrackItem_LAB_title = QtWidgets.QLabel(TrackItem_WDG)
        self.TrackItem_LAB_title.setObjectName("TrackItem_LAB_title")
        self.gridLayout.addWidget(self.TrackItem_LAB_title, 1, 1, 1, 4)
        self.TrackItem_LAB_length = QtWidgets.QLabel(TrackItem_WDG)
        self.TrackItem_LAB_length.setObjectName("TrackItem_LAB_length")
        self.gridLayout.addWidget(self.TrackItem_LAB_length, 2, 1, 1, 1)
        self.TrackItem_LAB_genre = QtWidgets.QLabel(TrackItem_WDG)
        self.TrackItem_LAB_genre.setObjectName("TrackItem_LAB_genre")
        self.gridLayout.addWidget(self.TrackItem_LAB_genre, 2, 2, 1, 1)
        self.TrackItem_LAB_bitrate = QtWidgets.QLabel(TrackItem_WDG)
        self.TrackItem_LAB_bitrate.setObjectName("TrackItem_LAB_bitrate")
        self.gridLayout.addWidget(self.TrackItem_LAB_bitrate, 2, 3, 1, 1)
        self.TrackItem_LAB_size = QtWidgets.QLabel(TrackItem_WDG)
        self.TrackItem_LAB_size.setObjectName("TrackItem_LAB_size")
        self.gridLayout.addWidget(self.TrackItem_LAB_size, 2, 4, 1, 1)

        self.retranslateUi(TrackItem_WDG)
        QtCore.QMetaObject.connectSlotsByName(TrackItem_WDG)

    def retranslateUi(self, TrackItem_WDG):
        _translate = QtCore.QCoreApplication.translate
        TrackItem_WDG.setWindowTitle(_translate("TrackItem_WDG", "Form"))
        self.TrackItem_PIXLB.setText(_translate("TrackItem_WDG", "TextLabel"))
        self.TrackItem_LAB_artist.setText(_translate("TrackItem_WDG", "TextLabel"))
        self.TrackItem_LAB_title.setText(_translate("TrackItem_WDG", "TextLabel"))
        self.TrackItem_LAB_length.setText(_translate("TrackItem_WDG", "TextLabel"))
        self.TrackItem_LAB_genre.setText(_translate("TrackItem_WDG", "TextLabel"))
        self.TrackItem_LAB_bitrate.setText(_translate("TrackItem_WDG", "TextLabel"))
        self.TrackItem_LAB_size.setText(_translate("TrackItem_WDG", "TextLabel"))        

    
class MusicItem_Delegate(QtWidgets.QStyledItemDelegate):# unfinished
    """"""

    def __init__(self, parent = None):
        """Constructor"""
        super().__init__(parent)
        self.TrackItem = TrackItemWidget(parent)
        
    def paint(self, painter = QtGui.QPainter, option = QtWidgets.QStyleOptionViewItem, index = None):
        painter.save()
        painter.fillRect(option.rect, option.widget.style())
        painter.translate(option.rect.x(), option.rect.y())
        self.TrackItem.setData(eval(index.data()))
        self.TrackItem.render(painter, QtCore.QPoint(), QtGui.QRegion(option.rect), QtWidgets.QWidget.DrawChildren)  
        painter.restore()
      

    def sizeHint(self, option, index):
        return QtCore.QSize(96, 96)
    
 
        

################################################################################
# NowPlayingTab     
################################################################################    
class NowPlayingTab:
    ## Issues
    
    def __init__(self, UI):
        if UI != None:
            self.UI = UI
        else:
            from apollo.app.apollo_TabBindings import ApolloTabBindings
            self.UI = ApolloTabBindings()
            
        self.TabConfig = { }
            
        self.LibraryManager = self.UI.LibraryManager
        self.Init_TableModel("nowplaying")
        self.ElementsBindings()
            
    def Init_TableModel(self, tablename):
        """
        initilizes table with a QStandardItemModel
        """
        self.UI.apollo_TBV_NPQ_maintable.setProperty("DB_Table", tablename)
        self.UI.apollo_TBV_NPQ_maintable.setProperty("DB_Columns", self.LibraryManager.db_fields)
        self.UI.apollo_TBV_NPQ_maintable.setProperty("Order", [])
        
        self.LibraryManager.SetTableModle(tablename, self.UI.apollo_TBV_NPQ_maintable, self.LibraryManager.db_fields)
        # self.UI.apollo_TBV_NPQ_maintable.setSortingEnabled(False)
        
    def ElementsBindings(self):
        """
        Binds and connects UI Signals to internal functions.
        """    
        self.UI.BindingLineSearch(self.UI.apollo_LEDT_NPQ_main_search, self.UI.apollo_TBV_NPQ_maintable)
 
        Header = self.UI.apollo_TBV_NPQ_maintable.horizontalHeader()
        Header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        Header.customContextMenuRequested.connect(self.ContextMenu_HeaderMenu)        
        self.UI.apollo_TLB_NPQ_maintable.setMenu(self.ContextMenu_MainGroupMenu())
        
        self.UI.apollo_TBV_NPQ_maintable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.UI.apollo_TBV_NPQ_maintable.customContextMenuRequested.connect(self.ContextMenu_MainTable)        
        
########################################################################################################################
# Context Menus
########################################################################################################################

    def ContextMenu_MainTable(self):
        """
        Context menu Bindings for the Library Tab UI.apollo.
        """
        def BindMenuActions(Element, Name, Method = lambda: ""):
            (Element).addAction(f"{Name}").triggered.connect(Method)            
        
        # Main Menu
        lv_1 = QtWidgets.QMenu()

        # Play More Menu
        lv_1_1 = (lv_1).addMenu("Play More")
        BindMenuActions(lv_1_1, "Try On Auto-DJ @")
        (lv_1_1).addMenu("Output To @")               
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
        BindMenuActions(lv_1, "Delete", lambda: self.UI.DeleteItem("Delete", self.UI.apollo_TBV_NPQ_maintable))
        BindMenuActions(lv_1, "Remove", lambda: self.UI.DeleteItem("Remove", self.UI.apollo_TBV_NPQ_maintable))
        (lv_1).addSeparator()

        # Search Menu
        lv_1_5 = (lv_1).addMenu("Search")
        BindMenuActions(lv_1_5, "Search Similar Artist", lambda:
                        self.UI.SearchSimilarField(self.UI.apollo_TBV_NPQ_maintable,"artist"))
        BindMenuActions(lv_1_5, "Search Similar Album", lambda:
                        self.UI.SearchSimilarField(self.UI.apollo_TBV_NPQ_maintable,"album"))
        BindMenuActions(lv_1_5, "Search Similar Genre", lambda:
                        self.UI.SearchSimilarField(self.UI.apollo_TBV_NPQ_maintable,"genre"))
        (lv_1_5).addSeparator()
        
        BindMenuActions(lv_1_5, "Open In Browser @")
        BindMenuActions(lv_1_5, "Locate In Explorer @")
        
        # Execution        
        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos())    
      
    def ContextMenu_MainGroupMenu(self):
        
        def BindMenuActions(Element, Name, Method = lambda: ""):
            (Element).addAction(f"{Name}").triggered.connect(Method)
        
        # Main Menu
        lv_1 = QtWidgets.QMenu()
        lv_1.aboutToShow.connect(lambda: lv_1.setMinimumWidth(self.UI.apollo_TLB_LBT_grouptool.width()))
        
        # Stats Menu
        StatsMenu = lv_1.addMenu("Table Stats")
        Tablename = self.UI.apollo_TBV_NPQ_maintable.property("DB_Table")
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
        TableArtistcount_act = QtWidgets.QAction(f"Artist Count {self.LibraryManager.TableArtistcount(Tablename)}", StatsMenu)
        TableArtistcount_act.hovered.connect(lambda: TableArtistcount_act.setText(f"Artist Count{self.LibraryManager.TableArtistcount(Tablename)}"))
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
        Model = self.UI.apollo_TBV_NPQ_maintable.model()
        Header = self.UI.apollo_TBV_NPQ_maintable.horizontalHeader()
        Actions = [(self.UI.HeaderActionsBinding(index, Model, Header)) for index in range(Model.columnCount())]
        lv_1.addMenu("Hide Section").addActions(Actions)
                
        # Execution        
        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos())    
    
if __name__ == "__main__":
    from apollo.app.apollo_main import ApolloExecute
    
    app = ApolloExecute()
    app.Execute()
    
