import sys, os
from queue import Queue

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QThread, QThreadPool

from apollo.utils import exe_time, dedenter, ThreadIt, ConfigManager
from apollo.db.library_manager import DataBaseManager, LibraryManager, ModelView_Manager, FileManager
from apollo.gui.library_manager_ui import Ui_MainWindow
from apollo.app.utils_app.file_explorer import FileExplorer
from apollo.gui.ledt_dialog import LEDT_Dialog

# TODO
# review for bugs
# write docs
# cleaning and refactor code and make dependency independent

# DB Import/Export still need to be figured out and written
ApolloLibraryManager = 1
currentdb = "Default1"
tempconfig = {
    "Default": {
        "name": "Default",
        "db_loc": "e:\\Apollo\\apollo\\db\\default.db",
        "file_mon": [
            "E:/"
        ],
        "filters": ['.mp3', '.flac', '.aac', '.wav']
    },
    "Default1": {
        "name": "Default1",
        "db_loc": "E:\\default1.db",
        "file_mon": [
            "E:/music/new"
        ],
        "filters": ['.mp3', '.flac', '.aac', '.wav']
    },
    "Default12": {
        "name": "Default12",
        "db_loc": "E:\\default12.db",
        "file_mon": [
            "E:/DemoPython",
            "E:/DevTools",
            "E:/Downloads",
            "E:/Factorio-Repack-Games.com",
            "E:/Peaky Blinders",
            "E:/apollo-git",
            "E:/books",
            "E:/include",
            "E:/movies",
            "E:/music",
            "E:/soft_down",
            "E:/test_samples"
        ],
        "filters": ['.mp3', '.flac', '.aac', '.wav']
    },
    "Default123": {
        "name": "Default123",
        "db_loc": "C:\\default123.db",
        "file_mon": [],
        "filters": ['.mp3', '.flac', '.aac', '.wav']
    }
}


class FileScanner_Thread(QThread):
    """"""
    
    def __init__(self, DB):
        """Constructor"""
        super().__init__()
        self.setObjectName("FileScanner")
        self.FileManager = FileManager()
        self.DB = DB
                
    def connect(self, DB):        
        self.FileManager.connect(DB)
        return self.FileManager.IsConneted()
        
    def setQueue(self, queue):
        self.Queue = queue

    def scannerSlot(self, path): ...

    def run(self):
        try:
            self.connect(self.DB)
            if self.FileManager.IsConneted():            
                while self.Queue.not_empty:                
                    item = self.Queue.get()
                    self.FileManager.BatchInsert_Metadata(self.FileManager.scan_directory(item[0], item[1], self.scannerSlot))
            self.FileManager.close_connection()
            self.finished.emit()
        except Exception as e:
            print(e)
            self.finished.emit()
            self.FileManager.close_connection()
               
                        
class FileScanner:
    """"""
    def __init__(self, Label):
        """Constructor"""
        self.ScannerQueue = Queue()
        self.SCANNING = False
        self.Label = Label
        
    def setLabelMsg(self, msg):
        self.Label.showMessage(msg)
        
    def addItem(self, item: ["Path", "Filters"]):
        self.ScannerQueue.put(item)    

    def start(self, DB):
        def onComplete():
            self.SCANNING = False
            
        # launch a thread to connect to a database and start the scan
        if self.SCANNING == False:                   
            self.SCANNING = True
            Thread = FileScanner_Thread(DB)
            Thread.setQueue(self.ScannerQueue)
            Thread.finished.connect(onComplete)
            Thread.scannerSlot = self.setLabelMsg
            Thread.start()            
            
            if not Thread.isRunning():                
                self.SCANNING = False
                raise Warning("Thread Failed to start")
            
        if self.SCANNING == True:
            # ignores the scann call as a thread is currently running
            print("Thread Scanning Directory")
            

                        
