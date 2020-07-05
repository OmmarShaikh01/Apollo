# local
from main_ui import Ui_MainWindow
from utils import *
from file_explorer import FileBrowser
from lib_up import Library_database_mang, Column_lut

# external dep
from PyQt5 import QtCore, QtGui, QtWidgets
import mutagen

# builtins
import sys, os, time, shutil

class UI_init(Ui_MainWindow, QtWidgets.QMainWindow):
    
    def __init__(self):
        super(UI_init, self).__init__()
        self.setupUi(self)
        self.root_imp_dir = os.path.split(__file__)[0]
        self.setStyleSheet(open(f"{self.root_imp_dir}\\resources\\style.qss").read())
        self.button_setter()
        
    def button_setter(self):
        path = f"{self.root_imp_dir}\\resources\\icons"
        for value in os.listdir(path):
            if os.path.splitext(value)[1] in [".svg"]:
                
                if re.search("play", value.lower()):
                    self.play_button.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(path,value))))
                    self.play_button.setIconSize(QtCore.QSize(20,20))
                    self.play_button.setText(None)
                    continue
                
                if re.search("stop", value.lower()):
                    self.stop_button.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(path,value))))
                    self.stop_button.setIconSize(QtCore.QSize(20,20))
                    self.stop_button.setText(None)
                    continue
                
                if re.search("pause", value.lower()):
                    self.pause_button.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(path,value))))
                    self.pause_button.setIconSize(QtCore.QSize(20,20))
                    self.pause_button.setText(None)
                    continue
                
                if re.search("next", value.lower()):
                    self.next_button.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(path,value))))
                    self.next_button.setIconSize(QtCore.QSize(20,20))
                    self.next_button.setText(None)
                    continue
                
                if re.search("previous", value.lower()):
                    self.prev_button.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(path,value))))
                    self.prev_button.setIconSize(QtCore.QSize(20,20))
                    self.prev_button.setText(None)
                    continue
                
                if re.search("forward", value.lower()):
                    self.seek_back_button.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(path,value))))
                    self.seek_back_button.setIconSize(QtCore.QSize(20,20))
                    self.seek_back_button.setText(None)
                    continue
                
                if re.search("rewind", value.lower()):
                    self.seek_fowd_button.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(path,value))))
                    self.seek_fowd_button.setIconSize(QtCore.QSize(20,20))
                    self.seek_fowd_button.setText(None)
                    continue
                
