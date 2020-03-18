from PyQt5 import QtCore, QtGui, QtWidgets
import settings_ui, file_explorer
import re, time, json
import yodel, pyaudio


class settings_main_window(settings_ui.Ui_setting_main_window, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_declaration()
        self.read_config()
    
    
    def button_declaration(self):
        self.pushButton_player.pressed.connect(self.player_pressed)
        self.pushButton_library.pressed.connect(self.library_pressed)
        self.apply_btn.pressed.connect(self.apply_pressed)
        self.cancel_btn.pressed.connect(self.cancle)
        self.toolButton_add.pressed.connect(self.file_exp)
        self.toolButton_remove.pressed.connect(self.path_removed)     
        self.toolButton_refresh.pressed.connect(self.path_refresh)
        
    def read_config(self, flag = ''):
        with open("config.txt") as config:
            self.config_dict = json.load(config)
            
    def settings_file_update(self, string, flag = None, owr = False, emp = False, filename = 'config.txt', dire = False):
        if dire == False:
            with open(filename) as json_file:
                data = json.load(json_file)
                if string not in data[flag] and not (owr):
                    data[flag].append(string)
                if string not in data[flag] and (owr):
                    if not emp:
                        data[flag] = string            
                json_file.close()
                
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent =2)
                json_file.close()
        if dire == True:
            with open(filename, 'w') as json_file:
                json.dump(string, json_file, indent =2)
                json_file.close()
    
    def apply_pressed(self):
        self.update_check_box(self.file_ext_list, "file_format_selected")
        print(self.config_dict)
        if len(self.config_dict) != 0:  
            self.settings_file_update(self.config_dict,dire = True)
        
    def player_pressed(self):
        self.stackedWidget.setCurrentIndex(0)
        
    def library_pressed(self):
        self.path_refresh()
        model = QtGui.QStandardItemModel()
        for item,value in zip(self.config_dict["file_format_selected"].keys(), \
                              self.config_dict["file_format_selected"].values()):
            temp_model = QtGui.QStandardItem(item)
            temp_model.setEditable(False)
            temp_model.setCheckable(True)
            if value == 1:
                check = QtCore.Qt.Checked
            else:
                check = QtCore.Qt.Unchecked
            temp_model.setCheckState(check)
            model.appendRow(temp_model)
        self.file_ext_list.setModel(model)
    
    def path_removed(self):
        model_og = self.file_path_list.model()
        index = 0;temp = [];
        while index >= 0:
            qindx = model_og.index(index, 0)
            data = model_og.data(qindx)
            item = model_og.item(index)
            if item == None:
                break
            if item.checkState() != 0:
                temp.append(data)   
            index += 1   
        self.config_dict["file_path"] = temp
        self.settings_file_update(temp, flag="file_path", owr=True)

        self.path_refresh()
        
    def path_refresh(self):
        self.read_config()
        self.stackedWidget.setCurrentIndex(1)
        model = QtGui.QStandardItemModel()
        for item in self.config_dict['file_path']:
            temp_model = QtGui.QStandardItem(item)
            temp_model.setEditable(False)
            temp_model.setCheckable(True)
            check = QtCore.Qt.Checked
            temp_model.setCheckState(check)
            model.appendRow(temp_model)
        self.file_path_list.setModel(model)
         
    def trial(self):
        print("TRIAL")
        
    def wrapper_second_window(self, cls):# wraps and displays second window
        self.ui = cls()
        return self.ui.show()
    
    def file_exp(self):
        """displays the file explorer"""
        self.wrapper_second_window(file_explorer.FileBrowser)
        
    def update_check_box(self, view, dtype = ''):
        model = view.model()
        index = 0; state = []
        while index >= 0:
            item = model.item(index)
            if item == None:
                break
            if item.checkState() == 0:    
                state.append(0)
            else:
                state.append(1)
            index += 1
        for indx, (key,value) in enumerate(self.config_dict[dtype].items()):
            self.config_dict[dtype][key] = state[indx]
        print(self.config_dict)
    def cancle(self):
        self.close() 
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = settings_main_window()
    main_window.show()
    sys.exit(app.exec_())    