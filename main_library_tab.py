from main_window_ui import Ui_MainWindow
from utils import *
from lib_up import Library_database_mang, Column_lut
from add_new_play_DB_ui import Ui_add_play_db
from file_explorer import FileBrowser

import sys, threading, re, logging, queue, json

from PyQt5 import QtGui, QtSql, QtCore, QtWidgets
import mutagen
       
        
class Main_window(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self, *args):
        super(Main_window, self).__init__()
        self.setupUi(self)

    @database_connector_wrap
    def table_creator(self, **kwargs):
        conn = kwargs["conn"]
        Library_database_mang().database_table_creator(conn)
    
    
    def database_statrup(self):
        self.table_creator()
        self.global_conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.global_conn.setDatabaseName('library.db')
        if self.global_conn.open():
            print("open")
            self.models_declaration()
            self.table_view_music_functions()
    
    def models_declaration(self):
        self.library_model_dec()
        self.now_playing_model_dec()
        self.playlist_model_dec()
        self.search_model_dec()
        self.library_play_model_dec()
        self.playlist_play_model_dec()

    def playlist_play_model_dec(self):
        self.playlist_play_model = QtSql.QSqlTableModel()
        self.playlist_play_model.setTable("now_playing")
        self.playlist_play_model.setQuery(QtSql.QSqlQuery("SELECT title FROM now_playing"))
        self.playlist_play_model.select()
        while self.playlist_play_model.canFetchMore():
            self.playlist_play_model.fetchMore(QtCore.QModelIndex())       
        self.playlist_play_model.setHeaderData(0, 1, ("title".replace("_", ' ')).title())
        self.playlist_play_view.setModel(self.playlist_play_model)        

    def library_play_model_dec(self):
        items = []
        self.audio_queue = Playback_queue(self.now_playing_model.rowCount())
        for i in range(self.now_playing_model.rowCount()):
            data = self.now_playing_model.index(i, Column_lut['title']).data()
            items.extend([QtGui.QStandardItem(data)])
            data = self.now_playing_model.index(i, Column_lut['path']).data()
            self.audio_queue.put(data)
            
        self.library_play_model = QtGui.QStandardItemModel()
        self.library_play_model.setHeaderData(1, 1, "Title")
        self.library_play_model.appendColumn(items)
        self.lib_play_view.setModel(self.library_play_model)        
                  

    def search_model_dec(self):
        self.search_model = QtSql.QSqlTableModel()
        self.search_model.setTable("search_query")
        self.search_model.select()
        while self.search_model.canFetchMore():
            self.search_model.fetchMore(QtCore.QModelIndex())           
        [self.search_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
        self.search_view.setModel(self.search_model)

    def playlist_model_dec(self):
        self.playlist_cbox_update(self.playlist_combo)
        self.playlist_model = QtSql.QSqlTableModel()
        self.playlist_model.setTable(f"{self.playlist_combo.currentText()}")
        self.playlist_model.select()
        while self.playlist_model.canFetchMore():
            self.playlist_model.fetchMore(QtCore.QModelIndex())           
        [self.playlist_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
        self.playlist_view.setModel(self.playlist_model)

    def now_playing_model_dec(self):
        self.now_playing_model = QtSql.QSqlTableModel()
        self.now_playing_model.setTable("now_playing")
        self.now_playing_model.select()
        while self.now_playing_model.canFetchMore():
            self.now_playing_model.fetchMore(QtCore.QModelIndex())           
        [self.now_playing_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
        self.now_playing_view.setModel(self.now_playing_model)

    def library_model_dec(self):
        self.library_model = QtSql.QSqlTableModel()
        self.library_model.setTable("library")
        [self.library_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
        self.library_model.select()
        while self.library_model.canFetchMore():
            self.library_model.fetchMore(QtCore.QModelIndex())        
        self.library_view.setModel(self.library_model)
        self.fields = list(Column_lut.keys())
        self.fields_flags = {i: 1 for i in self.fields}
        self.headers = [((i.replace("_", " ")).title()) for i in Column_lut.keys()]
        
    def table_view_music_functions(self):
        # Atribute Declaration
        (self.library_view.horizontalHeader()).setSectionsMovable(True)       
        
        # table views double click binding
        self.library_view.doubleClicked.connect(lambda: (self.lib_item_doubleclk()))
        
        self.Ui_add_play_obj = Ui_add_play_db()
        self.Ui_add_play_obj.lineEdit.returnPressed.connect(lambda: (self.playlist_add_new(self.Ui_add_play_obj.lineEdit.text(), self.playlist_combo),self.Ui_add_play_obj.close()))
        self.Ui_add_play_obj.buttonBox.accepted.connect(lambda: (self.playlist_add_new(self.Ui_add_play_obj.lineEdit.text(), self.playlist_combo),self.Ui_add_play_obj.close()))
        self.Ui_add_play_obj.buttonBox.rejected.connect(lambda: self.Ui_add_play_obj.close())
        
        self.library_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.library_view.customContextMenuRequested.connect(self.context_menu_tableView_music)          
        self.playlist_combo.currentTextChanged.connect(lambda: self.cbox_playlist_loader(self.playlist_combo))
        
        self.library_view.horizontalHeader().sortIndicatorChanged.connect(lambda: (self.lib_sort_hint()))
        self.playlist_view.horizontalHeader().sortIndicatorChanged.connect(lambda: (self.playlist_sort_hint()))
        
        self.file_explorer_object = FileBrowser()
        self.file_explorer_object.buttonBox.accepted.connect(lambda: (self.models_declaration(), self.file_explorer_object.close()))
        self.rescanA.triggered.connect(lambda: self.models_declaration())
        self.add_folders_to_libA.triggered.connect(lambda: self.menu_bar_actions(1))


    def menu_bar_actions(self,pos):
        if pos == 1:
            self.file_explorer_object.show()

    def context_menu_tableView_music(self):
        self.lv_1 = QtWidgets.QMenu()
        self.lv_1.setStyleSheet("""
        QMenuBar {
        background-color: rgb(0, 0, 0);
        spacing: 3px;
            color: rgb(255, 255, 255);
        }
        
        QMenuBar::item {
            padding: 1px 4px;
            background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(0, 146, 255, 255), stop:0.0511364 rgba(0, 24, 43, 255), stop:0.522727 rgba(0, 0, 0, 255), stop:0.948864 rgba(0, 30, 52, 255), stop:1 rgba(0, 149, 255, 255));
            border-radius: 4 px;
                color: rgb(255, 255, 255);
        }
        
        QMenuBar::item:selected { /* when selected using mouse or keyboard */
            background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(0, 146, 255, 255), stop:0.102273 rgba(0, 0, 0, 255), stop:0.522727 rgba(0, 0, 0, 255), stop:0.892045 rgba(0, 0, 0, 255), stop:1 rgba(0, 149, 255, 255))
        }
        
        QMenuBar::item:pressed {
            background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(0, 146, 255, 255), stop:0.102273 rgba(0, 0, 0, 255), stop:0.522727 rgba(0, 0, 0, 255), stop:0.892045 rgba(0, 0, 0, 255), stop:1 rgba(0, 149, 255, 255))
        }
        
        QMenu {
            background-color:rgb(0, 0, 0);
            border: 1px rgb(0, 170, 255);
                color: rgb(255, 255, 255);
        }
        
        QMenu::item {
            background-color: transparent;
                color: rgb(255, 255, 255);
        }
        
        QMenu::item:selected { /* when user selects item using mouse or keyboard */
            background-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(0, 98, 168, 255))
        }""")
        (self.lv_1).addAction("Play Now").triggered.connect(lambda: self.lib_view_play(Column_lut["id"], "id"))
        (self.lv_1).addAction("Queue Next").triggered.connect( lambda: self.lib_view_queue(Column_lut["id"], "id"))
        (self.lv_1).addAction("Queue Random").triggered.connect( lambda: self.lib_view_queue(Column_lut["id"], "id", flag = "shuffle"))
        self.lv_1_04 = self.lv_1.addMenu("Add To Playlist")
        (self.lv_1.addSection(''))
        self.lv_1_05 = self.lv_1.addMenu("Play (more)$")
        (self.lv_1).addAction("Edit$")
        self.lv_1_07 = self.lv_1.addMenu("Auto-Tags$")
        self.lv_1_08 = self.lv_1.addMenu("Ratings")
        (self.lv_1.addSection(''))
        (self.lv_1).addAction("Delete").triggered.connect(lambda: self.track_removal('delete', self.library_model, "library"))
        (self.lv_1).addAction("Remove").triggered.connect(lambda: self.track_removal('remove', self.library_model, "library"))
        self.lv_1_10 = self.lv_1.addMenu("Send To$")
        self.lv_1_11 = self.lv_1.addMenu("Search")
        self.lv_1_12 = self.lv_1.addMenu("Displayed Fields")
    
        (self.lv_1_04).addAction("Add To New Playlist").triggered.connect(lambda: self.Ui_add_play_obj.show())
        (self.lv_1_04).addAction("Add To Current Playlist").triggered.connect(lambda: (self.playlist_add_current(self.playlist_combo)))
        (self.lv_1_04.addSection(''))
        [(self.lv_1_04).addAction(keys).triggered.connect(lambda: (self.playlist_saver(self.library_view, keys))) for keys in self.playlist_cbox_update(self.playlist_combo)]
    
    
        (self.lv_1_05).addAction("Bypass Filters")
        self.lv_1_05_1 = self.lv_1_05.addMenu("Output To")
        (self.lv_1_05.addSection(''))
        (self.lv_1_05).addAction("Play Shuffle").triggered.connect( lambda: self.lib_view_play(Column_lut["id"], "id", flag = 'shuffle'))
        (self.lv_1_05).addAction("Play Similar").triggered.connect( lambda: self.lib_view_play(Column_lut["genre"], "genre"))
        (self.lv_1_05).addAction("Play Album").triggered.connect( lambda: self.lib_view_play(Column_lut["album"], "album"))
        (self.lv_1_05).addAction("Play Artist").triggered.connect( lambda: self.lib_view_play(Column_lut["artist"], "artist"))
        (self.lv_1_05.addSection(''))
        (self.lv_1_05).addAction("Queue Album").triggered.connect( lambda: self.lib_view_queue(Column_lut["artist"], "artist"))
        (self.lv_1_05).addAction("Queue AlbumArtist").triggered.connect( lambda: self.lib_view_queue(Column_lut["artist"], "artist"))
    
        (self.lv_1_08).addAction("0   Stars").triggered.connect( lambda: self.lib_view_ratings_update(0, self.library_model))
        (self.lv_1_08).addAction("1   Stars").triggered.connect( lambda: self.lib_view_ratings_update(1, self.library_model))
        (self.lv_1_08).addAction("1.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(1.5, self.library_model))
        (self.lv_1_08).addAction("2   Stars").triggered.connect( lambda: self.lib_view_ratings_update(2, self.library_model))
        (self.lv_1_08).addAction("2.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(2.5, self.library_model))
        (self.lv_1_08).addAction("3   Stars").triggered.connect( lambda: self.lib_view_ratings_update(3, self.library_model))
        (self.lv_1_08).addAction("3.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(3.5, self.library_model))
        (self.lv_1_08).addAction("4   Stars").triggered.connect( lambda: self.lib_view_ratings_update(4, self.library_model))
        (self.lv_1_08).addAction("4.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(4.5, self.library_model))
        (self.lv_1_08).addAction("5   Stars").triggered.connect( lambda: self.lib_view_ratings_update(5, self.library_model))
    
        (self.lv_1_10).addAction("Audio Fx")
        self.lv_1_10_1 = (self.lv_1_10).addMenu("File (Move)")
        self.lv_1_10_2 = (self.lv_1_10).addMenu("File (Copy)")
        self.lv_1_10_3 = (self.lv_1_10).addMenu("File (Replace)")
        (self.lv_1_10).addAction("File Converter")
        (self.lv_1_10).addAction("File Rescan")
        (self.lv_1_10).addAction("Analysis")
    
        (self.lv_1_11).addAction('Find Artist').triggered.connect( lambda: self.lib_view_search_query("artist",
                                                                                                                  self.library_view,
                                                                                                                  self.library_model,
                                                                                                                  self.tabWidget,
                                                                                                                  self.playlist_combo))
        
        (self.lv_1_11).addAction('Find Similar').triggered.connect( lambda: self.lib_view_search_query('similar',
                                                                                                                   self.library_view,
                                                                                                                   self.library_model,
                                                                                                                   self.tabWidget,
                                                                                                                   self.playlist_combo))
        
        (self.lv_1_11).addAction('Locate in Playlist').triggered.connect( lambda: self.lib_view_search_query('in_playlist',
                                                                                                                         self.library_view,
                                                                                                                         self.playlist_model,
                                                                                                                         self.tabWidget,
                                                                                                                         self.playlist_combo))
        
        (self.lv_1_11).addAction('Locate in Now Playing').triggered.connect( lambda: self.lib_view_search_query('in_now_play',
                                                                                                                            self.library_view,
                                                                                                                            self.now_playing_model,
                                                                                                                            self.tabWidget,
                                                                                                                            self.playlist_combo))
        
        (self.lv_1_11).addAction('Locate in File Explorer').triggered.connect( lambda: self.lib_view_search_query('in_file_exp',
                                                                                                                              self.library_view,
                                                                                                                              self.library_model,
                                                                                                                              self.tabWidget,
                                                                                                                              self.playlist_combo))
        
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
            if not(bool(j.isChecked())): self.library_view.hideColumn(index)
            if (bool(j.isChecked())): self.library_view.showColumn(index)

    
    def id_getter(self, model, view, col):
        rows = [(model.index(i.row(), col).data())for i in view.selectedIndexes()[::70]]
        rows = set(rows)
        ids = ""
        for data in rows:
            ids = f"{ids},'{data}'" 
        ids = f"({ids[1:]})"
        print(ids)
        return ids    
    
    def item_set_creator(self, data):
        item = ''
        for i in data: 
            item = f"{item}, '{i}'"
        item = f"({item[1:]})"
        return item
    
            
    def pixmap_setter(self, fname, obj, scale):
        # pixmap
        try:
            try:
                if os.path.splitext(fname)[1] != ".mp3":
                    meta_image = ((mutagen.File(fname)).pictures[0]).data
            except Exception as e:
                pass # print(e)
    
            try:
                meta_image = ((mutagen.File(fname)).get("APIC:")).data
            except Exception as e:
                pass # print(e)            
    
            try:
                meta_image = ((mutagen.File(fname)).get("APIC:Cover (front)")).data
            except Exception as e:
                pass # print(e)
    
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
    
    
    def lib_item_doubleclk(self):
        lib_mod = self.library_view.model()
        for i in self.library_view.selectedIndexes()[::70]:
            data = [(lib_mod.index(i.row(), Column_lut["path"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["artist"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["title"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["album"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["albumartist"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["composer"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["genre"]).data())]
            
            obj = [self.trackinfo_label_lib_artist, 
            self.trackinfo_label_lib_title,
            self.trackinfo_label_lib_album, 
            self.trackinfo_label_lib_album_arrtist,
            self.trackinfo_label_lib_comp, 
            self.trackinfo_label_lib_genre]
            self.metainfo_setter(obj, data, self.pixmaplib)
        self.lib_view_queue(Column_lut["id"], "id")
    
    def metainfo_setter(self, obj, data, pix, scale = (300, 300)):
        self.pixmap_setter(fname = data[0], obj = pix, scale = scale)
        obj[0].setText(f"Artist: {data[1]}")
        obj[1].setText(f"Title: {data[2]}")
        obj[2].setText(f"Album: {data[3]}")
        obj[3].setText(f"AlbumArtist: {data[4]}")
        obj[4].setText(f"Composer: {data[5]}")
        obj[5].setText(f"Genre: {data[6]}")
   

    @timeit
    def playlist_cbox_update(self, cbox):
        query = QtSql.QSqlQuery()
        query.exec_("SELECT name FROM sqlite_master WHERE type = 'view' and name NOT IN  ('search_query', 'now_playing')")
        items = []
        while query.next():
            items.append((query.record()).value('name'))
        cbox.clear()
        cbox.addItems(items)
        return items      


    def lib_sort_hint(self):
        self.lib_sort = self.library_view.horizontalHeader().sortIndicatorSection()      
        self.lib_ord = self.library_view.horizontalHeader().sortIndicatorOrder()  
    
    def playlist_sort_hint(self):
        self.playlist_sort = self.playlist_view.horizontalHeader().sortIndicatorSection()      
        self.playlist_ord = self.playlist_view.horizontalHeader().sortIndicatorOrder()
        
        
    def now_play_sort(self, tab):
        if tab == "lib":
            if not(hasattr(self, 'lib_sort')):
                self.lib_sort = 0
            if not(hasattr(self, 'lib_ord')):
                self.lib_ord = QtCore.Qt.AscendingOrder
            col = self.lib_sort
            order = self.lib_ord
            
            self.now_playing_view.sortByColumn(col, order)
       
        if tab == "playlist":
            if not (hasattr(self, 'playlist_sort')):
                self.playlist_sort = 0
            if not (hasattr(self, 'playlist_ord')):
                self.playlist_ord = QtCore.Qt.AscendingOrder
                
            col = self.playlist_sort
            order = self.playlist_ord
            
            self.now_playing_view.sortByColumn(col, order)    

    @timeit
    def view_refresher(self, query_model, table):
        query_model.setQuery(f"SELECT * FROM {table}")
        while query_model.canFetchMore():
            query_model.fetchMore(QtCore.QModelIndex())
    
    
    @timeit
    def lib_view_play(self, col, col_name, flag = None):
        query = QtSql.QSqlQuery()
        lib_mod = self.library_model
        now_play_mod = self.now_playing_model
        try:
            query.exec_("DROP VIEW now_playing")
        except Exception as e:
            print(e)
        if flag != "shuffle":
            rows = set([lib_mod.index(i.row(), col).data() for i in self.library_view.selectedIndexes()[::len(Column_lut)]])
            rows = str(rows).replace('{', '(').replace("}", ')')
            query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library WHERE {col_name} IN {rows}")
        if flag == "shuffle":
            query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library ORDER BY random()")
        now_play_mod.select()        
        while now_play_mod.canFetchMore():
            now_play_mod.fetchMore(QtCore.QModelIndex())
        self.now_play_sort("lib")    
        self.now_playing_view.setModel(now_play_mod)
        self.playing_queue()

    def playing_queue(self):
        items = []
        self.audio_queue = Playback_queue(self.now_playing_model.rowCount())
        for i in range(self.now_playing_model.rowCount()):
            data = self.now_playing_model.index(i, Column_lut['title']).data()
            items.extend([QtGui.QStandardItem(data)])
            data = self.now_playing_model.index(i, Column_lut['path']).data()
            self.audio_queue.put(data)
            
        model = QtGui.QStandardItemModel()
        model.setHeaderData(1, 1, "Title")
        model.appendColumn(items)
        self.lib_play_view.setModel(model)    
    
    @timeit
    def lib_view_queue(self, col, col_name, flag = None):
        try:
            query = QtSql.QSqlQuery()
            lib_mod = self.library_model
            now_play_mod = self.now_playing_model
            prev = []
            try:
                try:
                    query.exec_(f"SELECT id FROM now_playing")
                    while query.next():
                        prev.append((query.record()).value("id"))
                    prev = set(prev)
                    prev = str(prev).replace('{', '(').replace("}", ')')                    
                except: print(e)                
                query.exec_("DROP VIEW now_playing")
            except Exception as e:
                print(e)
            
            rows = set([lib_mod.index(i.row(), col).data() for i in self.library_view.selectedIndexes()[::len(Column_lut)]])
            rows = str(rows).replace('{', '(').replace("}", ')')
            if flag != 'shuffle':
                query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library WHERE {col_name} IN {rows} OR id in {prev}")
            if flag == 'shuffle':
                query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library WHERE id IN {rows} ORDER BY random()")
    
            now_play_mod.select()        
            while now_play_mod.canFetchMore():
                now_play_mod.fetchMore(QtCore.QModelIndex())
            self.now_play_sort("lib")
            
            self.now_playing_view.setModel(now_play_mod)
            
            self.playing_queue()    
   
        except Exception as e:
            print(e)
            self.lib_view_play(Column_lut["id"], "id")
   
   
    @timeit
    def lib_view_ratings_update(self, num):
        query = QtSql.QSqlQuery()
        rows = set([(self.library_model.index(i.row(), 0).data())for i in self.library_model.selectedIndexes()[::70]])
        ids = ""
        for data in rows:
            ids = f"{ids},'{data}'" 
        ids = f"({ids[1:]})"
        query.exec_(f"UPDATE library SET ratings = {num} WHERE id IN {ids}")
        
        self.library_model.setQuery(QtSql.QSqlQuery("SELECT * FROM library"))
        while self.library_model.canFetchMore():
            self.library_model.fetchMore(QtCore.QModelIndex())          
    
    
    @timeit
    def lib_view_search_query(self, field, view, query_model, tab = None, combo = None):
        rows = set([i.row() for i in self.library_view.selectedIndexes()[::len(Column_lut)]])
        data = []
        
        try:
            QtSql.QSqlQuery("DROP VIEW search_query")
        except:
            pass
        
        if (field == 'in_file_exp'):
            item = [(query_model.index((list(rows)[0]), Column_lut["path"]).data())]        
            os.startfile(os.path.split(item[0])[0], 'explore')
        else:
            if (field == "artist"):
                for row in rows:
                    data.extend([(query_model.index(row, Column_lut["artist"]).data()), (query_model.index(row, Column_lut["albumartist"]).data())])
                data = set(data) - set([' ', ''])
                data = str(data).replace('{', '(').replace("}", ')')
                sql = f"CREATE VIEW search_query AS SELECT * FROM library WHERE artist IN {data}"
                tab.setTabText(1, "Artist")
                tab.setCurrentIndex(1)

            if (field == 'similar'):
                for row in rows:
                    data.extend([(query_model.index(row, Column_lut["genre"]).data())])
                data = set(data) - set([' ', ''])
                data = str(data).replace('{', '(').replace("}", ')')
                sql = f"CREATE VIEW search_query AS SELECT * FROM library WHERE genre IN {data}"
                tab.setTabText(1, "Similar")
                tab.setCurrentIndex(1)
                
            if (field == 'in_playlist'):
                play = combo.currentText()
                for row in rows:
                    data.extend([(query_model.index(row, Column_lut["id"]).data())])
                data = set(data)
                data = str(data).replace('{', '(').replace("}", ')')
                sql = f"CREATE VIEW search_query AS SELECT * FROM {play} WHERE id IN {data}"
                tab.setTabText(1, "In Playlist")
                tab.setCurrentIndex(1)
                
            if (field == 'in_now_play'):
                for row in rows:
                    data.extend([(query_model.index(row, Column_lut["id"]).data())])
                data = set(data)
                data = str(data).replace('{', '(').replace("}", ')')
                sql = f"CREATE VIEW search_query AS SELECT * FROM now_playing WHERE id IN {data}"
                tab.setTabText(1, "In Now Playing")
                tab.setCurrentIndex(1)
                
            self.search_model.setQuery(QtSql.QSqlQuery(sql))
            self.search_model.setQuery(QtSql.QSqlQuery("SELECT * FROM search_query"))
            [self.search_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
            self.search_model.select()
            while self.search_model.canFetchMore():
                self.search_model.fetchMore(QtCore.QModelIndex())
            self.search_view.setModel(self.search_model)           

    
    def track_removal(self, flag, model, table): 
        ids = set([model.index(i.row(), Column_lut['id']).data() for i in self.library_view.selectedIndexes()[::len(Column_lut)]])
        ids = str(ids).replace('{', '(').replace("}", ')')
        
        query = QtSql.QSqlQuery()
        if flag == "remove":
            sql = f"""
            DELETE FROM library
            WHERE id IN {ids}
            """
            query.exec_(sql)
            
        if flag == "delete":
            sql = f"""
            DELETE FROM library
            WHERE id IN {ids}
            """
            query.exec_(sql)
            
        model.setQuery(QtSql.QSqlQuery(f"SELECT * FROM {table}"))
        while model.canFetchMore():
            model.fetchMore(QtCore.QModelIndex())    
       
        
    @timeit
    def playlist_cbox_update(self, cbox):
        query = QtSql.QSqlQuery()
        query.exec_("SELECT name FROM sqlite_master WHERE type = 'view' and name NOT IN  ('search_query', 'now_playing')")
        items = []
        while query.next():
            items.append((query.record()).value('name'))
        cbox.clear()
        cbox.addItems(items)
        return items
    
    
    @timeit
    def playlist_add_current(self, cbox):
        name = cbox.currentText()
        self.playlist_saver(self.library_view, name)
        self.playlist_model.setQuery(QtSql.QSqlQuery(f"SELECT * FROM {name}"))
        while self.playlist_model.canFetchMore():
            self.playlist_model.fetchMore(QtCore.QModelIndex())
        self.playlist_view.setModel(self.playlist_model)             
        self.cbox_playlist_loader(cbox)
    
    
    @timeit
    def playlist_add_new(self, view, name, cbox):
        if (re.match(r'[A-Za-z_-]', name) and not(re.match(r'library', name)) and not(re.match(r'search_query', name))  and not(re.match(r'now_playing', name))):
            query = QtSql.QSqlQuery()
            try:
                try:
                    query.exec_(f"DROP VIEW {name}")
                except Exception as e:
                    print(e)
                model = self.library_view.model()
                rows = set([model.index(i.row(), Column_lut['id']).data() for i in self.library_view.selectedIndexes()[::len(Column_lut)]])
                rows = str(rows).replace('{', '(').replace("}", ')')
                query.exec_(f"CREATE VIEW {name} AS SELECT * FROM library WHERE id IN {rows}")
            except Exception as e:
                    print(e)
            self.playlist_cbox_update(cbox)
    
   
    @timeit
    def playlist_saver(self, view, name):
        if (re.match(r'[A-Za-z_-]', name) and not(re.match(r'library', name)) and not(re.match(r'search_query', name))  and not(re.match(r'now_playing', name))):
            try:
                query = QtSql.QSqlQuery()
                model = view.model()
                prev = []
                try:
                    try:
                        query.exec_(f"SELECT id FROM {name}")
                        while query.next():
                            prev.append((query.record()).value("id"))
                    except Exception as e:
                        print(e)                
                    query.exec_(f"DROP VIEW {name}")
                except Exception as e:
                    print(e)
                rows = set([model.index(i.row(), Column_lut['id']).data() for i in self.library_view.selectedIndexes()[::len(Column_lut)]])
                rows = str(rows).replace('{', '(').replace("}", ')')
                query.exec_(f"CREATE VIEW {name} AS SELECT * FROM library WHERE id IN {rows}")
            except Exception as e:
                    print(e)
    
    
    def cbox_playlist_loader(self, cbox): 
        playlist = cbox.currentText()
        self.playlist_model.setQuery(QtSql.QSqlQuery(f"SELECT * FROM {playlist}"))
        while self.playlist_model.canFetchMore():
            self.playlist_model.fetchMore(QtCore.QModelIndex())
        self.playlist_view.setModel(self.playlist_model)        
        
        
class QueueIterator:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.index = 0
        
    def __next__(self):
        if (self.index < self.size):
            data = self.data[self.index]
            self.index += 1                
            return (self.index, data)
        else:
            raise StopIteration 
        
class Playback_queue():
    """"""

    def __init__(self, size, circ = False):
        self.playing_queue = {k:"" for k in range(size)}
        self.pointer_put = 0
        self.pointer_get = 0
        self.size = size
        self.circ = circ
        
    def __repr__(self):
        return json.dumps(self.playing_queue, indent = 2)
    
    def __str__(self):
        return json.dumps(self.playing_queue, indent = 2)    
    
    def __len__(self):
        return len(self.playing_queue)
    
    def __iter__(self):
        return QueueIterator(self)
    
    def __getitem__(self, index):
        return self.current()
       
    def put(self, data):
        self.playing_queue[self.pointer_put] = data
        self.pointer_put += 1
    
    def current(self):
        data = self.playing_queue[self.pointer_get]
        return (self.pointer_get, data)
    
    def _next(self):
        try:
            if self.pointer_get != (len(self.playing_queue) - 1):
                self.pointer_get += 1
                data = self.current()
                return data
            elif self.pointer_get == (len(self.playing_queue) - 1):
                if self.circ:
                    self.pointer_get = 0
                    data = self.current()
                    return data                   
                else:
                    return (self.pointer_get,"EOF")                 
            else:
                return (self.pointer_get,"EOF")            
        except KeyError:
            if self.circ:
                self.pointer_get = 0
            else:
                return (self.pointer_get,"EOF")
        
    def prev(self):
        try:
            if self.pointer_get != 0:
                self.pointer_get -= 1
                data = self.current()
                return data
            elif self.pointer_get == 0:
                if self.circ:
                    self.pointer_get = (len(self.playing_queue) - 1)
                    data = self.current()
                    return data                
                else:
                    return (self.pointer_get,"EOF")
            else:
                return (self.pointer_get,"EOF") 
        except KeyError:
            if self.circ:
                self.pointer_get = (len(self.playing_queue) - 1)
            else:
                return (self.pointer_get,"EOF")          
    
    def Setcircular(self, bl):
        self.circ = bl
    
    def empty(self):
        if (len(self.playing_queue) - self.pointer_get) == 1:
            return True
        else:
            return False
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    main_app = Main_window()
    main_app.database_statrup()
    main_app.show()
    app.exec_()