class Main_widget(UI_init):
    # sets up model and global model functions

    def __init__(self, *args):
        super(Main_widget, self).__init__()
        self.tab_wid_function_bindings()
        self.database_statrup()
        self.all_model_declaration()

    def tab_wid_function_bindings(self): 
        self.main_tabs.currentChanged.connect(lambda: self._now_play_queue_sub_split_shrink())
        tabBar = self.main_tabs.tabBar()

        # Context Menu Request Bindings
        tabBar.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        tabBar.customContextMenuRequested.connect(self.tab_cmenu)
        tabBar.setTabButton(0, QtWidgets.QTabBar.RightSide,None)

        # Tab Close Function Bindings
        tabBar.tabCloseRequested.connect(lambda x: self._hide_tab(x))

        # Declaration Of Filebrowser For The Player
        self.file_explorer_object = FileBrowser()
        self.file_explorer_object.buttonBox.accepted.connect(lambda: (self.all_model_declaration(), self.file_explorer_object.close()))
        self.rescanA.triggered.connect(lambda: self.all_model_declaration())
        self.add_folders_to_libA.triggered.connect(lambda: self.menu_bar_actions(1))

        # Header Sort Hint Getter
        self.music_table.horizontalHeader().sortIndicatorChanged.connect(lambda: (self.lib_sort_hint()))
        self.playlist_table.horizontalHeader().sortIndicatorChanged.connect(lambda: (self.playlist_sort_hint()))        
        self.search_table.horizontalHeader().sortIndicatorChanged.connect(lambda: (self.search_sort_hint()))
        self.audiobk_table.horizontalHeader().sortIndicatorChanged.connect(lambda: (self.audiobk_sort_hint()))          

    def lib_sort_hint(self):
        # Get The Sort Order
        self.lib_sort = self.music_table.horizontalHeader().sortIndicatorSection()      
        self.lib_ord = self.music_table.horizontalHeader().sortIndicatorOrder()  


    def playlist_sort_hint(self):
        # Get The Sort Order
        self.playlist_sort = self.playlist_table.horizontalHeader().sortIndicatorSection()      
        self.playlist_ord = self.playlist_table.horizontalHeader().sortIndicatorOrder()    

    def search_sort_hint(self):
        # Get The Sort Order
        self.search_sort = self.search_table.horizontalHeader().sortIndicatorSection()      
        self.search_ord = self.search_table.horizontalHeader().sortIndicatorOrder()  


    def audiobk_sort_hint(self):
        # Get The Sort Order
        self.audiobk_sort = self.audiobk_table.horizontalHeader().sortIndicatorSection()      
        self.audiobk_ord = self.audiobk_table.horizontalHeader().sortIndicatorOrder()      

    def menu_bar_actions(self,pos):
        if pos == 1:
            self.file_explorer_object.show()

    def tab_cmenu(self):
        if not hasattr(self, "tab_state_dic"):
            self.tab_state_dic = {}
            for i in range(self.main_tabs.count()):
                self.tab_state_dic[self.main_tabs.tabText(i)] = i

        lv_1 = QtWidgets.QMenu()

        (lv_1).addAction("Music").triggered.connect(lambda: self._unhide_tab("Music"))
        (lv_1).addAction("Search").triggered.connect(lambda: self._unhide_tab("Search"))
        (lv_1).addAction("Audio Book").triggered.connect(lambda: self._unhide_tab("Audio Book"))
        (lv_1).addAction("History").triggered.connect(lambda: self._unhide_tab("History"))
        (lv_1).addAction("Inbox").triggered.connect(lambda: self._unhide_tab("Inbox"))
        (lv_1).addAction("Now Playing").triggered.connect(lambda: self._unhide_tab("Now Playing"))
        (lv_1).addAction("Playlist").triggered.connect(lambda: self._unhide_tab("Playlist"))
        (lv_1).addAction("Audio Fx").triggered.connect(lambda: self._unhide_tab("Audio Fx"))

        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos())        

    def _now_play_queue_sub_split_shrink(self):
        # Closes The Left Sidebar When Now-Playing Tab Is Opend
        if self.main_tabs.tabText(self.main_tabs.currentIndex()) == "Now Playing":
            self.now_play_queue_sub_split.hide()

        # Closes The Left Sidebar When Audio-Fx Tab Is Opend
        elif self.main_tabs.tabText(self.main_tabs.currentIndex()) == "Audio Fx":
            self.now_play_queue_sub_split.hide()

        else:
            self.now_play_queue_sub_split.show()

    def _hide_tab(self, ind):    
        self.main_tabs.tabBar().setTabVisible(ind, False)

    def _unhide_tab(self, ind):
        ind = self.tab_state_dic[ind]
        self.main_tabs.tabBar().setTabVisible(ind, True)           


    def database_statrup(self):
        self.table_creator()
        self.global_conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.global_conn.setDatabaseName('library.db')
        if self.global_conn.open():
            print("open")
            self.all_model_declaration()

    @database_connector_wrap
    def table_creator(self, **kwargs):
        # Connectotor And Getter For Database
        conn = kwargs["conn"]
        Library_database_mang().database_table_creator(conn)    

    @timeit
    def all_model_declaration(self):

        self.music_table_model_dec()
        self.music_grp_srt_list_model_dec()
        self.search_table_model_dec()
        self.search_grp_srt_list_model_dec()
        self.audiobk_table_model_dec()
        self.audiobk_grp_srt_list_model_dec()
        self.history_table_model_dec()
        self.inbox_table_model_dec()
        self.now_play_queue_model_dec()
        self.playlist_table_model_dec()
        self.playlist_grp_srt_list_model_dec()
        self.now_play_queue_sub_model_dec()

    def music_table_model_dec(self):
        self.music_table_model = QtSql.QSqlTableModel()
        self.music_table_model.setTable("library")
        [self.music_table_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
        self.music_table_model.select()
        while self.music_table_model.canFetchMore():
            self.music_table_model.fetchMore(QtCore.QModelIndex())        
        self.music_table.setModel(self.music_table_model)

        # Extracts Fields And Headers
        self.fields = list(Column_lut.keys())
        self.fields_flags = {i: 1 for i in self.fields}
        self.headers = [((i.replace("_", " ")).title()) for i in Column_lut.keys()]     

    def music_grp_srt_list_model_dec(self):
        pass

    def search_table_model_dec(self):
        self.search_table_model = QtSql.QSqlTableModel()
        self.search_table_model.setTable("search_query")
        self.search_table_model.select()
        while self.search_table_model.canFetchMore():
            self.search_table_model.fetchMore(QtCore.QModelIndex())           
        [self.search_table_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
        self.search_table.setModel(self.search_table_model)

    def search_grp_srt_list_model_dec(self):
        pass

    def audiobk_table_model_dec(self):
        self.audiobk_table_model = QtSql.QSqlTableModel()
        self.audiobk_table_model.setTable("audio_bk")
        self.audiobk_table_model.select()
        while self.audiobk_table_model.canFetchMore():
            self.audiobk_table_model.fetchMore(QtCore.QModelIndex())           
        [self.audiobk_table_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
        self.audiobk_table.setModel(self.audiobk_table_model)

    def audiobk_grp_srt_list_model_dec(self):
        pass

    def history_table_model_dec(self):
        pass

    def inbox_table_model_dec(self):
        self.inbox_table_model = QtGui.QStandardItemModel()
        self.inbox_table_model.appendRow([QtGui.QStandardItem(''), QtGui.QStandardItem('')])
        [self.inbox_table_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for s, i in {0: "level", 1: "message",}.items()]
        self.inbox_table.setModel(self.inbox_table_model)

    def now_play_queue_model_dec(self):
        self.now_play_queue_model = QtSql.QSqlTableModel()
        self.now_play_queue_model.setTable("now_playing")
        self.now_play_queue_model.select()
        while self.now_play_queue_model.canFetchMore():
            self.now_play_queue_model.fetchMore(QtCore.QModelIndex())           
        [self.now_play_queue_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
        self.now_play_queue.setModel(self.now_play_queue_model)

    def playlist_table_model_dec(self):
        # Refreshes The Current Playlist Cbox
        self.playlist_cbox_update(self.playlist_combo)

        self.playlist_table_model = QtSql.QSqlTableModel()
        self.playlist_table_model = QtSql.QSqlTableModel()
        self.playlist_table_model.setTable(f"{self.playlist_combo.currentText()}")
        self.playlist_table_model.select()
        while self.playlist_table_model.canFetchMore():
            self.playlist_table_model.fetchMore(QtCore.QModelIndex())           
        [self.playlist_table_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
        self.playlist_table.setModel(self.playlist_table_model)

    def playlist_grp_srt_list_model_dec(self):
        pass

    def now_play_queue_sub_model_dec(self):
        self.now_play_queue_sub.setModel(self.now_play_queue_model) 


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

    def display_fields_box_check(self, actions):
        for index, (i,j) in enumerate(zip(self.fields_flags.keys(), actions)):
            self.fields_flags[i] = int(j.isChecked())
            if not(bool(j.isChecked())): self.music_table.hideColumn(index)
            if (bool(j.isChecked())): self.music_table.showColumn(index)


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

    def inbox_printer(self, e, fun = None, lvl = "INFO"):
        # logs events to the inbox
        fu_lam = lambda val: self.inbox_table_model.appendRow([QtGui.QStandardItem(lvl), QtGui.QStandardItem(val)])
        if fun == None:
            fun = lambda: ''
        logging_print(fun, e, fu_lam, None)    

    def pixmap_setter(self, fname, obj, scale):
        # Pixmap
        try:
            pixmap = QtGui.QPixmap()
            try:
                muta_obj = mutagen.File(fname)
                meta_image = [(self.muta_obj.get(i)).data for i in self.muta_obj.keys() if  re.search("APIC:", i)].pop()
                pixmap.loadFromData(meta_image)
            except Exception as e:
                pixmap = pixmap.scaled(scale[0], scale[1])
                obj.setPixmap(pixmap)
                obj.setScaledContents(True)

            pixmap = pixmap.scaled(scale[0], scale[1])
            obj.setPixmap(pixmap)
            obj.setScaledContents(True)

        except Exception as e:
            logging_print(self.pixmap_setter, e)

    @timeit        
    def lib_item_doubleclk(self, table):
        # Double Click Trigger Function
        lib_mod = table.model()
        for i in table.selectedIndexes()[::70]:
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
                   self.trackinfo_label_lib_album_artist,
                   self.trackinfo_label_lib_comp, 
                   self.trackinfo_label_lib_genre]

        self.metainfo_setter(obj, data, self.pixmap_lab)
        self.track_queue_func(table, Column_lut["id"], "id")     

    @timeit
    def now_play_item_doubleclk(self, table):
        # Double Click Trigger Function
        lib_mod = table.model()
        for i in table.selectedIndexes()[::70]:
            data = [(lib_mod.index(i.row(), Column_lut["path"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["artist"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["title"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["album"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["albumartist"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["composer"]).data()), 
                    (lib_mod.index(i.row(), Column_lut["genre"]).data())]

            obj = [self.trackinfo_label_lib_artist_NP, 
                   self.trackinfo_label_lib_title_NP,
                   self.trackinfo_label_lib_album_NP, 
                   self.trackinfo_label_lib_album_artist_NP,
                   self.trackinfo_label_lib_comp_NP, 
                   self.trackinfo_label_lib_genre_NP]

        self.metainfo_setter(obj, data, self.pixmap_lab_NP, (600, 600))
        self.track_queue_func(table, Column_lut["id"], "id")     

    def metainfo_setter(self, obj, data, pix, scale = (300, 300)):
        # Sets All The Track Info And The Cover Art
        # Pass The Scale And The Label Objects As List
        pix.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0));")
        self.pixmap_setter(fname = data[0], obj = pix, scale = scale)
        obj[0].setText(f"Artist: {data[1]}")
        obj[1].setText(f"Title: {data[2]}")
        obj[2].setText(f"Album: {data[3]}")
        obj[3].setText(f"AlbumArtist: {data[4]}")
        obj[4].setText(f"Composer: {data[5]}")
        obj[5].setText(f"Genre: {data[6]}")


    @timeit
    def playlist_cbox_update(self, cbox):
        # Updates The Playlist Combo Box For New Playlist
        query = QtSql.QSqlQuery()
        query.exec_("SELECT name FROM sqlite_master WHERE type = 'view' and name NOT IN  ('search_query', 'now_playing')")
        items = []
        while query.next():
            items.append((query.record()).value('name'))
        cbox.clear()
        cbox.addItems(items)
        return items  


    def now_play_sort(self, tab):
        # Creates The Sort Query 
        if tab == "library":
            if not(hasattr(self, 'lib_sort')):
                self.lib_sort = 0
            if not(hasattr(self, 'lib_ord')):
                self.lib_ord = QtCore.Qt.AscendingOrder
            col = [k for k, v in Column_lut.items() if v == self.lib_sort][0]
            order = "" if self.lib_ord == QtCore.Qt.AscendingOrder else "DESC"
            return (f"ORDER BY {col} {order}")         

        if tab == "search_query":
            if not(hasattr(self, 'search_sort')):
                self.search_sort = 0
            if not(hasattr(self, 'search_ord')):
                self.search_ord = QtCore.Qt.AscendingOrder
            col = [k for k, v in Column_lut.items() if v == self.search_sort][0]
            order = "" if self.search_ord == QtCore.Qt.AscendingOrder else "DESC"
            return (f"ORDER BY {col} {order}")         

        if tab == "audio_bk":
            if not (hasattr(self, 'audiobk_sort')):
                self.audiobk_sort = 0
            if not (hasattr(self, 'audiobk_ord')):
                self.audiobk_ord = QtCore.Qt.AscendingOrder
            col = [k for k, v in Column_lut.items() if v == self.audiobk_sort][0]
            order = "" if self.audiobk_ord == QtCore.Qt.AscendingOrder else "DESC"
            return (f"ORDER BY {col} {order}")

        if tab in [self.playlist_combo.itemText(i) for i in range(self.playlist_combo.count())]:
            if not (hasattr(self, 'playlist_sort')):
                self.playlist_sort = 0
            if not (hasattr(self, 'playlist_ord')):
                self.playlist_ord = QtCore.Qt.AscendingOrder
            col = [k for k, v in Column_lut.items() if v == self.playlist_sort][0]
            order = "" if self.playlist_ord == QtCore.Qt.AscendingOrder else "DESC"
            return (f"ORDER BY {col} {order}")

    @timeit
    def view_refresher(self, query_model, table):
        query_model.setQuery(f"SELECT * FROM {table}")
        while query_model.canFetchMore():
            query_model.fetchMore(QtCore.QModelIndex())


    @timeit
    def play_func(self, view, col, col_name, flag = None):
        query = QtSql.QSqlQuery()
        curr_view = view
        curr_model = view.model()
        now_play_mod = self.now_play_queue_model
        try:
            query.exec_("DROP VIEW now_playing")
        except Exception as e:
            logging_print(self.play_func, e)

        if flag != "shuffle":
            rows = set([curr_model.index(i.row(), col).data() for i in curr_view.selectedIndexes()[::len(Column_lut)]])
            rows = str(rows).replace('{', '(').replace("}", ')')
            query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library WHERE {col_name} IN {rows} {self.now_play_sort(curr_model.tableName())}")
        if flag == "shuffle":
            query.exec_(f"CREATE VIEW now_playing AS SELECT * FROM library ORDER BY random()")
        now_play_mod.select()        
        while now_play_mod.canFetchMore():
            now_play_mod.fetchMore(QtCore.QModelIndex())
        self.now_play_queue.setModel(now_play_mod)
        self.playing_queue()

    def playing_queue(self):
        self.audio_queue = Playback_queue(self.now_play_queue_model.rowCount())
        for i in range(self.now_play_queue_model.rowCount()):
            data = self.now_play_queue_model.index(i, Column_lut['path']).data()
            self.audio_queue.put(data)


    @timeit
    def track_queue_func(self, view, col, col_name, flag = None):
        try:
            query = QtSql.QSqlQuery()
            curr_view = view
            curr_model = view.model()
            now_play_mod = self.now_play_queue_model
            prev = []
            try:
                try:
                    query.exec_(f"SELECT id FROM now_playing")
                    while query.next():
                        prev.append((query.record()).value("id"))
                    prev = set(prev)
                    if prev == set():
                        prev = ()                    
                    prev = str(prev).replace('{', '(').replace("}", ')')                    
                except Exception as e:
                    logging_print(self.track_queue_func, e)

                query.exec_("DROP VIEW now_playing")
            except Exception as e:
                logging_print(self.track_queue_func, e)

            rows = set([curr_model.index(i.row(), col).data() for i in curr_view.selectedIndexes()[::len(Column_lut)]])
            rows = str(rows).replace('{', '(').replace("}", ')')
            if flag != 'shuffle':
                sql_q = (f"CREATE VIEW now_playing "
                         f"AS SELECT * "
                         f"FROM library "
                         f"WHERE {col_name} IN {rows} OR id in {prev} {self.now_play_sort(curr_model.tableName())} ")

            if flag == 'shuffle':
                sql_q = (f"CREATE VIEW now_playing AS SELECT * FROM library WHERE id IN {rows} ORDER BY random()")
            query.exec_(sql_q)
            now_play_mod.select()        
            while now_play_mod.canFetchMore():
                now_play_mod.fetchMore(QtCore.QModelIndex())
            self.now_play_queue.setModel(now_play_mod)
            self.playing_queue()    

        except Exception as e:
            logging_print(self.track_queue_func, e)
            self.play_func(curr_view, Column_lut["id"], "id")

    @timeit
    def audio_bk_adder(self, view, col, col_name):
        try:
            query = QtSql.QSqlQuery()
            curr_view = view
            curr_model = view.model()
            prev = []
            try:
                try:
                    query.exec_(f"SELECT id FROM audio_bk")
                    while query.next():
                        prev.append((query.record()).value("id"))
                    prev = set(prev)
                    if prev == set():
                        prev = ()
                    prev = str(prev).replace('{', '(').replace("}", ')')
                except Exception as e:
                    logging_print(self.track_queue_func, e)

                query.exec_("DROP VIEW audio_bk")
            except Exception as e:
                logging_print(self.track_queue_func, e)

            rows = set([curr_model.index(i.row(), col).data() for i in curr_view.selectedIndexes()[::len(Column_lut)]])
            rows = str(rows).replace('{', '(').replace("}", ')')
            sql_q = (f"CREATE VIEW audio_bk "
                     f"AS SELECT * "
                     f"FROM library "
                     f"WHERE {col_name} IN {rows} OR id in {prev} {self.now_play_sort(curr_model.tableName())} ")
            print(sql_q)
            query.exec_(sql_q)

            curr_model.select()        
            while curr_model.canFetchMore():
                curr_model.fetchMore(QtCore.QModelIndex())
            self.now_play_queue.setModel(curr_model)    

        except Exception as e:
            logging_print(self.track_queue_func, e)

    @timeit
    def lib_view_ratings_update(self, num, view, table):
        # Updates The Ratings Of The Track Globally
        model = view.model()
        query = QtSql.QSqlQuery()
        rows = set([(model.index(i.row(), 0).data())for i in view.selectedIndexes()[::70]])
        ids = ""
        for data in rows:
            ids = f"{ids},'{data}'" 
        ids = f"({ids[1:]})"
        query.exec_(f"UPDATE library SET ratings = {num} WHERE id IN {ids}")

        model.setQuery(QtSql.QSqlQuery(f"SELECT * FROM {table}"))
        while model.canFetchMore():
            model.fetchMore(QtCore.QModelIndex())          


    @timeit
    def lib_view_search_query(self, field, view, query_model, tab = None, combo = None):
        # Runs The Search Query And Moves The Cursour To The Search Tab
        """
        field = the field to search for
        view = the view to refernce for the selected data
        query_model = model for search query generation
        tab = search tab
        combo = the playlist combo box
        """
        rows = set([i.row() for i in view.selectedIndexes()[::len(Column_lut)]])
        data = []

        try:
            QtSql.QSqlQuery("DROP VIEW search_query")
        except Exception as e:
            logging_print(self.lib_view_search_query, e)

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
                tab.setTabText(1, "Search: Artist")
                tab.setCurrentIndex(1)

            if (field == 'similar'):
                for row in rows:
                    data.extend([(query_model.index(row, Column_lut["genre"]).data())])
                data = set(data) - set([' ', ''])
                data = str(data).replace('{', '(').replace("}", ')')
                sql = f"CREATE VIEW search_query AS SELECT * FROM library WHERE genre IN {data}"
                tab.setTabText(1, "Search: Similar")
                tab.setCurrentIndex(1)

            if (field == 'in_playlist'):
                play = combo.currentText()
                for row in rows:
                    data.extend([(query_model.index(row, Column_lut["id"]).data())])
                data = set(data)
                data = str(data).replace('{', '(').replace("}", ')')
                sql = f"CREATE VIEW search_query AS SELECT * FROM {play} WHERE id IN {data}"
                tab.setTabText(1, "Search: In Playlist")
                tab.setCurrentIndex(1)

            if (field == 'in_now_play'):
                for row in rows:
                    data.extend([(query_model.index(row, Column_lut["id"]).data())])
                data = set(data)
                data = str(data).replace('{', '(').replace("}", ')')
                sql = f"CREATE VIEW search_query AS SELECT * FROM now_playing WHERE id IN {data}"
                tab.setTabText(1, "Search: In Now Playing")
                tab.setCurrentIndex(1)

            # Sets The Data Into The Search Table Model   
            self.search_table_model.setQuery(QtSql.QSqlQuery(sql))
            self.search_table_model.setQuery(QtSql.QSqlQuery("SELECT * FROM search_query"))
            [self.search_table_model.setHeaderData(s, 1, (i.replace("_", ' ')).title()) for i, s in Column_lut.items()]
            self.search_table_model.select()
            while self.search_table_model.canFetchMore():
                self.search_table_model.fetchMore(QtCore.QModelIndex())
            self.search_table.setModel(self.search_table_model)           


    def track_removal(self, flag, view):
        model = view.model()
        ids = set([model.index(i.row(), Column_lut['id']).data() for i in view.selectedIndexes()[::len(Column_lut)]])
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
            # delete from local storage

        self.all_model_declaration() 



    @timeit
    def playlist_add_current(self, view, cbox):
        name = cbox.currentText()
        self.playlist_saver(view, name)
        self.playlist_table_model.setQuery(QtSql.QSqlQuery(f"SELECT * FROM {name}"))
        while self.playlist_table_model.canFetchMore():
            self.playlist_table_model.fetchMore(QtCore.QModelIndex())
        self.playlist_table.setModel(self.playlist_table_model)             
        self.cbox_playlist_loader(cbox)


    @timeit
    def playlist_add_new(self, view, name, cbox):
        if (re.match(r'[A-Za-z_-]', name) and not(re.match(r'library', name)) and not(re.match(r'search_query', name))  and not(re.match(r'now_playing', name))):
            query = QtSql.QSqlQuery()
            try:
                try:
                    query.exec_(f"DROP VIEW {name}")
                except Exception as e:
                    logging_print(self.playlist_add_new, e)
                model = view.model()
                rows = set([model.index(i.row(), Column_lut['id']).data() for i in view.selectedIndexes()[::len(Column_lut)]])
                rows = str(rows).replace('{', '(').replace("}", ')')
                query.exec_(f"CREATE VIEW {name} AS SELECT * FROM library WHERE id IN {rows}")
            except Exception as e:
                logging_print(self.playlist_add_new, e)
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
                        logging_print(self.playlist_saver, e)                
                    query.exec_(f"DROP VIEW {name}")
                except Exception as e:
                    logging_print(self.playlist_saver, e)
                rows = set([model.index(i.row(), Column_lut['id']).data() for i in self.music_table.selectedIndexes()[::len(Column_lut)]])
                rows = str(rows).replace('{', '(').replace("}", ')')
                query.exec_(f"CREATE VIEW {name} AS SELECT * FROM library WHERE id IN {rows}")
            except Exception as e:
                logging_print(self.playlist_saver, e)


    def cbox_playlist_loader(self, cbox): 
        playlist = cbox.currentText()
        self.playlist_table_model.setQuery(QtSql.QSqlQuery(f"SELECT * FROM {playlist}"))
        while self.playlist_table_model.canFetchMore():
            self.playlist_table_model.fetchMore(QtCore.QModelIndex())
        self.playlist_table.setModel(self.playlist_table_model)        


    def context_menu_srt_tab(self, view_list, view_label, view_table, db_table = None):
        lv_1 = self.srt_table_menu(view_list, view_label, view_table, db_table)
        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos())    

    def srt_table_menu(self, view_list, view_label, view_table, db_table):
        lv_1 = QtWidgets.QMenu("Group By")

        lv_1.addAction("No Grouping").triggered.connect(lambda: self.reset_groups(view_list, view_label, db_table))
        lv_1.addAction("Reset Displayed Groups").triggered.connect(lambda: self.reset_displayed_grps(view_list, db_table))
        (lv_1).addSeparator()
        lv_1.addAction("Group By Album").triggered.connect(lambda: self.groupby_srt_call(view_list, view_label, view_table, "album", db_table))
        lv_1.addAction("Group By Album Artist").triggered.connect(lambda: self.groupby_srt_call(view_list, view_label, view_table, "albumartist", db_table))
        lv_1.addAction("Group By Artist").triggered.connect(lambda: self.groupby_srt_call(view_list, view_label, view_table, "artist", db_table))
        lv_1.addAction("Group By Composer").triggered.connect(lambda: self.groupby_srt_call(view_list, view_label, view_table, "composer", db_table))
        lv_1.addAction("Group By Folder Name").triggered.connect(lambda: self.groupby_srt_call(view_list, view_label, view_table, "path", db_table))
        lv_1.addAction("Group By Genre").triggered.connect(lambda: self.groupby_srt_call(view_list, view_label, view_table, "genre", db_table))
        lv_1.addAction("Group By File Type").triggered.connect(lambda: self.groupby_srt_call(view_list, view_label, view_table, "filetype", db_table))
        lv_1.addAction("Group By Release Date").triggered.connect(lambda: self.groupby_srt_call(view_list, view_label, view_table, "date", db_table))
        (lv_1).addSeparator()

        (lv_1).addSeparator()
        (lv_1).addAction("Small Thumbnail").triggered.connect(lambda: print("exe"))
        (lv_1).addAction("Medium Thumbnail").triggered.connect(lambda: print("exe"))
        (lv_1).addAction("Large Thumbnail").triggered.connect(lambda: print("exe"))
        (lv_1).addAction("Hide Thumbnail").triggered.connect(lambda: print("exe"))
        return lv_1

    def groupby_srt_call(self, view_list, view_label, view_table, name = None, db_table = None):
        if  name == "path":
            sql = f"""
                WITH b(x,y) AS 
                (
                VALUES(({db_table}.path), (instr({db_table}.path, '\\')))
                UNION ALL 
                SELECT x ,instr(SUBSTR(x, y+1), "\\") + y 
                FROM b 
                LIMIT 10
                ) 
                SELECT substr(path, 0, (SELECT max(y) FROM b WHERE y != '')) as "folders" FROM {db_table} GROUP BY folders;
                """
            query = QtSql.QSqlQuery(sql)
            model = QtGui.QStandardItemModel()
            while query.next():
                data = query.value(0)
                model.appendRow(QtGui.QStandardItem(str(data.split("\\")[-1])))
            view_list.setModel(model)

        else:
            sql = f"SELECT {name} FROM {db_table} WHERE {name} NOT IN ('', ' ') GROUP BY {name}"
            query = QtSql.QSqlQuery(sql)
            model = QtSql.QSqlQueryModel()
            model.setQuery(query)
            while model.canFetchMore():
                model.fetchMore(QtCore.QModelIndex())             
            view_list.setModel(model)
        view_label.setText((name.title()))


    def reset_groups(self, view_list, view_label, db_table = None):
        view_list.setModel(QtGui.QStandardItemModel())
        view_label.setText(("No Grouping".title()))


    def reset_displayed_grps(self, view_list, db_table = None):
        if  db_table == "library":
            self.music_table_model_dec()        


    def display_grps(self, data, view, db_table, field):
        field = field.lower()
        model = view.model()
        if  field == 'path':
            sql = f"""
                WITH b(x,y) AS 
                (
                VALUES(({db_table}.path), (instr({db_table}.path, '\\')))
                UNION ALL 
                SELECT x ,instr(SUBSTR(x, y+1), "\\") + y 
                FROM b 
                LIMIT 10
                ) 

                -- selects files that are in the folder
                SELECT id 
                FROM {db_table} 
                WHERE instr(path,(
                SELECT folders 
                FROM (	
                SELECT substr(path, 0,(
                SELECT max(y) 
                FROM b 
                WHERE y != ''
                -- splits the path away from the 
                -- filename and gives the index to split at
                )
                ) 
                -- splits the path away from the
                -- and gives all the unique filenames
                as "folders" 
                FROM {db_table} 
                GROUP BY folders
                ) 
                -- selects folder that is required
                WHERE folders 
                LIKE "%{data}"))
                """
            query = QtSql.QSqlQuery(sql)
            items = []
            while query.next():
                data = query.value(0)
                items.append(data)

            model.setFilter(f"id IN {self.item_set_creator(items)}")
            model.select()            
        else:
            model.setFilter(f"{field} = '{data}'")
            model.select()

        while model.canFetchMore():
            model.fetchMore(QtCore.QModelIndex())                   
    
