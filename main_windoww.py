from PyQt5 import QtCore, QtGui, QtWidgets
import json
import re
import time
import os
import threading
import tinytag
import mutagen

import file_explorer
import preferences
from main_window_ui import Ui_MainWindow
from custom_qt_widgets import custom_playlist_display_widget


class main_window_player(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(main_window_player, self).__init__()
        self.setupUi(self)
        (threading.Thread(target = self.populate_trees, args = ())).start()
        self.all_actions()
        self.button_actions()
    
    
    def all_actions(self):
        self.actionAdd_Files_to_librayr.triggered.connect(self.file_exp)
        self.actionSettings.triggered.connect(self.settings_caller)
        self.actionRescan.triggered.connect(self.populate_trees)
        self.toolButton.pressed.connect(self.search_library)
        self.lineEdit.textChanged.connect(self.search_library)
        self.table_view_music_functions()
      

    def button_actions(self):
        self.play_button.pressed.connect(self.trial)
        self.skip_back.pressed.connect(self.trial)
        self.skip_track_back.pressed.connect(self.trial)
        self.stop.pressed.connect(self.trial)
        self.pause.pressed.connect(self.trial)
        self.skip_track_fwd.pressed.connect(self.trial)
        self.skip_ford.pressed.connect(self.trial)
        self.shuffle_btn.pressed.connect(self.trial)
        self.mute_btn.pressed.connect(self.trial)
        self.volume_btn.pressed.connect(self.trial)  

### button functions ###########################################################
################################################################################



### search functions ###########################################################
################################################################################

    def searching_alg(self, search_text = "", string = ""):
        match = [bool(re.search(search_text,string.capitalize())),
                 bool(re.search(search_text,string.upper())),
        bool(re.search(search_text,string.lower())),
        bool(re.search(search_text,string.title()))]
        match_fin = [int(i) for i in match]
        return sum(match_fin)

    def search_library(self):
        search_text = self.lineEdit.text()
        if search_text == '': 
            self.lib_refresh()

        else:
            self.lib_refresh()
            self.model_data = self.tableView_music.model()       
            data = [ i for i in range(self.model_data.columnCount()) if self.model_data.headerData(i, QtCore.Qt.Orientation(1)) == "Priority"][0]
            for rows in range(self.model_data.rowCount()):
                count = 20
                for cols in [2, 3, 5, 6, 17]:
                    if self.searching_alg(search_text, self.model_data.index(rows, cols).data()) >= 1:
                        count -= 1
                        self.table_model.setData(self.model_data.index(rows, data), str(count))
                if not (count in [19, 18, 17, 16, 15]):
                    self.tableView_music.setRowHidden(rows, True)
            self.tableView_music.setModel(self.model_data)
            self.tableView_music.sortByColumn(data, QtCore.Qt.AscendingOrder)
            self.tableView_music.scrollToTop()


### populate tree functions ####################################################
################################################################################

    def populate_cond_check(self): 
        with open("resources/settings/Music_library_data.txt") as update, open("resources/settings/Music_library_data.txt") as const:
            a, b = (len((json.load(update)).keys())), (len(const.readlines()))
            if a == b:
                self.populate_from_DB()
            if a != b:
                self.populate_from_DB_cal()               


    def populate_from_DB(self):
        t1 = time.monotonic()
        if os.path.isfile("resources/settings/library_data.txt"):
            with open('resources/settings/library_data.txt', 'r', encoding = 'utf-8') as lib_f:
                file_data = lib_f.readlines()
                for i in file_data:
                    temp_obj_data = eval(i)
                    self.table_model.appendRow([QtGui.QStandardItem(str(i)) for i in temp_obj_data])
        print(time.monotonic() - t1)


    def populate_from_DB_cal(self):
        t1 = time.monotonic()
        if True:
            file_data = self.file_to_data_typ(filename = "resources/settings/Music_library_data.txt")
            with open('resources/settings/library_data.txt', 'w+', encoding = 'utf-8') as lib_f:
                for (key,value) in file_data.items():
                    temp_obj_data = [(key),
                                     (value['file_path'].replace('\\', '/')),
                                     (((value['file_path']).split('/'))[-1]), 
                                     (str(round(( value['meta_tags']['filesize'] / 1000000), 2)) + " Mb" ),
                                     (value['meta_tags']['album']),
                                     (value['meta_tags']['albumartist']),
                                     (value['meta_tags']['artist']),
                                     (value['meta_tags']['audio_offset']),
                                     (str(int(value['meta_tags']['bitrate'])) + " Kbps" ),
                                     (value['meta_tags']['channels']),
                                     (value['meta_tags']['composer']),
                                     (value['meta_tags']['disc']),
                                     (value['meta_tags']['disc_total']), 
                                     (("{0}.{1} Min".format(str(int( value['meta_tags']['duration'] // 60)), str(int( value['meta_tags']['duration'] % 60))))), 
                                     (value['meta_tags']['genre']), 
                                     (value['meta_tags']['samplerate']),
                                     (value['meta_tags']['title']), 
                                     (value['meta_tags']['track']), 
                                     (value['meta_tags']['track_total']),
                                     (value['meta_tags']['year']),
                                     (value['ratings']),
                                     (value['date_added']),
                                     (str(20))
                                     ]
                    lib_f.write(f"{str(temp_obj_data)}\n")    
                    self.table_model.appendRow([QtGui.QStandardItem(str(i)) for i in temp_obj_data])
        print(time.monotonic() - t1)
   

########### misc functions #####################################################
################################################################################   
    
    
    def pixmap_setter(self, fname, obj, scale):
        # pixmap
        try:
            try:
                meta_image = ((mutagen.File(fname)).pictures[0]).data
            except Exception as e: pass #print(e)
            
            try:
                meta_image = ((mutagen.File(fname)).get("APIC:")).data
            except Exception as e: pass #print(e)            
            
            try:
                meta_image = ((mutagen.File(fname)).get("APIC:Cover (front)")).data
            except Exception as e: pass #print(e)
                
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
            
            
    def file_to_data_typ(self, filename, flagf = "read", string = None, key = None):

        """
        used for I/O in json files
        filename<string>
        flagf<string(read/write)>
        <string> is data to be written to a file
        <key> is the part to where the data needs to go
        """

        if flagf == "read":
            with open(filename) as json_file:
                data = json.load(json_file)
            return(data)

        if flagf == "write":
            with open(filename) as json_file:
                data = json.load(json_file)
                if string not in data[key] :
                    data[key].append(string)
            with open(filename, 'w') as json_file:
                json.dump(data, json_file)


    def wrapper_second_window(self, cls):# wraps and displays second window
        self.ui = cls()
        self.ui.show()


    def file_exp(self):
        """displays the file explorer"""
        self.wrapper_second_window(file_explorer.FileBrowser)

    
    def settings_caller(self):
        """displays the preferences"""
        self.wrapper_second_window(preferences.settings_main_window)

    
    def trial(self):
        print("trial")

############## Music Library Tab Functions #####################################
################################################################################
   
    
    def table_view_music_functions(self):
        # Atribute Declaration
        (self.tableView_music.horizontalHeader()).setSectionsMovable(True)
        self.tableView_music.setShowGrid(False)        
        
        # Style sheet Declartion
        self.tableView_music.setStyleSheet(("QTableView { selection-background-color: rgb(255,245,213); selection-color: black; }"))
        
        # table views double click binding
        self.tableView_music.doubleClicked.connect(lambda: self.handleSelectionChanged(((self.tableView_music.model()).index((self.tableView_music.currentIndex().row()), 1)).data(), 'dc'))

        # table views context menu
        self.tableView_music.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView_music.customContextMenuRequested.connect(self.context_menu_tableView_music)      
   
    
    def populate_trees(self):
        """
        this functin populates the table widget nd when called again delets the current row and rescans the
        library
        """
        self.table_model = QtGui.QStandardItemModel()
        with open("resources/settings/config.txt") as json_file:
            dicto = (json.load(json_file))["column_displayed"]
        count = 0

        for j in dicto.keys():
            self.table_model.setHorizontalHeaderItem(count, QtGui.QStandardItem(str(j)))
            count += 1

        for i,j in zip(dicto.values(), dicto.keys()):
            if not (bool(i)):
                self.tableView_music.setColumnHidden(count, True)
            count += 1
        self.tableView_music.setModel(self.table_model)
        self.populate_cond_check()    
    
    
    def lib_refresh(self):
        if True:
            self.tableView_music.clearSelection()
            model = self.tableView_music.model()

            # returns header data
            data = [ i for i in range(model.columnCount()) if model.headerData(i, QtCore.Qt.Orientation(1)) == "Priority"][0]
            for row in range(model.rowCount()):
                self.tableView_music.setRowHidden(row, False)
                if model.index(row, data).data() != "20":
                    self.table_model.setData(model.index(row, data), 20)

    
    def handleSelectionChanged(self, data, flag):
        if flag == 'dc':    
            try:
                data = data
                self.meta_data_getter(data)
                self.meta_image_getter(data)            
            except Exception as e: pass # print(e)        

    
    
    def meta_image_getter(self, data):     
        try:
            try:
                meta_image = ((mutagen.File(data)).pictures[0]).data
            except Exception as e: pass #print(e)
            
            try:
                meta_image = ((mutagen.File(data)).get("APIC:")).data
            except Exception as e: pass #print(e)            
            
            try:
                meta_image = ((mutagen.File(data)).get("APIC:Cover (front)")).data
            except Exception as e: pass #print(e)
            
            
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(meta_image)
            pixmap = pixmap.scaled(300, 300)
            self.pixmap_cov.setPixmap(pixmap)
            self.pixmap_cov.setScaledContents(True)
            
        except Exception as e:
            pixmap = QtGui.QPixmap()
            pixmap = pixmap.scaled(300, 300)
            self.pixmap_cov.setPixmap(pixmap)
            self.pixmap_cov.setScaledContents(True)
    
    
    def meta_data_getter(self, data):          
        meta_info = (tinytag.TinyTag.get(data)).as_dict()
        meta_info = [str(f'Artist: {meta_info["artist"]}'),
                     str(f'Title: {meta_info["title"]}'),
                     str(f'Album: {meta_info["album"]}'),
                     str(f'Album Artist: {meta_info["albumartist"]}'),
                     str(f'Composer: {meta_info["composer"]}'),
                     str(f'Genre: {meta_info["genre"]}'),
                     str(f'Samplerate: {meta_info["samplerate"]} Hz'),
                     str(f'Bitrate: {int(meta_info["bitrate"])} Kbps'),
                     str(f'Channels: {meta_info["channels"]} Channels'),
                     str(f'Duration: {(("{0}.{1} Min".format(str(int( meta_info["duration"] // 60)), str(int( meta_info["duration"] % 60)))))}'),
                     str(f'Year: {meta_info["year"]}')]
        file_meta_model = QtGui.QStandardItemModel()
        file_meta_model.appendColumn([QtGui.QStandardItem(str(i)) for i in meta_info])
        self.file_meta_info_list.setModel(file_meta_model) 
        self.tableView_music.clearSelection()      

    
    def context_menu_tableView_music(self):    
        
        self.lv_1 = QtWidgets.QMenu()
        
        
        (self.lv_1).addAction("PLay Now").triggered.connect(lambda: (self.playlist_gen('append')))
        (self.lv_1).addAction("Queue Next").triggered.connect(lambda: (self.playlist_gen("queue")))
        (self.lv_1).addAction("Queue Random")
        self.lv_1_04 = self.lv_1.addMenu("Add To Playlist")
        (self.lv_1.addSection(''))
        self.lv_1_05 = self.lv_1.addMenu("Play (more)")
        (self.lv_1).addAction("Edit")
        self.lv_1_07 = self.lv_1.addMenu("Auto-Tags")
        self.lv_1_08 = self.lv_1.addMenu("Ratings")
        (self.lv_1.addSection(''))
        (self.lv_1).addAction("Delete")
        self.lv_1_10 = self.lv_1.addMenu("Send To")
        self.lv_1_11 = self.lv_1.addMenu("Search")

        
        (self.lv_1_04).addAction("Add To New Playlist")
        (self.lv_1_04).addAction("Add To Current Playlist")
        (self.lv_1_04.addSection(''))
        (self.lv_1_04).addAction("Default Playlist")
        
        
        (self.lv_1_05).addAction("Bypass Filters")
        self.lv_1_05_1 = self.lv_1_05.addMenu("Output To")
        (self.lv_1_05.addSection(''))
        (self.lv_1_05).addAction("Play Shuffle")
        (self.lv_1_05).addAction("Play Similar")
        (self.lv_1_05).addAction("Play Album")
        (self.lv_1_05).addAction("Play Artist")
        (self.lv_1_05.addSection(''))
        (self.lv_1_05).addAction("Queue Album")
        (self.lv_1_05).addAction("Queue Album")
        
        (self.lv_1_08).addAction("0   Stars")
        (self.lv_1_08).addAction("1   Stars")
        (self.lv_1_08).addAction("1.5 Stars")
        (self.lv_1_08).addAction("2   Stars")
        (self.lv_1_08).addAction("2.5 Stars")
        (self.lv_1_08).addAction("3   Stars")
        (self.lv_1_08).addAction("3.5 Stars")
        (self.lv_1_08).addAction("4   Stars")
        (self.lv_1_08).addAction("4.5 Stars")
        (self.lv_1_08).addAction("5   Stars")

        (self.lv_1_10).addAction("Audio Fx")
        self.lv_1_10_1 = (self.lv_1_10).addMenu("File (Move)")
        self.lv_1_10_2 = (self.lv_1_10).addMenu("File (Copy)")
        self.lv_1_10_3 = (self.lv_1_10).addMenu("File (Replace)")
        (self.lv_1_10).addAction("File Converter")
        (self.lv_1_10).addAction("File Rescan")
        (self.lv_1_10).addAction("Analysis")
        
        (self.lv_1_11).addAction('Find Artist')
        (self.lv_1_11).addAction('Find Similar')
        (self.lv_1_11).addAction('Locate in Playlist')
        (self.lv_1_11).addAction('Locate in Library')
        (self.lv_1_11).addAction('Locate in File Explorer')
        (self.lv_1_11).addAction('Locate in Directory')
        
        cursor = QtGui.QCursor()
        self.lv_1.exec_(cursor.pos())         



########### Playlist  functions ################################################
################################################################################    
    
    def playlist_gen(self, flag):
        a = [[((self.tableView_music.model()).index(i.row(), col)).data() for col in [1, 6, 16, 13, 8, 19]] for i in (self.tableView_music.selectedIndexes())[::23]]
        if flag == 'append':
            self.tracks_list.clear()
            for i in a:
                self.playlist_listV_pop(i)
        
        if flag == 'queue':  
            for i in a:
                self.playlist_listV_pop(i)            
    
    def playlist_listV_pop(self, data):
        
        custom_playlist_display_widget_ob = custom_playlist_display_widget()
        
        #pixmap
        self.playlist_pop_pixmap(data, custom_playlist_display_widget_ob)
        # artist
        custom_playlist_display_widget_ob.label_2.setText(str(data[1]))
        # title
        custom_playlist_display_widget_ob.label_3.setText(str(data[2]))
        # duration
        custom_playlist_display_widget_ob.label_4.setText(str(data[3]))
        # bitrate
        custom_playlist_display_widget_ob.label_5.setText(str(data[4]))
        # rating
        custom_playlist_display_widget_ob.label_6.setText(str(data[5]))

        myQListWidgetItem = QtWidgets.QListWidgetItem(self.tracks_list)
        myQListWidgetItem.setSizeHint(custom_playlist_display_widget_ob.sizeHint())
        self.tracks_list.addItem(myQListWidgetItem)
        self.tracks_list.setItemWidget(myQListWidgetItem, custom_playlist_display_widget_ob)

    
    
    def playlist_pop_pixmap(self, data, custom_playlist_display_widget_ob):
        # pixmap
        try:
            try:
                meta_image = ((mutagen.File(data)).pictures[0]).data
            except Exception as e: pass #print(e)
            
            try:
                meta_image = ((mutagen.File(data)).get("APIC:")).data
            except Exception as e: pass #print(e)            
            
            try:
                meta_image = ((mutagen.File(data)).get("APIC:Cover (front)")).data
            except Exception as e: pass #print(e)
                
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(meta_image)
            pixmap = pixmap.scaled(400, 400)
            custom_playlist_display_widget_ob.label.setPixmap(pixmap)
            custom_playlist_display_widget_ob.label.setScaledContents(True)
            
        except Exception as e:
            pixmap = QtGui.QPixmap()
            pixmap = pixmap.scaled(400, 400)
            custom_playlist_display_widget_ob.label.setPixmap(pixmap)
            custom_playlist_display_widget_ob.label.setScaledContents(True)
            # print(e)         




################################################################################
################################################################################

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = main_window_player()
    main_window.show()
    sys.exit(app.exec_())
