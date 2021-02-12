import sys, os, re, datetime, re, hashlib, json, time

import mutagen
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from apollo.utils import exe_time, dedenter, ThreadIt, ConfigManager
from apollo.db.library_manager import DataBaseManager, LibraryManager, ModelView_Manager, FileManager
from apollo.gui.library_manager_ui import Ui_MainWindow
from apollo.app.utils_app.file_explorer import FileExplorer
from apollo.gui.LEDT_dialog_ui import LEDT_Dialog

# TODO
# review for bugs
# write docs

# adding creating new folder for adding new DB

class ApolloLibraryManager(Ui_MainWindow, QtWidgets.QMainWindow):
    """"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.setupUi(self)
        self.CONFG = ConfigManager()
        self.filters = self.ScanningFilters()
        self.UIfunction_Binding()
        
        
    def ScanningFilters(self):
        """
        defines the scanning filters for the File Manager
        """
        filters = ["mp3",
                    "flac", 
                    "aac", 
                    "wav"]
        return filters
    

    def UIfunction_Binding(self):
        """
        Binds UI with their corresponding functions
        """
        for Value in self.CONFG.Getvalue("MONITERED_DB").keys():
            self.populate_DBinfo(Value)

        self.LBM_LEDT_path.setReadOnly(True)
        self.LBM_LEDT_name.textChanged.connect(self.DBnameChanged)

        self.LEDT = LEDT_Dialog()

        self.LBM_CMBX_dbname.currentTextChanged.connect(self.populate_DBinfo)
        self.LBM_PSB_back.pressed.connect(lambda: self.iter_ComboBox(-1))
        self.LBM_PSB_fowd.pressed.connect(lambda: self.iter_ComboBox(1))
        self.LBM_PSB_libadd.pressed.connect(self.get_DBdata)

        self.FileExp_DB = FileExplorer()
        self.LBM_PSB_fileexp.pressed.connect(self.FileExp_DB.show)
        self.FileExp_DB.treeView.doubleClicked.connect(lambda index: self.add_NewDBpath(self.FileExp_DB.get_Path(index)))
        self.FileExp_DB.buttonBox.accepted.connect(lambda: (self.FileExp_DB.close(), self.LEDT.close()))
        self.FileExp_DB.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.FileExp_DB.treeView.customContextMenuRequested.connect(self.ContextMenu_FileExp_FilesDB)

        self.FileExp_Files = FileExplorer(_type = "checkbox")
        self.LBM_PSB_fileexp_2.pressed.connect(self.call_FileExplorer)
        self.FileExp_Files.buttonBox.accepted.connect(lambda: self.add_NewFiles(self.FileExp_Files.get_FilePath()))

        self.LBM_LSV_filesmon.setContextMenuPolicy(Qt.CustomContextMenu)
        self.LBM_LSV_filesmon.customContextMenuRequested.connect(self.ContextMenu_FileMonitor)


    def ContextMenu_FileMonitor(self):
        """
        Context Menu defination
        """
        main = QtWidgets.QMenu()
        main.addAction("Remove Directory").triggered.connect(lambda: self.remove_Dir(self.LBM_LSV_filesmon))
        main.addAction("Rescan Directory").triggered.connect(lambda: self.rescan_Dir(self.LBM_LSV_filesmon))

        cur = QtGui.QCursor()
        main.exec_(cur.pos())


    def ContextMenu_FileExp_FilesDB(self):
        """
        Context Menu defination
        """        
        main = QtWidgets.QMenu()
        main.addAction("Add Sub Folder").triggered.connect(self.add_Dir)
        main.addAction("Select Folder").triggered.connect(self.select_Dir)
        
        cur = QtGui.QCursor()
        main.exec_(cur.pos())


    def remove_Dir(self, View: QtWidgets.QListView):
        """
        Removes a fileitem for being monitored
        """
        index = View.selectedIndexes()
        model = View.model()
        model.removeRow(index[0].row())
        
    def rescan_Dir(self, View: QtWidgets.QListView):    
        """
        Rescans a particular directory
        """
        index = View.selectedIndexes()
        print(index)
        
    def add_Dir(self):
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
            self.LEDT.close()
        
        index = self.FileExp_DB.treeView.selectedIndexes()
        path = self.FileExp_DB.FilePathModel.filePath(index[0])
        
        # LineEdit Defination
        self.LEDT.setWindowTitle("Add Folder to Parent")
        self.LEDT.buttonBox.accepted.connect(lambda: add_DirtoFS(os.path.join(path, self.LEDT.lineEdit.text())))
        self.LEDT.buttonBox.rejected.connect(self.LEDT.close)
        self.LEDT.show()
        
    def select_Dir(self):
        """
        Selects the Directory at the given index
        """
        index = self.FileExp_DB.treeView.selectedIndexes()
        path = self.FileExp_DB.FilePathModel.filePath(index[0])
        self.add_NewDBpath(path)
        

    def call_FileExplorer(self):
        """
        calls the FileExplorer for the files to be added for scanning and updating the database
        """
        model = self.LBM_LSV_filesmon.model()
        for item in range(model.rowCount()):
            path = model.index(item, 0).data()
            if os.path.isdir(path):
                self.FileExp_Files.FilePathModel.checkStates[path] = Qt.Checked
        self.FileExp_Files.show()


    def DBnameChanged(self):
        """
        Called when a DB name is chaned and clears if the field is cleared for editing
        """
        Data = self.LBM_LEDT_name.text()
        if (Data in [self.LBM_CMBX_dbname.itemText(item) for item in range(self.LBM_CMBX_dbname.count())]):
            self.populate_DBinfo(Data)
        else:
            self.LBM_LEDT_path.clear()
            self.LBM_LSV_filesmon.setModel(QtGui.QStandardItemModel())
            filtersmodel = QtGui.QStandardItemModel()
            for itemname in self.filters:
                item = QtGui.QStandardItem(str(itemname))
                item.setCheckable(True)
                item.setCheckState(Qt.Unchecked)               
                filtersmodel.appendRow(item)
            self.LBM_LSV_filters.setModel(filtersmodel)
            
            

    def add_NewFiles(self, Files: list):
        """
        Adds the files that are being monitored that for the current DB

        :Args:
            Files: Files that needed to be added to the ListView
        """
        files = Files
        filesmodel = QtGui.QStandardItemModel()
        for item in files:
            filesmodel.appendRow(QtGui.QStandardItem(str(item)))
        self.LBM_LSV_filesmon.setModel(filesmodel)
        self.FileExp_Files.close()
        self.FileExp_Files.FilePathModel.checkStates = {}


    def add_NewDBpath(self, Path: str):
        """
        Called when a new name is entered and generates the corresponding path

        :Args:
            Path: Path of the new databse directory
        """
        name = self.LBM_LEDT_name.text().lower()
        # checks is the file name entered already exists or not
        if os.path.isfile(os.path.normpath(os.path.join(Path, f"{name}.db"))):
            self.statusbar.showMessage('File already exists')

        # checks for unaccepted names
        if all([(name != ""), (name != " "), name.isalnum()]):
            Path = os.path.normpath(os.path.join(Path, f"{name}.db"))
            self.LBM_LEDT_path.setText(Path)
        else:
            self.statusbar.showMessage('File name not valid')


    def iter_ComboBox(self, direction: int):
        """
        Iters and loads the corresponding for all the DB taht have been declared for Apollo

        :Args:
            direction: Direction for the list to iter in (Forward/Backward)
        """
        Index = self.LBM_CMBX_dbname.currentIndex() + (direction)
        if Index == self.LBM_CMBX_dbname.count():
            Index = 0
        if Index < 0:
            Index = self.LBM_CMBX_dbname.count() - 1
        self.LBM_CMBX_dbname.setCurrentIndex(Index)


    def populate_ComboBox(self, Data):
        """
        Populates the Combobox with new DB names

        :Args:
            Data: Unique Dataitem to add to the list
        """
        if not (Data in [self.LBM_CMBX_dbname.itemText(item) for item in range(self.LBM_CMBX_dbname.count())]):
            self.LBM_CMBX_dbname.addItem(Data)


    def populate_DBinfo(self, Data):
        """
        When a new DB name is loaded the corresponding data is loaded for the UI

        :Args:
            Data: name of the DB to load data for
        """
        DataDict = self.CONFG.Getvalue("MONITERED_DB")
        DataDict = (DataDict).get(Data)

        self.populate_ComboBox(DataDict.get("name"))
        self.LBM_LEDT_name.setText(DataDict.get("name"))
        self.LBM_LEDT_path.setText(DataDict.get("db_loc"))

        files = DataDict.get("file_mon")
        filesmodel = QtGui.QStandardItemModel()
        for item in files:
            filesmodel.appendRow(QtGui.QStandardItem(str(item)))
        self.LBM_LSV_filesmon.setModel(filesmodel)

        filtersEN = DataDict.get("filters")
        filtersmodel = QtGui.QStandardItemModel()
        for itemname in self.filters:
            item = QtGui.QStandardItem(str(itemname))
            item.setCheckable(True)
            if itemname in filtersEN:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)               
            filtersmodel.appendRow(item)
        self.LBM_LSV_filters.setModel(filtersmodel)


    def get_DBdata(self):
        """
        Retrieves and Stores the New data declared for the New DB
        """
        if not (self.LBM_LEDT_name.text() in self.CONFG.Getvalue("MONITERED_DB").keys()):
            DBdata = {}
            
            # gets the new DB name
            DBdata["name"] = self.LBM_LEDT_name.text()
            # gets thye new DB location
            DBdata["db_loc"] = self.LBM_LEDT_path.text()
            if self.LBM_LEDT_path.text() == "":
                self.statusbar.showMessage('Enter File name')
                return

            # gets the files to be monitored
            model = self.LBM_LSV_filesmon.model()
            DBdata["file_mon"] = [model.index(row, 0).data() for row in range(model.rowCount())]

            # sets the file scanning filter
            model = self.LBM_LSV_filters.model()
            filters = []
            for row in range(model.rowCount()):
                if model.index(row, 0).data(Qt.CheckStateRole) == 2:
                    filters.append(model.index(row, 0).data() )            
            DBdata["filters"] = filters
            
            # adds the data to the config
            self.CONFG.Setvalue(DBdata, f"MONITERED_DB/{DBdata['name']}")
            
            

if __name__ == "__main__":
    from apollo.resources.apptheme.theme import Theme

    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")
    app.setStyleSheet(Theme().GenStylesheet(eval(Theme().DefaultPallete())["THEME"]))

    UI = ApolloLibraryManager()
    UI.show()
    app.exec_()
