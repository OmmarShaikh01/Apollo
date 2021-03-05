import sys, os, itertools
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

DBFIELDS = ["file_id", "path_id","file_name","file_path","album",
            "albumartist","artist","author","bpm","compilation",
            "composer","conductor","date","discnumber","discsubtitle",
            "encodedby","genre","language","length","filesize",
            "lyricist","media","mood","organization","originaldate",
            "performer","releasecountry","replaygain_gain","replaygain_peak",
            "title","tracknumber","version","website","album_gain",
            "bitrate","bitrate_mode","channels","encoder_info","encoder_settings",
            "frame_offset","layer","mode","padding","protected","sample_rate",
            "track_gain","track_peak", "rating", "playcount"]

ApolloLibraryManager = 1
currentdb = "Default"
tempconfig = {
    "Default": {
        "name": "Default",
        "db_loc": "D:\\Apollo\\apollo\\db\\default.db",
        "file_mon": [
            "D:/music"
        ],
        "filters": ['.mp3', '.flac', '.aac', '.wav']
    }
}


class FileScanner_Thread(QThread):
    """"""

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

    def scannerSlot(self, path): ...
    def run(self):
        """
        Main Thread executor that runs the scanner.
        """
        try:
            self.connect(self.DB)
            if self.FileManager.IsConneted():
                while self.Queue.not_empty:
                    item = self.Queue.get()
                    self.FileManager.ScanDirectory(item[0], item[1], self.scannerSlot)
            self.FileManager.close_connection()
            self.finished.emit()
            self.SCANNING = False

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

    def addItem(self, item: ["Path", "Filters"]):
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
            filesmodel.appendRow(QtGui.QStandardItem(str(os.path.normpath(item))))
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



