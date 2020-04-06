from PyQt5 import QtCore, QtGui, QtWidgets
import file_explorer, preferences
import main_window_ui
import json, re, time, os


class main_window_player(main_window_ui.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(main_window_player, self).__init__()
        self.setupUi(self)
        self.populate_trees()
        self.all_actions()
        self.pallet_declaration()
        self.attributes_dec()
        self.button_actions()


    def pallet_declaration(self):
        self.tableView_music.setStyleSheet(("QTableView { selection-background-color: rgb(255,245,213); selection-color: black; }"))

    def attributes_dec(self):
        (self.tableView_music.horizontalHeader()).setSectionsMovable(True)

    def all_actions(self):
        self.actionAdd_Files_to_librayr.triggered.connect(self.file_exp)
        self.actionSettings.triggered.connect(self.settings_caller)
        self.actionRescan.triggered.connect(self.populate_trees)
        self.toolButton.pressed.connect(self.search_library)
        self.tableView_music.doubleClicked.connect(self.handleSelectionChanged)
        self.lineEdit.textChanged.connect(self.lib_refresh)

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



################################################################################
################################################################################


### misc functions #############################################################
################################################################################
    def searching_alg(self, search_text = "", string = ""):
        match = [bool(re.search(search_text,string.capitalize())),
        bool(re.search(search_text,string.upper())),
        bool(re.search(search_text,string.lower())),
        bool(re.search(search_text,string.title()))]
        match_fin = [int(i) for i in match]
        return sum(match_fin)

    def search_library(self):
        self.lib_refresh()
        search_text = self.lineEdit.text()
        self.model_data = self.tableView_music.model()
        data = [ i for i in range(self.model_data.columnCount()) if self.model_data.headerData(i, QtCore.Qt.Orientation(1)) == "priority"][0]
        for rows in range(self.model_data.rowCount()):
            count = 20
            for cols in [3, 4, 5, 14]:
                if self.searching_alg(search_text, self.model_data.index(rows, cols).data()) >= 1:
                    count -= 1
                    self.table_model.setData(self.model_data.index(rows, data), str(count))
            if not (count in [19, 18, 17, 16, 15]):
                self.tableView_music.setRowHidden(rows, True)
        self.tableView_music.setModel(self.model_data)
        self.tableView_music.sortByColumn(data, QtCore.Qt.AscendingOrder)
        self.tableView_music.scrollToTop()

    def populate_trees(self):
        """
        this functin populates the table widget nd when called again delets the current row and rescans the
        library
        """
        self.table_model = QtGui.QStandardItemModel()
        with open("resources\\settings\\config.txt") as json_file:
            dicto = (json.load(json_file))["column_displayed"]
        count = 0
        for j in dicto.keys():
            self.table_model.setHorizontalHeaderItem(count, QtGui.QStandardItem(str(j)))
            count += 1
        self.tableView_music.setModel(self.table_model)
        file_data = self.file_to_data_typ(filename = "resources\\settings\\Music_library_data.txt")


        for row_index, item in enumerate(file_data):
            temp = []
            temp = [QtGui.QStandardItem(str(item["file_path"]))]
            temp.append(QtGui.QStandardItem(((item["file_path"]).split('/'))[-1]))
            for key, value in  enumerate(item["meta_data"].values()):
                if key == 0 :
                    value = (str(round((value / 1000000), 2)) + " Mb")
                if key == 5 :
                    value = (str(int(value)) + " Kbps")
                if key == 10:
                    value = "{0}.{1} Min".format(str(int(value // 60)), str(int(value % 60)))
                temp.append(QtGui.QStandardItem(str(value)))
            temp.append(QtGui.QStandardItem(str(20)))
            self.table_model.appendRow(temp)
        # self.table_model.removeColumn(21)
        count = 0
        for i,j in zip(dicto.values(), dicto.keys()):
            if not (bool(i)):
                self.tableView_music.setColumnHidden(count, True)
            count += 1

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
        if self.lineEdit.text() == "":
            self.tableView_music.clearSelection()
            model = self.tableView_music.model()
            
            # returns header data
            data = [ i for i in range(model.columnCount()) if model.headerData(i, QtCore.Qt.Orientation(1)) == "priority"][0]
            for row in range(model.rowCount()):
                self.tableView_music.setRowHidden(row, False)
                if model.index(row, data).data() != "20":
                    self.table_model.setData(model.index(row, data), 20)
    
    def handleSelectionChanged(self):
        model = self.tableView_music.model()
        data = model.index((self.tableView_music.selectedIndexes())[1].row(),0).data()
        print(data)
        
        

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
