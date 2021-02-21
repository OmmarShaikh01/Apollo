import sys, os, re, datetime, re, hashlib, json, time, pathlib

import mutagen
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from apollo.utils import exe_time, dedenter, ThreadIt

import apollo
root_path = apollo.__path__

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

########################################################################################################################

class DataBaseManager:
    """
    Base class for all th sql related function and queries
    """
    def __init__(self):
        """
        Initilizes the Databse Driver and connects to DB and Initilizes the
        fields for the Database Tables
        """
        self.db_fields = DBFIELDS
        
    def connect(self, db, name = "ConnectionMain"): #Tested
        """
        Uses the Database Driver to create a connection with a local
        database.If Db not avaliable will create new Db

        >>> library_manager.connect("default.db")

        :Args:

            db: String
                path of a Valid Database or a Database name in order to
                create a blank one

        :Errors:
            ConnectionError: if database fails to connect or fails checks
        """
        if not ((os.path.splitext(db)[1] in [".db"]) or (db == ":memory:")):
            return False

        if not ((os.path.isfile(db)) or (db == ":memory:")):
            with open(db, "w"):
                pass

        self.db_driver = QSqlDatabase.addDatabase("QSQLITE")
        self.db_driver.setUserName(name)
        self.db_driver.setDatabaseName(db)
        if self.IsConneted():
            if not self.StartUpChecks():
                raise Exception("DB structure Invalid")
            else:
                return True
        else:
            raise ConnectionError()

    def IsConneted(self): #Tested
        if self.db_driver.open() and self.db_driver.isValid():           
            return True
        else:
            return False
            
    def fetchAll(self, Query, rows = None):
        """
        Fetches data from the given query
        
        >>> library_manager.fetchAll(Query, 5)
        """
        Data = []
        if rows == None:
            rows = Query.record().count()
        while Query.next():
            Data.append([Query.value(R) for R in range(rows)])
            
        return Data

    def close_connection(self): #Tested
        """
        Uses the Database Driver to commit and close a connection with a
        local database

        >>> library_manager.close_connection()

        """
        self.db_driver.commit()
        self.db_driver.close()
        if not self.db_driver.isOpen():
            return True

    def StartUpChecks(self): # Tested
        """
        Performs validation test for Table avalibility and structure.
        Creates the table or the view if it doesnt exist.
        """
        # checks for existance of library table
        query = QSqlQuery()
        query.prepare("SELECT name FROM sqlite_master WHERE type = 'table' AND name = library ")        
        query.exec_()
        if not query.next():
            self.Create_LibraryTable()
        query = QSqlQuery("SELECT cid FROM pragma_table_info('library')")
        query.exec_()
        if len(self.fetchAll(query, 1)) == len(self.db_fields):    
            LIB = True

        # checks for existance of nowplaying view
        query = QSqlQuery()
        query.prepare("SELECT name FROM sqlite_master WHERE type = 'view' AND name = nowplaying ")        
        query.exec_()
        if not query.next():
            self.Create_EmptyView("nowplaying")
            
        query = QSqlQuery("SELECT cid FROM pragma_table_info('nowplaying')")
        query.exec_()
        if len(self.fetchAll(query, 1)) == len(self.db_fields):    
            NPV = True
            
        return all([NPV, LIB])

    def ExeQuery(self, Query):
        """
        Executes an QSqlQuery and returns the query to get results

        >>> library_manager.ExeQuery(query)

        :Args:
            Query: QSqlQuery,String
                Query to execute
        :Returns:
            QSqlQuery
        """
        if isinstance(Query, str):
            QueryStr = Query
            Query = QSqlQuery()
            if Query.prepare(QueryStr) == False :
                msg = f"""
                    Query Build Failed
                    """
                msg = dedenter(msg, 16)
                raise Exception(msg)

        QueryExe = Query.exec_()
        if QueryExe == False :
            msg = f"""
                EXE: {QueryExe}
                ERROR: {(Query.lastError().text())}
                Query: {Query.lastQuery()}
                """
            msg = dedenter(msg, 12)
            raise Exception(msg)
        else:
            return Query

    def IndexSelector(self, view_name, Column):
        """
        Gets Column Data from a Table and View

        :Args:
            view_name: String
                Valid view name from (now_playing)
            Column: String
                Valid Column to select data from
        """
        query = QSqlQuery()
        querystate = query.prepare(f"SELECT {Column} FROM {view_name}")
        query_exe = query.exec_()

        if query_exe == False and querystate == False:
            raise Exception(f"<{query.lastQuery()}> Data retrieval Failed \nERROR: {query.lastError().text()}")
        Indexes = []
        while query.next():
            value = query.value(0)
            Indexes.append(value)
        return Indexes

