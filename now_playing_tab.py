from ui_init import Main_widget
from utils import *
from lib_up import Library_database_mang, Column_lut
from add_new_play_DB_ui import Ui_add_play_db
from file_explorer import FileBrowser

from PyQt5 import QtGui, QtSql, QtCore, QtWidgets
import mutagen

import sys, threading, re, logging, queue, json


class Now_playing_Tab(Main_widget):

    def __init__(self, *args):
        super(Now_playing_Tab, self).__init__()
        self.now_play_tab_functions()
    
    def now_play_tab_functions(self):

        # Table Views Double Click Binding
        self.now_play_queue.doubleClicked.connect(lambda: (self.now_play_item_doubleclk(self.now_play_queue)))

        # Declaration Of A Context Menu For Library View
        self.now_play_queue.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.now_play_queue.customContextMenuRequested.connect(self.context_menu_now_playing_view)
        
    def context_menu_now_playing_view(self):
        
        # External Popup For A New Playlist Name
        self.Ui_add_play_obj = Ui_add_play_db()
        self.Ui_add_play_obj.lineEdit.returnPressed.connect(lambda: (self.playlist_add_new(self.now_play_queue, self.Ui_add_play_obj.lineEdit.text(), self.playlist_combo),self.Ui_add_play_obj.close()))
        self.Ui_add_play_obj.buttonBox.accepted.connect(lambda: (self.playlist_add_new(self.now_play_queue, self.Ui_add_play_obj.lineEdit.text(), self.playlist_combo),self.Ui_add_play_obj.close()))
        self.Ui_add_play_obj.buttonBox.rejected.connect(lambda: self.Ui_add_play_obj.close())
        
        lv_1 = QtWidgets.QMenu()

        (lv_1).addAction("Add To Audio Books").triggered.connect( lambda: self.audio_bk_adder(self.now_play_queue, Column_lut["id"], "id"))
        lv_1_04 = lv_1.addMenu("Add To Playlist")
        (lv_1.addSection(''))
        (lv_1).addAction("Edit$")
        lv_1_07 = lv_1.addMenu("Auto-Tags$")
        lv_1_08 = lv_1.addMenu("Ratings")
        (lv_1.addSection(''))
        (lv_1).addAction("Delete").triggered.connect(lambda: self.track_removal('delete', self.now_play_queue))
        (lv_1).addAction("Remove").triggered.connect(lambda: self.track_removal('remove', self.now_play_queue))
        lv_1_10 = lv_1.addMenu("Send To$")
        lv_1_11 = lv_1.addMenu("Search")
    
        (lv_1_04).addAction("Add To New Playlist").triggered.connect(lambda: self.Ui_add_play_obj.show())
        (lv_1_04).addAction("Add To Current Playlist").triggered.connect(lambda: (self.playlist_add_current(self.playlist_combo)))
        (lv_1_04.addSection(''))
        [(lv_1_04).addAction(keys).triggered.connect(lambda: (self.playlist_saver(self.now_play_queue, keys))) for keys in self.playlist_cbox_update(self.playlist_combo)]
    
        (lv_1_08).addAction("0   Stars").triggered.connect( lambda: self.lib_view_ratings_update(0, self.now_play_queue, "now_playing"))
        (lv_1_08).addAction("1   Stars").triggered.connect( lambda: self.lib_view_ratings_update(1, self.now_play_queue, "now_playing"))
        (lv_1_08).addAction("1.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(1.5, self.now_play_queue, "now_playing"))
        (lv_1_08).addAction("2   Stars").triggered.connect( lambda: self.lib_view_ratings_update(2, self.now_play_queue, "now_playing"))
        (lv_1_08).addAction("2.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(2.5, self.now_play_queue, "now_playing"))
        (lv_1_08).addAction("3   Stars").triggered.connect( lambda: self.lib_view_ratings_update(3, self.now_play_queue, "now_playing"))
        (lv_1_08).addAction("3.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(3.5, self.now_play_queue, "now_playing"))
        (lv_1_08).addAction("4   Stars").triggered.connect( lambda: self.lib_view_ratings_update(4, self.now_play_queue, "now_playing"))
        (lv_1_08).addAction("4.5 Stars").triggered.connect( lambda: self.lib_view_ratings_update(4.5, self.now_play_queue, "now_playing"))
        (lv_1_08).addAction("5   Stars").triggered.connect( lambda: self.lib_view_ratings_update(5, self.now_play_queue, "now_playing"))
    
        lv_1_10_1 = (lv_1_10).addMenu("File (Move)")
        lv_1_10_2 = (lv_1_10).addMenu("File (Copy)")
        lv_1_10_3 = (lv_1_10).addMenu("File (Replace)")
        (lv_1_10).addAction("File Converter")
        (lv_1_10).addAction("File Rescan")
        (lv_1_10).addAction("Analysis")
    
        (lv_1_11).addAction('Find Artist')
 
        (lv_1_11).addAction('Find Similar')       
        (lv_1_11).addAction('Locate in Playlist')
        (lv_1_11).addAction('Locate in Now Playing')
        (lv_1_11).addAction('Locate in File Explorer')
                    
        cursor = QtGui.QCursor()
        lv_1.exec_(cursor.pos())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = Now_playing_Tab()
    main_app.main_tabs.setCurrentIndex(5)
    main_app.show()
    app.exec_()
