from PyQt5 import QtCore, QtGui, QtWidgets
import re, time, json, os

try:
    from . import preferences_ui
    from . import file_explorer
except:
    import file_explorer
    import preferences_ui


class settings_main_window(preferences_ui.Ui_preferences_window, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.read_config()
        self.button_declaration()
        self.initilization_run()


    def initilization_run(self):
        self.general_tab_functions()
        self.now_palying_tab_functions()

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
        self.general_tab_apply()
        self.now_playing_tab_apply()
        self.close()

    def save_pressed(self):
        self.general_tab_apply()

### misc functions #############################################################
################################################################################

    def read_config(self, flag = ''):
        with open(os.path.split(os.getcwd())[0]+'\\resources\\settings\\config.txt') as config:
            self.config_dict = json.load(config)
        self.general_tab_dict = {"application": {"startup_mode": 2, "bx1": 1, "bx2": 1, "bx3": 1, "bx4": 1},
                                "file_types": {".aac": [1, 34],".aiff": [1, 34],".alac": [1, 34],".mp3": [1, 34],".ogg": [1, 34],".wma": [1, 34],".wav": [1, 34],".flac": [1, 34],},
                                "misc": {10: 1, 11: 1, 12: 1, 13: 1, 71: 1, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1,}}


        self.now_playing_tab_dict ={
            "ply_track_lst": {"ply_cnt": 1,
                              "ply_stp": 1,
                              "ply_now": [0, 1, 0],},
            "shuffle": [0, 0, 1, 0, 0],
            "playback_list": {14: [1, 1], 15: [1, "title"], 16: [1, "title"], 17: [1, 0], 18: [1, 0], 19: [1, 0], 20: [1, 0], 21: [0, 0], "skip_ls": [ 0, 20], "skip_mr": [ 50, 120]}
        }





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


    def trial(self, value = 0):
        print("TRIAL ", value)


    def wrapper_second_window(self, cls):# wraps and displays second window
        self.ui = cls()
        return self.ui.show()


    def file_exp(self):
        """displays the file explorer"""
        self.wrapper_second_window(file_explorer.FileBrowser)


    def check_state(self, state, boxes):
        check_st = state
        for ind, value in enumerate(check_st):
            if value == 1:
                check_st[ind] = QtCore.Qt.Checked
            else:
                check_st[ind] = QtCore.Qt.Unchecked

        for (item,value) in zip(boxes, check_st):
            item.setCheckState(value)


################################################################################
################################################################################


### general tab functions#######################################################
################################################################################

    def general_tab_functions(self):
        ## connection
        self.comboBox_startup_mode.currentIndexChanged.connect(self.application_start_fun)
        self.apply_button_3.pressed.connect(self.select_all)
        self.apply_button_2.pressed.connect(self.select_none)

        ## filling
        self.file_types_list_pop()
        self.comboBox_startup_mode.setCurrentIndex(self.general_tab_dict["application"]["startup_mode"])
        box = [self.checkBoxsplash_screen, self.checkBox_min_totask, self.checkBox_play_str, self.checkBox_chkOnsstr]
        stat = [int (i) for i in self.general_tab_dict["application"].values()][1:]
        self.check_state(stat, box)

        box = [
            self.checkBox_10,
            self.checkBox_11,
            self.checkBox_12,
            self.checkBox_13,
            self.checkBox_71,
            self.checkBox_72,
            self.checkBox_73,
            self.checkBox_74,
            self.checkBox_75,
            self.checkBox_76,
        ]
        state = [int (i) for i in self.general_tab_dict["misc"].values()]
        self.check_state(state, box)

    def application_start_fun(self, value):
        if value == 0:
            self.startup_mode = 0
        if value == 1:
            self.startup_mode = 1
        if value == 2:
            self.startup_mode = 2
        if value == 3:
            self.startup_mode = 3


    def file_types_list_pop(self):
        check_stt = [int(i[0]) for i in (self.general_tab_dict ["file_types"].values())]
        self.num_file_type = ["number of files"]
        self.num_file_type.extend([int(i[1]) for i in (self.general_tab_dict ["file_types"].values())])

        temp_model = QtGui.QStandardItemModel()
        for item in self.num_file_type:
            mdl = QtGui.QStandardItem(str(item))
            mdl.setEditable(False)
            temp_model.appendRow(mdl)

        self.listView_num_each_fl_type.setModel(temp_model)
        box = [self.checkBox_acc, ## aac
              self.checkBox_aiff, ## aiff
              self.checkBox_alac, ## alac
              self.checkBox_flac, ## flac
              self.checkBox_mp3, ## mp3
              self.checkBox_ogg, ## ogg
              self.checkBox_wma, ## wma
              self.checkBox_wav] ## wav
        self.check_state(check_stt, box)
    def select_all(self):
        box = [self.checkBox_acc, ## aac
                   self.checkBox_aiff, ## aiff
                  self.checkBox_alac, ## alac
                  self.checkBox_flac, ## flac
                  self.checkBox_mp3, ## mp3
                  self.checkBox_ogg, ## ogg
                  self.checkBox_wma, ## wma
                  self.checkBox_wav] ## wav
        check_stt = [1, 1, 1, 1, 1, 1, 1, 1]
        self.check_state(check_stt, box)

    def select_none(self):
        box = [self.checkBox_acc, ## aac
                   self.checkBox_aiff, ## aiff
                  self.checkBox_alac, ## alac
                  self.checkBox_flac, ## flac
                  self.checkBox_mp3, ## mp3
                  self.checkBox_ogg, ## ogg
                  self.checkBox_wma, ## wma
                  self.checkBox_wav] ## wav
        check_stt = [0, 0, 0, 0, 0, 0, 0, 0]
        self.check_state(check_stt, box)

    def general_tab_apply(self):
        self.general_tab_dict["application"]["startup_mode"] = int(self.startup_mode)
        self.general_tab_dict["application"]["bx1"] = int(self.checkBox_min_totask.isChecked())
        self.general_tab_dict["application"]["bx2"] = int(self.checkBox_play_str.isChecked())
        self.general_tab_dict["application"]["bx3"] = int(self.checkBox_chkOnsstr.isChecked())

        self.general_tab_dict["file_types"][".aac"] = [int(self.checkBox_acc.isChecked()), self.num_file_type[0]]
        self.general_tab_dict["file_types"][".aiff"] = [int(self.checkBox_aiff.isChecked()), self.num_file_type[1]]
        self.general_tab_dict["file_types"][".alac"] = [int(self.checkBox_alac.isChecked()), self.num_file_type[2]]
        self.general_tab_dict["file_types"][".flac"] = [int(self.checkBox_flac.isChecked()), self.num_file_type[3]]
        self.general_tab_dict["file_types"][".mp3"] = [int(self.checkBox_mp3.isChecked()), self.num_file_type[4]]
        self.general_tab_dict["file_types"][".ogg"] = [int(self.checkBox_ogg.isChecked()), self.num_file_type[5]]
        self.general_tab_dict["file_types"][".wma"] = [int(self.checkBox_wma.isChecked()), self.num_file_type[6]]
        self.general_tab_dict["file_types"][".wav"] = [int(self.checkBox_wav.isChecked()), self.num_file_type[7]]

        self.general_tab_dict["misc"][10] = int(self.checkBox_10.isChecked())
        self.general_tab_dict["misc"][11] = int(self.checkBox_11.isChecked())
        self.general_tab_dict["misc"][12] = int(self.checkBox_12.isChecked())
        self.general_tab_dict["misc"][13] = int(self.checkBox_13.isChecked())
        self.general_tab_dict["misc"][71] = int(self.checkBox_71.isChecked())
        self.general_tab_dict["misc"][72] = int(self.checkBox_72.isChecked())
        self.general_tab_dict["misc"][73] = int(self.checkBox_73.isChecked())
        self.general_tab_dict["misc"][74] = int(self.checkBox_74.isChecked())
        self.general_tab_dict["misc"][75] = int(self.checkBox_75.isChecked())
        self.general_tab_dict["misc"][76] = int(self.checkBox_76.isChecked())


################################################################################
################################################################################


### now palying tab functions ##################################################
################################################################################
    def now_palying_tab_functions(self):
        # collection
        self.comboBox_13.currentIndexChanged.connect(self.comboBox_13_fun)
        self.comboBox_12.currentIndexChanged.connect(self.comboBox_12_fun)
        self.comboBox_2.currentIndexChanged.connect(self.comboBox_2_fun)
        self.pushButton.pressed.connect(self.trial)
        self.pushButton_2.pressed.connect(self.trial)

        # filling
        self.comboBox_13.setCurrentIndex(self.now_playing_tab_dict["ply_track_lst"]["ply_cnt"])
        self.comboBox_12.setCurrentIndex(self.now_playing_tab_dict["ply_track_lst"]["ply_stp"])
        self.radioButton_16.setChecked(self.now_playing_tab_dict["ply_track_lst"]["ply_now"][0])
        self.radioButton_17.setChecked(self.now_playing_tab_dict["ply_track_lst"]["ply_now"][1])
        self.radioButton_18.setChecked(self.now_playing_tab_dict["ply_track_lst"]["ply_now"][2])


        self.radioButton.setChecked(self.now_playing_tab_dict["shuffle"][0])
        self.radioButton_2.setChecked(self.now_playing_tab_dict["shuffle"][1])
        self.radioButton_3.setChecked(self.now_playing_tab_dict["shuffle"][2])
        self.radioButton_4.setChecked(self.now_playing_tab_dict["shuffle"][3])
        self.radioButton_5.setChecked(self.now_playing_tab_dict["shuffle"][4])

        self.comboBox_2.setCurrentIndex(self.now_playing_tab_dict["playback_list"][14][1])
        boxes =[self.checkBox_14,
                self.checkBox_15,
                self.checkBox_16,
                self.checkBox_17,
                self.checkBox_18,
                self.checkBox_19,
                self.checkBox_20,
                self.checkBox_21]
        state = [ i[0] for i in self.now_playing_tab_dict["playback_list"].values()]
        self.check_state(state[0:8], boxes)

        state = [[ str(i[0]) for i in self.now_playing_tab_dict["playback_list"].values()][-2:], [ str(i[1]) for i in self.now_playing_tab_dict["playback_list"].values()]]
        self.lineEdit.setText(state[0][0])
        self.lineEdit_2.setText(state[1][-2])
        self.lineEdit_3.setText(state[0][1])
        self.lineEdit_4.setText(state[1][-1])

    def comboBox_13_fun(self, value):
        self.cmb13 = value
    def comboBox_12_fun(self, value):
        self.cmb12 = value
    def comboBox_2_fun(self, value):
        self.cmb2 = value

    def now_playing_tab_apply(self):

        self.now_playing_tab_dict["ply_track_lst"]["ply_cnt"] = self.cmb13
        self.now_playing_tab_dict["ply_track_lst"]["ply_stp"] = self.cmb12
        self.now_playing_tab_dict["ply_track_lst"]["ply_now"][0] = int(self.radioButton_16.isChecked())
        self.now_playing_tab_dict["ply_track_lst"]["ply_now"][1] = int(self.radioButton_17.isChecked())
        self.now_playing_tab_dict["ply_track_lst"]["ply_now"][2] = int(self.radioButton_18.isChecked())

        self.now_playing_tab_dict["shuffle"][0] = int(self.radioButton.isChecked())
        self.now_playing_tab_dict["shuffle"][1] = int(self.radioButton_2.isChecked())
        self.now_playing_tab_dict["shuffle"][2] = int(self.radioButton_3.isChecked())
        self.now_playing_tab_dict["shuffle"][3] = int(self.radioButton_4.isChecked())
        self.now_playing_tab_dict["shuffle"][4] = int(self.radioButton_5.isChecked())


        temp_dict = {14: [int(self.checkBox_14.isChecked()), self.cmb2],
                     15: [int(self.checkBox_15.isChecked()), "title"],
                     16: [int(self.checkBox_16.isChecked()), "title"],
                     17: [int(self.checkBox_17.isChecked()), 0],
                     18: [int(self.checkBox_18.isChecked()), 0],
                     19: [int(self.checkBox_19.isChecked()), 0],
                     20: [int(self.checkBox_20.isChecked()), 0],
                     21: [int(self.checkBox_21.isChecked()), 0],
                     "skip_ls": [ self.lineEdit.text(), self.lineEdit_2.text()],
                     "skip_mr": [ self.lineEdit_3.text(), self.lineEdit_4.text()]}

        self.now_playing_tab_dict["playback_list"] = temp_dict


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
