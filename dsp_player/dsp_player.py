from PyQt5 import QtCore, QtGui, QtWidgets
import pyo
import dsp_player_ui
import subprocess as sp
    
class Dsp_player(dsp_player_ui.Ui_Dsp_player_mainwindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(Dsp_player, self).__init__()
        self.setupUi(self)
        self.button_action_decl()
        self.server_booted()
    
    def button_action_decl(self): 
        self.server_on_toolB.pressed.connect(self.server_on)
        self.server_off_toolB.pressed.connect(self.server_off)    
        self.amp_dial.valueChanged.connect(lambda : self.audio_server.setAmp(self.amp_dial.value() / 100))
        self.pan_diial.valueChanged.connect(lambda : (self.pan_audio.setPan(self.pan_diial.value() / 100))) 
   
        
           
    def audio_pipe_init(self, inp):
        start = inp
        self.parametric_eq_out = self.parametric_eq(start, enable=True)
        self.pan_audio = pyo.Pan(self.parametric_eq_out).out()
                 

    
    def audio_setup(self):
        audio_setup = {}
        audio_setup["PA-ver"] =pyo.pa_get_version()
        audio_setup["PA-ver_info"] =pyo.pa_get_version_text()
    
        list_host_apis = {}
        for line in (((sp.getoutput([sys.executable, "-c", "import pyo ;pyo.pa_list_host_apis()"]).split('Host APIS:'))[1]).split('\n')):
            temp = []
            line = (line.split(':'))
            if line != ['']:
                for item in line[1:]:
                    temp.append(item.split(',')[0])    
                list_host_apis[temp[0]] = {'id': temp[1], 'name': temp[2], 'num_devices': temp[3], 'default_in': temp[4], 'default_out': temp[5]}
                
        audio_setup["host_api"] = list_host_apis
        audio_setup["def_host_api"] =pyo.pa_get_default_host_api()
        in_dev, out_dev =  pyo.pa_get_devices_infos()[0], pyo.pa_get_devices_infos()[1]
        audio_setup["indev"] = in_dev
        audio_setup['outdev'] = out_dev
        audio_setup['def_in'] =out_dev[pyo.pa_get_default_output()]
        audio_setup['def-out'] =in_dev[pyo.pa_get_default_input()]
        
        
    def server_booted(self):
        #try:
            #pass
        self.audio_server = pyo.Server().boot()
        self.server_on()
        self.audio_server.setAmp(0.1)
        self.audio_server
        #except:
            #print("server_booted")
            
    def server_on(self):    
        # try:
        if self.audio_server.start():
            self.label.setText("Server Started ........")
            self.src = pyo.Sine(3000)
            self.audio_pipe_init(self.src)
        #except AttributeError:
            #self.label.setText("No Server is Initilized")
        
    def server_off(self):
        #try:
        if not (self.audio_server.stop()):
            self.label.setText("Server Stoped ........")
            self.close()
        #except AttributeError:
            #self.label.setText("No Server is Initilized")
            
    def trial(self):
        print('trial')
    
    
    
################################################################################
########################  Equlizer functions  ##################################
################################################################################    
    def eq_bar_cont(self, bnd_btn, band, freq, spr, amp):
        bnd_btn.pressed.connect(lambda: print(band.boost,band.freq,band.q, band.type))
        freq.valueChanged.connect(lambda: (band.setFreq(freq.value())))
        spr.valueChanged.connect(lambda: (band.setQ(spr.value())))        
        amp.valueChanged.connect(lambda: (band.setBoost((amp.value() / 10))))  

    def eq_buttons(self):
        self.lp_2.pressed.connect(lambda : (self.eq_1.setType(1)))
        self.lp_3.pressed.connect(lambda : (self.eq_2.setType(1)))
        self.lp_4.pressed.connect(lambda : (self.eq_3.setType(1)))
        self.lp_5.pressed.connect(lambda : (self.eq_4.setType(1)))
        self.lp_6.pressed.connect(lambda : (self.eq_5.setType(1)))
        self.lp_7.pressed.connect(lambda : (self.eq_6.setType(1)))
        self.lp_8.pressed.connect(lambda : (self.eq_7.setType(1)))
        
        self.hp_2.pressed.connect(lambda : (self.eq_1.setType(2)))
        self.hp_3.pressed.connect(lambda : (self.eq_2.setType(2)))
        self.hp_4.pressed.connect(lambda : (self.eq_3.setType(2)))
        self.hp_5.pressed.connect(lambda : (self.eq_4.setType(2)))
        self.hp_6.pressed.connect(lambda : (self.eq_5.setType(2)))
        self.hp_7.pressed.connect(lambda : (self.eq_6.setType(2)))
        self.hp_8.pressed.connect(lambda : (self.eq_7.setType(2)))

        self.pn_2.pressed.connect(lambda : (self.eq_1.setType(0)))
        self.pn_3.pressed.connect(lambda : (self.eq_2.setType(0)))
        self.pn_4.pressed.connect(lambda : (self.eq_3.setType(0)))
        self.pn_5.pressed.connect(lambda : (self.eq_4.setType(0)))
        self.pn_6.pressed.connect(lambda : (self.eq_5.setType(0)))
        self.pn_7.pressed.connect(lambda : (self.eq_6.setType(0)))
        self.pn_8.pressed.connect(lambda : (self.eq_7.setType(0)))
        
    def preset_eq_loader(self):
        self.settings_dict = {"Flat": [ 64, 1, 1,
                                        125, 1, 1, 
                                        200, 1, 1, 
                                        500, 1, 1, 
                                        400, 1, 1, 
                                        4000, 1, 1, 
                                        8000, 1, 1 ]
                               }
                              
        
        data = (self.settings_dict[self.comboBox.currentText()])
        items = [self.frd2, self.spd2, self.amp2,                
                 self.frd3, self.spd3, self.amp3,                 
                 self.frd4, self.spd4, self.amp4, 
                 self.frd5, self.spd5, self.amp5, 
                 self.frd6, self.spd6, self.amp6, 
                 self.frd7, self.spd7, self.amp7 ]
        for i,j in zip(items, data):
            i.setValue(j)
        
    def parametric_eq(self, inp, enable = False):
        if enable:
            self.preset_eq_loader()
            self.comboBox.currentIndexChanged.connect(self.preset_eq_loader)
            
            self.eq_1 = pyo.EQ(inp)
            self.eq_bar_cont(self.bnd1, self.eq_1, self.frd1, self.spd1, self.amp1) 

            self.eq_2 = pyo.EQ(self.eq_1)
            self.eq_bar_cont(self.bnd2, self.eq_2, self.frd2, self.spd2, self.amp2)
            
            self.eq_3 = pyo.EQ(self.eq_2)
            self.eq_bar_cont(self.bnd3, self.eq_3, self.frd3, self.spd3, self.amp3)
            
            self.eq_4 = pyo.EQ(self.eq_3)
            self.eq_bar_cont(self.bnd4, self.eq_4, self.frd4, self.spd4, self.amp4)
            
            self.eq_5 = pyo.EQ(self.eq_4)
            self.eq_bar_cont(self.bnd5, self.eq_5, self.frd5, self.spd5, self.amp5)
            
            self.eq_6 = pyo.EQ(self.eq_5)
            self.eq_bar_cont(self.bnd6, self.eq_6, self.frd6, self.spd6, self.amp6)
            
            self.eq_7 = pyo.EQ(self.eq_6).out()
            self.eq_bar_cont(self.bnd7, self.eq_7, self.frd7, self.spd7, self.amp7)
            self.eq_buttons()
            
            return self.eq_7
        else:            
            return inp
            
  
################################################################################
################################################################################

################################################################################
################################################################################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = Dsp_player()
    main_window.show()
    sys.exit(app.exec_())