class App_DataBaseManager:
    """
    Class that manages all function and mannagement of the database for Apollo using A GUI 
    """
    def __init__(self, UI: ApolloLibraryManager):
        self.UI = UI
        self.UI.filters = self.ScanningFilters()
        self.init_subWindows()
        self.init_UIbindings()
        
    
    def init_subWindows(self):
        self.DBFileexp = FileExplorer()
        self.DBFileexp.setWindowTitle("File Explorer")
        
        self.FileExp = FileExplorer(_type = "checkbox")
        self.FileExp.setWindowTitle("File Explorer")
        
        self.Dialog = LEDT_Dialog()
        self.Dialog.setWindowTitle("Add Directory")
        
        self.FileScanner = FileScanner(self.UI.statusbar)
        
    def init_UIbindings(self):
        """
        Ui and function bindings
        """
        # LBM_CMBX_dbname functions
        self.fill_CMBX(self.UI.LBM_CMBX_dbname)
        index = list(tempconfig.keys()).index(currentdb)
        self.UI.LBM_CMBX_dbname.currentTextChanged.connect(self.fill_DBinfo)
        self.UI.LBM_CMBX_dbname.setCurrentIndex(index)
        self.UI.LBM_PSB_back.pressed.connect(lambda: self.iter_ComboBox(-1, self.UI.LBM_CMBX_dbname))
        self.UI.LBM_PSB_fowd.pressed.connect(lambda: self.iter_ComboBox(1, self.UI.LBM_CMBX_dbname))        
        
        self.UI.LBM_PSB_libremove.pressed.connect(self.remove_DBdata)
        self.UI.LBM_PSB_libadd.pressed.connect(self.get_DBdata)
        self.UI.LBM_LEDT_path.setReadOnly(True)
        self.UI.LBM_LEDT_name.textChanged.connect(self.DBnameChanged)
        
        self.UI.LBM_LSV_filesmon.setContextMenuPolicy(Qt.CustomContextMenu)
        self.UI.LBM_LSV_filesmon.customContextMenuRequested.connect(self.ContextMenu_FileMonitor)        
        
        self.UI.LBM_PSB_fileexp_2.pressed.connect(self.call_FileExplorer)
        self.FileExp.buttonBox.accepted.connect(lambda: self.add_NewFiles(self.FileExp.get_FilePath()))
        
        self.UI.LBM_PSB_fileexp.pressed.connect(self.DBFileexp.show)
        self.DBFileexp.treeView.doubleClicked.connect(lambda index: self.add_NewDBpath(self.DBFileexp.get_Path(index)))
        self.DBFileexp.buttonBox.accepted.connect(lambda: (self.DBFileexp.close(), self.Dialog.close()))
        self.DBFileexp.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.DBFileexp.treeView.customContextMenuRequested.connect(self.ContextMenu_FileExp_FilesDB)        
        
        self.UI.LBM_PSB_dbactive.pressed.connect(lambda: self.set_AsActive(self.UI.LBM_CMBX_dbname.currentText()))
        self.UI.LBM_PSB_librescan.pressed.connect(lambda: self.rescan_Dir(self.UI.LBM_LSV_filesmon, "all"))
        
        
    def ScanningFilters(self): # getter
        """
        defines the scanning filters for the File Manager
        """
        filters = [".mp3",
                   ".flac", 
                   ".aac", 
                   ".wav"]
        return filters       
        

    def close(self):
        self.DBFileexp.close()
        self.FileExp.close()
        self.Dialog.close()
        
        
    def ContextMenu_FileMonitor(self):
        """
        Context Menu defination
        """
        main = QtWidgets.QMenu()
        main.addAction("Remove Directory").triggered.connect(lambda: self.remove_Dir(self.UI.LBM_LSV_filesmon))
        main.addAction("Rescan Directory").triggered.connect(lambda: self.rescan_Dir(self.UI.LBM_LSV_filesmon))

        cur = QtGui.QCursor()
        main.exec_(cur.pos())    
        
        
    def iter_ComboBox(self, direction: int, CMBX: QtWidgets.QComboBox): # independent
        """
        Iters and loads the corresponding for all the DB taht have been declared for Apollo

        :Args:
            direction: Direction for the list to iter in (Forward/Backward)
        """
        Index = CMBX.currentIndex() + (direction)
        if Index == CMBX.count():
            Index = 0
        if Index < 0:
            Index = CMBX.count() - 1
        CMBX.setCurrentIndex(Index)    
    
    
    def fill_CMBX(self, CMBX):
        for indx, keys in enumerate(tempconfig.keys()):
            self.fill_CMBXitem(CMBX, keys)
            
            
    def fill_CMBXitem(self, CMBX, item):
        if not (item in [CMBX.itemText(index) for index in range(CMBX.count())]):
            CMBX.addItem(item)        
            
            
    def fill_DBinfo(self, Data): # UI dep
        """
        When a new DB name is loaded the corresponding data is loaded for the UI

        :Args:
            Data: name of the DB to load data for
        """
        # gets the dict of data related to the DB anem passed in
        DataDict = tempconfig.get(Data)
        
        # clears the slection for each new DB loaded
        self.FileExp.close()
        self.FileExp.FilePathModel.checkStates = {}
        
        # Populates the UI
        self.UI.LBM_LEDT_name.setText(DataDict.get("name"))
        self.UI.LBM_LEDT_path.setText(os.path.normpath(DataDict.get("db_loc")))

        # Fills the Filename monitered by the DB in the UI
        files = DataDict.get("file_mon")
        filesmodel = QtGui.QStandardItemModel()
        for item in files:
            filesmodel.appendRow(QtGui.QStandardItem(str(os.path.normpath(item))))
        self.UI.LBM_LSV_filesmon.setModel(filesmodel)
        
        # Fills the File filters ion the UI
        filtersEN = DataDict.get("filters")
        filtersmodel = QtGui.QStandardItemModel()
        for itemname in self.UI.filters:
            item = QtGui.QStandardItem(str(itemname))
            item.setCheckable(True)
            if itemname in filtersEN:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)               
            filtersmodel.appendRow(item)
        self.UI.LBM_LSV_filters.setModel(filtersmodel)
                    
                
    def get_DBdata(self): # UI dep
        """
        Retrieves and Stores the New data declared for the New DB
        """
        DBdata = {}
        
        # gets the new DB name
        DBdata["name"] = self.UI.LBM_LEDT_name.text()
        
        # gets thye new DB location
        DBdata["db_loc"] = os.path.normpath(self.UI.LBM_LEDT_path.text())
        if self.UI.LBM_LEDT_path.text() == "":
            self.UI.statusbar.showMessage('Enter File name')
            return
    
        # gets the files to be monitored
        model = self.UI.LBM_LSV_filesmon.model()
        DBdata["file_mon"] = ([os.path.normpath(model.index(row, 0).data()) for row in range(model.rowCount())])
    
        # sets the file scanning filter
        model = self.UI.LBM_LSV_filters.model()
        filters = []
        for row in range(model.rowCount()):
            if model.index(row, 0).data(Qt.CheckStateRole) == 2:
                filters.append(model.index(row, 0).data())            
        DBdata["filters"] = filters
        
        # adds the data to the config
        temp = tempconfig
        temp[DBdata["name"]] = DBdata
        #### write to main config
        
        # updates the combobox
        self.fill_CMBX(self.UI.LBM_CMBX_dbname)
                    
                
    def remove_DBdata(self): # UI dep
        """
        Removes the given DB from Apollo
        """
        if (self.UI.LBM_LEDT_name.text() in tempconfig.keys()):
            # removes the data to the config
            DBData = tempconfig
            del DBData[self.UI.LBM_LEDT_name.text()]
            
            #### write to main config

    def DBnameChanged(self): # UI dependent
        """
        Called when a DB name is chaned and clears if the field is cleared for editing
        """
        Data = self.UI.LBM_LEDT_name.text()
        if (Data in [self.UI.LBM_CMBX_dbname.itemText(item) for item in range(self.UI.LBM_CMBX_dbname.count())]):
            # matches and fills data
            self.fill_DBinfo(Data)
        else:
            # clears data if no name matches
            self.UI.LBM_LEDT_path.clear()
            self.UI.LBM_LSV_filesmon.setModel(QtGui.QStandardItemModel())
            filtersmodel = QtGui.QStandardItemModel()
            for itemname in self.UI.filters:
                item = QtGui.QStandardItem(str(itemname))
                item.setCheckable(True)
                item.setCheckState(Qt.Unchecked)               
                filtersmodel.appendRow(item)
            self.UI.LBM_LSV_filters.setModel(filtersmodel)    
                
                        
    def remove_Dir(self, View: QtWidgets.QListView): # iNDEPENDENT
        """
        Removes a fileitem for being monitored
        """
        index = View.selectedIndexes()
        model = View.model()
        if len(index) >= 1:
            model.removeRow(index[0].row())
        
        
    def rescan_Dir(self, View: QtWidgets.QListView, Flag = "singular"): # unfinished
        """
        Rescans a particular directory
        """
        if Flag == "singular":
            index = View.selectedIndexes()
            if len(index) >= 1:
                index = [index[0].data()]                
        if Flag == 'all':
            model = View.model()
            index = [model.index(row, 0).data() for row in range(model.rowCount())]

        # sets the file scanning filter
        model = self.UI.LBM_LSV_filters.model()
        filters = []
        for row in range(model.rowCount()):
            if model.index(row, 0).data(Qt.CheckStateRole) == 2:
                filters.append(model.index(row, 0).data())            
        
        for Path in index:
            self.FileScanner.addItem([Path, filters])            
        self.FileScanner.start(self.UI.LBM_LEDT_path.text())
                
    def call_FileExplorer(self): # UI dependent
        """
        calls the FileExplorer for the files to be added for scanning and updating the database
        """
        model = self.UI.LBM_LSV_filesmon.model()
        for item in range(model.rowCount()):
            path = model.index(item, 0).data()
            if os.path.isdir(path):
                self.FileExp.FilePathModel.checkStates[path] = Qt.Checked
        self.FileExp.show()
        self.FileExp.raise_()
        
        
    def add_NewFiles(self, Files: list): # UI dependent
        """
        Adds the files that are being monitored that for the current DB

        :Args:
            Files: Files that needed to be added to the ListView
        """
        files = Files
        filesmodel = QtGui.QStandardItemModel()
        for item in files:
            filesmodel.appendRow(QtGui.QStandardItem(str(item)))
        self.UI.LBM_LSV_filesmon.setModel(filesmodel)
        self.FileExp.close()
        self.FileExp.FilePathModel.checkStates = {}    
                
                                  
    def ContextMenu_FileExp_FilesDB(self):
        """
        Context Menu defination
        """        
        main = QtWidgets.QMenu()
        main.addAction("Add Sub Folder").triggered.connect(self.add_Dir)
        main.addAction("Select Folder").triggered.connect(self.select_Dir)
        
        cur = QtGui.QCursor()
        main.exec_(cur.pos())    
        
        
    def add_Dir(self): # UI dependent
        """
        Adds a new Dir to the Filesystem
        """
        def add_DirtoFS(path):
            """
            Deals with conflicts of filepaths 
            """
            path = os.path.normpath(path)
            if os.path.isdir(path):
                path = path + "_Copy"
                os.mkdir(path)
            else:
                os.mkdir(path)
            self.Dialog.close()
        
        index = self.DBFileexp.treeView.selectedIndexes()
        path = self.DBFileexp.FilePathModel.filePath(index[0])
        
        # LineEdit Defination
        self.Dialog.setWindowTitle("Add Folder to Parent")
        self.Dialog.buttonBox.accepted.connect(lambda: add_DirtoFS(os.path.join(path, self.Dialog.lineEdit.text())))
        self.Dialog.buttonBox.rejected.connect(self.Dialog.close)
        self.Dialog.show()
        
        
    def select_Dir(self): # UI dependent
        """
        Selects the Directory at the given index
        """
        index = self.DBFileexp.treeView.selectedIndexes()
        path = self.DBFileexp.FilePathModel.filePath(index[0])
        self.add_NewDBpath(path)
                             

    def add_NewDBpath(self, Path: str): # UI dependent
        """
        Called when a new name is entered and generates the corresponding path

        :Args:
            Path: Path of the new databse directory
        """
        name = self.UI.LBM_LEDT_name.text().lower()
        # checks is the file name entered already exists or not
        if os.path.isfile(os.path.normpath(os.path.join(Path, f"{name}.db"))):
            self.UI.statusbar.showMessage('File already exists')

        # checks for unaccepted names
        if all([(name != ""), (name != " "), name.isalnum()]):
            Path = os.path.normpath(os.path.join(Path, f"{name}.db"))
            self.UI.LBM_LEDT_path.setText(Path)
        else:
            self.UI.statusbar.showMessage('File name not valid')                


    def set_AsActive(self, name): # unfinished
        print(name)
        
        
class ApolloLibraryManager(Ui_MainWindow, QtWidgets.QMainWindow):
    """"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.setupUi(self)
        self.CONFG = ConfigManager()
        
        self.init_Subtools()
        self.setWindowTitle("Library Manager")
        
        
    def init_Subtools(self):
        self.DBmanager = App_DataBaseManager(UI = self)
        
        
    def closeEvent(self, event):
        self.DBmanager.close()
        
                    
if __name__ == "__main__":
    from apollo.resources.apptheme.theme import Theme

    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")

    LoadTheme = lambda: (app.setStyleSheet(Theme().GenStylesheet(eval(Theme().DefaultPallete())["THEME"])))
    LoadTheme()

    UI = ApolloLibraryManager()
    UI.LBM_PSB_libimport.pressed.connect(LoadTheme)
    UI.show()
    app.exec_()
