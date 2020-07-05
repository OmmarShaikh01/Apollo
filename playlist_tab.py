from ui_init import Main_widget
from utils import *
from lib_up import Library_database_mang, Column_lut
from add_new_play_DB_ui import Ui_add_play_db
from file_explorer import FileBrowser

from PyQt5 import QtGui, QtSql, QtCore, QtWidgets
import mutagen

import sys, threading, re, logging, queue, json

class Playlist_Tab(Main_widget):

    def __init__(self, *args):
        super(Playlist_Tab, self).__init__()
        self.playlist_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.playlist_table.customContextMenuRequested.connect(self.context_menu_playlist_view)  
        self.playlist_table.doubleClicked.connect(lambda: (self.lib_item_doubleclk(self.playlist_table)))
        self.playlist_srt_list_func()
        
    def context_menu_playlist_view(self):
        lv_1 = QtWidgets.QMenu()
       
        # adds lv_1 to the global item stack to apply theme
        self.__dict__["playlist_cmenu"] = lv_1
        self.theme_setter.replace_item(self.__dict__)
        
        # applies the actual theme
        self.theme_setter.apply_theme(lv_1)      

        (lv_1).addAction("Play Now").triggered.connect(lambda: self.play_func(self.playlist_table, Column_lut["id"], "id"))
        (lv_1).addAction("Queue Next").triggered.connect( lambda: self.track_queue_func(self.playlist_table, Column_lut["id"], "id"))
        (lv_1).addAction("Queue Random").triggered.connect( lambda: self.track_queue_func(self.playlist_table, Column_lut["id"], "id", flag = "shuffle"))
        (lv_1.addSection(''))
        (lv_1).addAction("Add To Audio Books").triggered.connect( lambda: self.audio_bk_adder(self.playlist_table, Column_lut["id"], "id"))
        lv_1_05 = lv_1.addMenu("Play (more)$")
        (lv_1).addAction("Edit$")
        lv_1_07 = lv_1.addMenu("Auto-Tags$")
        lv_1_08 = lv_1.addMenu("Ratings")
        (lv_1.addSection(''))
        (lv_1).addAction("Delete").triggered.connect(lambda: self.track_removal('delete', self.playlist_table))
        (lv_1).addAction("Remove").triggered.connect(lambda: self.track_removal('remove', self.playlist_table))
        lv_1_10 = lv_1.addMenu("Send To$")
        lv_1_11 = lv_1.addMenu("Search")
        lv_1_12 = lv_1.addMenu("Displayed Fields")

        (lv_1_05.addSection(''))
        (lv_1_05).addAction("Play Shuffle").triggered.connect( lambda: self.play_func(self.playlist_table, Column_lut["id"], "id", flag = 'shuffle'))
        (lv_1_05).addAction("Play Similar").triggered.connect( lambda: self.play_func(self.playlist_table, Column_lut["genre"], "genre"))
        (lv_1_05).addAction("Play Album").triggered.connect( lambda: self.play_func(self.playlist_table, Column_lut["album"], "album"))
        (lv_1_05).addAction("Play Artist").triggered.connect( lambda: self.play_func(self.playlist_table, Column_lut["artist"], "artist"))
        (lv_1_05.addSection(''))
        (lv_1_05).addAction("Queue Album").triggered.connect( lambda: self.track_queue_func(self.playlist_table, Column_lut["artist"], "artist"))
        (lv_1_05).addAction("Queue AlbumArtist").triggered.connect( lambda: self.track_queue_func(self.playlist_table, Column_lut["artist"], "artist"))
    
        
        (lv_1_08).addAction("0   Stars").triggered.connect( lambda: self.lib_view_ratings_update(0, self.playlist_table, self.playlist_combo.currentText()))
        (lv_1_08).addAction("1   Stars").triggered.connect( lambda: self.lib_view_ratings_update(1, self.playlist_table, self.playlist_combo.currentText()))
        (lv_1_08).addAction("1.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(1.5, self.playlist_table, self.playlist_combo.currentText()))
        (lv_1_08).addAction("2   Stars").triggered.connect( lambda: self.lib_view_ratings_update(2, self.playlist_table, self.playlist_combo.currentText()))
        (lv_1_08).addAction("2.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(2.5, self.playlist_table, self.playlist_combo.currentText()))
        (lv_1_08).addAction("3   Stars").triggered.connect( lambda: self.lib_view_ratings_update(3, self.playlist_table, self.playlist_combo.currentText()))
        (lv_1_08).addAction("3.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(3.5, self.playlist_table, self.playlist_combo.currentText()))
        (lv_1_08).addAction("4   Stars").triggered.connect( lambda: self.lib_view_ratings_update(4, self.playlist_table, self.playlist_combo.currentText()))
        (lv_1_08).addAction("4.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(4.5, self.playlist_table, self.playlist_combo.currentText()))
        (lv_1_08).addAction("5   Stars").triggered.connect( lambda: self.lib_view_ratings_update(5, self.playlist_table, self.playlist_combo.currentText()))
    
        lv_1_10_1 = (lv_1_10).addMenu("File (Move)")
        lv_1_10_2 = (lv_1_10).addMenu("File (Copy)")
        lv_1_10_3 = (lv_1_10).addMenu("File (Replace)")
        (lv_1_10).addAction("File Converter")
        (lv_1_10).addAction("File Rescan")
        (lv_1_10).addAction("Analysis")
    
        (lv_1_11).addAction('Find Artist').triggered.connect( lambda: self.lib_view_search_query("artist",
                                                                                                 self.playlist_table,
                                                                                                 self.playlist_table_model,
                                                                                                 self.main_tabs,
                                                                                                 self.playlist_combo))

        (lv_1_11).addAction('Find Similar').triggered.connect( lambda: self.lib_view_search_query('similar',
                                                                                                  self.playlist_table,
                                                                                                  self.playlist_table_model,
                                                                                                  self.main_tabs,
                                                                                                  self.playlist_combo))

        (lv_1_11).addAction('Locate in Now Playing').triggered.connect( lambda: self.lib_view_search_query('in_now_play',
                                                                                                           self.playlist_table,
                                                                                                           self.now_play_queue_model,
                                                                                                           self.main_tabs,
                                                                                                           self.playlist_combo))

        (lv_1_11).addAction('Locate in File Explorer').triggered.connect( lambda: self.lib_view_search_query('in_file_exp',
                                                                                                             self.playlist_table,
                                                                                                             self.playlist_table_model,
                                                                                                             self.main_tabs,
                                                                                                             self.playlist_combo))

                    
        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos())
        
        
    def playlist_srt_list_func(self):
            
        function = lambda: (self.context_menu_srt_tab(self.playlist_grp_srt_list, self.playlist_grp_srt_btn, self.playlist_table, self.playlist_combo.currentText()))
        self.playlist_grp_srt_btn.setMenu(self.srt_table_menu(self.playlist_grp_srt_list, self.playlist_grp_srt_btn, self.playlist_table, self.playlist_combo.currentText()))        
        
        self.playlist_grp_srt_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.playlist_grp_srt_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.playlist_grp_srt_btn.customContextMenuRequested.connect(function)
        self.playlist_grp_srt_list.customContextMenuRequested.connect(function)
        self.playlist_grp_srt_list.doubleClicked.connect(lambda ind: self.display_grps(ind.data(), self.playlist_table, self.playlist_combo.currentText, self.playlist_grp_srt_btn.text()))

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = Playlist_Tab()
    main_app.show()
    app.exec_()
