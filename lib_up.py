import mutagen
import sqlite3 as sql
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver as Observer

import json
import time
import os
import threading
import datetime
import hashlib
import functools

Column_lut ={'acoustid_fingerprint': 18,
             'acoustid_id': 19,
             'added': 15,
             'album': 6,
             'albumartist': 7,
             'albumartistsort': 67,
             'albumsort': 68,
             'arranger': 69,
             'artist': 4,
             'artistsort': 70,
             'asin': 48,
             'author': 49,
             'barcode': 50,
             'bitrate': 10,
             'bitrate_mode': 22,
             'bpm': 17,
             'catalognumber': 51,
             'channels': 9,
             'compilation': 52,
             'composer': 53,
             'composersort': 71,
             'conductor': 42,
             'copyright': 43,
             'date': 44,
             'discnumber': 45,
             'discsubtitle': 46,
             'encodedby': 47,
             'encoder_settings': 23,
             'filename': 3,
             'filesize': 13,
             'filetype': 14,
             'frame_offset': 24,
             'genre': 8,
             'id': 0,
             'isrc': 30,
             'language': 31,
             'layer': 25,
             'length': 12,
             'lyricist': 32,
             'media': 33,
             'mode': 26,
             'mood': 34,
             'musicbrainz_albumartistid': 54,
             'musicbrainz_albumid': 55,
             'musicbrainz_albumstatus': 56,
             'musicbrainz_albumtype': 57,
             'musicbrainz_artistid': 58,
             'musicbrainz_discid': 59,
             'musicbrainz_releasegroupid': 60,
             'musicbrainz_releasetrackid': 61,
             'musicbrainz_trackid': 62,
             'musicbrainz_trmid': 63,
             'musicbrainz_workid': 64,
             'musicip_fingerprint': 65,
             'musicip_puid': 66,
             'organization': 35,
             'originaldate': 36,
             'padding': 27,
             'path': 2,
             'path_id': 1,
             'performer': 37,
             'protected': 28,
             'ratings': 16,
             'releasecountry': 38,
             'replaygain_gain': 20,
             'replaygain_peak': 21,
             'sample_rate': 11,
             'sketchy': 29,
             'title': 5,
             'titlesort': 72,
             'tracknumber': 39,
             'version': 40,
             'website': 41}

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