########################################################################################################################
# Create, Drop, Insert Type Functions
########################################################################################################################

    def Create_LibraryTable(self): # Tested
        """
        Creates the main Library table with yhe valid column fields
        """
        query = QSqlQuery()
        querystate = query.prepare(f"""
        CREATE TABLE IF NOT EXISTS library(
        file_id TEXT PRIMARY KEY ON CONFLICT IGNORE,
        path_id TEXT,
        file_name TEXT,
        file_path TEXT,
        album TEXT,
        albumartist TEXT,
        artist TEXT,
        author TEXT,
        bpm TEXT,
        compilation TEXT,
        composer TEXT,
        conductor TEXT,
        date TEXT,
        discnumber INTEGER,
        discsubtitle TEXT,
        encodedby TEXT,
        genre TEXT,
        language TEXT,
        length TEXT,
        filesize TEXT,
        lyricist TEXT,
        media TEXT,
        mood TEXT,
        organization TEXT,
        originaldate TEXT,
        performer TEXT,
        releasecountry TEXT,
        replaygain_gain TEXT,
        replaygain_peak TEXT,
        title TEXT,
        tracknumber TEXT,
        version TEXT,
        website TEXT,
        album_gain TEXT,
        bitrate TEXT,
        bitrate_mode TEXT,
        channels INTEGER,
        encoder_info TEXT,
        encoder_settings TEXT,
        frame_offset TEXT,
        layer TEXT,
        mode TEXT,
        padding TEXT,
        protected TEXT,
        sample_rate TEXT,
        track_gain TEXT,
        track_peak TEXT,
        rating INTEGER,
        playcount INTEGER)
        """)
        # Error handling and execution of the query
        if querystate:
            self.ExeQuery(query)
        else:
            raise Exception("Query Build Failed")

    def Create_EmptyView(self, view_name): # Tested
        """
        Creates an empty view as an placeholder for display

        >>> library_manager.Create_EmptyView("Example")

        :Args:
            view_name: String
                Valid view name from (now_playing)
        """
        query = QSqlQuery()
        columns = ", ".join([f"NULL AS {k}" for k in  self.db_fields])
        querystate = query.prepare(f"""
                                   CREATE VIEW IF NOT EXISTS {view_name} AS
                                   SELECT {columns}
                                   """)
        # Error handling and execution of the query
        if querystate:
            self.ExeQuery(query)
        else:
            raise Exception("Query Build Failed")
        
    def CreateView(self, view_name, Selector, **kwargs): # Tested
        """
        Creates an view from library Table by selection data from a valid field

        >>> library_manager.CreateView("Viewname", "File_id", [1,2,3,4])

        :Args:
            view_name: String
                Valid view name from (now_playing)
            FilterField: String
                Valid field to select data from
            Selector: List
                Valid Selector to select and filter out Rows from the table
            ID: List
                File_id to indexs from if provided
            Shuffled: Bool
                Query Type to use for selecting data
            Normal: Bool
                Query Type to use for selecting data
            Filter: Bool
                Query Type to use for selecting data
        """
        # Drops thgiven view to create a new view
        self.DropView(view_name)
        query = QSqlQuery()

        # creates a a query string of items needed to be selected
        FilterItems =  ", ".join([f"'{value}'"for value in Selector])

        # sets the column used to look data from
        if kwargs.get("FilterField") == None:
            Field = "file_id"
        else:
            Field = kwargs.get("FilterField")

        # a list of all file ID used for indexing
        if kwargs.get("Filter") != None:
            if kwargs.get("ID") != None:
                ID = ", ".join([f"'{v}'"for v in kwargs.get("ID")])
            else:
                ID = ""

            querystate = query.prepare(f"""
            CREATE VIEW IF NOT EXISTS {view_name} AS
            SELECT * FROM library WHERE file_id IN (
            SELECT file_id
            FROM library
            WHERE {Field} IN ({FilterItems})
            OR lower({Field}) IN ({FilterItems})
            OR file_id IN ({ID})
            )
            """)

        # indexing items and shuffling the order
        elif kwargs.get("Shuffled") != None:
            querystate = query.prepare(f"""
            CREATE VIEW IF NOT EXISTS {view_name} AS
            SELECT * FROM library WHERE {Field} IN ({FilterItems})
            ORDER BY RANDOM()
            """)

        # normal filtering using the selected indexes
        elif kwargs.get("Normal") != None:
            querystate = query.prepare(f"""
            CREATE VIEW IF NOT EXISTS {view_name} AS
            SELECT * FROM library WHERE {Field} IN ({FilterItems})
            """)
        else:
             pass

        # Error handling and execution of the query
        if querystate:
            self.ExeQuery(query)
        else:
            raise Exception("Query Build Failed")

        # gets the data that has been applied and selected
        return self.IndexSelector("nowplaying", "file_id")

    def DropTable(self, tablename):
        """
        Drops the table from the database

        :Args:
            table_name: String
                Name of the table to be dropped
        :Error:
            Exceptions are raised if the query fails
        """
        query = QSqlQuery()
        querystate = query.prepare(f"DROP TABLE IF EXISTS {tablename}")
        # Error handling and execution of the query
        if querystate:
            self.ExeQuery(query)
        else:
            raise Exception("Query Build Failed")


    def DropView(self, viewname):
        """
        Drops the view from the database

        >>> library_manager.drop_view("viewname")

        :Args:
            viewname: String
                Name of the view to be dropped
        :Error:
            Exceptions are raised if the query fails
        """
        query = QSqlQuery()
        querystate = query.prepare(f"DROP VIEW IF EXISTS {viewname}")
        # Error handling and execution of the query
        if querystate:
            self.ExeQuery(query)
        else:
            raise Exception("Query Build Failed")


    def BatchInsert_Metadata(self, metadata):
        """
        Batch Inserts data into library table

        :Args:
            metadata: Dict
                Distonary of all the combined metadata
        """       
        query = QSqlQuery()
        columns =", ".join(metadata.keys())
        placeholders =  ", ".join(["?" for i in range(len(metadata.keys()))])
        query.prepare(f"""INSERT INTO library ({columns}) VALUES ({placeholders})""")
        for keys in metadata.keys():
            query.addBindValue(metadata.get(keys))
            

        self.db_driver.transaction()
        
        QSqlQuery("PRAGMA journal_mode = MEMORY").exec_()

        if not query.execBatch():
            raise Exception(query.lastError().text())
        
        QSqlQuery("PRAGMA journal_mode = WAL").exec_()
        
        self.db_driver.commit()

