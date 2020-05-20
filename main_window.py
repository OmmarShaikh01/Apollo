from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
import tinytag
import mutagen
from beets import library
import sqlite3 as sql

import json
import re
import time
import os
import threading
import random
import datetime
import hashlib 

from add_new_play_DB_ui import Ui_add_play_db
from main_window_ui import Ui_MainWindow
import file_explorer
import preferences

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

class main_window_player(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(main_window_player, self).__init__()
        self.main()

    def main(self):
        self.setupUi(self)
        self.global_decs()
        self.FileBrowser_obj = file_explorer.FileBrowser()
        self.Ui_add_play_obj = Ui_add_play_db()
        self.settings_main_window_obj = preferences.settings_main_window()
        self.all_actions()


##########################       MISC  FUNCTIONS       #########################
    def global_decs(self):
        self.global_conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.global_conn.setDatabaseName('library.db')
        if self.global_conn.open():
            print("open")

    def all_actions(self):
        self.table_view_music_functions()
    
        self.actionAdd_Files_to_librayr.triggered.connect(lambda: self.FileBrowser_obj.show())
        self.actionRescan.triggered.connect(lambda: self.database_initializedModel())

        self.Ui_add_play_obj.lineEdit.returnPressed.connect(lambda: (self.playlist_add_new(self.Ui_add_play_obj.lineEdit.text())))
        self.Ui_add_play_obj.buttonBox.accepted.connect(lambda: (self.playlist_add_new(self.Ui_add_play_obj.lineEdit.text())))
        self.Ui_add_play_obj.buttonBox.rejected.connect(lambda: self.Ui_add_play_obj.close())
        
        self.comboBox.currentTextChanged.connect(lambda: self.cbox_playlist_loader())
        self.tabWidget.currentChanged.connect(lambda: self.models_declaration())
        
#########################       LIBRARY VIEW FUNCTIONS       ###################

    def table_view_music_functions(self):
        # Atribute Declaration
        (self.tableView_music.horizontalHeader()).setSectionsMovable(True)
        self.tableView_music.setShowGrid(False)        

        # Style sheet Declartion
        self.tableView_music.setStyleSheet(("QTableView { selection-background-color: rgb(255,245,213); selection-color: black; }"))
        self.now_playing_table.setStyleSheet(("QTableView { selection-background-color: rgb(255,245,213); selection-color: black; }"))
        self.playlist_table.setStyleSheet(("QTableView { selection-background-color: rgb(255,245,213); selection-color: black; }"))
        
        # table views double click binding
        self.tableView_music.doubleClicked.connect(lambda: (self.lib_item_doubleclk(), self.models_declaration()))
        header = self.tableView_music.horizontalHeader()
        header.sortIndicatorChanged.connect(lambda:(header.sortIndicatorSection()))
        
        # table views context menu
        self.tableView_music.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView_music.customContextMenuRequested.connect(self.context_menu_tableView_music)      
        
        #library startup sequence
        self.database_initializedModel()
    
    
    def models_declaration(self):
        self.library_model = QtSql.QSqlQueryModel()
        self.library_model.setQuery("SELECT * FROM library")

        while self.library_model.canFetchMore():
            self.library_model.fetchMore(QtCore.QModelIndex())
        self.tableView_music.setModel(self.library_model)
        
        self.now_play_model = QtSql.QSqlQueryModel()
        self.now_play_model.setQuery("SELECT * FROM now_playing")

        while self.now_play_model.canFetchMore():
            self.now_play_model.fetchMore(QtCore.QModelIndex())
        self.now_playing_table.setModel(self.now_play_model)        
        
        playlist = self.comboBox.currentText()
        self.playlist_model = QtSql.QSqlQueryModel()
        self.playlist_model.setQuery(f"SELECT * FROM {playlist}")

        while self.playlist_model.canFetchMore():
            self.playlist_model.fetchMore(QtCore.QModelIndex())
        self.playlist_table.setModel(self.playlist_model)        
        
    def database_initializedModel(self):
        self.playlist_cbox_update()
        self.models_declaration()
        self.fields = [self.library_model.headerData(i, 1) for i in range(69)]
        self.headers = [((i.replace("_", " ")).title()) for i in self.fields]
        self.fields_flags = {i: 1 for i in self.fields}
    
    def lib_item_doubleclk(self):
        meta_info = QtGui.QStandardItemModel()
        for i in range(self.tableView_music.model().columnCount()):
            header = (self.tableView_music.model().headerData(i, 1)).lower()
            if header == "path":
                path = (((self.tableView_music.model()).index((self.tableView_music.currentIndex().row()), i)).data())
                self.pixmap_setter(fname = path, obj = self.pixmap_cov, scale = (300, 300))

            if header in ['album', 'artist']:
                data = (((self.tableView_music.model()).index((self.tableView_music.currentIndex().row()), i)).data())
                meta_info.appendRow(QtGui.QStandardItem(f"{(header.title())}: {data}"))
        self.file_meta_info_list.setModel(meta_info)


    def context_menu_tableView_music(self):    

        self.lv_1 = QtWidgets.QMenu()

        (self.lv_1).addAction("Play Now").triggered.connect( lambda: self.lib_view_play(0, "id", self.tableView_music, self.now_playing_table))
        (self.lv_1).addAction("Queue Next").triggered.connect( lambda: self.lib_view_queue(0, "id", self.tableView_music, self.now_playing_table))
        (self.lv_1).addAction("Queue Random").triggered.connect( lambda: self.lib_view_queue(0, "id", self.tableView_music, self.now_playing_table, flag = "shuffle"))
        self.lv_1_04 = self.lv_1.addMenu("Add To Playlist")
        (self.lv_1.addSection(''))
        self.lv_1_05 = self.lv_1.addMenu("Play (more)$")
        (self.lv_1).addAction("Edit$")
        self.lv_1_07 = self.lv_1.addMenu("Auto-Tags$")
        self.lv_1_08 = self.lv_1.addMenu("Ratings")
        (self.lv_1.addSection(''))
        (self.lv_1).addAction("Delet$e")
        self.lv_1_10 = self.lv_1.addMenu("Send To$")
        self.lv_1_11 = self.lv_1.addMenu("Search")
        self.lv_1_12 = self.lv_1.addMenu("Displayed Fields")

        (self.lv_1_04).addAction("Add To New Playlist").triggered.connect(lambda: (self.Ui_add_play_obj).show())
        (self.lv_1_04).addAction("Add To Current Playlist").triggered.connect(lambda: (self.playlist_add_current()))
        (self.lv_1_04.addSection(''))
        [(self.lv_1_04).addAction(keys).triggered.connect(lambda: (self.playlist_saver(keys))) for keys in self.playlist_cbox_update()]


        (self.lv_1_05).addAction("Bypass Filters")
        self.lv_1_05_1 = self.lv_1_05.addMenu("Output To")
        (self.lv_1_05.addSection(''))
        (self.lv_1_05).addAction("Play Shuffle").triggered.connect( lambda: self.lib_view_play(0, "id", self.tableView_music, self.now_playing_table, flag = 'shuffle'))
        (self.lv_1_05).addAction("Play Similar").triggered.connect( lambda: self.lib_view_play(13, "genre", self.tableView_music, self.now_playing_table))
        (self.lv_1_05).addAction("Play Album").triggered.connect( lambda: self.lib_view_play(8, "album", self.tableView_music, self.now_playing_table))
        (self.lv_1_05).addAction("Play Artist").triggered.connect( lambda: self.lib_view_play(5, "artist", self.tableView_music, self.now_playing_table))
        (self.lv_1_05.addSection(''))
        (self.lv_1_05).addAction("Queue Album").triggered.connect( lambda: self.lib_view_queue(8, "artist", self.tableView_music, self.now_playing_table))
        (self.lv_1_05).addAction("Queue AlbumArtist").triggered.connect( lambda: self.lib_view_queue(5, "artist", self.tableView_music, self.now_playing_table))

        (self.lv_1_08).addAction("0   Stars").triggered.connect( lambda: self.lib_view_ratings_update(0))
        (self.lv_1_08).addAction("1   Stars").triggered.connect( lambda: self.lib_view_ratings_update(1))
        (self.lv_1_08).addAction("1.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(1.5))
        (self.lv_1_08).addAction("2   Stars").triggered.connect( lambda: self.lib_view_ratings_update(2))
        (self.lv_1_08).addAction("2.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(2.5))
        (self.lv_1_08).addAction("3   Stars").triggered.connect( lambda: self.lib_view_ratings_update(3))
        (self.lv_1_08).addAction("3.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(3.5))
        (self.lv_1_08).addAction("4   Stars").triggered.connect( lambda: self.lib_view_ratings_update(4))
        (self.lv_1_08).addAction("4.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(4.5))
        (self.lv_1_08).addAction("5   Stars").triggered.connect( lambda: self.lib_view_ratings_update(5))

        (self.lv_1_10).addAction("Audio Fx")
        self.lv_1_10_1 = (self.lv_1_10).addMenu("File (Move)")
        self.lv_1_10_2 = (self.lv_1_10).addMenu("File (Copy)")
        self.lv_1_10_3 = (self.lv_1_10).addMenu("File (Replace)")
        (self.lv_1_10).addAction("File Converter")
        (self.lv_1_10).addAction("File Rescan")
        (self.lv_1_10).addAction("Analysis")

        (self.lv_1_11).addAction('Find Artist').triggered.connect( lambda: self.lib_view_search_query(field = "artist"))
        (self.lv_1_11).addAction('Find Similar').triggered.connect( lambda: self.lib_view_search_query(field = 'similar'))
        (self.lv_1_11).addAction('Locate in Playlist').triggered.connect( lambda: self.lib_view_search_query(field = 'in_playlist'))
        (self.lv_1_11).addAction('Locate in Now Playing').triggered.connect( lambda: self.lib_view_search_query(field = 'in_now_play'))
        (self.lv_1_11).addAction('Locate in File Explorer').triggered.connect( lambda: self.lib_view_search_query(field = 'in_file_exp'))

        flags = self.fields_flags
        for (key,val) in flags.items():
            aa = (self.lv_1_12.addAction(str(key).title()))
            aa.setCheckable(True)
            aa.setChecked(bool(val))
            aa.triggered.connect(lambda: self.display_fields_box_check (self.lv_1_12.actions()))
        cursor = QtGui.QCursor()
        self.lv_1.exec_(cursor.pos())

    def display_fields_box_check(self, actions):
        for index, (i,j) in enumerate(zip(self.fields_flags.keys(), actions)):
            self.fields_flags[i] = int(j.isChecked())
            if not(bool(j.isChecked())): self.tableView_music.hideColumn(index)
            if (bool(j.isChecked())): self.tableView_music.showColumn(index)

    def pixmap_setter(self, fname, obj, scale):
        # pixmap
        try:
            try:
                if os.path.splitext(fname)[1] != ".mp3":
                    meta_image = ((mutagen.File(fname)).pictures[0]).data
            except Exception as e: pass # print(e)

            try:
                meta_image = ((mutagen.File(fname)).get("APIC:")).data
            except Exception as e: pass # print(e)            

            try:
                meta_image = ((mutagen.File(fname)).get("APIC:Cover (front)")).data
            except Exception as e:  pass # print(e)

            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(meta_image)
            pixmap = pixmap.scaled(scale[0], scale[1])
            obj.setPixmap(pixmap)
            obj.setScaledContents(True)

        except Exception as e:
            pixmap = QtGui.QPixmap()
            pixmap = pixmap.scaled(scale[0], scale[1])
            obj.setPixmap(pixmap)
            obj.setScaledContents(True)
            # print(e)
    
    
    def item_set_creator(self, data):
        item = ''
        for i in data: 
            item = f"{item}, '{i}'"
        item = f"({item[1:]})"
        return item
    
    @timeit
    def view_refresher(self, view, table):
        query_model = QtSql.QSqlQueryModel()
        query_model.setQuery(f"SELECT * FROM {table}")
        
        while query_model.canFetchMore():
            query_model.fetchMore(QtCore.QModelIndex())         
        view.setModel(query_model)     
    
    def colum_sort_hint_sorter(self, num, table, query_model):
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
        sql = f"SELECT * FROM {table} ORDER BY {dic[num]}"
        query_model.setQuery(sql)
        while query_model.canFetchMore():
            query_model.fetchMore(QtCore.QModelIndex())
            
################################      CONTEX MENU FUNCTIONS       ##################################
    
    @timeit
    def lib_view_play(self, col, col_name, library_view, now_palying_view, flag = None):
        query = QtSql.QSqlQuery()
        lib_mod = self.library_model
        now_play_mod = self.now_play_model
        try:
            query.exec_("DROP VIEW now_playing")
        except Exception as e:
            print(e)
    
        if flag != "shuffle":
            rows = [(lib_mod.index(i.row(), col).data())for i in library_view.selectedIndexes()[::70]]
            rows = set(rows)
            ids = ""
            for data in rows:
                ids = f"{ids},'{data}'" 
            ids = f"({ids[1:]})"        
            query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library WHERE {col_name} IN {ids}")
            
        if flag == "shuffle":
            query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library ORDER BY random()")
    
        now_play_mod.setQuery("SELECT * FROM now_playing")
        while now_play_mod.canFetchMore():
            now_play_mod.fetchMore(QtCore.QModelIndex()) 
        now_palying_view.setModel(now_play_mod)      

    @timeit
    def lib_view_queue(self, col, col_name, lib_view, now_play_view, flag = None):
        try:
            query = QtSql.QSqlQuery()
            lib_mod = self.library_model
            now_play_mod = self.now_play_model
            prev = []
            try:
                try:
                    query.exec_(f"SELECT id FROM now_playing")
                    while query.next():
                        prev.append((query.record()).value("id"))
                except: pass                
                query.exec_("DROP VIEW now_playing")
            except Exception as e:
                print(e)
            rows = set([(lib_mod.index(i.row(), col).data())for i in lib_view.selectedIndexes()[::70]])
            ids = ""
            for data in rows:
                ids = f"{ids},'{data}'" 
            ids = f"({ids[1:]})"
            
            if flag != 'shuffle':
                query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library WHERE {col_name} IN {ids} OR id in {self.item_set_creator(prev)}")
            if flag == 'shuffle':
                query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library WHERE id IN {ids} ORDER BY random()")
    
            now_play_mod.setQuery("SELECT * FROM now_playing")
            while now_play_mod.canFetchMore():
                now_play_mod.fetchMore(QtCore.QModelIndex()) 
            now_play_view.setModel(now_play_mod)             
   
        except:
            self.lib_view_playnow()
   
    @timeit
    def lib_view_ratings_update(self, num):
        query = QtSql.QSqlQuery()
        model = self.library_model
        rows = set([(model.index(i.row(), 0).data())for i in self.tableView_music.selectedIndexes()[::70]])
        ids = ""
        for data in rows:
            ids = f"{ids},'{data}'" 
        ids = f"({ids[1:]})"
        query.exec_(f"UPDATE library SET rating = {num} WHERE id IN {ids}")
        
        model.setQuery("SELECT * FROM library")
        while model.canFetchMore():
            model.fetchMore(QtCore.QModelIndex())          
        self.tableView_music.setModel(model)
    
    @timeit
    def lib_view_search_query(self, field):
        rows = set([i.row()for i in self.tableView_music.selectedIndexes()[::70]])
        data = []
     
        if (field == "artist"):
            query_model = self.library_model
            for row in rows:
                data.extend([(query_model.index(row, 5).data()), (query_model.index(row, 8).data())])
            data = set(data) - set([' ', ''])
            sel = f"SELECT * FROM library WHERE artist IN {self.item_set_creator(data)}"
            
            query_model.setQuery(sel)
            while query_model.canFetchMore():
                query_model.fetchMore(QtCore.QModelIndex())         
            self.tableView_music.setModel(query_model)
            
        if (field == 'similar'):
            query_model = self.library_model
            for row in rows:
                data.extend([(query_model.index(row, 13).data())])
            data = set(data) - set([' ', ''])
            sel = f"SELECT * FROM library WHERE genre IN {self.item_set_creator(data)}"
            query_model.setQuery(sel)           
            while query_model.canFetchMore():
                query_model.fetchMore(QtCore.QModelIndex())         
            self.tableView_music.setModel(query_model)
            
        if (field == 'in_playlist'):
            query_model = self.playlist_model
            play = self.comboBox.currentText()
            for row in rows:
                data.extend([(query_model.index(row, 0).data())])
            data = set(data)
            sel = f"SELECT * FROM {play} WHERE id IN {self.item_set_creator(data)}"
            query_model.setQuery(sel)
            
            while query_model.canFetchMore():
                query_model.fetchMore(QtCore.QModelIndex())         
            self.playlist_table.setModel(query_model)   
            
            
        if (field == 'in_now_play'):
            query_model = self.now_play_model
            self.tabWidget.setCurrentIndex(1)
            for row in rows:
                data.extend([(query_model.index(row, 0).data())])
            data = set(data)
            sel = f"SELECT * FROM now_playing WHERE id IN {self.item_set_creator(data)}"
            query_model.setQuery(sel)

            while query_model.canFetchMore():
                query_model.fetchMore(QtCore.QModelIndex())         
            self.now_playing_table.setModel(query_model)
            
        if (field == 'in_file_exp'):
            item = rows[0]


    
    @timeit
    def playlist_cbox_update(self):
        query = QtSql.QSqlQuery()
        query.exec_("SELECT name FROM sqlite_master WHERE type = 'view' and name != 'now_playing'")
        items = []
        while query.next():
            items.append((query.record()).value('name'))
        self.comboBox.clear()
        self.comboBox.addItems(items)
        return items
    
    @timeit
    def playlist_add_current(self):
        name = self.comboBox.currentText()
        self.playlist_saver(name)
        self.cbox_playlist_loader()
    
    @timeit
    def playlist_add_new(self, name):
        if (re.match(r'[A-Za-z_-]', name) and not(re.match(r'library', name)) and not(re.match(r'now_playing', name))):
            try:
                query = QtSql.QSqlQuery()
                model = self.tableView_music.model()
                rows = [(model.index(i.row(), 0).data())for i in self.tableView_music.selectedIndexes()[::70]]
                rows = set(rows)
                ids = ""
                for data in rows:
                    ids = f"{ids},'{data}'" 
                ids = f"({ids[1:]})"
                query.exec_(f"CREATE VIEW {name} AS SELECT * FROM library WHERE id IN {ids}")
            except:
                pass
            self.Ui_add_play_obj.close()
            self.playlist_cbox_update()
    
    @timeit
    def playlist_saver(self, name):
        if (re.match(r'[A-Za-z_-]', name) and not(re.match(r'library', name)) and not(re.match(r'now_playing', name))):
            try:
                query = QtSql.QSqlQuery()
                model = self.tableView_music.model()
                prev = []
                try:
                    try:
                        query.exec_(f"SELECT id FROM {name}")
                        while query.next():
                            prev.append((query.record()).value("id"))
                    except:
                        pass                
                    query.exec_(f"DROP VIEW {name}")
                except Exception as e:
                    print(e)
                rows = [(model.index(i.row(), 0).data())for i in self.tableView_music.selectedIndexes()[::70]]
                rows.extend(prev)
                rows = set(rows)
                ids = ""
                for data in rows:
                    ids = f"{ids},'{data}'" 
                ids = f"({ids[1:]})"
                query.exec_(f"CREATE VIEW {name} AS SELECT * FROM library WHERE id IN {ids}")
            except:
                pass
    
    def cbox_playlist_loader(self): 
        playlist = self.comboBox.currentText()
        self.playlist_model.setQuery(f"SELECT * FROM {playlist}")

        while self.playlist_model.canFetchMore():
            self.playlist_model.fetchMore(QtCore.QModelIndex())
        self.playlist_table.setModel(self.playlist_model)
    
################################################################################
################################################################################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = main_window_player()
    main_window.show()
    sys.exit(app.exec_())