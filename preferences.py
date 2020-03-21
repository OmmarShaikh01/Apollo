from PyQt5 import QtCore, QtGui, QtWidgets
import preferences_ui, file_explorer
import re, time, json
import yodel, pyaudio


class settings_main_window(preferences_ui.Ui_preferences_window, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.read_config()
        self.button_declaration()
        self.initilization_run()
        
    def initilization_run(self):
        self.file_types_list_pop()
    
    def button_declaration(self):       
        self.general_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(0)) 
        self.now_playing_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(1))
        self.layout_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(2))
        self.library_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(3)) 
        self.tags_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(4))
        self.players_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(5))
        self.hotkeys_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(6))
        self.sort_gp_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(7))
        self.file_con_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(8))
        self.tools_btn.pressed.connect(lambda : self.all_tabs_stacked.setCurrentIndex(9))        
        self.apply_button.pressed.connect(self.apply_pressed)
        self.save_button.pressed.connect(self.save_pressed)
        self.file_types_list_pop()
    
    def apply_pressed(self):
        print("apply")
        
    def save_pressed(self):
        print("save")
            
        
### misc functions #############################################################
################################################################################
    
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
        
        
    def trial(self):
        print("TRIAL")
        
        
    def wrapper_second_window(self, cls):# wraps and displays second window
        self.ui = cls()
        return self.ui.show()
    
    
    def file_exp(self):
        """displays the file explorer"""
        self.wrapper_second_window(file_explorer.FileBrowser)
        
        
################################################################################
################################################################################


### general tab functions########################################################
################################################################################
    def application_cox_fun(self):
        pass
        
    def file_types_list_pop(self):
        check_state = [1, 1, 1, 1, 0, 1, 0, 0]
        for ind, value in enumerate(check_state):
            if value == 1:
                check_state[ind] = QtCore.Qt.Checked
            else:
                check_state[ind] = QtCore.Qt.Unchecked
                
        self.checkBox_77.setCheckState(check_state[0]) ## wav
        self.checkBox_72.setCheckState(check_state[1]) ## aiff
        self.checkBox_73.setCheckState(check_state[2]) ## alac
        self.checkBox_74.setCheckState(check_state[3]) ## mp3
        self.checkBox_71.setCheckState(check_state[4]) ## aac
        self.checkBox_75.setCheckState(check_state[5]) ## ogg
        self.checkBox_76.setCheckState(check_state[6]) ## wma
        self.checkBox_78.setCheckState(check_state[7]) ## flac


################################################################################
################################################################################

        
### library tab functions#######################################################
################################################################################
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


################################################################################
################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = settings_main_window()
    main_window.show()
    sys.exit(app.exec_())    