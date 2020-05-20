from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
import tinytag
import mutagen
import musicbrainzngs as mb
import sqlite3 as sql

import json
import re
import time
import os
import threading
import random
import datetime
import hashlib

from file_pros_ui import Ui_MainWindow

def timeit(method):
    def timed(*args, **kw):
        ts = time.monotonic()
        result = method(*args, **kw)
        te = time.monotonic()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r %2.2f s' % (method.__name__, (te - ts)))
        return result
    return timed

def threadit(method):
    def thread_call(*args, **kw):
        print(args, kw)
        thread = threading.Thread(target = method, args = args, kwargs = kw)
        thread.start()
    return thread_call

json_pprint = lambda val: print(json.dumps(val, indent = 2))

class musicbrainz_bindings():
    """"""

    def __init__(self):
        """Constructor"""
        self.MB_setup()
    
    def MB_setup(self):
        app = "Apollo"
        version = "1.0"
        email = "ommarshaikh17@gmail.com"
        mb.set_useragent(app, version, contact = email)
        mb.set_rate_limit(limit_or_interval = 1.0, new_requests = 10)
        mb.set_format(fmt="json")

    
    def connector(self):
        self.conn = sql.connect("library.db")
        self.cur = self.conn.cursor()
        self.cur.execute("select * from library where id = '3c70fa9f4650fc6dfd6112a3023f795b' ")
        for values in  self.cur.fetchall():
            pass
    


