from PyQt5 import QtCore, QtGui, QtWidgets
import pyo
import dsp_player_ui
import subprocess as sp
import pyqtgraph as pg
    
class Dsp_player(dsp_player_ui.Ui_Dsp_player_mainwindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(Dsp_player, self).__init__()
        self.setupUi(self)
        self.button_action_decl()
        self.server_booted()
    
    def button_action_decl(self): 
        self.server_on_toolB.pressed.connect(self.server_on)
        self.server_off_toolB.pressed.connect(self.server_off)    
        self.amp_dial.valueChanged.connect(lambda : (self.audio_server.setAmp(self.amp_dial.value() / 100)))

        # Equlizer
        self.EnableB.pressed.connect(lambda: (self.eq_en_dis(True))) # calls Eq player function with Eq enabled
        self.DisableB.pressed.connect(lambda: (self.eq_en_dis(False))) # calls Eq player function with Eq disabled
        self.preset_eq_loader()
        self.eq_buttons()
                
        # Simple panning
        self.span_en.pressed.connect(lambda: (self.panner_en_dis(True, "simp"))) # calls panning simple function with panning enabled
        self.span_dis.pressed.connect(lambda: (self.panner_en_dis(False, "simp"))) # calls panning simple function with panning disabled        
        self.pan_sim_dial_2.valueChanged.connect(lambda: self.pan_out.setPan(self.pan_sim_dial_2.value() / 100))# calls panning simple function to set panning
        self.pan_spread_dial.valueChanged.connect(lambda: self.pan_out.setSpread(self.pan_spread_dial.value() / 100))# calls panning simple function to set spread  
        
        # binaura panning
        self.binaurp_en_3.pressed.connect(lambda: (self.panner_en_dis(True, "binaur"))) # calls panning binaural function with panning enabled
        self.binaurp_dis_3.pressed.connect(lambda: (self.panner_en_dis(False,  "binaur"))) # calls panning binaural function with panning disabled
        self.azimuth_dial_5.valueChanged.connect(lambda: self.pan_out.setAzimuth(self.azimuth_dial_5.value() / 100)) # calls panning biaural function to set azimuth
        self.azimuth_span_2.valueChanged.connect(lambda: self.pan_out.setAzispan(self.azimuth_span_2.value() / 100)) # calls panning biaural function to set azimuth span
        self.elev_dial3_2.valueChanged.connect(lambda: self.pan_out.setElevation(self.elev_dial3_2.value() / 100)) # calls panning biaural function to set elevation
        self.elev_span_d_2.valueChanged.connect(lambda: self.pan_out.setElespan(self.elev_span_d_2.value() / 100)) # calls panning biaural function to set elevation span
        
        
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
        self.audio_server.setAmp(0)

        #except:
            #print("server_booted")
            
    def server_on(self):    
        # try:
        if self.audio_server.start():
            self.label.setText("Server Started ........")
            self.src = pyo.Sine(1500)
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
########################  Panning functions  ###################################
################################################################################
    
        
################################################################################
################################################################################
################################################################################            
    
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
        
        self.settings_dict = {"Flat":
                              {"bands": [ 64, 1, 1,
                                        125, 1, 1, 
                                        200, 1, 1, 
                                        500, 1, 1, 
                                        400, 1, 1, 
                                        4000, 1, 1, 
                                        8000, 1, 1 ],
                                "filters": [0, 0, 2, 0, 2, 0, 1]
                                }
                               }
                              
        
        data_bands = (self.settings_dict[self.comboBox.currentText()]["bands"])
        items = [self.frd2, self.spd2, self.amp2,                
                 self.frd3, self.spd3, self.amp3,                 
                 self.frd4, self.spd4, self.amp4, 
                 self.frd5, self.spd5, self.amp5, 
                 self.frd6, self.spd6, self.amp6, 
                 self.frd7, self.spd7, self.amp7 ]
        for i,j in zip(items, data_bands):
            i.setValue(j)
            
        filters = (self.settings_dict[self.comboBox.currentText()]["filters"])
        items =[
            [self.pn_2, self.pn_3, self.pn_4, self.pn_5, self.pn_6, self.pn_7, self.pn_8],            
            [self.lp_2, self.lp_3, self.lp_4, self.lp_5, self.lp_6, self.lp_7, self.lp_8],
            [self.hp_2, self.hp_3, self.hp_4, self.hp_5, self.hp_6, self.hp_7, self.hp_8]]
            
        for index, filt in enumerate(filters):
            [items[0][index], items[1][index], items[2][index]][filt].setChecked(True)
        
    def parametric_eq(self, inp):
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

            return self.eq_7


########################## Audio pipeline ######################################
################################################################################
        
    def pre_plot_declaration(self):
        self.master_vu_meter_graph.plot()
        self.master_vu_meter_graph.setXRange(0, 2)
        self.master_vu_meter_graph.setYRange(0, 2600)
        xm = [0.5, 1.5]
        xl = [0, 1]
        xr = [1, 2]
        self.bg1 = pg.BarGraphItem(x = xm, x0 = xl, 
                                   x1 = xr, height = (range(2600)),
                                   y0 = [0, 0], width=1, brush=[255, 255, 255])
        self.master_vu_meter_graph.addItem(self.bg1) 
        
        
        self.eq_graph.plot()
        self.eq_graph.setYRange(20, 20000)        
        self.spectrogram_img = pg.ImageItem()
        self.eq_graph.addItem(self.spectrogram_img)
        
        
    def master_peak_plotter(self, *args):
        (l, r) = self.audio_server.getCurrentAmp()
        self.bg1.setOpts(height = [int(l*10000), int(r*10000)])
   
    def equlizer_plotter(self, *args):
        pass
   
    def audio_pipe_init(self, inp):
        self.pre_plot_declaration()
        self.start = inp 
        self.eq_en_dis(False) # goes to patametric EQ
        self.spectrogram = pyo.Spectrum(self.parametric_eq_out, function=self.equlizer_plotter)
        self.spectrogram.view()
        self.panning_in = self.parametric_eq_out # patametric EQ output to panning in
        self.panner_en_dis(True, "binaur")
        self.final_out = self.pan_out
        self.peak_amp = pyo.PeakAmp(self.final_out, function = self.master_peak_plotter)
        self.final_out.out()

    def eq_en_dis(self, val):
        self.enable_eq = val
        if self.enable_eq:
            self.parametric_eq_out = self.parametric_eq(self.start)
        else:
            try:
                self.parametric_eq_out.stop()
            except:
                pass
            self.parametric_eq_out = self.start
   
   
    def panner_en_dis(self, val, pan):
        self.panning_in = self.parametric_eq_out
        if val == True and pan == 'simp':
            self.pan_sim_dial_2.setEnabled(True)
            self.pan_spread_dial.setEnabled(True)
            
            self.azimuth_dial_5.setEnabled(False)
            self.azimuth_span_2.setEnabled(False)
            self.elev_dial3_2.setEnabled(False)
            self.elev_span_d_2.setEnabled(False)
            
            self.pan_out = pyo.Pan(self.panning_in)
        
        if val == False and pan == 'simp':
            try:
                self.pan_out.stop()
            except:
                pass
            self.pan_sim_dial_2.setEnabled(False)
            self.pan_spread_dial.setEnabled(False)            
            self.pan_out = self.panning_in
            
        if val == True and pan == 'binaur':
            self.pan_sim_dial_2.setEnabled(False)
            self.pan_spread_dial.setEnabled(False)
            
            self.azimuth_dial_5.setEnabled(True)
            self.azimuth_span_2.setEnabled(True)
            self.elev_dial3_2.setEnabled(True)
            self.elev_span_d_2.setEnabled(True)             
            self.pan_out = pyo.Binaural(self.panning_in)
        
        if val == False and pan == 'binaur':
            try:
                self.pan_out.stop()
            except:
                pass
            self.azimuth_dial_5.setEnabled(False)
            self.azimuth_span_2.setEnabled(False)
            self.elev_dial3_2.setEnabled(False)
            self.elev_span_d_2.setEnabled(False)         
            self.pan_out = self.panning_in            
        


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