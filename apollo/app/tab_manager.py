# UI item name : <form_name>_<item type>_<others>

# Item Type:
# # Layouts:
    # 1. VIL = Vertical Layout
    # 2. HIL = Horizontal Layout
    # 3. GIL = Grid Layout
    # 4. FIL = Form Layout
    # 5. HSP = Horizontal Splitter
    # 6. VSP = Vertical Splitter
    
# # Spacers
    # 1. VSPC = Vertical Spacer
    # 2. HSPC = Horizontal Spacer

# # Buttons
    # 1. PSB = Push Button
    # 2. TLB = Tool Button
    # 3. RDB = Radio Button
    # 4. CKB = Check Box
    # 5. CLB = Command Link Button
    # 6. DBB = Dialog Button Box

# # Item Views
    # 1. LSV = List View
    # 2. TRV = Tree View
    # 3. TBV = Table View
    # 4. CLV = Colum View

# # Item Widgets
    # 1. LSWG = List Widget
    # 2. TRWG = Tree Widget
    # 3. TBWG = Table Widget

# # Containers
    # 1. GBX = Group Box
    # 2. SCAR = Scroll Area
    # 3. TLBX = Tool Box
    # 4. TABWG = Tab Widget
    # 5. SKWG = Stack Widget
    # 6. FR = Frame
    # 7. WDG = Widget
    # 8. MDIA = Mdi Area
    # 9. DOKWG = Dock Widget

# # Input Widgets
    # 1. CMBX = Combo Box
    # 2. FCMBX = Font Combo Box
    # 3. LEDT = Line Edit
    # 4. TXEDT = Text Edit
    # 5. SPNBX = Spin Box
    # 6. DSPBX = Double Spin Box
    # 7. TMEDT = Time Edit
    # 8. DEEDT = Date Edit
    # 9. DTEDT = Date And Time Edit
    # 10. HSCB = Horizontal Scroll Bar
    # 11. VSCB = Vertical Scroll Bar
    # 12. HSLD = Horizontal Slider
    # 13. VSLD = Vertical Slider
    # 14. KSEDT = Key Sequence Edit

# # Display Widgets
    # 1. LAB = Label
    # 2. HDLBD = Header Label
    # 3. PIXLB = Pixmap
    # 4. TXBRW = Text Browser
    # 5. GRPVW = Graphics View
    # 6. CLDWG = Calender Widget
    # 7. LCD = Lcd Widget
    # 8. PGBR = Progress Bar
    # 9. HLN = Horizontal Line
    # 10. VLN = Vertical Line
    # 11. GLWDG = Open Gl Widget
# # Issues:
# QTToolButton : toolmenu doesnt support multi screen menu popups 
# and displays menu on primary screen irrespective of screen

##########################################################################################

from PyQt5 import QtWidgets, QtGui, QtCore

from apollo.db.library_manager import LibraryManager
from apollo.app.ux_startup import ApolloStartup

class ApolloTabFunctions(ApolloStartup):
    """
    Interface between all the tabs in Apollo. 
    """
    
    def __init__(self):
        super().__init__()
        self.LoadDB()
        self.LibraryTab = LibraryTab(self)
        self.NowPlayingTab = NowPlayingTab(self)
        
    def LoadDB(self):
        """
        Connects to the databse and returns Manager Object to communicate with
        """
        dbname = self.CONF_MANG.Getvalue(path = 'DBNAME')
        self.LIB_MANG = LibraryManager(dbname)
    
    def _BindingLineSearch(self, LEDT, TBV):
        """Binds the LineEdit text to a search term and searches in DB and refreshes table"""
        LEDT.returnPressed.connect(lambda: self.LIB_MANG.TableSearch(LEDT, TBV))
        LEDT.textChanged.connect(lambda : self._BindingLineClear(LEDT, TBV))
    
    def _BindingLineClear(self, LEDT, TBV):
        """Binds the LineEdit Clear to refresh table"""
        if LEDT.text() == "":
            self.LIB_MANG.TableSearch(LEDT, TBV)
    
    def _ColumnSelection(self, Table, Col):
        Col = self.LIB_MANG.db_fields.index(Col)
        selected = Table.selectedIndexes()[Col::len(self.LIB_MANG.db_fields)]
        return ([index.data() for index in  selected])
        
class LibraryTab:
    
    def __init__(self, UI = None):
        if UI != None:
            self.UI = UI
        else:
            self.UI = ApolloTabFunctions()
            
        self.init_table()
        self.ElementsBindings()
        
    def init_table(self):
        """
        initilizes table with database values
        """
        table = self.UI.LIB_MANG.GetTableModle("library")
        self.UI.LIB_MANG.SetTableModle(self.UI.apollo_TBV_LBT_maintable, table)

    def ElementsBindings(self):
        """
        Binds and connects UI Signals to internal functions.
        """
        self.UI._BindingLineSearch(self.UI.apollo_LEDT_LBT_main_search, self.UI.apollo_TBV_LBT_maintable)
        self.UI.apollo_TBV_LBT_maintable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.UI.apollo_TBV_LBT_maintable.customContextMenuRequested.connect(self.ContextMenu_MainTable)  

    def ContextMenu_MainTable(self):
        lv_1 = QtWidgets.QMenu()
        
        (lv_1).addAction("Play Now").triggered.connect(lambda: print(self.UI._ColumnSelection(Table = self.UI.apollo_TBV_LBT_maintable, Col = "file_path")))
        (lv_1).addAction("Queue Next").triggered.connect(lambda: self.UI._ColumnSelection(Table = self.UI.apollo_TBV_LBT_maintable, Col = "file_path"))
        (lv_1).addAction("Queue Last").triggered.connect(lambda: self.UI._ColumnSelection(Table = self.UI.apollo_TBV_LBT_maintable, Col = "file_path"))
        
        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos()) 


class NowPlayingTab:
    
    def __init__(self, UI = None):
        if UI != None:
            self.UI = UI
        else:
            self.UI = ApolloTabFunctions()
            
        self.init_table()
        
    def init_table(self):
        """
        initilizes table with database values
        """
        table = self.UI.LIB_MANG.GetTableModle("nowplaying")
        self.UI.LIB_MANG.SetTableModle(self.UI.apollo_TBV_NPQ_maintable, table)
        
        
if __name__ == "__main__":
    from apollo.app.apollo_exe import ApolloExecute
    app = ApolloExecute()
    app.Execute()
