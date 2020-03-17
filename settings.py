from PyQt5 import QtCore, QtGui, QtWidgets
import settings_ui
import re, time, json
import yodel, pyaudio

class settings_main_window(settings_ui.Ui_setting_main_window, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_declaration()
        self.read_config()
        
    def read_config(self):
        with open("config.txt") as config:
            self.config_dict = json.load(config)
        # print(self.config_dict)
    
    def player_pressed(self):
        self.stackedWidget.setCurrentIndex(0)
        
    def library_pressed(self):
        self.stackedWidget.setCurrentIndex(1)
        model = QtGui.QStandardItemModel()
        for item in self.config_dict['file_path']:
            temp_model = QtGui.QStandardItem(item)
            temp_model.setEditable(False)
            model.appendRow(temp_model)
        self.file_path_list.setModel(model)
        
        model = QtGui.QStandardItemModel()
        for item,value in zip(self.config_dict["file_format_selected"].keys(), \
                              self.config_dict["file_format_selected"].values()):
            temp_model = QtGui.QStandardItem(item)
            temp_model.setEditable(False)
            temp_model.setCheckable(True)
            if value == 1:
                check = QtCore.Qt.Checked
            else: check = QtCore.Qt.Unchecked
            temp_model.setCheckState(check)            
            
            model.appendRow(temp_model)
        self.file_ext_list.setModel(model)        
        
        
    def button_declaration(self):
        self.pushButton_player.pressed.connect(self.player_pressed)
        self.pushButton_library.pressed.connect(self.library_pressed)
        
    def trial(self):
        print("trial")





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = settings_main_window()
    main_window.show()
    sys.exit(app.exec_())    