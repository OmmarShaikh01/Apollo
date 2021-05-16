import sys, os, re, datetime, re, hashlib, json, time, pathlib

import mutagen
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from apollo.utils import exe_time, dedenter, ThreadIt
# from apollo.mediafile import MediaFile
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
            if rows == 1:
                Data.append(Query.value(0))
            else:
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
        else:
            LIB = False

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
        else:
            NPV = False

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
            Selector: List
                Valid Selector to select and filter out Rows from the table
            FilterField: String
                Valid field to select data from
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

            self.ExeQuery(f"""
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
            self.ExeQuery(f"""
            CREATE VIEW IF NOT EXISTS {view_name} AS
            SELECT * FROM library WHERE {Field} IN ({FilterItems})
            ORDER BY RANDOM()
            """)

        # normal filtering using the selected indexes
        else:
            self.ExeQuery(f"""
            CREATE VIEW IF NOT EXISTS {view_name} AS
            SELECT * FROM library WHERE {Field} IN ({FilterItems})
            """)

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
        query.prepare(f"""INSERT OR IGNORE INTO library ({columns}) VALUES ({placeholders})""")
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

    def TableSize(self, tablename = "library"):
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

    def TablePlaycount(self, tablename = "library"):
        """
        Calculates the total Playtime and returns an Int

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"SELECT sum(playcount) FROM {tablename}")
        query.exec_()
        if query.next():
            value = (query.value(0))
            if value != "":
                return value
            else:
                return 0
        else:
            return 0

    def TablePlaytime(self, tablename = "library"):
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

    def TableAlbumcount(self, tablename = "library"):
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

    def TableArtistcount(self, tablename = "library"):
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

    def TableTrackcount(self, tablename = "library"):
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

    def TopAlbum(self, Tablename = "library"):
        """
        Calculates the total playcount of Album of all the files monitered.

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"""
        SELECT album
        FROM {Tablename}
        WHERE album NOTNULL AND album NOT IN ('', ' ')
        GROUP BY album
        ORDER BY COUNT(playcount) DESC
        LIMIT 1;
        """)
        query.exec_()
        if query.next():
            return (query.value(0))
        else:
            return ""

    def Topgenre(self, Tablename = "library"):
        """
        Calculates the total playcount of genre of all the files monitered.

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"""
        SELECT genre
        FROM {Tablename}
        WHERE genre NOTNULL AND genre NOT IN ('', ' ')
        GROUP BY genre
        ORDER BY COUNT(playcount) DESC
        LIMIT 1;
        """)
        query.exec_()
        if query.next():
            return (query.value(0))
        else:
            return ""

    def Topartist(self, Tablename = "library"):
        """
        Calculates the total playcount of artist of all the files monitered.

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"""
        SELECT artist
        FROM {Tablename}
        WHERE artist NOTNULL AND artist NOT IN ('', ' ')
        GROUP BY artist
        ORDER BY COUNT(playcount) DESC
        LIMIT 1;
        """)
        query.exec_()
        if query.next():
            return (query.value(0))
        else:
            return ""

    def Toptrack(self, Tablename = "library"):
        """
        Calculates the total playcount of track of all the files monitered.

        :Args:
            tablename: String
                Name of the table or view to be queried
        """
        query = QSqlQuery(f"""
        SELECT title
        FROM {Tablename}
        WHERE playcount == (SELECT max(playcount) FROM {Tablename}) LIMIT 1;
        """)
        query.exec_()
        if query.next():
            return (query.value(0))
        else:
            return ""


class FileManager(DataBaseManager):
    """
    File manager classes manages:
    -> Scanning Directories
    -> Fetching metadata for the related file format

    Read Supported Formats:
    -> mp3
    -> flac
    -> m4a
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

        Slot(f"Scanning {Dir}")
        ID = ", ".join([f"'{v}'" for v in set(file_paths.keys())])
        query = QSqlQuery(f"SELECT path_id FROM library WHERE path_id IN ({ID})")
        query.exec_()
        while query.next():
            del file_paths[query.value(0)]

        self.FileChecker(file_paths, FileHashList, BatchMetadata)
        self.BatchInsert_Metadata(self.TransposeMeatadata(BatchMetadata))
        Slot(f"Completed Scanning {Dir}")

    def FileChecker(self, filepath, FileHashList, BatchMetadata):
        QSqlQuery("BEGIN TRANSCATION").exec_()
        for ID, file in filepath.items():
            Filehash = self.FileHasher(file)
            if (Filehash not in FileHashList):
                FileHashList.append(Filehash)
                Metadata = MediaFile(file).getMetadata()
                Metadata["path_id"] = ID
                Metadata["file_id"] = Filehash
                BatchMetadata.append(list(Metadata.values()))

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

class LibraryManager(FileManager):
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
