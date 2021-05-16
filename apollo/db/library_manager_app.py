import os, sys, re,shutil
from queue import Queue

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread

from apollo.gui.library_manager_ui import Ui_MainWindow
from apollo.db.library_manager import DataBaseManager, FileManager
from apollo.app.utils_app.file_explorer import FileExplorer
from apollo.gui.ledt_dialog import LEDT_Dialog

ApolloLibraryManager = 1
TEMPCONFIG = {
    "Default": {
        "name": "Default",
        "path": "C:\\Users\\Ommar\\Desktop\\temp\\default.db",
        "files_monitored": ['D:/Apollo', 'D:/Blender2.92', 'D:/Blockchain-project', 'D:/Program Files',
                            'D:/Temp', 'D:/blender-addons', 'D:/books', 'D:/class-notes', 'D:/games',
                            'D:/msys2', 'D:/music', 'D:/python-venv'],
        "file_extensions": [1, 0, 1, 1, 0, 1, 1],
    },
    "Default_2": {
        "name": "Default_2",
        "path": "C:\\Users\\Ommar\\Desktop\\temp\\default.db",
        "files_monitored": ['D:/Apollo', 'D:/Blender2.92', 'D:/Blockchain-project', 'D:/Program Files',
                            'D:/Temp', 'D:/blender-addons', 'D:/books', 'D:/class-notes', 'D:/games',
                            'D:/msys2', 'D:/music', 'D:/python-venv'],
        "file_extensions": [1, 2, 3, 4, 5, 6, 7],
    },
    "Default_3": {
        "name": "Default_3",
        "path": "C:\\Users\\Ommar\\Desktop\\temp\\default.db",
        "files_monitored": ['D:/Apollo', 'D:/Blender2.92', 'D:/Blockchain-project', 'D:/Program Files',
                            'D:/Temp', 'D:/blender-addons', 'D:/books', 'D:/class-notes', 'D:/games',
                            'D:/msys2', 'D:/music', 'D:/python-venv'],
        "file_extensions": [1, 2, 3, 4, 5, 6, 7],
    }
}
CURRENTDB = "Default"

class FileScanner_Thread(QThread): # untested
    """
    Threads that scans for all files metadata
    """
    def __init__(self, DB):
        """
        File scanner sub thread that launches,scans and fills file metadata into the database.
        """
        super().__init__()
        self.setObjectName("FileScanner")
        self.FileManager = FileManager()
        self.DB = DB

    def connect(self, DB: str):
        """
        Launches a thread specific connection to the given DB

        :Args:
            DB: Database filepath
        """
        self.FileManager.connect(DB)
        return self.FileManager.IsConneted()

    def setQueue(self, queue: Queue):
        """
        Sets the Queue that holds the directory names to scan.

        :Args:
            Queue: File name queue
        """
        self.Queue = queue

    def scannerSlot(self, path):
        """
        Interface for caller to be reimplemented
        """
        pass
    
    def run(self):
        """
        Main Thread executor that runs the scanner.
        """
        try:
            if self.connect(self.DB):
                while self.Queue.not_empty:
                    item = self.Queue.get() 
                    self.FileManager.ScanDirectory(item[0], item[1], self.scannerSlot)
            self.FileManager.close_connection()
            self.finished.emit()
            self.SCANNING = False
            self.scannerSlot("Scan Completed")
        
        except Exception as e:
            print(e)
            self.finished.emit()
            self.FileManager.close_connection()
            self.SCANNING = False


class FileScanner:
    """
    Main Filescanner instance that manages the file scanner thread
    """
    def __init__(self, Label):
        """Constructor"""
        self.ScannerQueue = Queue()
        self.SCANNING = False
        self.Label = Label

    def setLabelMsg(self, msg: str):
        """
        Sets the log message to the statusbar.

        :Args:
            msg: Msg to display out
        """
        self.Label.showMessage(msg)

    def addItem(self, item: ["Path", ["Filters", "Filters", "Filters"]]):
        """
        Adds a new item to the file scanner queue that the scanner thread uses to scan directories
        """
        self.ScannerQueue.put(item)

    def start(self, DB: str):
        """
        launches the scanner when the scan command is called

        :Args:
            DB: Database file name
        """
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

        elif self.SCANNING == True:
            # ignores the scann call as a thread is currently running
            print("Thread Scanning Directory")

        else:
            pass
        
        return self.SCANNING

