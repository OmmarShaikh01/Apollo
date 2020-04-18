from PyQt5 import QtCore, QtGui, QtWidgets
import pyo
import dsp_player_ui
import subprocess as sp
import pyqtgraph as pg
import numpy as np
import time
    
class Dsp_player(dsp_player_ui.Ui_Dsp_player_mainwindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(Dsp_player, self).__init__()
        self.setupUi(self)
        self.button_action_decl()
        self.server_booted()
        self.variable_dec()
        
    def variable_dec(self):
        self.equilizer = {}
        self.allPreset = {}
        
    def button_action_decl(self): 
        self.server_on_toolB.pressed.connect(self.server_on)
        self.server_off_toolB.pressed.connect(self.server_off)    
        self.amp_dial.valueChanged.connect(lambda : (self.audio_server.setAmp(self.amp_dial.value() / 100)))
        
        self.add_all.pressed.connect(lambda:(self.add_preset_all(self.all_combo_pre.text())))
        self.add_eq.pressed.connect(lambda:(self.add_preset_eq(self.eq_combo_pre.text())))
        
        # Gate
        self.gate_amp.valueChanged.connect(lambda : (self.gate_filter_out.setMul(self.gate_amp.value() / 100)))
        self.gate_tresh.valueChanged.connect(lambda : (self.gate_filter_out.setThresh(self.gate_tresh.value() / 10)))
        self.gate_la.valueChanged.connect(lambda : (self.gate_filter_out.setLookAhead(self.gate_la.value() / 100)))
        self.gate_rise.valueChanged.connect(lambda : (self.gate_filter_out.setRiseTime(self.gate_rise.value() / 1000)))
        self.gate_fall.valueChanged.connect(lambda : (self.gate_filter_out.setFallTime(self.gate_fall.value() / 1000)))
        
        self.Gate_en.pressed.connect(lambda: (self.gate_en_dis(True), self.gate_filter_out.play(), self.output_switch_gate.setVoice(1)))
        self.Gate_dis.pressed.connect(lambda: (self.gate_en_dis(False), self.gate_filter_out.stop(), self.output_switch_gate.setVoice(0)))
        
        # Simple panning
        self.span_en.pressed.connect(lambda:
                                     (self.binaurp_dis_3.setChecked(True),
                                      self.pan_out_simp.play(), 
                                      self.panner_en_dis(True, "simp"),
                                      self.output_switch_pan.setVoice(0),
                                      self.panner_bypass.setVoice(1))) # calls panning simple function with panning enabled
        self.span_dis.pressed.connect(lambda:
                                      (self.panner_en_dis(False, "simp"),
                                       self.pan_out_simp.stop(), 
                                       self.panner_bypass_call())) # calls panning simple function with panning disabled        
        self.pan_sim_dial_2.valueChanged.connect(lambda: self.pan_out_simp.setPan(self.pan_sim_dial_2.value() / 100))# calls panning simple function to set panning
        self.pan_spread_dial.valueChanged.connect(lambda: self.pan_out_simp.setSpread(self.pan_spread_dial.value() / 100))# calls panning simple function to set spread  
        
        # binaura panning
        self.binaurp_en_3.pressed.connect(lambda:
                                          (self.span_dis.setChecked(True),
                                           self.pan_out_bin.play(), 
                                           self.panner_en_dis(True, "binaur"),
                                           self.output_switch_pan.setVoice(1),
                                           self.panner_bypass.setVoice(1))) # calls panning binaural function with panning enabled
        self.binaurp_dis_3.pressed.connect(lambda: (self.panner_en_dis(False,  "binaur"), self.pan_out_bin.stop(),self.panner_bypass_call())) # calls panning binaural function with panning disabled
        self.azimuth_dial_5.valueChanged.connect(lambda: self.pan_out_bin.setAzimuth(self.azimuth_dial_5.value() / 100)) # calls panning biaural function to set azimuth
        self.azimuth_span_2.valueChanged.connect(lambda: self.pan_out_bin.setAzispan(self.azimuth_span_2.value() / 100)) # calls panning biaural function to set azimuth span
        self.elev_dial3_2.valueChanged.connect(lambda: self.pan_out_bin.setElevation(self.elev_dial3_2.value() / 100)) # calls panning biaural function to set elevation
        self.elev_span_d_2.valueChanged.connect(lambda: self.pan_out_bin.setElespan(self.elev_span_d_2.value() / 100)) # calls panning biaural function to set elevation span
  
        # Compressor
        
        self.Compress_en.pressed.connect(lambda: (self.com_ex_en_dis(True, "comp"),
                                                  self.output_switch_comex.setVoice(0),
                                                  self.compress_f.play())) 
        self.Compress_dis.pressed.connect(lambda: (self.com_ex_en_dis(False, "comp"), 
                                                   self.compress_f.play(),
                                                   self.comex_bypass_call())) 
        
        self.comp_amp.valueChanged.connect(lambda : (self.compress_f.setMul(self.comp_amp.value() / 100)))
        self.comp_tres.valueChanged.connect(lambda : (self.compress_f.setThresh(self.comp_tres.value() / 10)))
        self.comp_rat.valueChanged.connect(lambda : (self.compress_f.setRatio(self.comp_rat.value() / 100)))
        self.comp_rise.valueChanged.connect(lambda : (self.compress_f.setRiseTime(self.comp_rise.value() / 1000)))        
        self.comp_fa.valueChanged.connect(lambda : (self.compress_f.setFallTime(self.comp_fa.value() / 1000)))        
        self.comp_la.valueChanged.connect(lambda : (self.compress_f.setLookAhead(self.comp_la.value() / 10)))
        self.comp_kn.valueChanged.connect(lambda : (self.compress_f.setKnee(self.comp_kn.value() / 100)))

        # Expand
        self.Expand_en.pressed.connect(lambda: (self.com_ex_en_dis(True, "expd"),
                                                self.output_switch_comex.setVoice(1),
                                                self.expand_f.play())) 
        self.Expand_dis.pressed.connect(lambda: (self.com_ex_en_dis(False, "expd"),
                                                 self.expand_f.play(),
                                                 self.comex_bypass_call()))
        
        self.exp_amp.valueChanged.connect(lambda : (self.expand_f.setMul(self.exp_amp.value() / 100)))
        self.exp_dt.valueChanged.connect(lambda : (self.expand_f.setDownThresh(self.exp_dt.value() / 10)))
        self.exp_ut.valueChanged.connect(lambda : (self.expand_f.setUpThresh(self.exp_ut.value() / 10)))
        self.exp_la.valueChanged.connect(lambda : (self.expand_f.setLookAhead(self.exp_la.value() / 10)))
        self.exp_rat.valueChanged.connect(lambda : (self.expand_f.setRatio(self.exp_rat.value() / 1000)))
        self.exp_ra.valueChanged.connect(lambda : (self.expand_f.setRiseTime(self.exp_ra.value() / 1000)))
        self.exp_fall.valueChanged.connect(lambda : (self.expand_f.setFallTime(self.exp_fall.value() / 1000)))     
        
        # Clip
        self.clip_en.pressed.connect(lambda :
                                     (self.clip_en_dis(True),
                                      self.clip_fil_out.play(), 
                                      self.output_switch_clip.setVoice(1) ))
        
        self.clip_dis.pressed.connect(lambda : (self.clip_en_dis(False), 
                                                self.clip_fil_out.stop(), 
                                                self.output_switch_clip.setVoice(0)))
        self.clip_amp.valueChanged.connect(lambda : (self.clip_fil_out.setMul(self.clip_amp.value()/100)))
        self.clip_max.valueChanged.connect(lambda : (self.clip_fil_out.setMax(self.clip_max.value()/100)))
        self.clip_min.valueChanged.connect(lambda : (self.clip_fil_out.setMin(self.clip_min.value()/100)))
        
        # Chrous
        self.Chrous_en.pressed.connect(lambda : (self.chrous_en_dis(True), 
                                                 self.chor_fil_out.play(), 
                                                 self.output_switch_chor.setVoice(1)))
            
        self.Chrous_dis.pressed.connect(lambda : (self.chrous_en_dis(False),
                                                  self.chor_fil_out.stop(), 
                                                  self.output_switch_chor.setVoice(0)))
        
        self.chor_amp.valueChanged.connect(lambda : (self.chor_fil_out.setMul(self.chor_amp.value() / 100)))
        self.chor_f.valueChanged.connect(lambda : (self.chor_fil_out.setFeedback(self.chor_f.value() / 100)))
        self.chor_d.valueChanged.connect(lambda : (self.chor_fil_out.setDepth(self.chor_d.value() / 100)))
        self.chor_b.valueChanged.connect(lambda : (self.chor_fil_out.setBal(self.chor_b.value() / 100)))              
        
        # Freeverb
        self.FreeVerb_en.pressed.connect(lambda : (self.freeverb_en_dis(True), 
                                                   self.free_fil_out.play(), 
                                                   self.output_switch_free.setVoice(1)))
        self.FreeVerb_dis.pressed.connect(lambda : (self.freeverb_en_dis(False), 
                                                    self.free_fil_out.stop(), 
                                                    self.output_switch_free.setVoice(0)))
        
        self.free_a.valueChanged.connect(lambda : (self.free_fil_out.setMul(self.free_a.value() / 100)))
        self.free_s.valueChanged.connect(lambda : (self.free_fil_out.setSize(self.free_s.value() / 100)))
        self.free_d.valueChanged.connect(lambda : (self.free_fil_out.setDamp(self.free_d.value() / 100)))
        self.free_b.valueChanged.connect(lambda : (self.free_fil_out.setBal(self.free_b.value() / 100)))          

        # Equlizer
        self.EnableB.pressed.connect(lambda: (self.eq_en_dis(True), self.output_switch_eq.setVoice(0), self.eq_start())) # calls Eq player function with Eq enabled
        self.DisableB.pressed.connect(lambda: (self.eq_en_dis(False), self.output_switch_eq.setVoice(1), self.eq_stop())) # calls Eq player function with Eq disabled
          
        # Misc
        self.process.clicked.connect(lambda:(self.output_switch.setVoice(1), self.process_out.play(), self.enable_all()))
        self.bypass.clicked.connect(lambda:(self.output_switch.setVoice(0), self.process_out.stop(),  self.disabler_all()))
        
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
        self.audio_server.setAmp(0.010)
        #except:
            #print("server_booted")
            
    def server_on(self):    
        # try:
        if self.audio_server.start():
            self.label.setText("Server Started ........")
            self.audio_pipe_init()
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
    def eq_button_dec(self): 
        self.eq_sld_m_2.valueChanged.connect(lambda : (self.eq_sld.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_2.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_3.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_4.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_5.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_6.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_7.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_8.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_9.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_10.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_11.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_12.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_13.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_14.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_15.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_16.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_17.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_18.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_19.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_20.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_21.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_22.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_23.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_24.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_25.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_26.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_27.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_28.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_29.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_30.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_31.setValue(self.eq_sld_m_2.value()),
                                                       self.eq_sld_32.setValue(self.eq_sld_m_2.value())))
        
        self.dial_m_eq_2.valueChanged.connect(lambda:(self.dial.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_2.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_3.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_4.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_5.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_6.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_7.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_8.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_9.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_10.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_11.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_12.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_13.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_14.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_15.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_16.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_17.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_18.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_19.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_20.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_21.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_22.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_23.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_24.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_25.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_26.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_27.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_28.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_29.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_30.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_31.setValue(self.dial_m_eq_2.value()),
                                                      self.dial_32.setValue(self.dial_m_eq_2.value())))
        
        self.filter_type_s__1.valueChanged.connect(lambda:(self.filter_type_s__2.setValue(self.filter_type_s__1.value()), 
                                                           self.filter_type_s__3.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s__4.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s__5.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s__6.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s__7.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s__8.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s__9.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_10.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_11.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_12.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_13.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_14.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_15.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_16.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_17.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_18.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_19.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_20.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_21.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_22.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_23.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_24.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_25.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_26.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_27.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_28.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_29.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_30.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_31.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_32.setValue(self.filter_type_s__1.value()),
                                                           self.filter_type_s_33.setValue(self.filter_type_s__1.value())))
        
        self.filter_type_s__2.valueChanged.connect(lambda : self.e_1.setType(self.filter_type_s__2.value())) 
        self.filter_type_s__3.valueChanged.connect(lambda : self.e_2.setType(self.filter_type_s__3.value()))
        self.filter_type_s__4.valueChanged.connect(lambda : self.e_3.setType(self.filter_type_s__4.value()))
        self.filter_type_s__5.valueChanged.connect(lambda : self.e_4.setType(self.filter_type_s__5.value()))
        self.filter_type_s__6.valueChanged.connect(lambda : self.e_5.setType(self.filter_type_s__6.value()))
        self.filter_type_s__7.valueChanged.connect(lambda : self.e_6.setType(self.filter_type_s__7.value()))
        self.filter_type_s__8.valueChanged.connect(lambda : self.e_7.setType(self.filter_type_s__8.value()))
        self.filter_type_s__9.valueChanged.connect(lambda : self.e_8.setType(self.filter_type_s__9.value()))
        self.filter_type_s_10.valueChanged.connect(lambda : self.e_9.setType(self.filter_type_s_10.value()))
        self.filter_type_s_11.valueChanged.connect(lambda : self.e10.setType(self.filter_type_s_11.value()))
        self.filter_type_s_12.valueChanged.connect(lambda : self.e11.setType(self.filter_type_s_12.value()))
        self.filter_type_s_13.valueChanged.connect(lambda : self.e12.setType(self.filter_type_s_13.value()))
        self.filter_type_s_14.valueChanged.connect(lambda : self.e13.setType(self.filter_type_s_14.value()))
        self.filter_type_s_15.valueChanged.connect(lambda : self.e14.setType(self.filter_type_s_15.value()))
        self.filter_type_s_16.valueChanged.connect(lambda : self.e15.setType(self.filter_type_s_16.value()))
        self.filter_type_s_17.valueChanged.connect(lambda : self.e16.setType(self.filter_type_s_17.value()))
        self.filter_type_s_18.valueChanged.connect(lambda : self.e17.setType(self.filter_type_s_18.value()))
        self.filter_type_s_19.valueChanged.connect(lambda : self.e18.setType(self.filter_type_s_19.value()))
        self.filter_type_s_20.valueChanged.connect(lambda : self.e19.setType(self.filter_type_s_20.value()))
        self.filter_type_s_21.valueChanged.connect(lambda : self.e20.setType(self.filter_type_s_21.value()))
        self.filter_type_s_22.valueChanged.connect(lambda : self.e21.setType(self.filter_type_s_22.value()))
        self.filter_type_s_23.valueChanged.connect(lambda : self.e22.setType(self.filter_type_s_23.value()))
        self.filter_type_s_24.valueChanged.connect(lambda : self.e23.setType(self.filter_type_s_24.value()))
        self.filter_type_s_25.valueChanged.connect(lambda : self.e24.setType(self.filter_type_s_25.value()))
        self.filter_type_s_26.valueChanged.connect(lambda : self.e25.setType(self.filter_type_s_26.value()))
        self.filter_type_s_27.valueChanged.connect(lambda : self.e26.setType(self.filter_type_s_27.value()))
        self.filter_type_s_28.valueChanged.connect(lambda : self.e27.setType(self.filter_type_s_28.value()))
        self.filter_type_s_29.valueChanged.connect(lambda : self.e28.setType(self.filter_type_s_29.value()))
        self.filter_type_s_30.valueChanged.connect(lambda : self.e29.setType(self.filter_type_s_30.value()))
        self.filter_type_s_31.valueChanged.connect(lambda : self.e30.setType(self.filter_type_s_31.value()))
        self.filter_type_s_32.valueChanged.connect(lambda : self.e31.setType(self.filter_type_s_32.value()))
        self.filter_type_s_33.valueChanged.connect(lambda : self.e32.setType(self.filter_type_s_33.value()))
        

        self.eq_sld.valueChanged.connect(lambda : (self.e_1.setMul(self.eq_sld.value()/100)))
        self.dial.valueChanged.connect(lambda : (self.e_1.setQ(self.dial.value())))
        
        self.eq_sld_2.valueChanged.connect(lambda : (self.e_2.setMul(self.eq_sld.value()/100)))
        self.dial_2.valueChanged.connect(lambda : (self.e_2.setQ(self.dial_2.value())))
        
        self.eq_sld_3.valueChanged.connect(lambda : (self.e_3.setMul(self.eq_sld.value()/100)))
        self.dial_3.valueChanged.connect(lambda : (self.e_3.setQ(self.dial_3.value())))
        
        self.eq_sld_4.valueChanged.connect(lambda : (self.e_4.setMul(self.eq_sld.value()/100)))
        self.dial_4.valueChanged.connect(lambda : (self.e_4.setQ(self.dial_4.value())))
        
        self.eq_sld_5.valueChanged.connect(lambda : (self.e_5.setMul(self.eq_sld.value()/100)))
        self.dial_5.valueChanged.connect(lambda : (self.e_5.setQ(self.dial_5.value())))
        
        self.eq_sld_6.valueChanged.connect(lambda : (self.e_6.setMul(self.eq_sld.value()/100)))
        self.dial_6.valueChanged.connect(lambda : (self.e_6.setQ(self.dial_6.value())))
        
        self.eq_sld_7.valueChanged.connect(lambda : (self.e_7.setMul(self.eq_sld.value()/100)))
        self.dial_7.valueChanged.connect(lambda : (self.e_7.setQ(self.dial_7.value())))
        
        self.eq_sld_8.valueChanged.connect(lambda : (self.e_8.setMul(self.eq_sld.value()/100)))
        self.dial_8.valueChanged.connect(lambda : (self.e_8.setQ(self.dial_8.value())))
        
        self.eq_sld_9.valueChanged.connect(lambda : (self.e_9.setMul(self.eq_sld.value()/100)))
        self.dial_9.valueChanged.connect(lambda : (self.e_9.setQ(self.dial_9.value())))
        
        self.eq_sld_10.valueChanged.connect(lambda : (self.e10.setMul(self.eq_sld.value()/100)))
        self.dial_10.valueChanged.connect(lambda : (self.e10.setQ(self.dial_10.value())))
        
        self.eq_sld_11.valueChanged.connect(lambda : (self.e11.setMul(self.eq_sld.value()/100)))
        self.dial_11.valueChanged.connect(lambda : (self.e11.setQ(self.dial_11.value())))
        
        self.eq_sld_12.valueChanged.connect(lambda : (self.e12.setMul(self.eq_sld.value()/100)))
        self.dial_12.valueChanged.connect(lambda : (self.e12.setQ(self.dial_12.value())))
        
        self.eq_sld_13.valueChanged.connect(lambda : (self.e13.setMul(self.eq_sld.value()/100)))
        self.dial_13.valueChanged.connect(lambda : (self.e13.setQ(self.dial_13.value())))
        
        self.eq_sld_14.valueChanged.connect(lambda : (self.e14.setMul(self.eq_sld.value()/100)))
        self.dial_14.valueChanged.connect(lambda : (self.e14.setQ(self.dial_14.value())))
        
        self.eq_sld_15.valueChanged.connect(lambda : (self.e15.setMul(self.eq_sld.value()/100)))
        self.dial_15.valueChanged.connect(lambda : (self.e15.setQ(self.dial_15.value())))
        
        self.eq_sld_16.valueChanged.connect(lambda : (self.e16.setMul(self.eq_sld.value()/100)))
        self.dial_16.valueChanged.connect(lambda : (self.e16.setQ(self.dial_16.value())))
        
        self.eq_sld_17.valueChanged.connect(lambda : (self.e17.setMul(self.eq_sld.value()/100)))
        self.dial_17.valueChanged.connect(lambda : (self.e17.setQ(self.dial_17.value())))
        
        self.eq_sld_18.valueChanged.connect(lambda : (self.e18.setMul(self.eq_sld.value()/100)))
        self.dial_18.valueChanged.connect(lambda : (self.e18.setQ(self.dial_18.value())))
        
        self.eq_sld_19.valueChanged.connect(lambda : (self.e19.setMul(self.eq_sld.value()/100)))
        self.dial_19.valueChanged.connect(lambda : (self.e19.setQ(self.dial_19.value())))
        
        self.eq_sld_20.valueChanged.connect(lambda : (self.e20.setMul(self.eq_sld.value()/100)))
        self.dial_20.valueChanged.connect(lambda : (self.e20.setQ(self.dial_20.value())))
        
        self.eq_sld_21.valueChanged.connect(lambda : (self.e21.setMul(self.eq_sld.value()/100)))
        self.dial_21.valueChanged.connect(lambda : (self.e21.setQ(self.dial_21.value())))
        
        self.eq_sld_22.valueChanged.connect(lambda : (self.e22.setMul(self.eq_sld.value()/100)))
        self.dial_22.valueChanged.connect(lambda : (self.e22.setQ(self.dial_22.value())))
        
        self.eq_sld_23.valueChanged.connect(lambda : (self.e23.setMul(self.eq_sld.value()/100)))
        self.dial_23.valueChanged.connect(lambda : (self.e23.setQ(self.dial_23.value())))
        
        self.eq_sld_24.valueChanged.connect(lambda : (self.e24.setMul(self.eq_sld.value()/100)))
        self.dial_24.valueChanged.connect(lambda : (self.e24.setQ(self.dial_24.value())))
        
        self.eq_sld_25.valueChanged.connect(lambda : (self.e25.setMul(self.eq_sld.value()/100)))
        self.dial_25.valueChanged.connect(lambda : (self.e25.setQ(self.dial_25.value())))
        
        self.eq_sld_26.valueChanged.connect(lambda : (self.e26.setMul(self.eq_sld.value()/100)))
        self.dial_26.valueChanged.connect(lambda : (self.e26.setQ(self.dial_26.value())))
        
        self.eq_sld_27.valueChanged.connect(lambda : (self.e27.setMul(self.eq_sld.value()/100)))
        self.dial_27.valueChanged.connect(lambda : (self.e27.setQ(self.dial_27.value())))
        
        self.eq_sld_28.valueChanged.connect(lambda : (self.e28.setMul(self.eq_sld.value()/100)))
        self.dial_28.valueChanged.connect(lambda : (self.e28.setQ(self.dial_28.value())))
        
        self.eq_sld_29.valueChanged.connect(lambda : (self.e29.setMul(self.eq_sld.value()/100)))
        self.dial_29.valueChanged.connect(lambda : (self.e29.setQ(self.dial_29.value())))
        
        self.eq_sld_30.valueChanged.connect(lambda : (self.e30.setMul(self.eq_sld.value()/100)))
        self.dial_30.valueChanged.connect(lambda : (self.e30.setQ(self.dial_30.value())))
        
        self.eq_sld_31.valueChanged.connect(lambda : (self.e31.setMul(self.eq_sld.value()/100)))
        self.dial_31.valueChanged.connect(lambda : (self.e31.setQ(self.dial_31.value())))
        
        self.eq_sld_32.valueChanged.connect(lambda : (self.e32.setMul(self.eq_sld.value()/100)))
        self.dial_32.valueChanged.connect(lambda : (self.e32.setQ(self.dial_32.value())))
    
    def parametric_eq(self, inp):
        osc = inp
        
        self.e_1 = pyo.Biquadx(osc, type = 0, freq = 20)
        self.e_2 = pyo.Biquadx(osc, type = 0, freq = 40)
        self.e_3 = pyo.Biquadx(osc, type = 0, freq = 60)
        self.e_4 = pyo.Biquadx(osc, type = 0, freq = 80)
        self.e_5 = pyo.Biquadx(osc, type = 0, freq = 100)
        self.e_6 = pyo.Biquadx(osc, type = 0, freq = 150)
        self.e_7 = pyo.Biquadx(osc, type = 0, freq = 200)
        self.e_8 = pyo.Biquadx(osc, type = 0, freq = 250)
        self.e_9 = pyo.Biquadx(osc, type = 0, freq = 300)
        self.e10 = pyo.Biquadx(osc, type = 0, freq = 350)
        self.e11 = pyo.Biquadx(osc, type = 0, freq = 400)
        self.e12 = pyo.Biquadx(osc, type = 0, freq = 500)
        self.e13 = pyo.Biquadx(osc, type = 0, freq = 630)
        self.e14 = pyo.Biquadx(osc, type = 0, freq = 800)
        self.e15 = pyo.Biquadx(osc, type = 0, freq = 1000)
        self.e16 = pyo.Biquadx(osc, type = 0, freq = 1250)
        self.e17 = pyo.Biquadx(osc, type = 0, freq = 1500)
        self.e18 = pyo.Biquadx(osc, type = 0, freq = 2000)
        self.e19 = pyo.Biquadx(osc, type = 0, freq = 2500)
        self.e20 = pyo.Biquadx(osc, type = 0, freq = 3160)
        self.e21 = pyo.Biquadx(osc, type = 0, freq = 4000)
        self.e22 = pyo.Biquadx(osc, type = 0, freq = 5000)
        self.e23 = pyo.Biquadx(osc, type = 0, freq = 6300)
        self.e24 = pyo.Biquadx(osc, type = 0, freq = 6500)
        self.e25 = pyo.Biquadx(osc, type = 0, freq = 7000)
        self.e26 = pyo.Biquadx(osc, type = 0, freq = 7500)
        self.e27 = pyo.Biquadx(osc, type = 0, freq = 8000)
        self.e28 = pyo.Biquadx(osc, type = 0, freq = 9000)
        self.e29 = pyo.Biquadx(osc, type = 0, freq = 10000)
        self.e30 = pyo.Biquadx(osc, type = 0, freq = 12500)
        self.e31 = pyo.Biquadx(osc, type = 0, freq = 16000)
        self.e32 = pyo.Biquadx(osc, type = 0, freq = 20000)
        self.eq_button_dec()
        
        
        a = [self.e_1,
             self.e_2,
             self.e_3,
             self.e_4,
             self.e_5,
             self.e_6,
             self.e_7,
             self.e_8,
             self.e_9,
             self.e10,
             self.e11,
             self.e12,
             self.e13,
             self.e14,
             self.e15,
             self.e16,
             self.e17,
             self.e18,
             self.e19,
             self.e20,
             self.e21,
             self.e22,
             self.e23,
             self.e24,
             self.e25,
             self.e26,
             self.e27,
             self.e28,
             self.e29,
             self.e30,
             self.e31,
             self.e32]
        
        temp = []
        while len(a) != 1:
            for i in range(int(len(a) / 2)):
                a1 = a.pop()
                b1 = a.pop()
                temp.append(pyo.Selector([a1, b1], 0.5))
            a = temp
            temp = []        
        
        return a[0]
    
    def eq_stop(self):
        
        self.e_1.stop()
        self.e_2.stop()
        self.e_3.stop()
        self.e_4.stop()
        self.e_5.stop()
        self.e_6.stop()
        self.e_7.stop()
        self.e_8.stop()
        self.e_9.stop()
        self.e10.stop()
        self.e11.stop()
        self.e12.stop()
        self.e13.stop()
        self.e14.stop()
        self.e15.stop()
        self.e16.stop()
        self.e17.stop()
        self.e18.stop()
        self.e19.stop()
        self.e20.stop()
        self.e21.stop()
        self.e22.stop()
        self.e23.stop()
        self.e24.stop()
        self.e25.stop()
        self.e26.stop()
        self.e27.stop()
        self.e28.stop()
        self.e29.stop()
        self.e30.stop()
        self.e31.stop()
        self.e32.stop()
        
        
    def eq_start(self):
        
        self.e_1.play()
        self.e_2.play()
        self.e_3.play()
        self.e_4.play()
        self.e_5.play()
        self.e_6.play()
        self.e_7.play()
        self.e_8.play()
        self.e_9.play()
        self.e10.play()
        self.e11.play()
        self.e12.play()
        self.e13.play()
        self.e14.play()
        self.e15.play()
        self.e16.play()
        self.e17.play()
        self.e18.play()
        self.e19.play()
        self.e20.play()
        self.e21.play()
        self.e22.play()
        self.e23.play()
        self.e24.play()
        self.e25.play()
        self.e26.play()
        self.e27.play()
        self.e28.play()
        self.e29.play()
        self.e30.play()
        self.e31.play()
        self.e32.play()
        
        
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
        
    def master_peak_plotter(self, *args):
        (l, r) = self.audio_server.getCurrentAmp()
        self.bg1.setOpts(height = [int(l*10000), int(r*10000)])
  
    def audio_pipe_init(self):
        self.pre_plot_declaration()
        self.in_table = pyo.SndTable("C:\\Users\\OMMAR\\Desktop\\dsp_player\\ui_forms\\01 Jumpstarter (Original Mix).flac")
        self.src = pyo.Osc(self.in_table, self.in_table.getRate())
        self.process_in = self.src
        
        self.gate_filter_in = self.process_in # self.process_in
        self.gate_filter_out = pyo.Gate(self.gate_filter_in)
        self.gate_filter_out.stop()
        self.output_switch_gate = pyo.Selector([self.process_in, self.gate_filter_out], 0)
        self.filter_input_line = self.output_switch_gate

        self.panning_in = self.filter_input_line
        self.pan_out_bin = pyo.Binaural(self.panning_in)
        self.pan_out_simp = pyo.Pan(self.panning_in)
        self.pan_out_bin.stop()
        self.pan_out_simp.stop()
        self.output_switch_pan = pyo.Selector([self.pan_out_simp, self.pan_out_bin], 0)
        self.panner_bypass = pyo.Selector([self.filter_input_line, self.output_switch_pan], 0)
        self.filter_input_line = self.panner_bypass
        
        self.com_ex_in = self.filter_input_line
        self.compress_f = pyo.Compress(self.com_ex_in)
        self.expand_f = pyo.Expand(self.com_ex_in)
        self.compress_f.stop()
        self.expand_f.stop()
        self.output_switch_comex = pyo.Selector([self.compress_f, self.expand_f], 0)
        self.comex_bypass = pyo.Selector([self.filter_input_line, self.output_switch_comex], 0)
        self.filter_input_line = self.comex_bypass
        
        self.clip_in = self.filter_input_line
        self.clip_fil_out = pyo.Clip(self.clip_in)
        self.clip_fil_out.stop()
        self.output_switch_clip = pyo.Selector([self.filter_input_line, self.clip_fil_out], 0)
        self.filter_input_line = self.output_switch_clip
        
        self.chor_in = self.filter_input_line
        self.chor_fil_out = pyo.Chorus(self.chor_in)
        self.chor_fil_out.stop()
        self.output_switch_chor = pyo.Selector([self.filter_input_line, self.chor_fil_out], 0)
        self.filter_input_line = self.output_switch_chor
        
        self.free_in  = self.filter_input_line
        self.free_fil_out = pyo.Freeverb(self.free_in )
        self.free_fil_out.stop()
        self.output_switch_free = pyo.Selector([self.filter_input_line, self.free_fil_out], 0)
        self.filter_input_line = self.output_switch_free
        
        self.eq_in = self.parametric_eq(self.src)
        self.eq_stop()
        self.eq_bypass = pyo.Selector([self.eq_in, self.src], 0)
        self.output_switch_eq = pyo.Selector([self.eq_bypass, self.filter_input_line], 1)
        self.process_out = self.output_switch_eq

        self.output_switch = pyo.Selector([self.src, self.process_out], 0)
        self.peak_amp = pyo.PeakAmp(self.output_switch, function = self.master_peak_plotter)
        self.output_switch.out()
        self.disabler_all()

    def processs(self):
        self.main_input_line = None

    def gate_en_dis(self, val):
        self.enable_gate = val
        if self.enable_gate:
            self.gate_amp.setEnabled(True)
            self.gate_fall.setEnabled(True)
            self.gate_la.setEnabled(True)
            self.gate_tresh.setEnabled(True)
            self.gate_rise.setEnabled(True)
        else:
            self.gate_amp.setEnabled(False)
            self.gate_fall.setEnabled(False)
            self.gate_la.setEnabled(False)
            self.gate_tresh.setEnabled(False)
            self.gate_rise.setEnabled(False)                
  
    def panner_en_dis(self, val, pan):
        if val == True and pan == 'simp':
            self.pan_sim_dial_2.setEnabled(True)
            self.pan_spread_dial.setEnabled(True)
            self.azimuth_dial_5.setEnabled(False)
            self.azimuth_span_2.setEnabled(False)
            self.elev_dial3_2.setEnabled(False)
            self.elev_span_d_2.setEnabled(False)
            self.binaurp_dis_3.setEnabled(True)
            
        if val == False and pan == 'simp':
            self.pan_sim_dial_2.setEnabled(False)
            self.pan_spread_dial.setEnabled(False)            
            
        if val == True and pan == 'binaur':
            self.pan_sim_dial_2.setEnabled(False)
            self.pan_spread_dial.setEnabled(False)
            self.azimuth_dial_5.setEnabled(True)
            self.azimuth_span_2.setEnabled(True)
            self.elev_dial3_2.setEnabled(True)
            self.elev_span_d_2.setEnabled(True)             
            self.span_dis.setEnabled(True)
            
        if val == False and pan == 'binaur':
            self.azimuth_dial_5.setEnabled(False)
            self.azimuth_span_2.setEnabled(False)
            self.elev_dial3_2.setEnabled(False)
            self.elev_span_d_2.setEnabled(False)  
    
    def eq_en_dis(self, val):
        self.enable_eq = val
        
        if self.enable_eq:
            self.eq_bar_frame.setEnabled(True) 
            self.state = [self.Compress_dis.isChecked(), 
                          self.Gate_dis.isChecked(), 
                          self.span_dis.isChecked(), 
                          self.binaurp_dis_3.isChecked(), 
                          self.Compress_dis.isChecked(), 
                          self.Expand_dis.isChecked(), 
                          self.clip_dis.isChecked(), 
                          self.Chrous_dis.isChecked(), 
                          self.FreeVerb_dis.isChecked()]
            
            self.frame_gate.setEnabled(False)
            self.frame_span.setEnabled(False)
            self.frame_binaur.setEnabled(False)
            self.frame_comp.setEnabled(False)
            self.frame_expa.setEnabled(False)
            self.frame_clip.setEnabled(False)
            self.frame_chrous.setEnabled(False)
            self.frame_free.setEnabled(False)
            
        else:
            self.eq_bar_frame.setEnabled(False)
            try:
                
                self.frame_gate.setEnabled(True)
                self.frame_span.setEnabled(True)
                self.frame_binaur.setEnabled(True)
                self.frame_comp.setEnabled(True)
                self.frame_expa.setEnabled(True)
                self.frame_clip.setEnabled(True)
                self.frame_chrous.setEnabled(True)
                self.frame_free.setEnabled(True)                
                
                [self.Compress_dis.click()  for i in '1' if (bool(self.state[0] ))]
                [self.Gate_dis.click()   for i in '1' if (bool(self.state[1] ))]
                [self.span_dis.click()   for i in '1' if (bool(self.state[2] ))]
                [self.binaurp_dis_3.click()   for i in '1' if (bool(self.state[3] ))]
                [self.Compress_dis.click()   for i in '1' if (bool(self.state[4] ))]
                [self.Expand_dis.click()   for i in '1' if (bool(self.state[5] ))]
                [self.clip_dis.click()   for i in '1' if (bool(self.state[6] ))]
                [self.Chrous_dis.click()   for i in '1' if (bool(self.state[7] ))]
                [self.FreeVerb_dis.click()   for i in '1' if (bool(self.state[8] ))]
                
                [self.Compress_en.click()   for i in '1' if (not(bool(self.state[0] )))]
                [self.Gate_en.click()   for i in '1' if (not(bool(self.state[1] )))]
                [self.span_en.click()   for i in '1' if (not(bool(self.state[2] )))]
                [self.binaurp_en_3.click()   for i in '1' if (not(bool(self.state[3] )))]
                [self.Compress_en.click()   for i in '1' if (not(bool(self.state[4] )))]
                [self.Expand_en.click()   for i in '1' if (not(bool(self.state[5] )))]
                [self.clip_en.click()   for i in '1' if (not(bool(self.state[6] )))]
                [self.Chrous_en.click()   for i in '1' if (not(bool(self.state[7] )))]
                [self.FreeVerb_en.click()   for i in '1' if (not(bool(self.state[8] )))]
            except:
                pass
                
    def com_ex_en_dis(self, val, pan):
        if val == True and pan == 'comp':
            self.comp_amp.setEnabled(True)
            self.comp_fa.setEnabled(True)
            self.comp_kn.setEnabled(True)
            self.comp_la.setEnabled(True)
            self.comp_rat.setEnabled(True)
            self.comp_rise.setEnabled(True)
            self.comp_tres.setEnabled(True)
            self.exp_amp.setEnabled(False)
            self.exp_dt.setEnabled(False)
            self.exp_la.setEnabled(False)
            self.exp_ra.setEnabled(False)
            self.exp_rat.setEnabled(False)
            self.exp_ut.setEnabled(False)
            self.exp_fall.setEnabled(False)
        if val == False and pan == 'comp':
            self.comp_amp.setEnabled(False)
            self.comp_fa.setEnabled(False)
            self.comp_kn.setEnabled(False)
            self.comp_la.setEnabled(False)
            self.comp_rat.setEnabled(False)
            self.comp_rise.setEnabled(False)
            self.comp_tres.setEnabled(False)
        if val == True and pan == 'expd':          
            self.comp_amp.setEnabled(False)
            self.comp_fa.setEnabled(False)
            self.comp_kn.setEnabled(False)
            self.comp_la.setEnabled(False)
            self.comp_rat.setEnabled(False)
            self.comp_rise.setEnabled(False)
            self.comp_tres.setEnabled(False)
            self.exp_amp.setEnabled(True)
            self.exp_dt.setEnabled(True)
            self.exp_la.setEnabled(True)
            self.exp_ra.setEnabled(True)
            self.exp_rat.setEnabled(True)
            self.exp_ut.setEnabled(True)
            self.exp_fall.setEnabled(True)  
        if val == False and pan == 'expd':
            self.exp_amp.setEnabled(False)
            self.exp_dt.setEnabled(False)
            self.exp_la.setEnabled(False)
            self.exp_ra.setEnabled(False)
            self.exp_rat.setEnabled(False)
            self.exp_ut.setEnabled(False)
            self.exp_fall.setEnabled(False)
    def clip_en_dis(self, val):
        self.enable_clip = val
        if self.enable_clip:
            self.clip_amp.setEnabled(True)
            self.clip_max.setEnabled(True)
            self.clip_min.setEnabled(True)
        else:
            self.clip_amp.setEnabled(False)
            self.clip_max.setEnabled(False)
            self.clip_min.setEnabled(False)                
    
    def chrous_en_dis(self, val):
        self.enable_chrous = val
        if self.enable_chrous:
            self.chor_d.setEnabled(True)
            self.chor_b.setEnabled(True)
            self.chor_f.setEnabled(True)
            self.chor_amp.setEnabled(True)
        else:
            self.chor_d.setEnabled(False)
            self.chor_b.setEnabled(False)
            self.chor_f.setEnabled(False)
            self.chor_amp.setEnabled(False)                
    def freeverb_en_dis(self, val):
        self.enable_free = val
        if self.enable_free:
            self.free_a.setEnabled(True)
            self.free_s.setEnabled(True)
            self.free_d.setEnabled(True)
            self.free_b.setEnabled(True)
        else:
            self.free_a.setEnabled(False)
            self.free_s.setEnabled(False)
            self.free_d.setEnabled(False)
            self.free_b.setEnabled(False)  
    



################################################################################
################################# Misc Functions ##############################   
################################################################################
   
    def panner_bypass_call(self): 
        if (self.span_dis.isChecked() or self.binaurp_dis_3.isChecked()):
            self.panner_bypass.setVoice(0)
    
    def disabler_all(self):
        self.state_all = [self.Gate_en.isChecked(), 
                          self.span_en.isChecked(),
                          self.binaurp_en_3.isChecked(), 
                          self.Compress_en.isChecked(),
                          self.Expand_en.isChecked(),
                          self.clip_en.isChecked(),
                          self.Chrous_en.isChecked(), 
                          self.FreeVerb_en.isChecked(),
                          self.EnableB.isChecked()]
        
        self.frame_gate.setEnabled(False)
        self.frame_span.setEnabled(False)
        self.frame_binaur.setEnabled(False)
        self.frame_comp.setEnabled(False)
        self.frame_expa.setEnabled(False)
        self.frame_clip.setEnabled(False)
        self.frame_chrous.setEnabled(False)
        self.frame_free.setEnabled(False)
        self.eq_grid_frame.setEnabled(False)

    def enable_all(self):
        self.frame_gate.setEnabled(True)
        self.frame_span.setEnabled(True)
        self.frame_binaur.setEnabled(True)
        self.frame_comp.setEnabled(True)
        self.frame_expa.setEnabled(True)
        self.frame_clip.setEnabled(True)
        self.frame_chrous.setEnabled(True)
        self.frame_free.setEnabled(True)
        self.eq_grid_frame.setEnabled(True)
        
        [self.Gate_en.click()  for i in '1' if (bool(self.state_all[0]))]
        [self.span_en.click() for i in '1' if (bool(self.state_all[1]))]
        [self.binaurp_en_3.click()  for i in '1' if (bool(self.state_all[2]))]
        [self.Compress_en.click() for i in '1' if (bool(self.state_all[3]))]
        [self.Expand_en.click() for i in '1' if (bool(self.state_all[4]))]
        [self.clip_en.click() for i in '1' if (bool(self.state_all[5]))]
        [self.Chrous_en.click()  for i in '1' if (bool(self.state_all[6]))]
        [self.FreeVerb_en.click() for i in '1' if (bool(self.state_all[7]))]
        
        [self.Gate_dis.click()  for i in '1' if not(bool(self.state_all[0]))]
        [self.span_dis.click() for i in '1' if not(bool(self.state_all[1]))]
        [self.binaurp_dis_3.click()  for i in '1' if not(bool(self.state_all[2]))]
        [self.Compress_dis.click() for i in '1' if not(bool(self.state_all[3]))]
        [self.Expand_dis.click() for i in '1' if not(bool(self.state_all[4]))]
        [self.clip_dis.click() for i in '1' if not(bool(self.state_all[5]))]
        [self.Chrous_dis.click()  for i in '1' if not(bool(self.state_all[6]))]
        [self.FreeVerb_dis.click() for i in '1' if not(bool(self.state_all[7]))]

        [self.DisableB.click() for i in '1' if not(bool(self.state_all[8]))]
        [self.EnableB.click() for i in '1' if (bool(self.state_all[8]))]

    def comex_bypass_call(self): 
        if (self.Compress_dis.isChecked() or self.Expand_dis.isChecked()):
            self.comex_bypass.setVoice(0)
    
    def add_preset_all(self, name):
        if name != '':
                
            self.add_preset_eq(self.eq_combo.currentText())
            self.allPreset[name] = {"gate": [self.Gate_en.isChecked(),
                                             self.Gate_dis.isChecked(),
                                             self.gate_amp.value(),
                                             self.gate_fall.value(),
                                             self.gate_la.value(),
                                             self.gate_tresh.value(),
                                             self.gate_rise.value()],            
                                    
                                    "span": [self.span_en.isChecked(),
                                             self.span_dis.isChecked(),
                                             self.pan_sim_dial_2.value(),
                                             self.pan_spread_dial.value()], 
                                    
                                    'binaur': [self.binaurp_en_3.isChecked(),
                                               self.binaurp_dis_3.isChecked(),
                                               self.azimuth_dial_5.value(),
                                               self.azimuth_span_2.value(),
                                               self.elev_dial3_2.value(),
                                               self.elev_span_d_2.value()],  
                                    
                                    "compress": [self.Compress_en.isChecked(),
                                                 self.Compress_dis.isChecked(),
                                                 self.comp_amp.value(),
                                                 self.comp_fa.value(),
                                                 self.comp_kn.value(),
                                                 self.comp_la.value(),
                                                 self.comp_rat.value(),
                                                 self.comp_rise.value(),
                                                 self.comp_tres.value()],
                                    
                                    "expand": [self.Expand_en.isChecked(),
                                               self.Expand_dis.isChecked(),
                                               self.exp_amp.value(),
                                               self.exp_dt.value(),
                                               self.exp_la.value(),
                                               self.exp_ra.value(),
                                               self.exp_rat.value(),
                                               self.exp_ut.value(),
                                               self.exp_fall.value()], 
                                    
                                    'clip': [self.clip_en.isChecked(),
                                             self.clip_dis.isChecked(),
                                             self.clip_amp.value(),
                                             self.clip_max.value(),
                                             self.clip_min.value()],
                                    
                                    "chrous": [self.Chrous_en.isChecked(),
                                               self.Chrous_dis.isChecked(),
                                               self.chor_d.value(),
                                               self.chor_b.value(),
                                               self.chor_f.value(),
                                               self.chor_amp.value()],
                                    
                                    "freeverb": [self.FreeVerb_en.isChecked(),
                                                 self.FreeVerb_dis.isChecked(),
                                                 self.free_a.value(),
                                                 self.free_s.value(),
                                                 self.free_d.value(),
                                                 self.free_b.value()],
                            
                                    'equilizer': [self.EnableB.isChecked(),
                                                  self.DisableB.isChecked(),
                                                  {self.eq_combo.currentText(): self.equilizer[self.eq_combo.currentText()]}]}
            for i in range(self.eq_combo.count()):
                if self.eq_combo.itemText(i) != name:
                    self.eq_combo.addItem(name)
            self.all_combo_pre.clear()
            
    def add_preset_eq(self, name):
        if name != '':
            self.equilizer[name] = {"slider_values_eq" : [self.eq_sld.value(), 
                                                    self.eq_sld_2.value(),
                                                    self.eq_sld_3.value(),
                                                    self.eq_sld_4.value(),
                                                    self.eq_sld_5.value(),
                                                    self.eq_sld_6.value(),
                                                    self.eq_sld_7.value(),
                                                    self.eq_sld_8.value(),
                                                    self.eq_sld_9.value(),
                                                    self.eq_sld_10.value(),
                                                    self.eq_sld_11.value(),
                                                    self.eq_sld_12.value(),
                                                    self.eq_sld_13.value(),
                                                    self.eq_sld_14.value(),
                                                    self.eq_sld_15.value(),
                                                    self.eq_sld_16.value(),
                                                    self.eq_sld_17.value(),
                                                    self.eq_sld_18.value(),
                                                    self.eq_sld_19.value(),
                                                    self.eq_sld_20.value(),
                                                    self.eq_sld_21.value(),
                                                    self.eq_sld_22.value(),
                                                    self.eq_sld_23.value(),
                                                    self.eq_sld_24.value(),
                                                    self.eq_sld_25.value(),
                                                    self.eq_sld_26.value(),
                                                    self.eq_sld_27.value(),
                                                    self.eq_sld_28.value(),
                                                    self.eq_sld_29.value(),
                                                    self.eq_sld_30.value(),
                                                    self.eq_sld_31.value(),
                                                    self.eq_sld_32.value()], 
      
            
                              "dial_values_eq" : [self.dial.value(),
                                                  self.dial_2.value(),
                                                  self.dial_3.value(),
                                                  self.dial_4.value(),
                                                  self.dial_5.value(),
                                                  self.dial_6.value(),
                                                  self.dial_7.value(),
                                                  self.dial_8.value(),
                                                  self.dial_9.value(),
                                                  self.dial_10.value(),
                                                  self.dial_11.value(),
                                                  self.dial_12.value(),
                                                  self.dial_13.value(),
                                                  self.dial_14.value(),
                                                  self.dial_15.value(),
                                                  self.dial_16.value(),
                                                  self.dial_17.value(),
                                                  self.dial_18.value(),
                                                  self.dial_19.value(),
                                                  self.dial_20.value(),
                                                  self.dial_21.value(),
                                                  self.dial_22.value(),
                                                  self.dial_23.value(),
                                                  self.dial_24.value(),
                                                  self.dial_25.value(),
                                                  self.dial_26.value(),
                                                  self.dial_27.value(),
                                                  self.dial_28.value(),
                                                  self.dial_29.value(),
                                                  self.dial_30.value(),
                                                  self.dial_31.value(),
                                                  self.dial_32.value()], 
                              
                              
                              "filter_values_eq" : [self.filter_type_s__2.value(),
                                                  self.filter_type_s__3.value(),
                                                  self.filter_type_s__4.value(),
                                                  self.filter_type_s__5.value(),
                                                  self.filter_type_s__6.value(),
                                                  self.filter_type_s__7.value(),
                                                  self.filter_type_s__8.value(),
                                                  self.filter_type_s__9.value(),
                                                  self.filter_type_s_10.value(),
                                                  self.filter_type_s_11.value(),
                                                  self.filter_type_s_12.value(),
                                                  self.filter_type_s_13.value(),
                                                  self.filter_type_s_14.value(),
                                                  self.filter_type_s_15.value(),
                                                  self.filter_type_s_16.value(),
                                                  self.filter_type_s_17.value(),
                                                  self.filter_type_s_18.value(),
                                                  self.filter_type_s_19.value(),
                                                  self.filter_type_s_20.value(),
                                                  self.filter_type_s_21.value(),
                                                  self.filter_type_s_22.value(),
                                                  self.filter_type_s_23.value(),
                                                  self.filter_type_s_24.value(),
                                                  self.filter_type_s_25.value(),
                                                  self.filter_type_s_26.value(),
                                                  self.filter_type_s_27.value(),
                                                  self.filter_type_s_28.value(),
                                                  self.filter_type_s_29.value(),
                                                  self.filter_type_s_30.value(),
                                                  self.filter_type_s_31.value(),
                                                  self.filter_type_s_32.value(),
                                                  self.filter_type_s_33.value()]}
        
            self.eq_combo_pre.clear()
            for i in range(self.all_p_combo.count()):
                if self.all_p_combo.itemText(i) != name:
                    self.all_p_combo.addItem(name)
    
    def set_preset_all(self):
        self.set_preset_eq('')
        
        self.gate_amp.setValue()
        self.gate_fall.setValue()
        self.gate_la.setValue()
        self.gate_tresh.setValue()
        self.gate_rise.setValue()            
        
        self.pan_sim_dial_2.setValue()
        self.pan_spread_dial.setValue()
        
        self.azimuth_dial_5.setValue()
        self.azimuth_span_2.setValue()
        self.elev_dial3_2.setValue()
        self.elev_span_d_2.setValue()  
        
        self.frame_gate.setValue()
        self.frame_span.setValue()
        self.frame_binaur.setValue()
        self.frame_comp.setValue()
        self.frame_expa.setValue()
        self.frame_clip.setValue()
        self.frame_chrous.setValue()
        self.frame_free.setValue()
        
        self.comp_amp.setValue()
        self.comp_fa.setValue()
        self.comp_kn.setValue()
        self.comp_la.setValue()
        self.comp_rat.setValue()
        self.comp_rise.setValue()
        self.comp_tres.setValue()
        
        self.exp_amp.setValue()
        self.exp_dt.setValue()
        self.exp_la.setValue()
        self.exp_ra.setValue()
        self.exp_rat.setValue()
        self.exp_ut.setValue()
        self.exp_fall.setValue()  
        
        self.clip_amp.setValue()
        self.clip_max.setValue()
        self.clip_min.setValue()
        
        self.chor_d.setValue()
        self.chor_b.setValue()
        self.chor_f.setValue()
        self.chor_amp.setValue()
        
        self.free_a.setValue()
        self.free_s.setValue()
        self.free_d.setValue()
        self.free_b.setValue()

        self.Gate_dis.setValue()
        self.span_dis.setValue()
        self.binaurp_dis_3.setValue()
        self.Compress_dis.setValue()
        self.Expand_dis.setValue()
        self.clip_dis.setValue()
        self.Chrous_dis.setValue()
        self.FreeVerb_dis.setValue()       
        

        self.Gate_en.setValue()
        self.span_en.setValue()
        self.binaurp_en_3.setValue()
        self.Compress_en.setValue()
        self.Expand_en.setValue()
        self.clip_en.setValue()
        self.Chrous_en.setValue()
        self.FreeVerb_en.setValue()
        
        self.EnableB.setValue()
        self.DisableB.setValue()
        
        
    
    def set_preset_eq(self, val):
        self.eq_sld.setValue()
        self.eq_sld_2.setValue()
        self.eq_sld_3.setValue()
        self.eq_sld_4.setValue()
        self.eq_sld_5.setValue()
        self.eq_sld_6.setValue()
        self.eq_sld_7.setValue()
        self.eq_sld_8.setValue()
        self.eq_sld_9.setValue()
        self.eq_sld_10.setValue()
        self.eq_sld_11.setValue()
        self.eq_sld_12.setValue()
        self.eq_sld_13.setValue()
        self.eq_sld_14.setValue()
        self.eq_sld_15.setValue()
        self.eq_sld_16.setValue()
        self.eq_sld_17.setValue()
        self.eq_sld_18.setValue()
        self.eq_sld_19.setValue()
        self.eq_sld_20.setValue()
        self.eq_sld_21.setValue()
        self.eq_sld_22.setValue()
        self.eq_sld_23.setValue()
        self.eq_sld_24.setValue()
        self.eq_sld_25.setValue()
        self.eq_sld_26.setValue()
        self.eq_sld_27.setValue()
        self.eq_sld_28.setValue()
        self.eq_sld_29.setValue()
        self.eq_sld_30.setValue()
        self.eq_sld_31.setValue()
        self.eq_sld_32.setValue()
        
        
        self.dial.setValue()
        self.dial_2.setValue()
        self.dial_3.setValue()
        self.dial_4.setValue()
        self.dial_5.setValue()
        self.dial_6.setValue()
        self.dial_7.setValue()
        self.dial_8.setValue()
        self.dial_9.setValue()
        self.dial_10.setValue()
        self.dial_11.setValue()
        self.dial_12.setValue()
        self.dial_13.setValue()
        self.dial_14.setValue()
        self.dial_15.setValue()
        self.dial_16.setValue()
        self.dial_17.setValue()
        self.dial_18.setValue()
        self.dial_19.setValue()
        self.dial_20.setValue()
        self.dial_21.setValue()
        self.dial_22.setValue()
        self.dial_23.setValue()
        self.dial_24.setValue()
        self.dial_25.setValue()
        self.dial_26.setValue()
        self.dial_27.setValue()
        self.dial_28.setValue()
        self.dial_29.setValue()
        self.dial_30.setValue()
        self.dial_31.setValue()
        self.dial_32.setValue()
        
        
        self.filter_type_s__2.setValue()
        self.filter_type_s__3.setValue()
        self.filter_type_s__4.setValue()
        self.filter_type_s__5.setValue()
        self.filter_type_s__6.setValue()
        self.filter_type_s__7.setValue()
        self.filter_type_s__8.setValue()
        self.filter_type_s__9.setValue()
        self.filter_type_s_10.setValue()
        self.filter_type_s_11.setValue()
        self.filter_type_s_12.setValue()
        self.filter_type_s_13.setValue()
        self.filter_type_s_14.setValue()
        self.filter_type_s_15.setValue()
        self.filter_type_s_16.setValue()
        self.filter_type_s_17.setValue()
        self.filter_type_s_18.setValue()
        self.filter_type_s_19.setValue()
        self.filter_type_s_20.setValue()
        self.filter_type_s_21.setValue()
        self.filter_type_s_22.setValue()
        self.filter_type_s_23.setValue()
        self.filter_type_s_24.setValue()
        self.filter_type_s_25.setValue()
        self.filter_type_s_26.setValue()
        self.filter_type_s_27.setValue()
        self.filter_type_s_28.setValue()
        self.filter_type_s_29.setValue()
        self.filter_type_s_30.setValue()
        self.filter_type_s_31.setValue()
        self.filter_type_s_32.setValue()
        self.filter_type_s_33.setValue()

################################################################################
################################################################################ 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = Dsp_player()
    main_window.show()
    sys.exit(app.exec_())