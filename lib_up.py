from beets import library
import sqlite3 as sql
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver as Observer

import json
import time
import os
import threading
import datetime
import hashlib

def timeit(method):
    def timed(*args, **kw):
        ts = time.monotonic()
        result = method(*args, **kw)
        te = time.monotonic()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r %2.4f s' % (method.__name__, (te - ts)))
        return result
    return timed

def database_connector_wrap(funct):
    def database_connector_exec(*args, **kwargs):
        conn = sql.connect('library.db')
        out = funct(conn = conn, *args, **kwargs)
        conn.commit()
        conn.close()            
        return out
    return database_connector_exec

class ChangesEventHandler(FileSystemEventHandler):
   
    @timeit
    def on_moved(self, event):
        super(ChangesEventHandler, self).on_moved(event)
        what = 'directory' if event.is_directory else 'file'
        out = (f"Moved {what}: from {os.path.abspath(event.src_path)} to {os.path.abspath(event.dest_path)}")
        self.file_path, self.action = os.path.abspath(event.src_path), 'moved'
        print(out)
        self.database_execute(path = self.file_path, action = self.action, dest_path = os.path.abspath(event.dest_path))
   
    @timeit
    def on_created(self, event):
        super(ChangesEventHandler, self).on_created(event)
        what = 'directory' if event.is_directory else 'file'
        out = (f"Created {what}: {os.path.abspath(event.src_path)}")
        self.file_path, self.action = os.path.abspath(event.src_path), 'created'
        print(out)
        print()
        self.database_execute(path = self.file_path, action = self.action)
   
    @timeit
    def on_deleted(self, event):
        super(ChangesEventHandler, self).on_deleted(event)
        what = 'directory' if event.is_directory else 'file'
        out = (f"Deleted {what}: {os.path.abspath(event.src_path)}")
        self.file_path, self.action = os.path.abspath(event.src_path), 'deleted'
        self.database_execute(path = self.file_path, action = self.action)
        print(out)
        print()

    def on_modified(self, event):
        super(ChangesEventHandler, self).on_modified(event)
        what = 'directory' if event.is_directory else 'file'
        out = (f"Modified {what}: {os.path.abspath(event.src_path)}")
        self.file_path, self.action = os.path.abspath(event.src_path), 'modified'
        print(out)
        print()

    
    @database_connector_wrap
    def database_execute(self,*args, **kwargs):
        cur = (kwargs['conn']).cursor()
        action = kwargs['action']
        path = kwargs["path"]
        if path != None:
            if action == 'deleted':
                path_hashv = (hashlib.md5(path.encode())).hexdigest()             
                cur.execute("DELETE FROM library WHERE path_id LIKE ? ", (f"%{path_hashv}%", ))
            
            if action == "created":
                (Library_database_mang()).file_parser( fname = path, cur = cur)
               
            if action == 'moved':
                dest_path = kwargs["dest_path"]
                cur.execute("DELETE FROM library WHERE path LIKE ? ", (f"%{path}%", ))
                result = (Library_database_mang()).file_parser(fname = dest_path, cur = cur)
                if len(result) == 69:                
                    sql = """
                    INSERT INTO library
                    (id,
                    path_id,
                    path,
                    album_id,
                    title,
                    artist, 
                    artist_sort, 
                    artist_credit, 
                    album, 
                    albumartist, 
                    albumartist_sort, 
                    albumartist_credit, 
                    genre, 
                    lyricist, 
                    composer, 
                    composer_sort, 
                    arranger, 
                    grouping, 
                    year, 
                    month, 
                    day, 
                    track, 
                    tracktotal, 
                    disc, 
                    disctotal, 
                    lyrics, 
                    comments, 
                    bpm, 
                    comp, 
                    mb_trackid, 
                    mb_albumid, 
                    mb_artistid, 
                    mb_albumartistid, 
                    mb_releasetrackid, 
                    albumtype, 
                    label, 
                    acoustid_fingerprint, 
                    acoustid_id, 
                    mb_releasegroupid, 
                    asin, 
                    catalognum, 
                    script, 
                    language, 
                    country, 
                    albumstatus, 
                    media, 
                    albumdisambig, 
                    releasegroupdisambig, 
                    disctitle, 
                    encoder, 
                    rg_track_gain, 
                    rg_track_peak, 
                    rg_album_gain, 
                    rg_album_peak, 
                    r128_track_gain, 
                    r128_album_gain, 
                    original_year, 
                    original_month, 
                    original_day, 
                    initial_key, 
                    length, 
                    bitrate, 
                    format, 
                    samplerate, 
                    bitdepth, 
                    channels, 
                    mtime, 
                    added, 
                    file_size) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    cur.executemany(sql, (result,))                
    

class Watcher:
    def __init__(self):
        self.observer = Observer()
        self.run()
    
    def run(self):
        event_handler = ChangesEventHandler()
        with open('resources/settings/config.txt') as json_file:
            data = json.load(json_file)
        stringlist = data["file_path"]
        for paths in stringlist:
            self.observer.schedule(event_handler, path = paths, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()
    

class Library_database_mang():
    
    def __init__(self, *args):
        pass
    
    @database_connector_wrap
    def database_scan_init(self, *args, **kwargs):
        conn = kwargs["conn"]
        self.obj = kwargs["label"]
        self.button = kwargs["scan_b"]
        self.button.setEnabled(False)
        self.database_table_creator(conn)
        self.database_insert_values(conn)
        self.library_stat_query(conn)
        self.obj.setText("Scanning Directories Completed")
        self.button.setEnabled(True)
        
    @timeit
    def database_table_creator(self, conn = None, *args, **kwargs):
        """
        CREATES TABLES ON FIRST STARTUP
        """
        try:
            conn.execute(f"""
                        CREATE TABLE IF NOT EXISTS library (
                        id                 TEXT UNIQUE PRIMARY KEY,
                        path_id                 TEXT UNIQUE,
                        path               TEXT,
                        album_id           TEXT,
    
                        title             TEXT,
                        artist            TEXT,
                        rating            INTEGER,
                        artist_sort       TEXT,
                        artist_credit     TEXT,
                        album             TEXT,
                        albumartist       TEXT,
                        albumartist_sort  TEXT,
                        albumartist_credit TEXT,
                        genre             TEXT,
                        lyricist          TEXT,
                        composer          TEXT,
                        composer_sort     TEXT,
                        arranger          TEXT,
                        grouping          TEXT,
                        year           INTEGER,
                        month          INTEGER,
                        day            INTEGER,
                        track          INTEGER,
                        tracktotal     INTEGER,
                        disc           INTEGER,
                        disctotal      INTEGER,
                        lyrics            TEXT,
                        comments          TEXT,
                        bpm            INTEGER,
                        comp           BOOLEAN,
                        mb_trackid        TEXT,
                        mb_albumid        TEXT,
                        mb_artistid       TEXT,
                        mb_albumartistid  TEXT,
                        mb_releasetrackid TEXT,
                        albumtype         TEXT,
                        label             TEXT,
                        acoustid_fingerprint TEXT,
                        acoustid_id       TEXT,
                        mb_releasegroupid TEXT,
                        asin              TEXT,
                        catalognum        TEXT,
                        script            TEXT,
                        language          TEXT,
                        country           TEXT,
                        albumstatus       TEXT,
                        media             TEXT,
                        albumdisambig     TEXT,
                        releasegroupdisambig TEXT,
                        disctitle         TEXT,
                        encoder           TEXT,
                        rg_track_gain        FLOAT,
                        rg_track_peak        FLOAT,
                        rg_album_gain        FLOAT,
                        rg_album_peak        FLOAT,
                        r128_track_gain      INTEGER,
                        r128_album_gain      INTEGER,
                        original_year    INTEGER,
                        original_month   INTEGER,
                        original_day     INTEGER,
                        initial_key          TEXT,
    
                        length      INTEGER,
                        bitrate     INTEGER,
                        format         TEXT,
                        samplerate  INTEGER,
                        bitdepth    INTEGER,
                        channels    INTEGER,
                        mtime       INTEGER,
                        added       INTEGER,
                        file_size   INTEGER)
                        """)
            conn.commit()
        except Exception as e:
            print("sql_table_alter:",e)   

    @timeit
    def database_insert_values(self, conn = None, *args, **kwargs):
        """
        SCANS THE PATH ON A NEW THREAD AND A NEW CONNECTION IS CREATED AND DATA IS COMMITED WHEN ALL QUERIES ARE DONE
        """
        with open('resources/settings/config.txt') as json_file:
            data = json.load(json_file)
        stringlist = data["file_path"]
        for paths in stringlist:
            self.directory_scanner(paths, conn)
    
    @timeit
    def directory_scanner(self, root, conn):      
        for dire,subd,files in os.walk(root):
            if files != []:
                self.threaded_parser(files, dire, conn)
                conn.commit()
        
    
    @timeit
    def threaded_parser(self, files, dire, conn):
        cur = conn.cursor()
        sql = f"""
        INSERT INTO library
        (id, path_id, path, album_id, title, artist, rating, 
        artist_sort, artist_credit, album, albumartist, albumartist_sort, albumartist_credit, 
        genre, lyricist, composer, composer_sort, arranger, grouping, 
        year, month, day, track, tracktotal, disc, 
        disctotal, lyrics, comments, bpm, comp, mb_trackid, 
        mb_albumid, mb_artistid, mb_albumartistid, mb_releasetrackid, albumtype, label, 
        acoustid_fingerprint, acoustid_id, mb_releasegroupid, asin, catalognum, script,
        language, country, albumstatus, media, albumdisambig, releasegroupdisambig,
        disctitle, encoder, rg_track_gain, rg_track_peak, rg_album_gain, rg_album_peak,
        r128_track_gain, r128_album_gain, original_year,original_month,original_day,initial_key,
        length, bitrate, format, samplerate, bitdepth, channels,
        mtime, added, file_size)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,?,?)
        """        
        for file in files:
            fname = os.path.abspath(os.path.join(dire, file))
            self.scanning_label_setter(self.obj, fname)
            result = (self.file_parser(fname, cur))
            try:
                if len(result) == 70:
                    cur.execute(sql, result)
            except Exception as e:
                print(e)
    
    def file_parser(self, fname, cur):
        if os.path.splitext(fname)[1] not in ['', '.jpg', ".wav", '.ini', '.png', ".txt"]:
            path_hashv = (hashlib.md5(fname.encode())).hexdigest()
            cur.execute('SELECT id FROM library WHERE path_id LIKE ?', (f"%{path_hashv}%", ))
            
            if not (cur.fetchall()): 
                item_info = library.Item.from_path(fname)
                temp = ((item_info.get("artist")) + os.path.split(item_info.get("path").decode())[1]).encode()
                hashv = (hashlib.md5(temp)).hexdigest() 
                cur.execute('SELECT id FROM library WHERE id LIKE ?', (f"%{hashv}%", ))
               
                if not cur.fetchall():
                    query = {}
                    for i in item_info.items(): query[i[0]] = i[1]                    
                    query["id"] = hashv
                    query['path_id'] = path_hashv
                    a = time.gmtime()
                    query['added'] = f"{a.tm_year}-{a.tm_mon}-{a.tm_mday} {a.tm_hour}:{a.tm_min}:{a.tm_sec}"
                    query['path'] = fname
                    query['length'] = str(datetime.timedelta(seconds=int(query['length'])))
                    query['file_size'] = item_info.try_filesize()
                    query['rating'] = 0                    
                    sql = (query['id'], query['path_id'], query['path'], query['album_id'], query['title'], query['artist'],query['rating'], 
                           query['artist_sort'], query['artist_credit'], query['album'], query['albumartist'], query['albumartist_sort'], query['albumartist_credit'], 
                           query['genre'], query['lyricist'], query['composer'], query['composer_sort'], query['arranger'], query['grouping'], 
                           query['year'], query['month'], query['day'], query['track'], query['tracktotal'], query['disc'], 
                           query['disctotal'], query['lyrics'], query['comments'], query['bpm'], query['comp'], query['mb_trackid'], 
                           query['mb_albumid'], query['mb_artistid'], query['mb_albumartistid'], query['mb_releasetrackid'], query['albumtype'], query['label'], 
                           query['acoustid_fingerprint'], query['acoustid_id'], query['mb_releasegroupid'], query['asin'], query['catalognum'], query['script'],
                           query['language'], query['country'], query['albumstatus'], query['media'], query['albumdisambig'], query['releasegroupdisambig'],
                           query['disctitle'], query['encoder'], query['rg_track_gain'], query['rg_track_peak'], query['rg_album_gain'], query['rg_album_peak'],
                           query['r128_track_gain'], query['r128_album_gain'], query['original_year'],query['original_month'],query['original_day'],query['initial_key'],
                           query['length'], query['bitrate'], query['format'], query['samplerate'], query['bitdepth'], query['channels'],
                           query['mtime'], query['added'], query['file_size'])
                    return sql
                else:
                    return ()
            
            else:
                return ()            
        
        else:
            return ()

    def library_stat_query(self, conn = None, *args, **kwargs):
        try:
            cur = conn.cursor()
            sql = f"SELECT  round(SUM(file_size)/1000000000.0,4)||' Gb' AS 'Size in Gb' FROM library"
            cur.execute(sql)
            size = cur.fetchone()[0]
        except Exception as e:
            print(e)        
        
        try:
            sql = f"SELECT sum(substr(length,-8,2) * 360) + sum(substr(length,-2,2) * 60) + sum(substr(length,-5,2)) AS 'Total Playtime' FROM library"
            cur.execute(sql)
            play_time = str(datetime.timedelta(seconds=cur.fetchone()[0]))
        except Exception as e:
            print(e)   
        
        try:
            sql = f"SELECT count(DISTINCT album) FROM library"
            cur.execute(sql)
            albums = cur.fetchone()[0]
        except Exception as e:
            print(e)           
        
        try:
            sql = f"SELECT count(DISTINCT id) FROM library"
            cur.execute(sql)
            items = cur.fetchone()[0]        
        except Exception as e:
            print(e)           
        
        try:
            sql = f"SELECT count(DISTINCT artist) from library"
            cur.execute(sql)
            artists = cur.fetchone()[0]
        except Exception as e:
            print(e)   
        
        print(size, play_time, items, albums, artists)

    def scanning_label_setter(self, obj, text):
        obj.setText(str(text))
    
class LIbrary_database_queries():
    
    def __init__(self, *args):
        pass
    
    @timeit
    def library_search_query(self, search, cur):
        search = f"%{search}%"
        sql = f"SELECT * FROM library WHERE title LIKE ?  OR artist LIKE ? OR album LIKE ? OR albumartist LIKE ?"
        cur.execute(sql, [search, search, search, search])
        result = cur.fetchall()
        print(result)
        
    
    @timeit
    def library_select_query(self, search, cur):
        search = [search] if type(search) != type(list()) else search
        temp = "".join([",?" for i in range(len(search))])
        temp = temp[1:]
        sql = f"SELECT * FROM library WHERE id in ({temp})"
        cur.execute(sql, search)
        result = cur.fetchall()
        print(result)

if __name__ == "__main__":
    (Library_database_mang()).database_scan_init()
    thread = (threading.Thread(target = Watcher, daemon = True))
    thread.start() 