class DBnameFileExp(FileExplorer):
    
    def __init__(self):
        super().__init__()
        self.subwindow_init()
        self.UI_Bindings()
        
    def subwindow_init(self):
        self.LEDT_Dialog = LEDT_Dialog()
        self.LEDT_Dialog.buttonBox.rejected.connect(lambda: self.LEDT_Dialog.close())
        self.treeView.doubleClicked.connect(lambda x: self.Create_DataBase())
        
    def closeEvent(self, Event):
        self.LEDT_Dialog.close()        
        
    def UI_Bindings(self):
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.RequestContextMenu)
            
    def RequestContextMenu(self, Point):
        MainMenu = QtWidgets.QMenu()
        MainMenu.addAction("Add New Folder").triggered.connect(self.Add_New_Folder)
        MainMenu.addAction("Rename Folder").triggered.connect(self.Rename_Folder)
        MainMenu.addAction("Delete Folder").triggered.connect(self.Delete_Folder)
        MainMenu.addAction("Create DataBase").triggered.connect(self.Create_DataBase)
    
        Cursor = QtGui.QCursor()
        MainMenu.exec_(Cursor.pos())        
        
    def acceptText(self, text):
        if text in ["", " "]:
            return False
        if re.search("[<>:/\\|?*\"]|[\0-\31]", text):
            return False
        else:
            return True            
                             
    def Add_New_Folder(self):
        
        def CreateDirectory():
            Index = list(map(lambda x: self.FilePathModel.filePath(x), self.treeView.selectedIndexes()))
            if len(Index) != 0 and self.acceptText(self.LEDT_Dialog.lineEdit.text()):                
                path = os.path.normpath(os.path.join(Index[0], self.LEDT_Dialog.lineEdit.text()))
                os.mkdir(path)
            self.LEDT_Dialog.close()
                      
        self.LEDT_Dialog.setWindowTitle("Add New Folder")
        self.LEDT_Dialog.lineEdit.clear()        
        self.LEDT_Dialog.show()
        self.LEDT_Dialog.buttonBox.accepted.connect(CreateDirectory)                
        
    def Rename_Folder(self):
        
        def MoveDirectory():
            Index = list(map(lambda x: self.FilePathModel.filePath(x), self.treeView.selectedIndexes()))
            if len(Index) != 0 and self.acceptText(self.LEDT_Dialog.lineEdit.text()):
                src = Index[0]
                if (not os.path.ismount(src)):                                
                    dest = os.path.normpath(os.path.join(os.path.split(src)[0], self.LEDT_Dialog.lineEdit.text()))
                    os.rename(src, dest)
                    self.LEDT_Dialog.close()
                      
        self.LEDT_Dialog.setWindowTitle("Rename Folder")
        self.LEDT_Dialog.lineEdit.clear()        
        self.LEDT_Dialog.show()
        self.LEDT_Dialog.buttonBox.accepted.connect(MoveDirectory)
        
        
    def Delete_Folder(self):        
        Index = list(map(lambda x: self.FilePathModel.filePath(x), self.treeView.selectedIndexes()))
        if len(Index) != 0:
            src = Index[0]
            if (not os.path.ismount(src)):                                
                shutil.rmtree(src)
                self.LEDT_Dialog.close()
                                      
    def SelectedPath(self):
        Index = list(map(lambda x: self.FilePathModel.filePath(x), self.treeView.selectedIndexes()))
        if len(Index) != 0:
            src = Index[0]                               
            return src
        else:
            return ""        
                
    def Create_DataBase(self): ...
                            
                              
class MusicFolder_FileExp(FileExplorer):
    
    def __init__(self):
        super().__init__(_type = "checkbox")
        self.UI_Bindings()
        
    def UI_Bindings(self): ...
        
    