class App_MetadataManager:
    """
    Supports:
    -> .mp3
    -> .flac
    -> .m4a
    """
    def __init__(self, UI: ApolloLibraryManager):
        """Constructor"""
        self.UI = UI
        self.FileManager = FileManager()
        self.init_UIbindings()

    def init_UIbindings(self):
        self.init_FilesMonitor()
        self.populate_DataView("D:\\music\\theclock.mp3")

        self.UI.MDE_PSB_save.pressed.connect(self.save_DataView)
        self.UI.MDE_CMBX_cover.currentTextChanged.connect(self.change_CoverImage)

    def init_FilesMonitor(self):
        if self.FileManager.connect(tempconfig[currentdb]["db_loc"]):
            Query = self.FileManager.ExeQuery("SELECT file_path FROM library")
            data = self.FileManager.fetchAll(Query)
            self.FileManager.close_connection()
            if len(data) >= 1:
                self.FilesMonitored = itertools.cycle(data)
            else:
                self.FilesMonitored = itertools.cycle([None])

    def iter_FilesMonitored(self):
        path = next(self.FilesMonitored)

    def save_DataView(self):
        print((self.getMetadata()))

    def getMetadata(self):
        metadata = dict.fromkeys(DBFIELDS, "")

        metadata["originaldate"] = str(self.UI.MDE_LEDT_orginaldate.text()).strip()
        metadata["artist"] = str(self.UI.MDE_LEDT_artist.text()).strip()
        metadata["album"] = str(self.UI.MDE_LEDT_album.text()).strip()
        metadata["author"] = str(self.UI.MDE_LEDT_author.text()).strip()
        metadata["date"] = str(self.UI.MDE_LEDT_date.text()).strip()
        metadata["composer"] = str(self.UI.MDE_LEDT_composer.text()).strip()
        metadata["conductor"] = str(self.UI.MDE_LEDT_conductor.text()).strip()
        metadata["title"] = str(self.UI.MDE_LEDT_title.text()).strip()
        metadata["discsubtitle"] = str(self.UI.MDE_LEDT_dsub.text()).strip()
        metadata["albumartist"] = str(self.UI.MDE_LEDT_albumartist.text()).strip()
        metadata["discnumber"] = str(self.UI.MDE_LEDT_dnum.text()).strip()
        metadata["tracknumber"] = str(self.UI.MDE_LEDT_tnum.text()).strip()
        metadata["genre"] = str(self.UI.MDE_LEDT_genre.text()).strip()
        metadata["website"] = str(self.UI.MDE_LEDT_website.text()).strip()
        metadata["releasecountry"] = str(self.UI.MDE_LEDT_releasecountry.text()).strip()
        metadata["mood"] = str(self.UI.MDE_LEDT_mood.text()).strip()
        metadata["lyricist"] = str(self.UI.MDE_LEDT_lyricist.text()).strip()
        metadata["organization"] = str(self.UI.MDE_LEDT_org.text()).strip()
        metadata["language"] = str(self.UI.MDE_LEDT_lang.text()).strip()
        metadata["version"] = str(self.UI.MDE_LEDT_version.text()).strip()
        metadata["performer"] = str(self.UI.MDE_LEDT_performer.text()).strip()
        metadata["media"] = str(self.UI.MDE_LEDT_media.text()).strip()
        metadata["encodedby"] = str(self.UI.MDE_LEDT_encoded.text()).strip()

        return metadata

    def populate_DataView(self, file):
        if os.path.isfile(file):
            self.UI.MDE_LEDT_filename.setText(os.path.split(file)[1])
            self.setMetadata(file)
            self.setCoverImage(file)

    def change_CoverImage(self, name = None):
        Image = QtGui.QPixmap()
        if name == None:
            Image.loadFromData(list(self.COVERDATA.values())[0])
        else:
            Image.loadFromData(self.COVERDATA.get(str(name).replace(" ", "_").upper()))
        self.UI.MDE_PIXLB_cover.setPixmap(Image)
        self.UI.MDE_PIXLB_cover.setScaledContents(True)

    def setCoverImage(self, file):
        self.COVERDATA = self.FileManager.get_CoverImage(file)
        self.change_CoverImage()
        [self.UI.MDE_CMBX_cover.removeItem(row) for row in range(self.UI.MDE_CMBX_cover.count())]
        self.UI.MDE_CMBX_cover.addItems(map(lambda x: str(x).replace("_", " ").title(), self.COVERDATA.keys()))

    def setMetadata(self, file):
        metadata = self.FileManager.ScanFile(os.path.normpath(file))

        self.UI.MDE_LEDT_orginaldate.setText(str(metadata.get("originaldate", "")))
        self.UI.MDE_LEDT_artist.setText(str(metadata.get("artist", "")))
        self.UI.MDE_LEDT_album.setText(str(metadata.get("album", "")))
        self.UI.MDE_LEDT_author.setText(str(metadata.get("author", "")))
        self.UI.MDE_LEDT_date.setText(str(metadata.get("date", "")))
        self.UI.MDE_LEDT_composer.setText(str(metadata.get("composer", "")))
        self.UI.MDE_LEDT_conductor.setText(str(metadata.get("conductor", "")))
        self.UI.MDE_LEDT_title.setText(str(metadata.get("title", "")))
        self.UI.MDE_LEDT_dsub.setText(str(metadata.get("discsubtitle", "")))
        self.UI.MDE_LEDT_albumartist.setText(str(metadata.get("albumartist", "")))
        self.UI.MDE_LEDT_dnum.setText(str(metadata.get("discnumber", "")))
        self.UI.MDE_LEDT_tnum.setText(str(metadata.get("tracknumber", "")))
        self.UI.MDE_LEDT_genre.setText(str(metadata.get("genre", "")))
        self.UI.MDE_LEDT_website.setText(str(metadata.get("website", "")))
        self.UI.MDE_LEDT_releasecountry.setText(str(metadata.get("releasecountry", "")))
        self.UI.MDE_LEDT_mood.setText(str(metadata.get("mood", "")))
        self.UI.MDE_LEDT_lyricist.setText(str(metadata.get("lyricist", "")))
        self.UI.MDE_LEDT_org.setText(str(metadata.get("organization", "")))
        self.UI.MDE_LEDT_lang.setText(str(metadata.get("language", "")))
        self.UI.MDE_LEDT_version.setText(str(metadata.get("version", "")))
        self.UI.MDE_LEDT_performer.setText(str(metadata.get("performer", "")))
        self.UI.MDE_LEDT_media.setText(str(metadata.get("media", "")))
        self.UI.MDE_LEDT_encoded.setText(str(metadata.get("encodedby", "")))

        RICHTEXT = ""
        HEADER = """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
        <html><head><meta name="qrichtext" content="1" /><style type="text/css">
        p, li { white-space: pre-wrap; }
        </style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;">
        """
        RICHTEXT += HEADER

        LINE = '<p style = "margin:0px; text-indent:0px;"> <span style=" font-size:10pt;">$TEXT</span></p>'
        RICHTEXT += LINE.replace("$TEXT", f"File Name: {metadata.get('file_name', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"File Path: {metadata.get('file_path', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Filesize: {metadata.get('filesize', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Bitrate Mode: {metadata.get('bitrate_mode', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Bitrate: {metadata.get('bitrate', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Length: {metadata.get('length', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Channels: {metadata.get('channels', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Album Gain: {metadata.get('album_gain', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Encoder Info: {metadata.get('encoder_info', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Encoder Settings: {metadata.get('encoder_settings', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Frame Offset: {metadata.get('frame_offset', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Layer: {metadata.get('layer', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Mode: {metadata.get('mode', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Padding: {metadata.get('padding', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Protected: {metadata.get('protected', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Track Gain: {metadata.get('track_gain', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Track Peak: {metadata.get('track_peak', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Version: {metadata.get('version', '')}")
        RICHTEXT += LINE.replace("$TEXT", f"Sample Rate: {metadata.get('sample_rate', '')}")

        FOOTER = """</body></html>"""
        RICHTEXT += FOOTER

        self.UI.MDE_TXBRW_mediainfo.setText(dedenter(RICHTEXT, 8))

    def close(self):
        """
        controls safe exit of the subwindow
        """


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
        self.MetadataManager = App_MetadataManager(UI = self)

    def closeEvent(self, event):
        self.DBmanager.close()
        self.MetadataManager.close()


if __name__ == "__main__":
    from apollo.resources.apptheme.theme import Theme
    from apollo.resources.apptheme import style


    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")

    LoadTheme = lambda: (app.setStyleSheet(Theme().GenStylesheet(eval(Theme().DefaultPallete())["THEME"])))
    LoadTheme()

    UI = ApolloLibraryManager()
    UI.LBM_PSB_libimport.pressed.connect(LoadTheme)
    UI.MDE_PSB_cancel.pressed.connect(LoadTheme)
    UI.show()
    app.exec_()
