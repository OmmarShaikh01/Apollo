import sys
import os
import re
import datetime
import re
import hashlib
import json
import time
import pathlib

import mutagen
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from apollo import exe_time, dedenter, ThreadIt, PathUtils
# from apollo.mediafile import MediaFile
from apollo import PARENT_DIR


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

class DBStructureError(Exception): __module__ = "LibraryManager"
class QueryBuildFailed(Exception): __module__ = "LibraryManager"
class QueryExecutionFailed(Exception): __module__ = "LibraryManager"


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

    def connect(self, db): #Tested
        """
        Uses the Database Driver to create a connection with a local
        database.If Db not avaliable will create new Db

        >>> library_manager.connect("default.db")

        Parameters
        ----------
        db : String
            path of a Valid Database or a Database name in order to create a blank one

        Returns
        -------
        Boolean
            returns true if connection was succesful

        Raises
        ------
        ConnectionError
            if database fails to connect or fails checks
        """
        if not os.path.isfile(db) and PathUtils.isFileExt(db, ".db"): open(db, "w").close()
        elif (db == ":memory:") or (os.path.isfile(db) and PathUtils.isFileExt(db, ".db")): pass
        else: return False

        self.db_driver = QSqlDatabase.addDatabase("QSQLITE")
        self.db_driver.database(db)
        self.DB_NAME = db
        if self.db_driver.open() and self.IsConneted():
            if not self.StartUpChecks(): raise DBStructureError("Startup Checks Failed")
            else: return True

        # only executes when connection fails and app closes
        else: # pragma: no cover
            raise ConnectionError()

    def IsConneted(self): #Tested
        """
        Returns a value if DB is connected or not

        Returns
        -------
        Boolean
            boolean abased according to the state of the connection
        """
        return (self.db_driver.isOpen() and self.db_driver.isValid())

    def close_connection(self): #Tested
        """
        Uses the Database Driver to commit and close a connection with a
        local database

        >>> library_manager.close_connection()

        Returns
        -------
        boolean
            closes connection and give true on success
        """
        self.db_driver.commit()
        self.db_driver.close()
        self.db_driver.removeDatabase(self.DB_NAME)
        if not self.db_driver.isOpen():
            return True

    def StartUpChecks(self): # Tested
        """
        Performs validation test for Table avalibility and structure.
        Creates the table or the view if it doesnt exist.

        Returns
        -------
        Boolean
            Returns true if all checks are passed
        """

        # checks for existance of library table
        state = False
        [[TABLE, COLUMNS]] = self.fetchAll(
            self.ExeQuery("""
            SELECT
            (
                SELECT
                IIF(name = 'library', TRUE, FALSE)
                FROM sqlite_master
                WHERE type = 'table'
            ) AS TABLE_CHECK,
            (
                SELECT
                min(
                    IIF( name IN(
                        'file_id', 'path_id','file_name','file_path','album',
                        'albumartist','artist','author','bpm','compilation',
                        'composer','conductor','date','discnumber','discsubtitle',
                        'encodedby','genre','language','length','filesize',
                        'lyricist','media','mood','organization','originaldate',
                        'performer','releasecountry','replaygain_gain','replaygain_peak',
                        'title','tracknumber','version','website','album_gain',
                        'bitrate','bitrate_mode','channels','encoder_info','encoder_settings',
                        'frame_offset','layer','mode','padding','protected','sample_rate',
                        'track_gain','track_peak', 'rating', 'playcount'), TRUE, FALSE
                    )
                )
                FROM pragma_table_info('library')
            ) AS COLUMN_CHECK;
        """)
        )
        if not bool(TABLE) or not bool(COLUMNS):
            self.Create_LibraryTable()
            state = True
        else:
            state = True

        # checks for existance of nowplaying view
        state = False
        [[TABLE, COLUMNS]] = self.fetchAll(
            self.ExeQuery("""
            SELECT
            (
                SELECT
                IIF(name = 'nowplaying', TRUE, FALSE)
                FROM sqlite_master
                WHERE type = 'view'
            ) AS TABLE_CHECK,
            (
                SELECT
                min(
                    IIF( name IN(
                        'file_id', 'path_id','file_name','file_path','album',
                        'albumartist','artist','author','bpm','compilation',
                        'composer','conductor','date','discnumber','discsubtitle',
                        'encodedby','genre','language','length','filesize',
                        'lyricist','media','mood','organization','originaldate',
                        'performer','releasecountry','replaygain_gain','replaygain_peak',
                        'title','tracknumber','version','website','album_gain',
                        'bitrate','bitrate_mode','channels','encoder_info','encoder_settings',
                        'frame_offset','layer','mode','padding','protected','sample_rate',
                        'track_gain','track_peak', 'rating', 'playcount'), TRUE, FALSE
                    )
                )
                FROM pragma_table_info('nowplaying')
            ) AS COLUMN_CHECK
        """)
        )
        if not bool(TABLE) or not bool(COLUMNS):
            self.Create_EmptyView("nowplaying")
            state = True
        else:
            state = True

        return state

    def ExeQuery(self, Query): #Tested
        """
        Executes an QSqlQuery and returns the query to get results

        >>> library_manager.ExeQuery(query)

        Parameters
        ----------
        Query: QSqlQuery,String
            Query to execute

        Returns
        -------
        QSqlQuery
            SQLQuery
        """
        if isinstance(Query, str):
            QueryStr = Query
            Query = QSqlQuery()
            if Query.prepare(QueryStr) == False:
                raise QueryBuildFailed(QueryStr)

        QueryExe = Query.exec()
        if QueryExe == False :
            msg = f"""
                EXE: {QueryExe}
                ERROR: {(Query.lastError().text())}
                Query: {Query.lastQuery()}
                """
            raise QueryExecutionFailed(dedenter(msg, 12))
        else:
            return Query

    def fetchAll(self, Query, Column = None): #Tested
        """
        Fetches data from the given query

        >>> library_manager.fetchAll(Query, 5)

        Parameters
        ----------
        Query : QSqlQuery
            Query to fetch result set from
        Column : [Int], optional
            index of Column to get data for, by default None

        Returns
        -------
        List
            list of matrix of Row X Column, if NULL []
        """
        Data = []
        if Column == None:
            Column = Query.record().count()
            while Query.next():
                Data.append([Query.value(C) for C in range(Column)])
        else:
            while Query.next():
                Data.append([Query.value(Column)])

        return Data

    def IndexSelector(self, view_name, Column): #Tested
        """
        Gets Column Data from a Table and View

        Parameters
        ----------
        view_name : String
            Valid view name from (now_playing)
        Column : String
            Valid Column to select data from

        Returns
        -------
        list
            Column data requested for

        Raises
        ------
        Exception
            if data retruival failed
        """

        return self.fetchAll(self.ExeQuery(f"SELECT {Column} FROM {view_name}"),1)

    def SelectAll(self, name):
        """
        Gets All Data from a Table and View

        Parameters
        ----------
        view_name : String
            Valid view name from (now_playing)

        Returns
        -------
        list
            Table data requested for

        Raises
        ------
        Exception
            if data retruival failed
        """
        return self.fetchAll(self.ExeQuery(f"SELECT * FROM {name}"))

    ####################################################################################################################
    # Create, Drop, Insert Type Functions
    ####################################################################################################################

    def Create_LibraryTable(self): # Tested
        """
        Creates the main Library table with yhe valid column fields
        """
        return self.ExeQuery(f"""
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

    def Create_EmptyView(self, view_name): # Tested
        """
        Creates an empty view as an placeholder for display

        >>> library_manager.Create_EmptyView("Example")

        Parameters
        ----------
        view_name : String
            Valid view name from (now_playing)
        """
        columns = ", ".join([f"NULL AS {k}" for k in  self.db_fields])
        self.ExeQuery(f"CREATE VIEW IF NOT EXISTS {view_name} AS SELECT {columns}")

    def CreateView(self, view_name, Selector, **kwargs):
        """
        Creates an view from library Table by selection data from a valid field

        >>> library_manager.CreateView("Viewname", "File_id", [1,2,3,4])

        Parameters
        ----------
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
        if kwargs.get("ID") != None and kwargs.get("Shuffled") == None:
            ID = ", ".join([f"'{v}'"for v in kwargs.get("ID")])
            self.ExeQuery(f"""
            CREATE VIEW IF NOT EXISTS {view_name} AS
            SELECT *
            FROM library
            WHERE file_id IN (
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
            SELECT *
            FROM library
            WHERE {Field} IN ({FilterItems})
            ORDER BY RANDOM()
            """)

        else:
            self.ExeQuery(f"""
            CREATE VIEW IF NOT EXISTS {view_name} AS
            SELECT *
            FROM library
            WHERE {Field}
            IN ({FilterItems})
            """)

    def DropTable(self, tablename):
        """
        Drops the table from the database

        Parameters
        ----------
        table_name: String
            Name of the table to be dropped
        """
        self.ExeQuery(f"DROP TABLE IF EXISTS {tablename}")

    def DropView(self, viewname):
        """
        Drops the view from the database

        >>> library_manager.drop_view("viewname")

        Parameters
        ----------
        viewname: String
            Name of the view to be dropped
        """
        self.ExeQuery(f"DROP VIEW IF EXISTS {viewname}")

    def BatchInsert_Metadata(self, metadata):
        """
        Batch Inserts data into library table

        Parameters
        ----------
        metadata: Dict
            Distonary of all the combined metadata
        """
        query = QSqlQuery()
        columns =", ".join(metadata.keys())
        placeholders =  ", ".join(["?" for i in range(len(metadata.keys()))])
        query.prepare(f"""INSERT OR IGNORE INTO library ({columns}) VALUES ({placeholders})""")
        for keys in metadata.keys():
            query.addBindValue(metadata.get(keys))

        # sets up the transcation
        self.db_driver.transaction()
        self.ExeQuery("PRAGMA journal_mode = MEMORY")

        if not query.execBatch(): # pragma: no cover
            msg = f"""
                ERROR: {(Query.lastError().text())}
                Query: {Query.lastQuery()}
                """
            raise QueryExecutionFailed(dedenter(msg, 12))

        self.ExeQuery("PRAGMA journal_mode = WAL")
        self.db_driver.commit()

    ###################################################################################################################
    # Table Stats Query
    ###################################################################################################################

    def TableSize(self, tablename = "library"):
        """
        Calculates the total size in Gigabytes of all the files monitered.
        Returns the Gigabyte as a Float.

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT IIF(OUTPUT, OUTPUT, 0) AS FINAL
        FROM (
            SELECT round(sum(filesize)/1024, 2) AS OUTPUT
            FROM {tablename}
            )
        """)
        )
        return query.pop().pop()

    def TablePlaycount(self, tablename = "library"):
        """
        Calculates the total Playtime and returns an Int

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT IIF(OUTPUT, OUTPUT, 0) AS FINAL
        FROM (
            SELECT sum(playcount) AS OUTPUT
            FROM {tablename}
            )
        """)
        )
        return query.pop().pop()

    def TablePlaytime(self, tablename = "library"):
        """
        Calculates the total playtime of all the files monitered.
        Returns the Playtime as a String.

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT IIF(TIME_SEC, TIME_SEC, 0) AS FINAL
        FROM (
            SELECT (sum(substr(length,1,1))*360 + sum(substr(length,3,2))*60 + sum(substr(length,6,2)))
            AS TIME_SEC
            FROM {tablename}
            )
        """)
        )
        return datetime.timedelta(seconds = query.pop().pop())

    def TableAlbumcount(self, tablename = "library"):
        """
        Calculates the total count of album of all the files monitered.
        Returns the album count as a Int.

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT IIF(OUTPUT, OUTPUT, 0) AS FINAL
        FROM (
            SELECT count(DISTINCT album) AS OUTPUT
            FROM {tablename}
            )
        """)
        )
        return query.pop().pop()

    def TableArtistcount(self, tablename = "library"):
        """
        Calculates the total count of albumartist of all the files monitered.
        Returns the albumartist count as a Int.

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT IIF(OUTPUT, OUTPUT, 0) AS FINAL
        FROM (
            SELECT count(DISTINCT artist) AS OUTPUT
            FROM {tablename}
            )
        """)
        )
        return query.pop().pop()

    def TableTrackcount(self, tablename = "library"):
        """
        Calculates the total count of Tracks of all the files monitered.
        Returns the track count as a Int.

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT IIF(OUTPUT, OUTPUT, 0) AS FINAL
        FROM (
            SELECT count(DISTINCT file_id) AS OUTPUT
            FROM {tablename}
            )
        """)
        )
        return query.pop().pop()

    def TopAlbum(self, Tablename = "library"):
        """
        Calculates the total playcount of Album of all the files monitered.

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT album
        FROM {Tablename}
        WHERE album NOTNULL AND album NOT IN ('', ' ')
        GROUP BY album
        ORDER BY COUNT(playcount) DESC
        LIMIT 1;
        """)
        )
        if query != []:
            return query.pop().pop()
        else:
            return ""

    def Topgenre(self, Tablename = "library"):
        """
        Calculates the total playcount of genre of all the files monitered.

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT genre
        FROM {Tablename}
        WHERE genre NOTNULL AND genre NOT IN ('', ' ')
        GROUP BY genre
        ORDER BY COUNT(playcount) DESC
        LIMIT 1;
        """)
        )
        if query != []:
            return query.pop().pop()
        else:
            return ""

    def Topartist(self, Tablename = "library"):
        """
        Calculates the total playcount of artist of all the files monitered.

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT artist
        FROM {Tablename}
        WHERE artist NOTNULL AND artist NOT IN ('', ' ')
        GROUP BY artist
        ORDER BY COUNT(playcount) DESC
        LIMIT 1;
        """)
        )
        if query != []:
            return query.pop().pop()
        else:
            return ""

    def Toptrack(self, Tablename = "library"):
        """
        Calculates the total playcount of track of all the files monitered.

        Parameters
        ----------
        tablename: String
            Name of the table or view to be queried
        """
        query = self.fetchAll(self.ExeQuery(f"""
        SELECT title
        FROM {Tablename}
        WHERE playcount == (
            SELECT max(playcount)
            FROM {Tablename}
        )
        LIMIT 1
        """)
        )
        if query != []:
            return query.pop().pop()
        else:
            return ""


class FileManager(DataBaseManager): # pragma: no cover
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
            if not self.connect(DBname):# pragma: coverage
                raise DBStructureError("Startup Checks Failed")


if __name__ == "__main__": # pragma: no cover
    inst = DataBaseManager()
    inst.connect(":memory:")
    print(inst.IsConneted(), inst.IsConneted())