class LibraryManagerTab: 
    
    def __init__(self, UI: ApolloLibraryManager, Setup = True):
        """
        Library Manager Tab
        Manages all library related functions.
        
        TODO:
        Binding path management and context menu function for File Exp
        """
        self.UI = UI
        self.FileExt = [".mp3", ".flac", ".m4a", ".wav"] # supported Files
        if Setup:
            self.SetUp()
        
    def SetUp(self): # No Tests Needed
        """
        setup funtion that calls all the sub functions. that init and populate the UI. 
        """
        self.DeclareSuWindows()
        self.UI_Bindings()
        self.PopulateCMBX(self.UI.apollo_CMBX_LBM_libname)
        self.PopulateUI(self.UI.CurrentDB)
        
    def DeclareSuWindows(self):
        """
        initilizes and declares all te subwindows
        """
        self.DBFileExp = DBnameFileExp()
        self.DBFileExp.Create_DataBase = self.Create_NewDB
        self.DBFileExp.buttonBox.accepted.connect(self.DBFileExp.close)
        self.DBFileExp.buttonBox.rejected.connect(self.DBFileExp.close)
        
        self.MusicFileExp = MusicFolder_FileExp()
        self.MusicFileExp.buttonBox.accepted.connect(lambda: self.UpdateFilesMon())
        
        self.FileScanner = FileScanner(self.UI.statusBar)
        
    def call_MusicFileExp(self): # UI dependent
        """
        calls the FileExplorer for the files to be added for scanning and updating the database
        """
        self.MusicFileExp.FilePathModel.checkStates = {}
        model = self.UI.apollo_LBM_LSV_filesmon.model()
        for item in range(model.rowCount()):
            path = model.index(item, 0).data()
            if os.path.isdir(path):
                self.MusicFileExp.FilePathModel.checkStates[path] = QtCore.Qt.Checked
        self.MusicFileExp.show()
        self.MusicFileExp.raise_()    
        
    def CloseSubWindows(self):
        self.DBFileExp.close()
        self.MusicFileExp.close()
        
    def UI_Bindings(self): # No Tests Needed
        """
        Binda all the UI elements with all the valid functions.
        """
        def pressed(UI, Function):
            UI.pressed.connect(Function)
            
        self.UI.apollo_CMBX_LBM_libname.currentTextChanged.connect(self.PopulateUI)
        self.UI.apollo_LEDT_LBM_dbname.textChanged.connect(self.DBname_TextChange)
        
        pressed(self.UI.apollo_PSB_LBM_libnext, (lambda: self.IterComboBox(1, self.UI.apollo_CMBX_LBM_libname)))
        pressed(self.UI.apollo_PSB_LBM_libprev, (lambda: self.IterComboBox(-1, self.UI.apollo_CMBX_LBM_libname)))
        pressed(self.UI.apollo_PSB_LBM_active, (self.setActiveDB))
        pressed(self.UI.apollo_PSB_LBM_libadd, (self.Get_Data))
        pressed(self.UI.apollo_PSB_LBM_export, (self.ExportLibrary))
        pressed(self.UI.apollo_PSB_LBM_import, (self.ImportLibrary))
        pressed(self.UI.apollo_PSB_LBM_libremove, (self.RemoveLibrary))
        pressed(self.UI.apollo_PSB_LBM_librescan, (self.RescanLibrary))
        pressed(self.UI.apollo_PSB_LBM_libpathedit, (lambda: (self.DBFileExp.show(), self.DBFileExp.raise_())))
        pressed(self.UI.apollo_PSB_LBM_fileadd, self.call_MusicFileExp)
        pressed(self.UI.apollo_PSB_LBM_fileremove, self.RemoveFilesMon)
        pressed(self.UI.apollo_PSB_LBM_filerescan, self.Rescan_File)
        
    def Create_NewDB(self): # No tests, but works
        """
        Creates a New DB inside the given parent directory.
        """
        name = self.UI.apollo_LEDT_LBM_dbname.text()
        name = name.lower().replace(" ", "_").replace("-", "_")
        if self.DBFileExp.acceptText(name):            
            path = os.path.normpath(os.path.join(self.DBFileExp.SelectedPath(), f"{name}.db"))       
            self.UI.apollo_LEDT_LBM_dbpath.setText(path)
            if self.UI.DBManager.connect(path):
                self.UI.DBManager.close_connection()
        else:
            self.UI.statusBar.showMessage("DB Path Not valid")
                
        
    def DBname_TextChange(self, text): # No Tests Needed
        """
        Called when the DB name and populate the UI if the DB is monitored and
        clears the UI of the DB is not mOnitored

        :Args:
        text: str
            the DB text name
        """
        if text in self.UI.DB_Monitored.keys():
            self.PopulateUI(text)
        else:
            self.UI.apollo_LEDT_LBM_dbpath.clear()            
            self.UI.apollo_LBM_LSV_filesmon.setModel(QtGui.QStandardItemModel())
            self.UI.apollo_LBM_LSV_filters.setModel(QtGui.QStandardItemModel())
            self.UI.apollo_LEDT_LBM_topalbum.setText("")
            self.UI.apollo_LEDT_LBM_topgenre.setText("")
            self.UI.apollo_LEDT_LBM_toptrack.setText("")
            self.UI.apollo_LEDT_LBM_topartist.setText("")
            self.UI.apollo_LEDT_LBM_totalbum.setText("")
            self.UI.apollo_LEDT_LBM_totartist.setText("")
            self.UI.apollo_LEDT_LBM_totplay.setText("")
            self.UI.apollo_LEDT_LBM_tottrack.setText("")
            self.UI.apollo_LEDT_LBM_totsize.setText("")
            self.UI.apollo_LEDT_LBM_totplaytime.setText("")            
            
    def PopulateUI(self, DBname): # No Tests Needed
        """
        populate the complete UI with the DB info and stats.        

        :Args:
        DBname: str
            the DB text name
        """

        DBInfo = self.UI.DB_Monitored.get(DBname)
        if DBInfo == None:
            return None
            
        DBpath = DBInfo.get("path")
        DBfiles = DBInfo.get("files_monitored")
        DBext = DBInfo.get("file_extensions")
        self.UI.DBManager.connect(DBpath)
                
        self.UI.apollo_LEDT_LBM_dbname.setText(DBname)
        self.UI.apollo_LEDT_LBM_dbpath.setText(DBpath)
        
        self.PopulateFilesMonitored(DBfiles)        
        self.PopulateFileExt(DBext)        
        self.PopulateStats()
        
        self.UI.DBManager.close_connection()      

    def PopulateStats(self): # No Tests Needed
        """
        Queries the DB and gets the DB stats.
        """
        self.UI.apollo_LEDT_LBM_topalbum.setText(str(self.UI.DBManager.TopAlbum())) 
        self.UI.apollo_LEDT_LBM_topgenre.setText(str(self.UI.DBManager.Topgenre()))
        self.UI.apollo_LEDT_LBM_toptrack.setText(str(self.UI.DBManager.Toptrack()))
        self.UI.apollo_LEDT_LBM_topartist.setText(str(self.UI.DBManager.Topartist()))
        self.UI.apollo_LEDT_LBM_totalbum.setText(str(self.UI.DBManager.TableAlbumcount()))  
        self.UI.apollo_LEDT_LBM_totartist.setText(str(self.UI.DBManager.TableArtistcount()))
        self.UI.apollo_LEDT_LBM_totplay.setText(str(self.UI.DBManager.TablePlaycount()))
        self.UI.apollo_LEDT_LBM_tottrack.setText(str(self.UI.DBManager.TableTrackcount()))
        self.UI.apollo_LEDT_LBM_totsize.setText(f'{self.UI.DBManager.TableSize()} GB')
        self.UI.apollo_LEDT_LBM_totplaytime.setText(str(self.UI.DBManager.TablePlaytime()))
        
    def PopulateFileExt(self, DBext): # Tested
        """
        Populate the LSV with the file extension data that are filtered.
        
        :Args:
        DBext: list[str, str, str]
            file extensions that is used to scan the FS
        """
        if len(DBext) > len(self.FileExt):
            DBext = DBext[0:len(self.FileExt)]
        Filesext = QtGui.QStandardItemModel()        
        Column = []
        for Item, State in zip(self.FileExt, DBext):
            Item = QtGui.QStandardItem(Item)
            Item.setCheckable(True)
            Item.setTristate(False)
            if State == 0:               
                Item.setCheckState(QtCore.Qt.Unchecked)
            else:
                Item.setCheckState(QtCore.Qt.Checked)
            Column.append(Item)            
        Filesext.appendColumn(Column)
        self.UI.apollo_LBM_LSV_filters.setModel(Filesext)
        
    def PopulateFilesMonitored(self, DBfiles):  
        """
        Populate the LSV with the file path data that are filtered.
        
        :Args:
        DBfiles: list[str, str, str]
            file path that is used to scan the FS
        """  
        Filesmodel = QtGui.QStandardItemModel()        
        Column = []
        for Item in map(str, DBfiles):
            Item = QtGui.QStandardItem(str(Item))
            Item.setCheckable(True)
            Item.setTristate(False)
            Item.setCheckState(QtCore.Qt.Checked)
            Column.append(Item)            
        Filesmodel.appendColumn(Column)       
        self.UI.apollo_LBM_LSV_filesmon.setModel(Filesmodel)
        
    
    def PopulateCMBX(self, CMBX: QtWidgets.QComboBox, Data = None): # Tested
        """
        Populates the CMBX with the data provided

        :Args:
        CMBX: QtWidgets.QComboBox
            Combobox with all the DB names.
        Data: list[str, str, str]
            data to fill in the combobox
        """
        if Data == None:
            DBnames = self.UI.DB_Monitored.keys()
        else:
            DBnames = Data
            
        [CMBX.removeItem(item) for item in range(CMBX.count())]
        CMBXitems = [CMBX.itemText(item) for item in range(CMBX.count())]
        for Name in DBnames:
            if Name not in CMBXitems:
                CMBX.addItem(Name)
                
        
    def Get_FileExt(self): # Tested
        """
        Gets the file extensions and their check state
        """
        Model = self.UI.apollo_LBM_LSV_filters.model()
        Ext_state = [Model.index(r, 0).data(QtCore.Qt.CheckStateRole) for r in range(Model.rowCount())]
        if Ext_state == []:
            return Ext_state
        Ext_state = [state for indx, state in enumerate(self.FileExt) if Ext_state[indx] == 2]
        return Ext_state
        
    def Get_FileMon(self): # Tested
        """
        Gets the file paths and their check state
        """
        Model = self.UI.apollo_LBM_LSV_filesmon.model()
        file_paths = [Model.index(r, 0).data() for r in range(Model.rowCount())]
        return file_paths
    
    def Get_Data(self):
        DBname = self.UI.apollo_LEDT_LBM_dbname.text()
        if DBname in ["", " "]:
            self.UI.statusBar.showMessage("DB name is empty")
            return None    
        else:                
            DBnewname = DBname.replace(" ", "_").replace("-", "_").lower() + ".db"
                    
        # root path bug, raise an error
        DBpath = self.UI.apollo_LEDT_LBM_dbpath.text()
        if DBpath in ["", " "]:
            self.UI.statusBar.showMessage("DB path is empty")
            return None            
        else:
            if DBpath.find("\\"):
                DBpath = os.path.join(f"{os.path.split(DBpath)[0]}", DBnewname)
            else:                
                DBpath = os.path.join(f"{DBpath}", DBnewname)
                
        
        DBfile_ext = self.Get_FileExt()
        DBfile_Paths = self.Get_FileMon()
        
        print(DBname, DBpath, DBfile_ext, DBfile_Paths)

    
    def IterComboBox(self, direction: int, CMBX: QtWidgets.QComboBox): # Tested
        """
        Iters and loads the corresponding for all the DB that have been declared for Apollo

        :Args:
        direction: int
            Direction for the list to iter in (Forward/Backward)
        CMBX: QtWidgets.QComboBox
            Combobox with all the DB names.
        """
        Index = CMBX.currentIndex() + (direction)
        if Index == CMBX.count():
            Index = 0
        elif Index < 0:
            Index = CMBX.count() - 1
        else:
            pass
        CMBX.setCurrentIndex(Index)   
        
    def UpdateFilesMon(self):
        """"""
        Files = self.MusicFileExp.get_FilePath()
        self.PopulateFilesMonitored(Files)
        self.MusicFileExp.close()
        
    def RemoveFilesMon(self):
        """
        Issues:
        rows deletion fails
        """
        model = self.UI.apollo_LBM_LSV_filesmon.model()
        selected = list(map(lambda x: x.row(), self.UI.apollo_LBM_LSV_filesmon.selectedIndexes()))        
        if len(selected) == model.rowCount():
            self.UI.apollo_LBM_LSV_filesmon.setModel(QtGui.QStandardItemModel())
            return None                
        
        if selected != 0:                        
            model.beginRemoveRows(QtCore.QModelIndex(), selected[0], selected[-1])
            for r in selected:
                print(model.removeRow(r))
            model.endRemoveRows()
        
    def setActiveDB(self):
        DBname = self.UI.apollo_CMBX_LBM_libname.currentText()
        print(DBname)
        
    def ImportLibrary(self):
        print("Not Implemented")
    
    def ExportLibrary(self):
        print("Not Implemented")
        
    def RemoveLibrary(self):
        RemoveDB = self.UI.apollo_LEDT_LBM_dbname.text()
        if RemoveDB == "":
            return None
        
        self.UI.DB_Monitored.pop(RemoveDB)
        self.UI.apollo_LEDT_LBM_dbname.setText('')
        self.PopulateCMBX(self.UI.apollo_CMBX_LBM_libname)        
        self.UI.CurrentDB = self.UI.apollo_CMBX_LBM_libname.currentText()
        
        print(self.UI.CurrentDB)
        
    def Rescan_File(self):
        selected = list(map(lambda x: os.path.normpath(x.data()), self.UI.apollo_LBM_LSV_filesmon.selectedIndexes()))
        model = self.UI.apollo_LBM_LSV_filters.model()
        EXT = [model.index(r, 0).data() for r in range(model.rowCount())]
        for file in selected:            
            self.FileScanner.addItem([file, EXT])
        self.FileScanner.start(self.UI.apollo_LEDT_LBM_dbpath.text())        
    
    def RescanLibrary(self):
        model = self.UI.apollo_LBM_LSV_filesmon.model()
        selected = [model.index(r, 0).data() for r in range(model.rowCount())]

        model = self.UI.apollo_LBM_LSV_filters.model()
        EXT = [model.index(r, 0).data() for r in range(model.rowCount())]
        for file in selected:            
            self.FileScanner.addItem([file, EXT])
        self.FileScanner.start(self.UI.apollo_LEDT_LBM_dbpath.text())
            
                  