def exception(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
    except:
        return None
    return result

def muta_dict_init(path, path_hashv = None):
    
    def dic_simp(dic, key):
        try:
            if key == "bitrate_mode":
                result = str(dic[key]).replace("BitrateMode.", "")
            else: result = dic[key]
        except:
            result = None    
        return result          
    
    muta_obj = mutagen.File(path, easy = True)
    if path_hashv == None:
        path_hashv = (hashlib.md5(path.encode())).hexdigest()
        
    t = time.gmtime()        
    muta_dict = {'id': None,
                 'path_id': path_hashv,
                 'path': path,   
                 'filename': os.path.split(muta_obj.filename)[1],
                 'artist': muta_obj.get('artist'),
                 'title': muta_obj.get('title'),
                 'album': muta_obj.get('album'),
                 'albumartist': muta_obj.get('albumartist'),             
                 'genre': muta_obj.get('genre'),
                 
                 'channels': dic_simp(muta_obj.info.__dict__, 'channels'),
                 'bitrate': dic_simp(muta_obj.info.__dict__, 'bitrate'),
                 'sample_rate': dic_simp(muta_obj.info.__dict__, 'sample_rate'),
                 'length': str(datetime.timedelta(seconds = dic_simp(muta_obj.info.__dict__, 'length'))),
                 'filesize': os.stat(path).st_size,
                 'filetype': (os.path.splitext(path)[1][1:]).upper(), 
                 'added': str(datetime.datetime.now()),
                 'ratings': 0,
                 'bpm': muta_obj.get('bpm'),             
                         
                 'acoustid_fingerprint': muta_obj.get('acoustid_fingerprint'),
                 'acoustid_id': muta_obj.get('acoustid_id'),             
                 'replaygain_gain': muta_obj.get('replaygain_*_gain'),
                 'replaygain_peak': muta_obj.get('replaygain_*_peak'),             
                 'bitrate_mode': dic_simp(muta_obj.info.__dict__, 'bitrate_mode'),
                 'encoder_settings': dic_simp(muta_obj.info.__dict__, 'encoder_settings'),
                 'frame_offset': dic_simp(muta_obj.info.__dict__, 'frame_offset'),
                 'layer': dic_simp(muta_obj.info.__dict__, 'layer'),
                 'mode': dic_simp(muta_obj.info.__dict__, 'mode'),
                 'padding': dic_simp(muta_obj.info.__dict__, 'padding'),
                 'protected': dic_simp(muta_obj.info.__dict__, 'protected'),
                 'sketchy': dic_simp(muta_obj.info.__dict__, 'sketchy'),
                         
                 'isrc': muta_obj.get('isrc'),
                 'language': muta_obj.get('language'),
                 'lyricist': muta_obj.get('lyricist'),
                 'media': muta_obj.get('media'),
                 'mood': muta_obj.get('mood'),
                 'organization': muta_obj.get('organization'),
                 'originaldate': muta_obj.get('originaldate'),
                 'performer': muta_obj.get('performer'),
                 'releasecountry': muta_obj.get('releasecountry'),             
                 'tracknumber': muta_obj.get('tracknumber'),
                 'version': muta_obj.get('version'),
                 'website': muta_obj.get('website'),
                 'conductor': muta_obj.get('conductor'),
                 'copyright': muta_obj.get('copyright'),
                 'date': muta_obj.get('date'),
                 'discnumber': muta_obj.get('discnumber'),
                 'discsubtitle': muta_obj.get('discsubtitle'),
                 'encodedby': muta_obj.get('encodedby'),             
                 'asin': muta_obj.get('asin'),
                 'author': muta_obj.get('author'),
                 'barcode': muta_obj.get('barcode'),
                 'catalognumber': muta_obj.get('catalognumber'),
                 'compilation': muta_obj.get('compilation'),
                 'composer': muta_obj.get('composer'),             
                         
                 'musicbrainz_albumartistid': muta_obj.get('musicbrainz_albumartistid'),
                 'musicbrainz_albumid': muta_obj.get('musicbrainz_albumid'),
                 'musicbrainz_albumstatus': muta_obj.get('musicbrainz_albumstatus'),
                 'musicbrainz_albumtype': muta_obj.get('musicbrainz_albumtype'),
                 'musicbrainz_artistid': muta_obj.get('musicbrainz_artistid'),
                 'musicbrainz_discid': muta_obj.get('musicbrainz_discid'),
                 'musicbrainz_releasegroupid': muta_obj.get('musicbrainz_releasegroupid'),
                 'musicbrainz_releasetrackid': muta_obj.get('musicbrainz_releasetrackid'),
                 'musicbrainz_trackid': muta_obj.get('musicbrainz_trackid'),
                 'musicbrainz_trmid': muta_obj.get('musicbrainz_trmid'),
                 'musicbrainz_workid': muta_obj.get('musicbrainz_workid'),
                 'musicip_fingerprint': muta_obj.get('musicip_fingerprint'),
                 'musicip_puid': muta_obj.get('musicip_puid'),
                         
                 'albumartistsort': muta_obj.get('albumartistsort'),
                 'albumsort': muta_obj.get('albumsort'),
                 'arranger': muta_obj.get('arranger'),
                 'artistsort': muta_obj.get('artistsort'),
                 'composersort': muta_obj.get('composersort'),
                 'titlesort': muta_obj.get('titlesort'),             
                 }
    for k, v in muta_dict.items(): 
        if type(list()) == type(v):
            muta_dict[k] = v[0]
        if v == None:
            muta_dict[k] = ""
    muta_dict["id"] = hashlib.md5((muta_dict["artist"].lower() + muta_dict["title"].lower() + muta_dict["album"].lower()).encode()).hexdigest()
    
    return muta_dict


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
        self.obj = kwargs["label"] if ("label" in kwargs) else None
        self.button = kwargs["scan_b"] if ("scan_b" in kwargs) else None
        if (self.button is not None): self.button.setEnabled(False)
        self.database_table_creator(conn)
        self.directory_scanner(conn)
        self.library_stat_query(conn)
        if (self.obj is not None): self.obj.setText("Scanning Directories Completed")
        if (self.button is not None): self.button.setEnabled(True)
        
    @timeit
    def database_table_creator(self, conn = None, *args, **kwargs):
        """
        CREATES TABLES ON FIRST STARTUP
        """
        try:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS
            library(
            id TEXT,
            path_id TEXT,
            path TEXT,
            filename TEXT,
            artist TEXT,
            title TEXT,
            album TEXT,
            albumartist TEXT,
            genre TEXT,
            
            channels INTEGER,
            bitrate INTEGER,
            sample_rate INTEGER,
            length INTEGER,
            filesize INTEGER,
            filetype TEXT,
            added INTEGER,
            ratings INTEGER,
            bpm INTEGER,
            
            acoustid_fingerprint TEXT,
            acoustid_id TEXT,
            replaygain_gain TEXT,
            replaygain_peak TEXT,
            bitrate_mode TEXT,
            encoder_settings TEXT,
            frame_offset TEXT,
            layer TEXT,
            mode TEXT,
            padding TEXT,
            protected TEXT,
            sketchy TEXT,
            
            isrc TEXT,
            language TEXT,
            lyricist TEXT,
            media TEXT,
            mood TEXT,
            organization TEXT,
            originaldate TEXT,
            performer TEXT,
            releasecountry TEXT,
            tracknumber INTEGER,
            version TEXT,
            website TEXT,
            conductor TEXT,
            copyright TEXT,
            date TEXT,
            discnumber INTEGER,
            discsubtitle TEXT,
            encodedby TEXT,
            asin TEXT,
            author TEXT,
            barcode INTEGER,
            catalognumber INTEGER,
            compilation TEXT,
            composer TEXT,
            
            musicbrainz_albumartistid TEXT,
            musicbrainz_albumid TEXT,
            musicbrainz_albumstatus TEXT,
            musicbrainz_albumtype TEXT,
            musicbrainz_artistid TEXT,
            musicbrainz_discid TEXT,
            musicbrainz_releasegroupid TEXT,
            musicbrainz_releasetrackid TEXT,
            musicbrainz_trackid TEXT,
            musicbrainz_trmid TEXT,
            musicbrainz_workid TEXT,
            musicip_fingerprint TEXT,
            musicip_puid TEXT,
            
            albumartistsort TEXT,
            albumsort TEXT,
            arranger TEXT,
            artistsort TEXT,
            composersort TEXT,
            titlesort TEXT
            )
            """)
            
            views = ["now_playing", "playlist", "audio_bk", "search_query", "history"]
            for view in  views:
                conn.execute(f"""
                CREATE VIEW {view} AS
                SELECT 
                NULL AS id,
                NULL AS path_id,
                NULL AS path,
                NULL AS filename,
                NULL AS artist,
                NULL AS title,
                NULL AS album,
                NULL AS albumartist,
                NULL AS genre,
                
                NULL AS channels,
                NULL AS bitrate,
                NULL AS sample_rate,
                NULL AS length,
                NULL AS filesize,
                NULL AS filetype,
                NULL AS added,
                NULL AS ratings,
                NULL AS bpm,
                
                NULL AS acoustid_fingerprint,
                NULL AS acoustid_id,
                NULL AS replaygain_gain,
                NULL AS replaygain_peak,
                NULL AS bitrate_mode,
                NULL AS encoder_settings,
                NULL AS frame_offset,
                NULL AS layer,
                NULL AS mode,
                NULL AS padding,
                NULL AS protected,
                NULL AS sketchy,
                
                NULL AS isrc,
                NULL AS language,
                NULL AS lyricist,
                NULL AS media,
                NULL AS mood,
                NULL AS organization,
                NULL AS originaldate,
                NULL AS performer,
                NULL AS releasecountry,
                NULL AS tracknumber,
                NULL AS version,
                NULL AS website,
                NULL AS conductor,
                NULL AS copyright,
                NULL AS date,
                NULL AS discnumber,
                NULL AS discsubtitle,
                NULL AS encodedby,
                NULL AS asin,
                NULL AS author,
                NULL AS barcode,
                NULL AS catalognumber,
                NULL AS compilation,
                NULL AS composer,
                
                NULL AS musicbrainz_albumartistid,
                NULL AS musicbrainz_albumid,
                NULL AS musicbrainz_albumstatus,
                NULL AS musicbrainz_albumtype,
                NULL AS musicbrainz_artistid,
                NULL AS musicbrainz_discid,
                NULL AS musicbrainz_releasegroupid,
                NULL AS musicbrainz_releasetrackid,
                NULL AS musicbrainz_trackid,
                NULL AS musicbrainz_trmid,
                NULL AS musicbrainz_workid,
                NULL AS musicip_fingerprint,
                NULL AS musicip_puid,
                
                NULL AS albumartistsort,
                NULL AS albumsort,
                NULL AS arranger,
                NULL AS artistsort,
                NULL AS composersort,
                NULL AS titlesort
                """)
            
            conn.commit()
        except Exception as e:
            print("sql_table_alter:",e)   


    @timeit
    def directory_scanner(self, conn):
        cur = conn.cursor()
        with open('resources/settings/config.txt') as json_file:
            data = json.load(json_file)
        stringlist = data["file_path"]
        for root in stringlist:        
            for dire,subd,files in os.walk(root):
                if files != []:
                    for file in files:
                        fname = os.path.abspath(os.path.join(dire, file))
                        if os.path.splitext(fname)[1] not in ['', '.jpg', ".wav", '.ini', '.png', ".txt"]:
                            self.parser(fname, cur)
                conn.commit()
    
    def parser(self, path, cur):  
        try:
            self.scanning_label_setter(self.obj, path)
            path_hashv = (hashlib.md5(path.encode())).hexdigest()
            cur.execute('SELECT id FROM library WHERE path_id LIKE ?', (f"%{path_hashv}%", ))
            if not (cur.fetchall()): 
                muta_dict = muta_dict_init(path, path_hashv)
                
                cur.execute('SELECT id FROM library WHERE id LIKE ?', (f"%{muta_dict['id']}%", ))
                if not cur.fetchall():
                    sql = """
                        INSERT INTO library(
                        id,
                        path_id,
                        path,
                        filename,
                        artist,
                        title,
                        album,
                        albumartist,
                        genre,
            
                        channels,
                        bitrate,
                        sample_rate,
                        length,
                        filesize,
                        filetype,
                        added,
                        ratings,
                        bpm,
            
                        acoustid_fingerprint,
                        acoustid_id,
                        replaygain_gain,
                        replaygain_peak,
                        bitrate_mode,
                        encoder_settings,
                        frame_offset,
                        layer,
                        mode,
                        padding,
                        protected,
                        sketchy,
            
                        isrc,
                        language,
                        lyricist,
                        media,
                        mood,
                        organization,
                        originaldate,
                        performer,
                        releasecountry,
                        tracknumber,
                        version,
                        website,
                        conductor,
                        copyright,
                        date,
                        discnumber,
                        discsubtitle,
                        encodedby,
                        asin,
                        author,
                        barcode,
                        catalognumber,
                        compilation,
                        composer,
            
                        musicbrainz_albumartistid,
                        musicbrainz_albumid,
                        musicbrainz_albumstatus,
                        musicbrainz_albumtype,
                        musicbrainz_artistid,
                        musicbrainz_discid,
                        musicbrainz_releasegroupid,
                        musicbrainz_releasetrackid,
                        musicbrainz_trackid,
                        musicbrainz_trmid,
                        musicbrainz_workid,
                        musicip_fingerprint,
                        musicip_puid,
            
                        albumartistsort,
                        albumsort,
                        arranger,
                        artistsort,
                        composersort,
                        titlesort) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                        ?,?,?,?,?)
                        """                    
                    cur.execute(sql, list(muta_dict.values()))
        except Exception as e:
            print(e)
    
    def scanning_label_setter(self, obj, text):
        if (self.obj is not None): obj.setText(str(text))
    
    
    @database_connector_wrap
    def library_stat_query(self, *args, **kwargs):
        conn = kwargs["conn"]
        if conn:
            try:
                cur = conn.cursor()
                sql = f"SELECT  round(SUM(filesize)/1000000000.0,4)||' Gb' AS 'Size in Gb' FROM library"
                cur.execute(sql)
                size = cur.fetchone()[0]
            except Exception as e:
                size = 0
                print(e)        
            
            try:
                sql = f"SELECT sum(substr(length,1,1))*360 + sum(substr(length,3,2))*60 +sum(substr(length,6,2)) FROM library"
                cur.execute(sql)
                play_time = str(datetime.timedelta(seconds=cur.fetchone()[0]))
            except Exception as e:
                play_time = 0
                print(e)   
            
            try:
                sql = f"SELECT count(DISTINCT album) FROM library"
                cur.execute(sql)
                albums = cur.fetchone()[0]
            except Exception as e:
                albums = 0
                print(e)           
            
            try:
                sql = f"SELECT count(DISTINCT id) FROM library"
                cur.execute(sql)
                items = cur.fetchone()[0]        
            except Exception as e:
                items = 0        
                print(e)           
            
            try:
                sql = f"SELECT count(DISTINCT artist) from library"
                cur.execute(sql)
                artists = cur.fetchone()[0]
            except Exception as e:
                artists = 0
                print(e)   
            
            out = f"Library Size: {size}, Play time: {play_time}, Files: {items}, Albums:{albums}, Artists:{artists}"
            return out

if __name__ == "__main__":
    (Library_database_mang()).database_scan_init()
    thread = (threading.Thread(target = Watcher, daemon = True))
    thread.start() 