########################################################################################################################
# Table Stats Query
########################################################################################################################

    def TableSize(self, tablename):
        """
        Calculates the total size in Gigabytes of all the files monitered.
        Returns the Gigabyte as a Float.

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"SELECT round(sum(filesize)/1024, 2) FROM {tablename}")
        query.exec_()
        if query.next():
            value = (query.value(0))
            if value != "":
                return value
            else:
                return 0
        else:
            return 0

    def TablePlaytime(self, tablename):
        """
        Calculates the total playtime of all the files monitered.
        Returns the Playtime as a String.

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"""
                          SELECT sum(substr(length,1,1))*360 + sum(substr(length,3,2))*60 +sum(substr(length,6,2))
                          FROM {tablename}""")
        query.exec_()
        if query.next():
            value = query.value(0)
            value = "0" if value == "" else datetime.timedelta(seconds = value)

            return value
        else:
            return "0"

    def TableAlbumcount(self, tablename):
        """
        Calculates the total count of album of all the files monitered.
        Returns the album count as a Int.

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"SELECT count(DISTINCT album) FROM {tablename}")
        query.exec_()
        if query.next():
            return (query.value(0))
        else:
            return 0

    def TableArtistcount(self, tablename):
        """
        Calculates the total count of albumartist of all the files monitered.
        Returns the albumartist count as a Int.

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"SELECT count(DISTINCT artist) FROM {tablename}")
        query.exec_()
        if query.next():
            return (query.value(0))
        else:
            return 0

    def TableTrackcount(self, tablename):
        """
        Calculates the total count of Tracks of all the files monitered.
        Returns the track count as a Int.

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"SELECT count(DISTINCT file_id) FROM {tablename}")
        query.exec_()
        if query.next():
            return (query.value(0))
        else:
            return 0

class FileManager(DataBaseManager):
    """
    File manager classes manages:
    -> Scanning Directories
    -> Fetching metadata for the related file format
    
    Read Supported Formats:
    -> mp3
    -> flac
    """
    
    def __init__(self):
        """Constructor"""
        self.db_fields = DBFIELDS
    
    def TransposeMeatadata(self, Metadata):
        T_metadata = dict.fromkeys(DBFIELDS, "")
        for index, key in enumerate(T_metadata.keys()):
            T_metadata[key] = [value[index] for value in Metadata]            
        return T_metadata    

   
    def ScanDirectory(self, Dir, include = [], Slot = lambda: ''):
        BatchMetadata = []
        FileHashList = []
        
        file_paths = {}
        for D, SD, F in os.walk(os.path.normpath(Dir)):
            for file in F:
                if os.path.splitext(file)[1] in include:
                    file = os.path.normpath(os.path.join(D, file))
                    file_paths[(hashlib.md5(file.encode())).hexdigest()] = file
                    
        ID = ", ".join([f"'{v}'" for v in set(file_paths.keys())])
        query = QSqlQuery(f"SELECT path_id FROM library WHERE path_id IN ({ID})")
        query.exec_()
        while query.next():
            del file_paths[query.value(0)]
        self.FileChecker(file_paths, FileHashList, BatchMetadata)            
        self.BatchInsert_Metadata(self.TransposeMeatadata(BatchMetadata))

    def FileChecker(self, filepath, FileHashList, BatchMetadata):
        QSqlQuery("BEGIN TRANSCATION").exec_()
        for ID, file in filepath.items():
            Filehash = self.FileHasher(file)            
            if (Filehash not in FileHashList):
                FileHashList.append(Filehash)
                Metadata = self.ScanFile(file)
                Metadata["path_id"] = ID
                Metadata["file_id"] = Filehash                    
                BatchMetadata.append(list(Metadata.values()))                        
                
    def ScanFile(self, Path):
        """
        Reads the file metadata and generates a metadata dict and returns it.

        :Args:
            path: String
                Path of the file        
        """
        EXT = os.path.splitext(Path)[1]
        if EXT == ".mp3":
            return self.get_MP3(Path)
        
        elif EXT == ".flac":
            return self.get_FLAC(Path)
        
        else:
            pass

    def FileHasher(self, file, hashfun = hashlib.md5):
        """
        Creates a hash id for the file path passed and returns hash id.
        Hash id is calculated with the 1024 bytes of the file.

        :Args:
            file: String
                File for which the hash is generated
            hashfun: Method
                Hashing algorithm method from hashlib
        """
        with open(file, "rb") as fobj:
            bytes_ = fobj.read(1024)
            hashval = (hashfun(bytes_)).hexdigest()
        return hashval    

    def get_FLAC(self, Path):
        muta_file = mutagen.File(Path, easy = True)
        metadata = dict.fromkeys(DBFIELDS, "")
        
        for key in muta_file.keys():
            metadata[key] = muta_file.get(key)[0]
            
        metadata['sample_rate'] = f"{muta_file.info.sample_rate}Hz"
        metadata["length"] = str(datetime.timedelta(seconds = muta_file.info.length))
        metadata["bitrate"] = f"{int(muta_file.info.bitrate / 1000)}Kbps"                  
        metadata['channels'] = muta_file.info.channels
        metadata["filesize"] = f"{round(os.path.getsize(muta_file.filename) * 0.00000095367432, 2)}Mb"
        metadata["file_name"] = os.path.split(muta_file.filename)[1]
        metadata["file_path"] = muta_file.filename
        metadata["rating"] = 0
        metadata["playcount"] = 0
        
        return metadata
   
    def get_MP3(self, Path): 
        muta_file = mutagen.File(Path, easy = True)
        metadata = dict.fromkeys(DBFIELDS, "")
        
        for key in muta_file.keys():
            metadata[key] = muta_file.get(key)[0]
            
        metadata["bitrate_mode"] = str(muta_file.info.bitrate_mode).replace(')', "").replace('BitrateMode(', "")
        metadata['album_gain'] = muta_file.info.album_gain
        metadata['encoder_info'] = muta_file.info.encoder_info
        metadata['encoder_settings'] = muta_file.info.encoder_settings
        metadata['frame_offset'] = muta_file.info.frame_offset
        metadata['layer'] = muta_file.info.layer
        metadata['mode'] = muta_file.info.mode
        metadata['padding'] = muta_file.info.padding
        metadata['protected'] = muta_file.info.protected
        metadata['track_gain'] = muta_file.info.track_gain
        metadata['track_peak'] = muta_file.info.track_peak
        metadata['version'] = muta_file.info.version
        
        metadata['sample_rate'] = f"{muta_file.info.sample_rate}Hz"
        metadata["length"] = str(datetime.timedelta(seconds = muta_file.info.length))
        metadata["bitrate"] = f"{int(muta_file.info.bitrate / 1000)}Kbps"                  
        metadata['channels'] = muta_file.info.channels
        metadata["filesize"] = f"{round(os.path.getsize(muta_file.filename) * 0.00000095367432, 2)}Mb"
        metadata["file_name"] = os.path.split(muta_file.filename)[1]
        metadata["file_path"] = muta_file.filename
        metadata["rating"] = 0
        metadata["playcount"] = 0
    
        return metadata

class ModelView_Manager(FileManager):
    """"""

    def __init__(self):
        """Constructor"""
        self.db_fields = DBFIELDS

    def SetTable_horizontalHeader(self, View, Labels):
        """
        Sets the table header

        >>> library_manager.SetTable_horizontalHeader(View, [1, 2, 3])

        :Args:
            View: QtWidgets.QTableView
                Table object to modify the header

            Labels: List
                Labels to set as TableHeader
        """

        header = View.horizontalHeader().model()
        Labels = Labels[:header.columnCount()]
        for col, data in enumerate(Labels):
            header.setHeaderData(col, Qt.Horizontal, str(data).replace("_", " ").title())

    def GetTable_horizontalHeader(self, View):
        """
        Gets the table header and replaces the space with underscore
        and swaps the string to lower case.

        :Args:
            View: QtWidgets.QTableView
                Table object to retrieve the header from
        """
        header = View.horizontalHeader().model()
        labels = []
        for col in range(header.columnCount()):
            col_label = header.headerData(col, Qt.Horizontal)
            labels.append(str(col_label).replace(" ", "_").lower())
        return labels

    def SetTableModle(self, Tablename, View = QtWidgets.QTableView, Headers = None) -> "QStandardItemModel":
        """
        Gets the TableData for the given Table In the DB

        >>> library_manager.SetTableModle(Tablename"Table", View = TableView, Headers = [1,2,3,4,5])

        :Args:
            Tablename: String
                Table name for the model to points to
            View: TableView
                view to set Modle into
            Headers: List
                List of all Labels to add to View Header

        :Return:
            TableModel: if evrything passes
            None: if Tablename is invalid
        """
        #  Runs a select query to return QueryPointer
        query = QSqlQuery()
        if Tablename in ["library", 'nowplaying']:
            if not query.prepare(f"SELECT * FROM {Tablename}"):
                msg = dedenter(f"""
                               Query(SELECT * FROM {Tablename})
                               Error: {query.lastError().text()}
                               query failed to build""", 16)
                raise Exception(msg)

        query_exe = query.exec_()
        if query_exe == False:
            raise Exception(f"<{Tablename}> Table Doesnt Exists")

        # Sets all the required Property forn the view
        View.setProperty("DB_Table", Tablename)
        View.setProperty("DB_Columns", self.db_fields)
        Order = View.property("Order")

        # Order is passed in predefined
        if not(len(Order) == 0):
            TableModel = self.OrderedSqlTableModel(query, Order)

        # Table population by Normal method
        elif len(Order) == 0:
            TableModel = self.SqlTableModel(query)

        else:
            pass

        # Sets all the header labels
        View.setModel(TableModel)
        if  Headers == None:
            Headers = list(range(TableModel.columnCount()))
        self.SetTable_horizontalHeader(View, Headers)

        return TableModel

    def OrderedSqlTableModel(self, Query, Order): # untested
        """
        Returns a TableModel Ordered according to the Order.

        >>> LibraryManager.OrderedSqlTableModel(Query, [1,2,3,4,5])

        :Args:
            Query: QSqlQuery
                Query to get data from
            Order: List
                Order to use for the TableModel Items

        :Return: QStandardItemModel
        """
        TableModel = QtGui.QStandardItemModel()
        Cols = range(len(self.db_fields))

        TableModel.beginInsertRows(QtCore.QModelIndex(), 0, len(Order) - 1)

        # uses the query to get data
        while Query.next():
            for Column in Cols:
                Item = Query.value(Column)
                if Column == 0:
                    Row = Order.index(Item)
                # set the query items into the TableModel
                TableModel.setItem(Row, Column, QtGui.QStandardItem(Item))

        TableModel.endInsertRows()

        # removes the rows that are empty
        for Row in range(TableModel.rowCount()):
            if TableModel.item(Row) == None:
                TableModel.removeRow(Row)

        return TableModel

    def SqlTableModel(self, Query): # untested
        """
        Returns a TableModel filled with Query data.

        >>> LibraryManager.OrderedSqlTableModel(Query)

        :Args:
            Query: QSqlQuery
                Query to get data from
        :Return: QStandardItemModel
        """

        TableModel = QtGui.QStandardItemModel()
        Cols = range(len(self.db_fields))
        Row = 0

        # gets and sets the query item
        while Query.next():
            TableModel.insertRow(Row, [QtGui.QStandardItem(str(Query.value(Column))) for Column in Cols])
            Row += 1
        return TableModel

    def Refresh_TableModelData(self, View) -> "QStandardItemModel":
        """
        Refreshes the TableModel

        :Args:
            parent_view: QTableView
                View containing the model
        """
        Table = View.property("DB_Table")
        return self.SetTableModle(Table, View, View.property("DB_Columns"))

########################################################################################################################
# Table Searches
########################################################################################################################
    def ClearView_Masks(self, View = QtWidgets.QTableView):
        TableModel = View.model()
        for Row in range(TableModel.rowCount()):
            View.showRow(Row)

    def TableSearch(self, Line_Edit = QtWidgets.QLineEdit, View = QtWidgets.QTableView):
        """
        Applies a filter to the QSqlTableModel and refreshes it.
        Searches in [album, albumartist, artist, author, composer, performer, title] Fields

        >>> library_manager.TableSearch(QLineEdit, QTableView)

        :Args:
            Line_Edit: QtWidgets.QLineEdit
                LineEdit that provides the text

            View: QtWidgets.QTableView
                View that provides the model
        """
        Text = Line_Edit.text().strip()
        if Text == "":
            [View.showRow(Row) for Row in range(View.model().rowCount())]
            return None

        tablename = View.property("DB_Table")
        query = QSqlQuery()

        if tablename in ["library", 'nowplaying']:
            querystate = query.prepare(f"""
            SELECT file_id FROM {tablename}
            WHERE
            album LIKE '%{Text}%'
            OR albumartist LIKE '%{Text}%'
            OR artist LIKE '%{Text}%'
            OR author LIKE '%{Text}%'
            OR composer LIKE '%{Text}%'
            OR performer LIKE '%{Text}%'
            OR title LIKE '%{Text}%'
            OR lower(album) LIKE '%{Text}%'
            OR lower(albumartist) LIKE '%{Text}%'
            OR lower(artist) LIKE '%{Text}%'
            OR lower(author) LIKE '%{Text}%'
            OR lower(composer) LIKE '%{Text}%'
            OR lower(performer) LIKE '%{Text}%'
            OR lower(title) LIKE '%{Text}%'
            """)
        else:
            querystate = False

        query_exe = query.exec_()
        if query_exe == False and querystate == False:
            raise Exception(f"<{tablename}> View Not Created")

        # shows matching rows
        QueryData = []
        Row = 0
        while query.next():
            QueryData.append(str(query.value(0)))
            Row += 1

        TableModel = View.model()
        for Row in range(TableModel.rowCount()):
            if TableModel.index(Row, 0).data() in QueryData:
                View.showRow(Row)
            else:
                View.hideRow(Row)

    def SearchSimilarField(self, View, Field, Indexes):
        """
        Applies a filter to the QtableView and refreshes it.
        Searches in [album, artist, genre] Fields

        >>> library_manager.SearchSimilarField(TableView, String, List)

        :Args:
            View: QtWidgets.QTableView
                View that provides the model
            Field:
                Field to search data from
            Indexes:
                Selected Indexes
        """
        if Indexes in ["", None, []]:
            return False

        # creates a query to filter
        Tablename = View.property("DB_Table")
        exp = "({0} LIKE '%{1}%') OR (lower({2}) LIKE '%{3}%')"
        LikeExpression = [exp.format(Field, Upper, Field, Upper) for Upper in Indexes]
        LikeExpression = " OR ".join(LikeExpression)

        Query = QSqlQuery()
        if not (Query.prepare(f"SELECT file_id FROM {Tablename} WHERE {LikeExpression}")):
            print(f"SELECT file_id FROM {Tablename} WHERE {LikeExpression}")
            raise Exception("Query Build Failed")
        Query = self.ExeQuery(Query)

        # shows matching rows
        QueryData = []
        Row = 0
        while Query.next():
            QueryData.append(str(Query.value(0)))
            Row += 1

        TableModel = View.model()
        for Row in range(TableModel.rowCount()):
            if TableModel.index(Row, 0).data() in QueryData:
                View.showRow(Row)
            else:
                View.hideRow(Row)

    def TableSearchAdvanced(self, query, View):
        """
        Applies a filter to the QSqlTableModel and refreshes it.
        Advanced query filter will be used

        :Args:
            Line_Edit: QtWidgets.QLineEdit
                LineEdit that provides the text

            View: QtWidgets.QTableView
                View that provides the model

            query: String
                Claues Use for filtering the Table
        :Errors:
            Unable to execute multiple statements at a time
        """
        model = View.model()
        model.setFilter()
        ERROR = model.lastError().text()
        if  ERROR != "":
            model.setFilter('')
            self.Refresh_TableModelData(View)
            raise Exception(ERROR)


class LibraryManager(ModelView_Manager):
    """
    Controls the database queries for table and view (creation, modification
    and deletion).

    >>> library_manager = LibraryManager()
    >>> library_manager.connect("database.db")
    """
    def __init__(self, DBname = None):
        """Constructor"""
        self.db_fields = DBFIELDS
        super().__init__()

        if DBname != None:
            if not self.connect(DBname):
                raise Exception("Startup Checks Failed")



if __name__ == '__main__':
    from apollo.test.testUtilities import TestSuit_main
    from apollo.test.Test_LIbraryManager import Test_LibraryManager

    Suite = TestSuit_main()
    Suite.AddTest(Test_LibraryManager)
    Suite.Run(QT=True)

    