class FileManagerTab: 
    
    def __init__(self, UI: ApolloLibraryManager):
        self.UI = UI


class ApolloLibraryManager(Ui_MainWindow, QtWidgets.QMainWindow):
    """"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.setupUi(self)        
    
        self.DBManager = DataBaseManager()
        self.LibraryManagerTab = LibraryManagerTab(self)
        self.FileManagerTab = FileManagerTab(self)

    def closeEvent(self, Event):
        self.LibraryManagerTab.CloseSubWindows()

    @property
    def CurrentDB(self):
        return CURRENTDB
    
    @CurrentDB.setter
    def CurrentDB(self, value):
        CURRENTDB = value
    
    @property
    def DB_Monitored(self):
        return TEMPCONFIG
    
    @DB_Monitored.setter
    def DB_Monitored(self, value):
        TEMPCONFIG = value
      
if __name__ == "__main__":
    from apollo.resources.apptheme.theme import Theme
    from apollo.resources.apptheme import style
    
    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")
    UI = ApolloLibraryManager()
        
    
    def LoadTheme():
        with open("stylesheet.css") as sheet:
            stylesheet = sheet.read().split("\n")
            stylesheet = Theme().GenStylesheet(pallete = eval(Theme().DefaultPallete())["THEME"], stylesheet = stylesheet)
            app.setStyleSheet(stylesheet)
        
    LoadTheme()
    
    UI.apollo_PSB_LBM_import.pressed.connect(LoadTheme)
    UI.apollo_PSB_MDE_undo.pressed.connect(LoadTheme)
    #Timer = QtCore.QTimer()
    #Timer.setInterval(300)
    #Timer.timeout.connect(LoadTheme)
    #Timer.start()
    
    UI.show()
    app.exec_()