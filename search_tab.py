from ui_init import Main_widget
from utils import *
from lib_up import Library_database_mang, Column_lut
from add_new_play_DB_ui import Ui_add_play_db
from file_explorer import FileBrowser

from PyQt5 import QtGui, QtSql, QtCore, QtWidgets
import mutagen

import sys, threading, re, logging, queue, json

class Search_Tab(Main_widget):

    # View = self.search_table
    # Model = self.search_table_model    

    def __init__(self, *args):
        super(Search_Tab, self).__init__()
        self.search_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.search_table.customContextMenuRequested.connect(self.context_menu_search_view)
        self.search_table.doubleClicked.connect(lambda: (self.lib_item_doubleclk(self.search_table)))
        self.search_srt_list_func()
        
    def context_menu_search_view(self):
        
        # External Popup For A New Playlist Name
        self.Ui_add_play_obj = Ui_add_play_db()
        self.Ui_add_play_obj.lineEdit.returnPressed.connect(lambda: (self.playlist_add_new(self.search_table, self.Ui_add_play_obj.lineEdit.text(), self.playlist_combo),self.Ui_add_play_obj.close()))
        self.Ui_add_play_obj.buttonBox.accepted.connect(lambda: (self.playlist_add_new(self.search_table, self.Ui_add_play_obj.lineEdit.text(), self.playlist_combo),self.Ui_add_play_obj.close()))
        self.Ui_add_play_obj.buttonBox.rejected.connect(lambda: self.Ui_add_play_obj.close())         
        
        lv_1 = QtWidgets.QMenu()
        
        (lv_1).addAction("Play Now").triggered.connect(lambda: self.play_func(self.search_table, Column_lut["id"], "id"))
        (lv_1).addAction("Queue Next").triggered.connect( lambda: self.track_queue_func(self.search_table, Column_lut["id"], "id"))
        (lv_1).addAction("Queue Random").triggered.connect( lambda: self.track_queue_func(self.search_table, Column_lut["id"], "id", flag = "shuffle"))
        (lv_1).addAction("Add To Audio Books").triggered.connect( lambda: self.audio_bk_adder(self.search_table, Column_lut["id"], "id"))
        lv_1_04 = lv_1.addMenu("Add To Playlist")
        (lv_1.addSection(''))
        lv_1_05 = lv_1.addMenu("Play (more)$")
        (lv_1).addAction("Edit$")
        lv_1_07 = lv_1.addMenu("Auto-Tags$")
        lv_1_08 = lv_1.addMenu("Ratings")
        (lv_1.addSection(''))
        (lv_1).addAction("Delete").triggered.connect(lambda: self.track_removal('delete', self.search_table_model))
        (lv_1).addAction("Remove").triggered.connect(lambda: self.track_removal('remove', self.search_table_model))
        lv_1_10 = lv_1.addMenu("Send To$")
        lv_1_11 = lv_1.addMenu("Search")
        lv_1_12 = lv_1.addMenu("Displayed Fields")
    
        (lv_1_04).addAction("Add To New Playlist").triggered.connect(lambda: self.Ui_add_play_obj.show())
        (lv_1_04).addAction("Add To Current Playlist").triggered.connect(lambda: (self.playlist_add_current(self.playlist_combo)))
        (lv_1_04.addSection(''))
        [(lv_1_04).addAction(keys).triggered.connect(lambda: (self.playlist_saver(self.search_table, keys))) for keys in self.playlist_cbox_update(self.playlist_combo)]


        (lv_1_05.addSection(''))
        (lv_1_05).addAction("Play Shuffle").triggered.connect( lambda: self.play_func(self.search_table, Column_lut["id"], "id", flag = 'shuffle'))
        (lv_1_05).addAction("Play Similar").triggered.connect( lambda: self.play_func(self.search_table, Column_lut["genre"], "genre"))
        (lv_1_05).addAction("Play Album").triggered.connect( lambda: self.play_func(self.search_table, Column_lut["album"], "album"))
        (lv_1_05).addAction("Play Artist").triggered.connect( lambda: self.play_func(self.search_table, Column_lut["artist"], "artist"))
        (lv_1_05.addSection(''))
        (lv_1_05).addAction("Queue Album").triggered.connect( lambda: self.track_queue_func(self.search_table, Column_lut["artist"], "artist"))
        (lv_1_05).addAction("Queue AlbumArtist").triggered.connect( lambda: self.track_queue_func(self.search_table, Column_lut["artist"], "artist"))
    
        (lv_1_08).addAction("0   Stars").triggered.connect( lambda: self.lib_view_ratings_update(0, self.search_table, "search_query"))
        (lv_1_08).addAction("1   Stars").triggered.connect( lambda: self.lib_view_ratings_update(1, self.search_table, "search_query"))
        (lv_1_08).addAction("1.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(1.5, self.search_table, "search_query"))
        (lv_1_08).addAction("2   Stars").triggered.connect( lambda: self.lib_view_ratings_update(2, self.search_table, "search_query"))
        (lv_1_08).addAction("2.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(2.5, self.search_table, "search_query"))
        (lv_1_08).addAction("3   Stars").triggered.connect( lambda: self.lib_view_ratings_update(3, self.search_table, "search_query"))
        (lv_1_08).addAction("3.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(3.5, self.search_table, "search_query"))
        (lv_1_08).addAction("4   Stars").triggered.connect( lambda: self.lib_view_ratings_update(4, self.search_table, "search_query"))
        (lv_1_08).addAction("4.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(4.5, self.search_table, "search_query"))
        (lv_1_08).addAction("5   Stars").triggered.connect( lambda: self.lib_view_ratings_update(5, self.search_table, "search_query"))
    
        lv_1_10_1 = (lv_1_10).addMenu("File (Move)")
        lv_1_10_2 = (lv_1_10).addMenu("File (Copy)")
        lv_1_10_3 = (lv_1_10).addMenu("File (Replace)")
        (lv_1_10).addAction("File Converter").triggered.connect(lambda: print("exe"))
        (lv_1_10).addAction("File Rescan").triggered.connect(lambda: print("exe"))
        (lv_1_10).addAction("Analysis").triggered.connect(lambda: print("exe"))

        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos())

    def search_srt_list_func(self):
        
        function = lambda: (self.context_menu_srt_tab(self.search_grp_srt_list, self.search_grp_srt_btn, self.search_table, "search_query"))
        self.search_grp_srt_btn.setMenu(self.srt_table_menu(self.search_grp_srt_list, self.search_grp_srt_btn, self.search_table, "search_query"))
        self.search_grp_srt_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.search_grp_srt_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        self.search_grp_srt_btn.customContextMenuRequested.connect(function)
        self.search_grp_srt_list.customContextMenuRequested.connect(function)
        self.search_grp_srt_list.doubleClicked.connect(lambda ind: self.display_grps(ind.data(), self.search_table, 'search_query', self.search_grp_srt_btn.text()))

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = Search_Tab()
    main_app.show()
    app.exec_()
