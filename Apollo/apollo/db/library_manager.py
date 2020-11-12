import sys
import os
import re
import sqlite3 as sql
import threading
import datetime
import re
import hashlib

import mutagen
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from apollo.utils import exe_time, dedenter
import apollo
root_path = apollo.__path__


########################################################################################################################

class LibraryManager():
    """
    Controls the database queries for table and view (creation, modification
    and deletion).
    
    >>> library_manager = LibraryManager()
    >>> library_manager.connect("database.db")
    """
    
    def __init__(self):
        """
        Initilizes the Databse Driver and returns a QSqlDatabase Driver and
        Initilizes the fields for the Database Tables 
        """
        self.db_driver = QSqlDatabase.addDatabase("QSQLITE")   
        self.db_fields = ["file_id", "path_id","file_name","file_path","album",
                          "albumartist","artist","author","bpm","compilation",
                          "composer","conductor","date","discnumber","discsubtitle",
                          "encodedby","genre","language","length","filesize",
                          "lyricist","media","mood","organization","originaldate",
                          "performer","releasecountry","replaygain_gain","replaygain_peak",
                          "title","tracknumber","version","website","album_gain",
                          "bitrate","bitrate_mode","channels","encoder_info","encoder_settings",
                          "frame_offset","layer","mode","padding","protected","sample_rate",
                          "track_gain","track_peak"]
        
    def connect(self, db):
        """
        Uses the Database Driver to create a connection with a local
        database
        
        :Args:
            
            db: String
                path of a Valid Database or a Database name in order to
                create a blank one
                
        :Errors:
            ConnectionError: if database fails to connect or fails checks 
        """
        self.db_driver.setDatabaseName(db)
        if self.db_driver.open():
            self.startupchecks()
            return True
        else:
            raise ConnectionError()


    def close_connection(self):
        """
        Uses the Database Driver to commit and close a connection with a
        local database
        """        
        self.db_driver.commit()
        self.db_driver.close()
        if not self.db_driver.isOpen():
            return True


    def startupchecks(self):
        """
        Performs validation test for Table avalibility and structure.
        Creates the table or the view if it doesnt exist.
        """
        query = QSqlQuery()
        query.prepare("SELECT name FROM sqlite_master WHERE type = 'table' AND name = :tablename ")
        query.bindValue(":tablename", "library")
        query.exec_()
        if not query.next():
            query_library = self.create_library_table("library")
        
        
    def create_library_table(self):
        """Creates the main Library table with yhe valid column fields"""
        query = QSqlQuery()
        querystate = query.prepare(f"""
        CREATE TABLE IF NOT EXISTS library(
        file_id TEXT PRIMARY KEY, 
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
        track_peak TEXT)
        """)
        query_exe = query.exec_()
        if query_exe == False and querystate == False:
            raise Exception(f"Table Not Created")
        else:
            return True         
    
    
    def create_empty_view(self, view_name):
        """
        Creates an empty view as an placeholder for display
        
        :Args:
            view_name: String
                Valid view name from (now_playing)
        """
        query = QSqlQuery()
        columns = ", ".join([f"NULL AS {k}" for k in  self.db_fields])
        querystate = query.prepare(f"""
        CREATE VIEW {view_name} AS
        SELECT {columns}
        """)
        query_exe = query.exec_()
        if query_exe == False and querystate == False:
            raise Exception(f"<{view_name}> View Not Created")
        else:
            return query 


    def create_view(self, view_name, field, data):
        """
        Creates an view by selection data from a valid field
        
        :Args:
            view_name: String
                Valid view name from (now_playing)
            field: String
                Valid field to select data from
            data: List
                Valid data to select and filter out Rows from the table
        """        
        query = QSqlQuery()
        placeholders =  ", ".join([f"'{v}'"for v in data])
        querystate = query.prepare(f"""
        CREATE VIEW IF NOT EXISTS {view_name} AS
        SELECT * FROM library WHERE {field} IN ({placeholders})
        """)
        
        query_exe = query.exec_()
        if query_exe == False and querystate == False:
            print(querystate, query.executedQuery())
            raise Exception(f"<{view_name}> View Not Created \nERROR {query.lastError().text()}")
        else:
            return query 
           
            
    def drop_table(self, tablename):
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
        query_exe = query.exec_()
        if query_exe == False and querystate == False:
            raise Exception(f"ERROR {query.lastError().text()}")
        else:
            return query 
        
        
    def drop_view(self, viewname):
        """
        Drops the view from the database

        :Args:
            viewname: String
                Name of the view to be dropped
        :Error:
            Exceptions are raised if the query fails 
        """            
        query = QSqlQuery()
        querystate = query.prepare(f"DROP VIEW IF EXISTS {viewname}")
        query_exe = query.exec_()
        if query_exe == False and querystate == False:
            raise Exception(f"ERROR {query.lastError().text()}")
        else:
            return query 
                
    
    
    def scan_directory(self, path, include = []):
        """
        Walks the root directory and scans the directory for media files.
        It also fetches the metadata of the media file and runs an insert query
        on the database with the metadata.
        
        :Args:
            path: String
                Path of the root level directory
            include: List
                List of file extentions to include
        """
        file_list = []
        for (dirc, subdir, files) in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] in include:
                    path = os.path.join(dirc, file)
                    file_list.append(path)
        metadata_dict = self.scan_file(file_list)
        query = self.insert_metadata_batch(metadata_dict)
        if not query.execBatch():
            raise Exception(query.lastError().text())
            
            
    def scan_file(self, file_list):
        """
        Fetches Metadata of the files that have been scanned and returns a
        metadata dict.
        
        :Args:
            file_list: List
                List of files scanned 
        """
        metadata_dict = {k: []for k in self.db_fields}
        filehash_list = []
        for file in file_list:         
            pathhash = (hashlib.md5(file.encode())).hexdigest()
            query = QSqlQuery(f"SELECT path_id FROM library WHERE path_id = '{pathhash}' ")
            query.exec_()
            if not query.next():
                filehash = self.file_hasher(file)
                if filehash not in filehash_list:
                    filehash_list.append(filehash)                
                    metadata = self.file_parser(file, metadata_dict)
                    metadata["path_id"] = pathhash
                    metadata["file_id"] = filehash                    
                    query = QSqlQuery(f"SELECT file_id FROM library WHERE file_id = '{filehash}' ")
                    query.exec_()
                    if not query.next():
                        for key in metadata_dict.keys():
                            metadata_dict[key].append(metadata.get(key))
        return metadata_dict
       
       
    def file_hasher(self, file, hashfun = hashlib.md5):
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
    
    
    def file_parser(self, path, metadata_fields):        
        """
        Reads the file metadata and generates a metadata dict and returns it.
        
        :Args:
            path: String
                Path of the file                
            metadata_fields: Dict
                Fields that should be read
        """
        muta_file = mutagen.File(path, easy = True)
        metadata = {}   
        for key in metadata_fields:
            try:                
                if key == "length":
                    value = muta_file.info.length
                    metadata[key] = str(datetime.timedelta(seconds = value))
                    
                elif key == "bitrate":
                    # bitrate info is stored as bps so need to scale it ro Kbps
                    value = int(muta_file.info.bitrate / 1000)
                    metadata[key] = f"{value}Kbps"
                    
                elif key == "bitrate_mode":
                    value = re.sub('BitrateMode(.)', "", str(muta_file.info.bitrate_mode))
                    metadata[key] = value
     
                elif key == 'album_gain':
                    value = muta_file.info.album_gain
                    metadata[key] = value
                    
                elif key == 'channels':
                    value = muta_file.info.channels
                    metadata[key] = value
                    
                elif key == 'encoder_info':
                    value = muta_file.info.encoder_info
                    metadata[key] = value
                    
                elif key == 'encoder_settings':
                    value = muta_file.info.encoder_settings
                    metadata[key] = value
                    
                elif key == 'frame_offset':
                    value = muta_file.info.frame_offset
                    metadata[key] = value
                    
                elif key == 'layer':
                    value = muta_file.info.layer
                    metadata[key] = value
                    
                elif key == 'mode':
                    value = muta_file.info.mode
                    metadata[key] = value
                    
                elif key == 'padding':
                    value = muta_file.info.padding
                    metadata[key] = value
                    
                elif key == 'protected':
                    value = muta_file.info.protected
                    metadata[key] = value
                    
                elif key == 'sample_rate':
                    value = muta_file.info.sample_rate
                    metadata[key] = f"{value}Hz"
                    
                elif key == 'track_gain':
                    value = muta_file.info.track_gain
                    metadata[key] = value
                    
                elif key == 'track_peak':
                    value = muta_file.info.track_peak
                    metadata[key] = value
                    
                elif key == 'version':
                    value = muta_file.info.version
                    metadata[key] = value
                
                elif key == "filesize":
                    value = int(os.path.getsize(muta_file.filename))
                    value = round(value * 0.00000095367432, 2)
                    metadata[key] = f"{value}Mb"
                    
                else:
                    value = muta_file.get(key)
                    if value != None:
                        metadata[key] = value[0]                    
                    else:
                        metadata[key] = ''
                
                if metadata[key] == None:
                        metadata[key] = ''  
            except Exception as e:
                metadata[key] = ''
        metadata["file_name"] = os.path.split(muta_file.filename)[1]
        metadata["file_path"] = muta_file.filename        
        return metadata
 
 
    def insert_metadata_batch(self, metadata):
        """
        Creates the insert query for all the metadata adn returns query object. 
        
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
        return query
      
      
    def TableSize(self, tablename):
        """
        Calculates the total size in bytes of all the files monitered.
        Returns the bytesize as a Float.
        
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
     
     
    def SetTable_horizontalHeader(self, View):
        """
        Sets the table header in an appropriate format thet replaces the
        underscore with space and swaps the string to title case. 
        
        :Args:
            View: QtWidgets.QTableView
                Table object to modify the header 
        """
        
        header = View.horizontalHeader().model()
        for col in range(header.columnCount()):
            col_label = header.headerData(col, Qt.Horizontal)
            data = (col_label.replace("_", " ").title())
            header.setHeaderData(col, Qt.Horizontal, data)
          
          
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
            labels.append(col_label.replace(" ", "_").lower())
        return labels

            
    def GetTableModle(self, tablename): 
        """
        Gets the QSqlTableModel for the given Table In the DB
        
        :Args:
            tablename: String
                Table name the table the model points to
        """
        tablemodel = QSqlTableModel()
        tablemodel.setTable(tablename)
        return tablemodel 
    
    
    def SetTableModle(self, View, Table): 
        """
        Sets the QTableView with the QSqlTableModel 
        
        :Args:
            View: QTableView
                view for the table to be displayed in
            
            Table: QSqlTableModel
                table with the data
        """
        View.setModel(Table)
        self.SetTable_horizontalHeader(View)
        Table.select()
      
       
    def RefreshData(self, View):
        """
        Refreshes the QTableModel
        
        :Args:
            parent_view: QTableView
                View containing the model
        """        
        table_model = View.model()
        table_model.select()        

    
    def TableSearch(self, Line_Edit, View):
        """
        Applies a filter to the QSqlTableModel and refreshes it.
        
        :Args:
            Line_Edit: QtWidgets.QLineEdit
                LineEdit that provides the text
                
            View: QtWidgets.QTableView
                View that provides the model
        
        :Errors:
            Unable to execute multiple statements at a time
        """
        Text = Line_Edit.text().strip()
        model = View.model()
        model.setFilter(f"""
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
        ERROR = model.lastError().text()
        if  ERROR != "":
            Line_Edit.clear()
            model.setFilter('')
            self.RefreshData(View)
            raise Exception(ERROR)
        
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
            self.RefreshData(View)
            raise Exception(ERROR)    
            
        
if __name__ == "__main__":
    pass
    
    
    
    

            