class file_properties_main(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(file_properties_main, self).__init__()
        self.setupUi(self)
        self.connector()
    
    
    def connector(self):
        self.conn = sql.connect("library.db")
        self.cur = self.conn.cursor()
        self.cur.execute("select * from library where id = '3c70fa9f4650fc6dfd6112a3023f795b' ")
        for values in  self.cur.fetchall():
            (self.IP_loader(value = values))
        
    def value_binder(self, values):
        dic = {0: 'id',1: 'path_id',2: 'path',3: 'album_id',4: 'title',5: 'artist',6: 'rating',7: 'artist_sort',
               8: 'artist_credit',9: 'album',10: 'albumartist',11: 'albumartist_sort',12: 'albumartist_credit',13: 'genre',14: 'lyricist',
               15: 'composer',16: 'composer_sort',17: 'arranger',18: 'grouping',19: 'year',20: 'month',21: 'day',
               22: 'track',23: 'tracktotal',24: 'disc',25: 'disctotal',26: 'lyrics',27: 'comments',28: 'bpm',
               29: 'comp',30: 'mb_trackid',31: 'mb_albumid',32: 'mb_artistid',33: 'mb_albumartistid',34: 'mb_releasetrackid',
               35: 'albumtype',36: 'label',37: 'acoustid_fingerprint',38: 'acoustid_id',39: 'mb_releasegroupid',40: 'asin',
               41: 'catalognum',42: 'script',43: 'language',44: 'country',45: 'albumstatus',46: 'media',47: 'albumdisambig',
               48: 'releasegroupdisambig',49: 'disctitle',50: 'encoder',51: 'rg_track_gain',52: 'rg_track_peak',53: 'rg_album_gain',
               54: 'rg_album_peak',55: 'r128_track_gain',56: 'r128_album_gain',57: 'original_year',58: 'original_month',
               59: 'original_day',60: 'initial_key',61: 'length',62: 'bitrate',63: 'format',64: 'samplerate',65: 'bitdepth',
               66: 'channels',67: 'mtime',68: 'added',69: 'file_size'}
        result = {k: v for k, v in zip(dic.values(), values)}
        return result
    
    def IP_loader(self, value):

        data = ['', 'Title', 'Artist', 'Rating', 'Artist Sort', 'Artist Credit', 'Album', 'Albumartist',
                'Albumartist Sort', 'Albumartist Credit', 'Genre', 'Lyricist', 'Composer', 'Composer Sort',
                'Arranger', 'Grouping', 'Year', 'Month', 'Day', 'Track', 'Tracktotal', 'Disc', 'Disctotal',
                'Lyrics', 'Comments', 'Bpm', 'Comp', 'Albumtype', 'Label', 'Acoustid Fingerprint', 'Acoustid Id',
                'Mb Releasegroupid', 'Asin', 'Catalognum', 'Script', 'Language', 'Country', 'Albumstatus', 'Media',
                'Albumdisambig', 'Releasegroupdisambig', 'Disctitle', 'Encoder', 'Rg Track Gain', 'Rg Track Peak',
                'Rg Album Gain', 'Rg Album Peak', 'R128 Track Gain', 'R128 Album Gain', 'Original Year',
                'Original Month', 'Original Day', 'Initial Key', 'Length', 'Bitrate', 'Format', 'Samplerate',
                'Bitdepth', 'Channels', 'Mtime', 'Added', 'File Size']
       
        value = self.value_binder(value)
        path = value["path"]
        value = ["", value['title'],value['artist'],value['rating'],value['artist_sort'],value['artist_credit'],value['album'],value['albumartist'],value['albumartist_sort'],
                value['albumartist_credit'],value['genre'],value['lyricist'],value['composer'],value['composer_sort'],value['arranger'],value['grouping'],value['year'],
                value['month'],value['day'],value['track'],value['tracktotal'],value['disc'],value['disctotal'],value['lyrics'],value['comments'],value['bpm'],value['comp'],
                value['albumtype'],value['label'],value['acoustid_fingerprint'],value['acoustid_id'],value['mb_releasegroupid'],value['asin'],value['catalognum'],
                value['script'],value['language'],value['country'],value['albumstatus'],value['media'],value['albumdisambig'],value['releasegroupdisambig'],
                value['disctitle'],value['encoder'],value['rg_track_gain'],value['rg_track_peak'],value['rg_album_gain'],value['rg_album_peak'],value['r128_track_gain'],
                value['r128_album_gain'],value['original_year'],value['original_month'],value['original_day'],value['initial_key'],
                value['length'],value['bitrate'],value['format'],value['samplerate'],value['bitdepth'],value['channels'],value['mtime'],value['added'],
                value['file_size']]
        
        self.IP_label.setText(data[1]); self.IP_edit.setText(str(value[1]))
        self.IP_label_2.setText(data[2]); self.IP_edit_2.setText(str(value[2]))
        self.IP_label_3.setText(data[3]); self.IP_edit_3.setText(str(value[3]))
        self.IP_label_4.setText(data[4]); self.IP_edit_4.setText(str(value[4]))
        self.IP_label_5.setText(data[5]); self.IP_edit_5.setText(str(value[5]))
        self.IP_label_6.setText(data[6]); self.IP_edit_6.setText(str(value[6]))
        self.IP_label_7.setText(data[7]); self.IP_edit_7.setText(str(value[7]))
        self.IP_label_8.setText(data[8]); self.IP_edit_8.setText(str(value[8]))
        self.IP_label_9.setText(data[9]); self.IP_edit_9.setText(str(value[9]))
        self.IP_label_10.setText(data[10]); self.IP_edit_10.setText(str(value[10]))

        self.IP_label_11.setText(data[11]); self.IP_edit_11.setText(str(value[11]))
        self.IP_label_12.setText(data[12]); self.IP_edit_12.setText(str(value[12]))
        self.IP_label_13.setText(data[13]); self.IP_edit_13.setText(str(value[13]))
        self.IP_label_14.setText(data[14]); self.IP_edit_14.setText(str(value[14]))
        self.IP_label_15.setText(data[15]); self.IP_edit_15.setText(str(value[15]))
        self.IP_label_16.setText(data[16]); self.IP_edit_16.setText(str(value[16]))
        self.IP_label_17.setText(data[17]); self.IP_edit_17.setText(str(value[17]))
        self.IP_label_18.setText(data[18]); self.IP_edit_18.setText(str(value[18]))
        self.IP_label_19.setText(data[19]); self.IP_edit_19.setText(str(value[19]))
        self.IP_label_20.setText(data[20]); self.IP_edit_20.setText(str(value[20]))
        
        self.IP_label_21.setText(data[21]); self.IP_edit_21.setText(str(value[21]))
        self.IP_label_22.setText(data[22]); self.IP_edit_22.setText(str(value[22]))
        self.IP_label_23.setText(data[23]); self.IP_edit_23.setText(str(value[23]))
        self.IP_label_24.setText(data[24]); self.IP_edit_24.setText(str(value[24]))
        self.IP_label_25.setText(data[25]); self.IP_edit_25.setText(str(value[25]))
        self.IP_label_26.setText(data[26]); self.IP_edit_26.setText(str(value[26]))
        self.IP_label_27.setText(data[27]); self.IP_edit_27.setText(str(value[27]))
        self.IP_label_28.setText(data[28]); self.IP_edit_28.setText(str(value[28]))
        self.IP_label_29.setText(data[29]); self.IP_edit_29.setText(str(value[29]))
        self.IP_label_30.setText(data[30]); self.IP_edit_30.setText(str(value[30]))
        
        self.IP_label_31.setText(data[31]); self.IP_edit_31.setText(str(value[31]))
        self.IP_label_32.setText(data[32]); self.IP_edit_32.setText(str(value[32]))
        self.IP_label_33.setText(data[33]); self.IP_edit_33.setText(str(value[33]))
        self.IP_label_34.setText(data[34]); self.IP_edit_34.setText(str(value[34]))
        self.IP_label_35.setText(data[35]); self.IP_edit_35.setText(str(value[35]))
        self.IP_label_36.setText(data[36]); self.IP_edit_36.setText(str(value[36]))
        self.IP_label_37.setText(data[37]); self.IP_edit_37.setText(str(value[37]))
        self.IP_label_38.setText(data[38]); self.IP_edit_38.setText(str(value[38]))
        self.IP_label_39.setText(data[39]); self.IP_edit_39.setText(str(value[39]))
        self.IP_label_40.setText(data[40]); self.IP_edit_40.setText(str(value[40]))
        
        self.IP_label_41.setText(data[41]); self.IP_edit_41.setText(str(value[41]))
        self.IP_label_42.setText(data[42]); self.IP_edit_42.setText(str(value[42]))
        self.IP_label_43.setText(data[43]); self.IP_edit_43.setText(str(value[43]))
        self.IP_label_44.setText(data[44]); self.IP_edit_44.setText(str(value[44]))
        self.IP_label_45.setText(data[45]); self.IP_edit_45.setText(str(value[45]))
        self.IP_label_46.setText(data[46]); self.IP_edit_46.setText(str(value[46]))
        self.IP_label_47.setText(data[47]); self.IP_edit_47.setText(str(value[47]))
        self.IP_label_48.setText(data[48]); self.IP_edit_48.setText(str(value[48]))
        self.IP_label_49.setText(data[49]); self.IP_edit_49.setText(str(value[49]))
        self.IP_label_50.setText(data[50]); self.IP_edit_50.setText(str(value[50]))
        
        self.IP_label_51.setText(data[51]); self.IP_edit_51.setText(str(value[51]))
        self.IP_label_52.setText(data[52]); self.IP_edit_52.setText(str(value[52]))
        self.IP_label_53.setText(data[53]); self.IP_edit_53.setText(str(value[53]))
        self.IP_label_54.setText(data[54]); self.IP_edit_54.setText(str(value[54]))
        self.IP_label_55.setText(data[55]); self.IP_edit_55.setText(str(value[55]))
        self.IP_label_56.setText(data[56]); self.IP_edit_56.setText(str(value[56]))
        self.IP_label_57.setText(data[57]); self.IP_edit_57.setText(str(value[57]))
        self.IP_label_58.setText(data[58]); self.IP_edit_58.setText(str(value[58]))
        self.IP_label_59.setText(data[59]); self.IP_edit_59.setText(str(value[59]))
        self.IP_label_60.setText(data[60]); self.IP_edit_60.setText(str(value[60]))
        
        self.IP_label_61.setText("File Name"); self.IP_edit_61.setText(os.path.split(path)[1])
        self.IP_label_62.setText('File Path'); self.IP_edit_62.setText(path)
    
if __name__ == "__main__":
    import sys
    #app = QtWidgets.QApplication(sys.argv)
    #main_window = file_properties_main()
    #main_window.show()
    #sys.exit(app.exec_())
    musicbrainz_bindings()