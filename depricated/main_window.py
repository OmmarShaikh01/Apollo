from PyQt5 import QtCore, QtGui, QtWidgets
import file_explorer
import preferences
from main_window_ui import Ui_MainWindow
import json, re, time, os
import threading, tinytag


class main_window_player(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(main_window_player, self).__init__()
        self.setupUi(self)
        (threading.Thread(target = self.populate_trees, args = ())).start()
        self.all_actions()
        self.pallet_declaration()
        self.attributes_dec()
        self.button_actions()


    def pallet_declaration(self):
        self.tableView_music.setStyleSheet(("QTableView { selection-background-color: rgb(255,245,213); selection-color: black; }"))

    def attributes_dec(self):
        (self.tableView_music.horizontalHeader()).setSectionsMovable(True)
        self.tableView_music.setShowGrid(False)

    def all_actions(self):
        self.actionAdd_Files_to_librayr.triggered.connect(self.file_exp)
        self.actionSettings.triggered.connect(self.settings_caller)
        self.actionRescan.triggered.connect(self.populate_trees)
        self.toolButton.pressed.connect(self.search_library)
        self.tableView_music.doubleClicked.connect(self.handleSelectionChanged)
        self.lineEdit.textChanged.connect(self.search_library)

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

    def handleSelectionChanged(self):
        model = self.tableView_music.model()
        data = model.index((self.tableView_music.selectedIndexes())[1].row(),1).data()
        row = model.index((self.tableView_music.selectedIndexes())[1].row(),0).data()

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

        [QtGui.QStandardItem(str(i)) for i in meta_info]
        self.tableView_music.clearSelection()
        print(row, data)

    def trial(self):
        print("trial")


################################################################################
################################################################################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = main_window_player()
    main_window.show()
    sys.exit(app.exec_())
