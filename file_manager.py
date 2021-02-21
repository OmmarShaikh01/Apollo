import os, datetime, hashlib

from mutagen import File
from PyQt5.QtSql import QSqlQuery, QSqlDatabase

from apollo.utils import exe_time
from apollo.db.library_manager import DBFIELDS, DataBaseManager
    
class FileManager:
    """
    File manager classes manages:
    -> Scanning Directories
    -> Fetching metadata for the related file format
    
    Read Supported Formats:
    -> mp3
    -> flac
    """
    def __init__(self):
        self.DBINS = DataBaseManager()
        self.DBINS.connect("E:\\music\\MYDB.db")
    
    def TransposeMeatadata(self, Metadata):
        T_metadata = dict.fromkeys(DBFIELDS, "")
        for index, key in enumerate(T_metadata.keys()):
            T_metadata[key] = [value[index] for value in Metadata]            
        return T_metadata    

    @exe_time
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
        self.DBINS.BatchInsert_Metadata(self.TransposeMeatadata(BatchMetadata))

    @exe_time
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
        muta_file = File(Path, easy = True)
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
        muta_file = File(Path, easy = True)
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
        
if __name__ == "__main__":
        
    INST = FileManager()
    INST.ScanDirectory("E:\\music", [".mp3", ".flac", "aac", "wav"])
    INST.ScanDirectory("E:\\music", [".mp3", ".flac", "aac", "wav"])
    INST.ScanDirectory("E:\\music", [".mp3", ".flac", "aac", "wav"])
    INST.ScanDirectory("E:\\music", [".mp3", ".flac", "aac", "wav"])
