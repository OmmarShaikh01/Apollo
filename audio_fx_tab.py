from ui_init import Main_widget
from utils import *

from PyQt5 import QtGui, QtSql, QtCore, QtWidgets
import pyo, av, io
import subprocess as sp
import pyqtgraph as pg
import numpy as np

import sys, threading, re, logging, queue, json, time, itertools

class QueueReaderThread(threading.Thread):
    """A thread that consumes data from a filehandle and sends the data
    over a Queue.
    """
    
    @timeit
    def __init__(self, channels, rate, path = "E:\\music\\file_example_MP3_700KB.mp3"):
        super(QueueReaderThread, self).__init__()
        self.file_h = av.open(path)
        self.duration = self.file_h.duration
        self.channels = channels
        self.sample_rate = rate
        self.decoder_vars()
        self.daemon = True
        self.queue_init()
        print(f"<{self.name}> Created")
    
    def decoder_vars(self):
        self.bit_depth = 16
        codec_dic = {16: {"codec": "pcm_s16le",
                          "format": "s16",
                          "file": "wav",
                          "data_type": "int16",}}
        
        codec_dic = codec_dic[self.bit_depth]
        self.data_type = codec_dic["data_type"]
        self.io_buffer = io.BytesIO()
        self.out = av.open(self.io_buffer, 'w', codec_dic["file"])
        self.out_stream = self.out.add_stream(codec_dic["codec"])
        
        # resampler object details how we want to change frame information
        self.audio_resampler = av.AudioResampler(
            format = av.AudioFormat(codec_dic["format"]).packed,
            layout = self.channels,
            rate = self.sample_rate
        )
        
        
    @tryit
    def data_extractor(self, frame, flag = None):
        if  flag == None:
            self.queue.put(frame.to_ndarray(), True, 0.1)
        else:
            # clears the buffer for new data entry
            self.io_buffer.seek(0)
            self.io_buffer.truncate()
            self.io_buffer.flush()
      
            frame.pts = None  # pts is presentation time-stamp. Not relevant here
            frame = self.audio_resampler.resample(frame)  # get current working frame and re-sample it for encoding
            for p in self.out_stream.encode(frame):  # encode the re-sampled frame
                self.out.mux(p)
             
            data_buffer = np.frombuffer(self.io_buffer.getbuffer().tobytes(), dtype = self.data_type)            
            data_dic = {}
            for i in range(self.channels):
                data_dic[i] = data_buffer[i::self.channels]
            data = list(data_dic.values())
            self.queue.put(data, True, 0.1)

    
    def queue_init(self):
        try:
            self.queue = queue.Queue(2)
            self.file_gen = self.file_h.decode(audio = 0)
            data = next(self.file_gen)
            with self.queue.mutex:
                self.queue.queue.clear()
            self.queue.put(data.to_ndarray(), True, 0.1)
        except Exception as e:
            print(f"<{self.name}><fseek> {e}")
            
    @timeit  
    def fseek(self, time): # sync calls to stop crashes
        self.stream_state = "FSK"
        self.seek_time = time
    
    def fseeker(self, time):
        try:
            lock = threading.RLock()
            with lock:
                time = int(time*1000000)
                self.file_h.seek(time, any_frame = True)
                self.file_gen = self.file_h.decode(audio = 0)
                data = next(self.file_gen)
                self.queue.queue.clear()
                self.queue.put(data.to_ndarray(), True, 0.1)
        except Exception as e:
            print(f"<{self.name}><fseek> {e}")

    def run(self):
        while True:
            if not hasattr(self, 'stream_state'):
                self.stream_state = "PLAY"
                
            if self.stream_state == "END":
                return None
            
            elif self.stream_state == "LOOP":
                time.sleep(0.2)
                continue
            elif self.stream_state == "FSK":
                self.fseeker(self.seek_time)
                self.stream_state = "PLAY"
                
            elif self.stream_state == "PLAY":
                try:
                    data = next(self.file_gen)
                    self.queue.put(data.to_ndarray(), True, 0.1)
                except StopIteration:
                    self.stream_state = "LOOP"
                except av.EOFError:
                    continue
                except Exception as e:
                    print(f"<{self.name}><run> {e}")
                    continue
            
            elif self.stream_state == "PAUSE":
                time.sleep(0.2)
            elif self.stream_state == "STOP":
                time.sleep(0.2)
            else:
                time.sleep(0.2)

    
    def Pause(self):
        self.stream_state = "PAUSE"
        
    def Stop(self):
        self.fseek(0)
        self.stream_state = "STOP"
    
    def Play(self):
        self.stream_state = "PLAY"
        
    def isPaused(self):
        return self.stream_state == "PAUSE"
    
    def isStop(self):
        self.stream_state == "STOP"
    
    def Kill(self):
        self.stream_state = "END"
        
    def file_format(self):
        return self.file_h.format.name
    
class Decoder:
    """"""
    def __init__(self, server, sr = 48000, chans = 2):
        self.pos = 0
        self.sr = sr
        self.server = server
        self.channels = chans
        self.executionslot = []
        
    @tryit    
    def fopen(self, path):
        self.reader = QueueReaderThread(self.channels, self.sr, path)
        self.duration = int(self.reader.duration / 1000000)
        self.tablesize = (self.sr * 100)
        self.dtable = pyo.DataTable(size = self.tablesize, chnls = self.channels)
        self.pdata = self.tablesize
        self.original_pdata = self.tablesize
            
    @tryit
    def data_to_list(self, data):
        if self.channels == 1:
            data = data[0].tolist()
            return (data,len(data))
        
        if self.channels == 2:
            data = [data[0].tolist(), data[1].tolist()]
            return (data,len(data[0]))
   
    @tryit   
    def table_update(self):
        [i() for i in self.executionslot]
        if not self.reader.queue.empty():
            try:
                data = self.reader.queue.get()
            except Exception as e:
                print(f"<{__name__}> {e}")
        else:
            return None
        
        try:
            if self.pdata <= 0:
                self.pos = 0
                self.pdata = self.original_pdata
            if type(data) != None:
                data,lent = self.data_to_list(data)
                table = pyo.DataTable(lent, self.channels, data)
                self.dtable.copyData(table, destpos = self.pos)
                self.pos += lent
                self.pdata -= lent
        except Exception as e:
            print(f"<{__name__}> {e}")            
        
    @tryit
    def play(self):
        self.reader.start()
        self.table_update()
        self.server.setCallback(self.table_update)
        freq = self.dtable.getRate()
        self.osci = pyo.Osc(table=self.dtable, freq = freq)
        return self.osci
    
        
    def decoder_stopper(self):
        self.server.setCallback(lambda: "")
        self.decoder_stopped = True
    
    def decoder_isStopped(self):
        return self.decoder_stopped
    
    def decoder_restarter(self):
        self.reader.fseek(0)
        self.table_update()
        self.server.setCallback(self.table_update)
        freq = self.dtable.getRate()
        self.osci = pyo.Osc(table=self.dtable, freq=freq)        

    def dec_seek(self, stime):
        self.osci.stop()
        self.reader.fseek(stime)
        self.pdata = self.tablesize
        self.original_pdata = self.tablesize
        self.dtable.reset()
        self.osci.setTable(self.dtable)
        self.osci.play()    
    
    def kill_decoder(self):
        self.reader.Kill()
        self.osci.stop()

class Audio_FX_Tab(Main_widget):

    def __init__(self, *args):
        super(Audio_FX_Tab, self).__init__()
        self.CHUNK = 1024
        self.Gbuffer = int(self.CHUNK /4)
        self.Gsamples = 44100
        self.Gchannels = 2
        
        self.server_startup()
        self.all_frames()
        
       
    def all_frames(self):
        self.master_frame_buttons()
        
        
    def master_frame_buttons(self):
        self.server_state_box.stateChanged.connect(lambda x: self.server_on() if x == 2 else self.server_off())
        self.equilizer_state_box.stateChanged.connect(lambda x: self.equilizer_on())
        self.audiofx_state_box.stateChanged.connect(lambda x: self.audiofx_on())
        self.server_bypass_state_box.stateChanged.connect(lambda x: self.processing_on())
        
        
    def server_startup(self):
        # server bootup
        self.audio_server = pyo.Server(sr = self.Gsamples,
                                       nchnls = self.Gchannels,
                                       buffersize = self.Gbuffer).boot()
        self.audio_server.setAmp(0.001)
        self.master_amp_slider.valueChanged.connect(lambda x: self.audio_server.setAmp(x / 200))
        self.server_on()
        self.master_audio_pipeline()

    def server_on(self):
        # server start processing
        try:
            if self.audio_server.start():
                self.server_debug_lab.setText("Server Started")
        except AttributeError:
            self.server_debug_lab.setText("Not Initilized")
     
     
    def server_off(self):
        # server stop processing
        try:
            if not (self.audio_server.stop()):
                self.server_debug_lab.setText("Server Stoped ")
        except AttributeError:
            self.server_debug_lab.setText("Not Initilized")     
     
     
    def equilizer_on(self):
        self.audio_fx_stack.setCurrentIndex(1)
        self.equilizer_pipe_on()
        self.audiofx_pipe_off()
        self.main_output.setVoice(0)
        self.audio_fx_stack.setEnabled(True)
        
        
    def audiofx_on(self):
        self.audio_fx_stack.setCurrentIndex(0)
        self.audiofx_pipe_on()
        self.equilizer_pipe_off()
        self.main_output.setVoice(1)
        self.audio_fx_stack.setEnabled(True)
        
        
    def processing_on(self):
        self.equilizer_pipe_off()
        self.audiofx_pipe_off()
        self.audio_fx_stack.setEnabled(False)
        self.main_output.setVoice(2)
              
                                
    def audio_server_info(self):
        audio_server_info = {}
        audio_server_info["PA-ver"] =pyo.pa_get_version()
        audio_server_info["PA-ver_info"] =pyo.pa_get_version_text()
    
        list_host_apis = {}
        for line in (((sp.getoutput([sys.executable, "-c", "import pyo ;pyo.pa_list_host_apis()"]).split('Host APIS:'))[1]).split('\n')):
            temp = []
            line = (line.split(':'))
            if line != ['']:
                for item in line[1:]:
                    temp.append(item.split(',')[0])    
                list_host_apis[temp[0]] = {'id': temp[1], 'name': temp[2], 'num_devices': temp[3], 'default_in': temp[4], 'default_out': temp[5]}
                
        audio_server_info["host_api"] = list_host_apis
        audio_server_info["def_host_api"] =pyo.pa_get_default_host_api()
        in_dev, out_dev =  pyo.pa_get_devices_infos()[0], pyo.pa_get_devices_infos()[1]
        audio_server_info["indev"] = in_dev
        audio_server_info['outdev'] = out_dev
        audio_server_info['def_in'] =out_dev[pyo.pa_get_default_output()]
        audio_server_info['def-out'] =in_dev[pyo.pa_get_default_input()]    
        return audio_server_info    
       
    def eq_btn_binder(self, eq_bar, spread_dial, spread_bar, amp_dial, amp_bar, filter_btn):
        try:
            eq_1_list = itertools.cycle([0, 1, 2, 3, 4])   
            spread_dial.valueChanged["int"].connect(lambda x: (eq_bar.setQ(x),
                                                        spread_bar.setValue(x)))
            amp_dial.valueChanged["int"].connect(lambda x: (eq_bar.setMul(x / 100),
                                                     amp_bar.setValue(x)))
            filter_btn.pressed.connect(lambda : self.filter_type(eq_1_list, filter_btn, eq_bar))
        except Exception as e:
            print(e)
        
    def master_audio_pipeline(self):
        
        # path = pyo.SNDS_PATH + "/transparent.aif"
        
        # # stereo playback with a slight shift between the two channels.
        # sf = pyo.SfPlayer(path, loop=True, mul=0.4)        
        
        self.main_input = pyo.InputFader(pyo.Sine(0))
        self.audio_fx_pipe(self.main_input)
        self.equilizer_pipe(self.main_input)
        self.equilizer_pipe_off()
        self.audiofx_pipe_off()

        self.main_output = pyo.Selector([self.eq_processed_stream, self.audiofx_processed_stream, self.main_input], 2)
        self.main_output.out()        
        
    def audiofx_pipe_off(self):
        self.freeverb_filter.stop()
        self.chrous_filter.stop()
        self.clip_filter.stop()
        self.compress.stop()
        self.expand.stop()
        self.simple_pan.stop()
        self.binaural_pan.stop()
        self.gate_filter.stop()
        
    def audiofx_pipe_on(self):        
        self.freeverb_filter.play()
        self.chrous_filter.play()
        self.clip_filter.play()
        self.compress.play()
        self.expand.play()
        self.simple_pan.play()
        self.binaural_pan.play()
        self.gate_filter.play()
    
    def audio_fx_pipe(self, main_input):
        self.audiofx_processed_stream = main_input
        self.gate_filter_init()
        self.panner_init()
        self.comex_init()
        self.clip_filter_init()
        self.chrous_filter_init()
        self.freeverb_filter_init()
        self.audio_fx_setter()
        
    def freeverb_filter_init(self):
        self.freeverb_filter = pyo.Freeverb(self.audiofx_processed_stream)
        self.freeverb_processed_stream = pyo.Selector([self.freeverb_filter, self.audiofx_processed_stream], 0)
        
        self.freeverb_size_dial.valueChanged.connect(lambda x : (self.freeverb_filter.setSize(x/100), self.freeverb_pbar.setValue(x))) # (1 - 100)
        self.freeverb_damp_dial.valueChanged.connect(lambda x : (self.freeverb_filter.setDamp(x/100), self.freeverb_pbar_2.setValue(x))) # (1 - 100)
        self.freeverb_bal_dial.valueChanged.connect(lambda x : (self.freeverb_filter.setBal(x/100), self.freeverb_pbar_3.setValue(x))) # (1 - 100)
        self.freeveerb_amp_dial.valueChanged.connect(lambda x : (self.freeverb_filter.setMul(x/100), self.freeverb_pbar_4.setValue(x))) # (1 - 200)
        
        self.freeverb_bypass.clicked.connect(lambda x : self.freeverb_processed_stream.setVoice(int(x)))
        self.audiofx_processed_stream = self.freeverb_processed_stream        

    def chrous_filter_init(self):
        self.chrous_filter = pyo.Chorus(self.audiofx_processed_stream)
        self.chrous_processed_stream = pyo.Selector([self.chrous_filter, self.audiofx_processed_stream], 0)
        
        self.chrous_depth_dial.valueChanged.connect(lambda x : (self.chrous_filter.setDepth(x/100), self.chrous_pbar.setValue(x))) # (1 - 100)
        self.chrous_feedback_dial.valueChanged.connect(lambda x : (self.chrous_filter.setFeedback(x/100), self.chrous_pbar_2.setValue(x))) # (1 - 100)
        self.chrous_bal_dial.valueChanged.connect(lambda x : (self.chrous_filter.setBal(x/100), self.chrous_pbar_3.setValue(x))) # (1 - 100)
        self.chrous_amp_dial.valueChanged.connect(lambda x : (self.chrous_filter.setMul(x/100), self.chrous_pbar_4.setValue(x))) # (1 - 200)        
        
        self.chrous_bypass.clicked.connect(lambda x : self.chrous_processed_stream.setVoice(int(x)))
        self.audiofx_processed_stream = self.chrous_processed_stream

    def clip_filter_init(self):
        self.clip_filter = pyo.Clip(self.audiofx_processed_stream)
        self.clip_processed_stream = pyo.Selector([self.clip_filter, self.audiofx_processed_stream], 0)
        
        self.clip_min_dial.valueChanged.connect(lambda x : (self.clip_filter.setMin(x/100), self.clip_pbar.setValue(x))) # (-100 - 100)
        self.clip_max_dial.valueChanged.connect(lambda x : (self.clip_filter.setMax(x/100), self.clip_pbar_2.setValue(x))) # (-100 - 100)
        self.clip_amp_dial.valueChanged.connect(lambda x : (self.clip_filter.setMul(x/100), self.clip_pbar_3.setValue(x))) # (1 - 200)          
        
        self.clip_bypass.clicked.connect(lambda x : self.clip_processed_stream.setVoice(int(x)))
        self.audiofx_processed_stream = self.clip_processed_stream

    def comex_init(self):
        self.compress = pyo.Compress(self.audiofx_processed_stream)
        self.expand = pyo.Expand(self.audiofx_processed_stream)
        
        self.expand_upthresh_dial.valueChanged.connect(lambda x: (self.expand.setUpThresh(x), self.expand_pbar.setValue(x))) # (-70 - 30)
        self.expand_downthresh_dial.valueChanged.connect(lambda x: (self.expand.setDownThresh(x), self.expand_pbar_2.setValue(x))) # (-70 - 30)
        self.expand_fall_dial.valueChanged.connect(lambda x: (self.expand.setFallTime(x / 100), self.expand_pbar_3.setValue(x))) # (-70 - 30)
        self.expand_rise_dial.valueChanged.connect(lambda x: (self.expand.setRiseTime(x / 100), self.expand_pbar_4.setValue(x))) # (-70 - 30)
        self.expand_look_dial.valueChanged.connect(lambda x: (self.expand.setLookAhead(x), self.expand_pbar_5.setValue(x)))  # (0 - 25)
        self.expand_ratio_dial.valueChanged.connect(lambda x: (self.expand.setRatio(x / 100), self.expand_pbar_6.setValue(x))) # (1 - 100)
        self.expand_amp_dial.valueChanged.connect(lambda x: (self.expand.setMul(x / 100))) # (1 - 200) 
        
        self.compress_thresh_dial.valueChanged.connect(lambda x: (self.compress.setThresh(x), self.compress_pbar.setValue(x))) # (-70 - 30)
        self.compress_ratio_dial.valueChanged.connect(lambda x: (self.compress.setRatio(x / 100), self.compress_pbar_2.setValue(x)))  # (-70 - 30)
        self.compress_fall_dial.valueChanged.connect(lambda x: (self.compress.setFallTime(x / 100), self.compress_pbar_3.setValue(x))) # (1 - 1000)
        self.compress_rise_dial.valueChanged.connect(lambda x: (self.compress.setRiseTime(x / 100), self.compress_pbar_4.setValue(x))) # (1 - 1000)
        self.compress_look_dial.valueChanged.connect(lambda x: (self.compress.setLookAhead(x), self.compress_pbar_5.setValue(x))) # (0 - 25)
        self.compress_knee_dial.valueChanged.connect(lambda x: (self.compress.setKnee(x / 100), self.compress_pbar_6.setValue(x))) # (1 - 100)
        self.compress_amp_dial.valueChanged.connect(lambda x: (self.compress.setMul(x / 100))) # (1 - 200)      
    
        self.comex_stream = pyo.Selector([self.compress, self.expand], 0)
        self.expand_en.clicked.connect(lambda x : self.comex_stream.setVoice(int(x)))
        self.compress_en.clicked.connect(lambda x : self.comex_stream.setVoice(int(x)))
        
        self.comex_processed_stream = pyo.Selector([self.comex_stream, self.audiofx_processed_stream], 0)                
        self.expand_bypass.clicked.connect(lambda x : self.comex_processed_stream.setVoice(int(x)))
        self.compress_bypass.clicked.connect(lambda x : self.comex_processed_stream.setVoice(int(x)))
        
        self.audiofx_processed_stream = self.comex_processed_stream
                
    def panner_init(self):
        self.simple_pan = pyo.Pan(self.audiofx_processed_stream)
        self.binaural_pan = pyo.Binaural(self.audiofx_processed_stream)
        
        self.binaural_azi_dial.valueChanged.connect(lambda x : (self.binaural_pan.setAzimuth(x), self.binaural_pbar.setValue(x)))
        self.binaural_azispan_dial.valueChanged.connect(lambda x : (self.binaural_pan.setAzispan(x / 100), self.binaural_pbar_2.setValue(x)))
        self.binaural_eleva_dial.valueChanged.connect(lambda x : (self.binaural_pan.setElevation(x), self.binaural_pbar_3.setValue(x)))
        self.binaural_elespan_dial.valueChanged.connect(lambda x : (self.binaural_pan.setElespan(x / 100), self.binaural_pbar_4.setValue(x)))
        
        self.pan_pan_dial.valueChanged.connect(lambda x : (self.simple_pan.setPan(x / 100), self.pan_pbar.setValue(x)))
        self.pan_spread_dial.valueChanged.connect(lambda x : (self.simple_pan.setSpread(x / 100), self.pan_pbar_2.setValue(x)))
        
        self.panning_stream = pyo.Selector([self.simple_pan, self.binaural_pan], 0)
        self.binaural_en.clicked.connect(lambda x : self.panning_stream.setVoice(int(x)))
        self.pan_en.clicked.connect(lambda x : self.panning_stream.setVoice(int(x)))
        
        self.panning_processed_stream = pyo.Selector([self.panning_stream, self.audiofx_processed_stream], 0)                
        self.binaural_bypass.clicked.connect(lambda x : self.panning_processed_stream.setVoice(int(x)))
        self.pan_bypass.clicked.connect(lambda x : self.panning_processed_stream.setVoice(int(x)))
        
        self.audiofx_processed_stream = self.panning_processed_stream         

    def gate_filter_init(self):
        self.gate_filter = pyo.Gate(self.audiofx_processed_stream)
        
        self.gate_falltime_dial.valueChanged.connect(lambda x : (self.gate_filter.setFallTime(x / 100), self.gate_slider_2.setValue(int(x)))) # seconds (0 - 1000)
        self.gate_lookahead_dial.valueChanged.connect(lambda x : (self.gate_filter.setLookAhead(x), self.gate_slider_3.setValue(int(x)))) # ms (0 - 25)
        self.gate_risetime_dial.valueChanged.connect(lambda x : (self.gate_filter.setRiseTime(x / 100), self.gate_slider.setValue(int(x)))) # seconds (0 - 1000)
        self.gate_tresh_dial.valueChanged.connect(lambda x : (self.gate_filter.setThresh(x), self.gate_slider_4.setValue(int(x)))) # decibles (-70 - 30)
        self.gate_amp_slid.valueChanged.connect(lambda x : self.gate_filter.setMul(x / 100)) # seconds (0 - 200)
        
        self.gate_processed_stream = pyo.Selector([self.gate_filter, self.audiofx_processed_stream], 0)
        self.gate_bypass.clicked.connect(lambda x : self.gate_processed_stream.setVoice(int(x)))
        self.audiofx_processed_stream = self.gate_processed_stream

    def equilizer_pipe_off(self):
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

    def equilizer_pipe_on(self):
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

    def equilizer_pipe(self, main_input):

        self.e_1 = pyo.Biquad(main_input, type = 0, freq = 20)
        self.e_2 = pyo.Biquad(main_input, type = 0, freq = 40)
        self.e_3 = pyo.Biquad(main_input, type = 0, freq = 60)
        self.e_4 = pyo.Biquad(main_input, type = 0, freq = 80)
        self.e_5 = pyo.Biquad(main_input, type = 0, freq = 100)
        self.e_6 = pyo.Biquad(main_input, type = 0, freq = 150)
        self.e_7 = pyo.Biquad(main_input, type = 0, freq = 200)
        self.e_8 = pyo.Biquad(main_input, type = 0, freq = 250)
        self.e_9 = pyo.Biquad(main_input, type = 0, freq = 300)
        self.e10 = pyo.Biquad(main_input, type = 0, freq = 350)
        self.e11 = pyo.Biquad(main_input, type = 0, freq = 400)
        self.e12 = pyo.Biquad(main_input, type = 0, freq = 500)
        self.e13 = pyo.Biquad(main_input, type = 0, freq = 630)
        self.e14 = pyo.Biquad(main_input, type = 0, freq = 800)
        self.e15 = pyo.Biquad(main_input, type = 0, freq = 1000)
        self.e16 = pyo.Biquad(main_input, type = 0, freq = 1250)
        self.e17 = pyo.Biquad(main_input, type = 0, freq = 1500)
        self.e18 = pyo.Biquad(main_input, type = 0, freq = 2000)
        self.e19 = pyo.Biquad(main_input, type = 0, freq = 2500)
        self.e20 = pyo.Biquad(main_input, type = 0, freq = 3160)
        self.e21 = pyo.Biquad(main_input, type = 0, freq = 4000)
        self.e22 = pyo.Biquad(main_input, type = 0, freq = 5000)
        self.e23 = pyo.Biquad(main_input, type = 0, freq = 6300)
        self.e24 = pyo.Biquad(main_input, type = 0, freq = 6500)
        self.e25 = pyo.Biquad(main_input, type = 0, freq = 7000)
        self.e26 = pyo.Biquad(main_input, type = 0, freq = 7500)
        self.e27 = pyo.Biquad(main_input, type = 0, freq = 8000)
        self.e28 = pyo.Biquad(main_input, type = 0, freq = 9000)
        self.e29 = pyo.Biquad(main_input, type = 0, freq = 10000)
        self.e30 = pyo.Biquad(main_input, type = 0, freq = 12500)
        self.e31 = pyo.Biquad(main_input, type = 0, freq = 16000)
        self.e32 = pyo.Biquad(main_input, type = 0, freq = 20000)

        self.eq_btn_binder(self.e_1, self.spread_dial,    self.spread_bar,    self.amp_dial,    self.amp_bar,    self.filter_type_btm)
        self.eq_btn_binder(self.e_2, self.spread_dial_2,  self.spread_bar_2,  self.amp_dial_2,  self.amp_bar_2,  self.filter_type_btm_2)
        self.eq_btn_binder(self.e_3, self.spread_dial_3,  self.spread_bar_3,  self.amp_dial_3,  self.amp_bar_3,  self.filter_type_btm_3)
        self.eq_btn_binder(self.e_4, self.spread_dial_4,  self.spread_bar_4,  self.amp_dial_4,  self.amp_bar_4,  self.filter_type_btm_4)
        self.eq_btn_binder(self.e_5, self.spread_dial_5,  self.spread_bar_5,  self.amp_dial_5,  self.amp_bar_5,  self.filter_type_btm_5)
        self.eq_btn_binder(self.e_6, self.spread_dial_6,  self.spread_bar_6,  self.amp_dial_6,  self.amp_bar_6,  self.filter_type_btm_6)
        self.eq_btn_binder(self.e_7, self.spread_dial_7,  self.spread_bar_7,  self.amp_dial_7,  self.amp_bar_7,  self.filter_type_btm_7)
        self.eq_btn_binder(self.e_8, self.spread_dial_8,  self.spread_bar_8,  self.amp_dial_8,  self.amp_bar_8,  self.filter_type_btm_8)
        self.eq_btn_binder(self.e_9, self.spread_dial_9,  self.spread_bar_9,  self.amp_dial_9,  self.amp_bar_9,  self.filter_type_btm_9)
        self.eq_btn_binder(self.e10, self.spread_dial_10, self.spread_bar_10, self.amp_dial_10, self.amp_bar_10, self.filter_type_btm_10)
        self.eq_btn_binder(self.e11, self.spread_dial_11, self.spread_bar_11, self.amp_dial_11, self.amp_bar_11, self.filter_type_btm_11)
        self.eq_btn_binder(self.e12, self.spread_dial_12, self.spread_bar_12, self.amp_dial_12, self.amp_bar_12, self.filter_type_btm_12)
        self.eq_btn_binder(self.e13, self.spread_dial_13, self.spread_bar_13, self.amp_dial_13, self.amp_bar_13, self.filter_type_btm_13)
        self.eq_btn_binder(self.e14, self.spread_dial_14, self.spread_bar_14, self.amp_dial_14, self.amp_bar_14, self.filter_type_btm_14)
        self.eq_btn_binder(self.e15, self.spread_dial_15, self.spread_bar_15, self.amp_dial_15, self.amp_bar_15, self.filter_type_btm_15)
        self.eq_btn_binder(self.e16, self.spread_dial_16, self.spread_bar_16, self.amp_dial_16, self.amp_bar_16, self.filter_type_btm_16)
        self.eq_btn_binder(self.e17, self.spread_dial_17, self.spread_bar_17, self.amp_dial_17, self.amp_bar_17, self.filter_type_btm_17)
        self.eq_btn_binder(self.e18, self.spread_dial_18, self.spread_bar_18, self.amp_dial_18, self.amp_bar_18, self.filter_type_btm_18)
        self.eq_btn_binder(self.e19, self.spread_dial_19, self.spread_bar_19, self.amp_dial_19, self.amp_bar_19, self.filter_type_btm_19)
        self.eq_btn_binder(self.e20, self.spread_dial_20, self.spread_bar_20, self.amp_dial_20, self.amp_bar_20, self.filter_type_btm_20)
        self.eq_btn_binder(self.e21, self.spread_dial_21, self.spread_bar_21, self.amp_dial_21, self.amp_bar_21, self.filter_type_btm_21)
        self.eq_btn_binder(self.e22, self.spread_dial_22, self.spread_bar_22, self.amp_dial_22, self.amp_bar_22, self.filter_type_btm_22)
        self.eq_btn_binder(self.e23, self.spread_dial_23, self.spread_bar_23, self.amp_dial_23, self.amp_bar_23, self.filter_type_btm_23)
        self.eq_btn_binder(self.e24, self.spread_dial_24, self.spread_bar_24, self.amp_dial_24, self.amp_bar_24, self.filter_type_btm_24)
        self.eq_btn_binder(self.e25, self.spread_dial_25, self.spread_bar_25, self.amp_dial_25, self.amp_bar_25, self.filter_type_btm_25)
        self.eq_btn_binder(self.e26, self.spread_dial_26, self.spread_bar_26, self.amp_dial_26, self.amp_bar_26, self.filter_type_btm_26)
        self.eq_btn_binder(self.e27, self.spread_dial_27, self.spread_bar_27, self.amp_dial_27, self.amp_bar_27, self.filter_type_btm_27)
        self.eq_btn_binder(self.e28, self.spread_dial_28, self.spread_bar_28, self.amp_dial_28, self.amp_bar_28, self.filter_type_btm_28)
        self.eq_btn_binder(self.e29, self.spread_dial_29, self.spread_bar_29, self.amp_dial_29, self.amp_bar_29, self.filter_type_btm_29)
        self.eq_btn_binder(self.e30, self.spread_dial_30, self.spread_bar_30, self.amp_dial_30, self.amp_bar_30, self.filter_type_btm_30)
        self.eq_btn_binder(self.e31, self.spread_dial_31, self.spread_bar_31, self.amp_dial_31, self.amp_bar_31, self.filter_type_btm_31)
        self.eq_btn_binder(self.e32, self.spread_dial_32, self.spread_bar_32, self.amp_dial_32, self.amp_bar_32, self.filter_type_btm_32)        

        items = [self.e_1,self.e_2,self.e_3,self.e_4,self.e_5, self.e_6, self.e_7, self.e_8,
                 self.e_9, self.e10, self.e11, self.e12, self.e13, self.e14, self.e15, self.e16,
                 self.e17, self.e18, self.e19, self.e20, self.e21, self.e22, self.e23, self.e24,
                 self.e25, self.e26, self.e27, self.e28, self.e29, self.e30, self.e31, self.e32]  
        temp = []
        while len(items) != 1:
            for i in range(int(len(items) / 2)):
                a1 = items.pop()
                b1 = items.pop()
                temp.append(pyo.Selector([a1, b1], 0.5))
            items = temp
            temp = []        
        
        self.eq_preset_setter()
        self.eq_processed_stream = items[0]        

    def filter_type(self, items, obj, eq_obj):
        
        filters = {'lowpass' :0, 
                   'highpass':1, 
                   'bandpass':2, 
                   'bandstop':3, 
                   'allpass' :4, 
                   }
        # syncing the cycle
        curr = filters[(obj.text()).lower()]
        type_ = next(items)
        while type_ != curr:
            type_ = next(items)
            
        type_ = next(items)
        filter_ = list(filters.keys())[type_]
        print(filter_)
        obj.setText(filter_.title())
        eq_obj.setType(type_)    

    def eq_preset_getter(self):
        self.eq_variables = {}
        items = [self.e_1,self.e_2,self.e_3,self.e_4,self.e_5, self.e_6, self.e_7, self.e_8,
                 self.e_9, self.e10, self.e11, self.e12, self.e13, self.e14, self.e15, self.e16,
                 self.e17, self.e18, self.e19, self.e20, self.e21, self.e22, self.e23, self.e24,
                 self.e25, self.e26, self.e27, self.e28, self.e29, self.e30, self.e31, self.e32]        
        for ind, x in enumerate(items):
            self.eq_variables[ind] = {'q': x.q , 
                                      'freq': x.freq, 
                                      'type': x.type, 
                                      'mul': x.mul}        
    def eq_preset_setter(self):  
        items = [(self.e_1, self.spread_dial,    self.spread_bar,    self.amp_dial,    self.amp_bar,    self.filter_type_btm),
                 (self.e_2, self.spread_dial_2,  self.spread_bar_2,  self.amp_dial_2,  self.amp_bar_2,  self.filter_type_btm_2),
                 (self.e_3, self.spread_dial_3,  self.spread_bar_3,  self.amp_dial_3,  self.amp_bar_3,  self.filter_type_btm_3),
                 (self.e_4, self.spread_dial_4,  self.spread_bar_4,  self.amp_dial_4,  self.amp_bar_4,  self.filter_type_btm_4),
                 (self.e_5, self.spread_dial_5,  self.spread_bar_5,  self.amp_dial_5,  self.amp_bar_5,  self.filter_type_btm_5),
                 (self.e_6, self.spread_dial_6,  self.spread_bar_6,  self.amp_dial_6,  self.amp_bar_6,  self.filter_type_btm_6),
                 (self.e_7, self.spread_dial_7,  self.spread_bar_7,  self.amp_dial_7,  self.amp_bar_7,  self.filter_type_btm_7),
                 (self.e_8, self.spread_dial_8,  self.spread_bar_8,  self.amp_dial_8,  self.amp_bar_8,  self.filter_type_btm_8),
                 (self.e_9, self.spread_dial_9,  self.spread_bar_9,  self.amp_dial_9,  self.amp_bar_9,  self.filter_type_btm_9),
                 (self.e10, self.spread_dial_10, self.spread_bar_10, self.amp_dial_10, self.amp_bar_10, self.filter_type_btm_10),
                 (self.e11, self.spread_dial_11, self.spread_bar_11, self.amp_dial_11, self.amp_bar_11, self.filter_type_btm_11),
                 (self.e12, self.spread_dial_12, self.spread_bar_12, self.amp_dial_12, self.amp_bar_12, self.filter_type_btm_12),
                 (self.e13, self.spread_dial_13, self.spread_bar_13, self.amp_dial_13, self.amp_bar_13, self.filter_type_btm_13),
                 (self.e14, self.spread_dial_14, self.spread_bar_14, self.amp_dial_14, self.amp_bar_14, self.filter_type_btm_14),
                 (self.e15, self.spread_dial_15, self.spread_bar_15, self.amp_dial_15, self.amp_bar_15, self.filter_type_btm_15),
                 (self.e16, self.spread_dial_16, self.spread_bar_16, self.amp_dial_16, self.amp_bar_16, self.filter_type_btm_16),
                 (self.e17, self.spread_dial_17, self.spread_bar_17, self.amp_dial_17, self.amp_bar_17, self.filter_type_btm_17),
                 (self.e18, self.spread_dial_18, self.spread_bar_18, self.amp_dial_18, self.amp_bar_18, self.filter_type_btm_18),
                 (self.e19, self.spread_dial_19, self.spread_bar_19, self.amp_dial_19, self.amp_bar_19, self.filter_type_btm_19),
                 (self.e20, self.spread_dial_20, self.spread_bar_20, self.amp_dial_20, self.amp_bar_20, self.filter_type_btm_20),
                 (self.e21, self.spread_dial_21, self.spread_bar_21, self.amp_dial_21, self.amp_bar_21, self.filter_type_btm_21),
                 (self.e22, self.spread_dial_22, self.spread_bar_22, self.amp_dial_22, self.amp_bar_22, self.filter_type_btm_22),
                 (self.e23, self.spread_dial_23, self.spread_bar_23, self.amp_dial_23, self.amp_bar_23, self.filter_type_btm_23),
                 (self.e24, self.spread_dial_24, self.spread_bar_24, self.amp_dial_24, self.amp_bar_24, self.filter_type_btm_24),
                 (self.e25, self.spread_dial_25, self.spread_bar_25, self.amp_dial_25, self.amp_bar_25, self.filter_type_btm_25),
                 (self.e26, self.spread_dial_26, self.spread_bar_26, self.amp_dial_26, self.amp_bar_26, self.filter_type_btm_26),
                 (self.e27, self.spread_dial_27, self.spread_bar_27, self.amp_dial_27, self.amp_bar_27, self.filter_type_btm_27),
                 (self.e28, self.spread_dial_28, self.spread_bar_28, self.amp_dial_28, self.amp_bar_28, self.filter_type_btm_28),
                 (self.e29, self.spread_dial_29, self.spread_bar_29, self.amp_dial_29, self.amp_bar_29, self.filter_type_btm_29),
                 (self.e30, self.spread_dial_30, self.spread_bar_30, self.amp_dial_30, self.amp_bar_30, self.filter_type_btm_30),
                 (self.e31, self.spread_dial_31, self.spread_bar_31, self.amp_dial_31, self.amp_bar_31, self.filter_type_btm_31),
                 (self.e32, self.spread_dial_32, self.spread_bar_32, self.amp_dial_32, self.amp_bar_32, self.filter_type_btm_32)]
        
        if not hasattr(self, "eq_variables"):
            self.eq_preset_getter()
            
        for ind, x in enumerate(items):
            self.per_bar_setter(self.eq_variables[ind]['q'], 
                                self.eq_variables[ind]['freq'], 
                                self.eq_variables[ind]['type'], 
                                self.eq_variables[ind]['mul'],
                                x)
    
    def per_bar_setter(self, q, freq, type_, mul, objs):
        objs[0].setQ(q)
        objs[0].setFreq(freq)
        objs[0].setType(type_)
        objs[0].setMul(mul)
        objs[1].setValue(q)
        objs[2].setValue(q)
        objs[3].setValue((mul * 100))
        objs[4].setValue((mul * 100))
        
        if type_ == 0:
            filter_ = 'lowpass' 

        if type_ == 1:
            filter_ = 'highpass'

        if type_ == 2:
            filter_ = 'bandpass'

        if type_ == 3:
            filter_ = 'bandstop'

        if type_ == 4:
            filter_ = 'allpass'
            
        objs[5].setText(filter_.title())
        
        
    def audio_fx_getter(self):
        self.audiofx_para = {"freeverb" : {"size": self.freeverb_filter.size,
                                           "damp": self.freeverb_filter.damp,
                                           "bal": self.freeverb_filter.bal,
                                           "mul": self.freeverb_filter.mul,
                                           "bypass" : self.freeverb_processed_stream.voice}, 
              
                             "chrous" : {"depth": self.chrous_filter.depth,
                                         "feedback": self.chrous_filter.feedback,
                                         "bal": self.chrous_filter.bal,
                                         "mul": self.chrous_filter.mul,
                                         "bypass" : self.chrous_processed_stream.voice,}, 
              
                             "clip" : {"min": self.clip_filter.min, 
                                       "max": self.clip_filter.max, 
                                       "mul": self.clip_filter.mul, 
                                       "bypass" : self.clip_processed_stream.voice},
              
                             "comex" : {"comp_thresh": self.compress.thresh,
                                        "comp_ratio": self.compress.ratio,
                                        "comp_risetime": self.compress.risetime,
                                        "comp_falltime": self.compress.falltime,
                                        "comp_lookahead": self.compress.lookahead,
                                        "comp_knee": self.compress.knee,
                                        "comp_mul": self.compress.mul,
                                        "exp_upthresh": self.expand.upthresh,
                                        "exp_downthresh": self.expand.downthresh,
                                        "exp_risetime": self.expand.risetime,
                                        "exp_falltime": self.expand.falltime,
                                        "exp_ratio": self.expand.ratio,
                                        "exp_lookahead": self.expand.lookahead,
                                        "exp_mul": self.expand.mul,
                                        "type" : self.comex_stream.voice,
                                        "bypass" : self.comex_processed_stream.voice,}, 
              
                             "panning" : {"pan" : self.simple_pan.pan,
                                          "apread" : self.simple_pan.spread, 
                                          "azimuth": self.binaural_pan.azimuth,
                                          "azipan": self.binaural_pan.azispan,
                                          "elevation": self.binaural_pan.elevation,
                                          "ele_pan": self.binaural_pan.elespan,
                                          "type" : self.panning_stream.voice,
                                          "bypass" : self.panning_processed_stream.voice,
                                          }, 
                             
                             "gate" : {"thresh": self.gate_filter.thresh,
                                       "risetime": self.gate_filter.risetime,
                                       "falltime": self.gate_filter.falltime,
                                       "lookahead": self.gate_filter.lookahead,
                                       "mul": self.gate_filter.mul,
                                       "bypass" : self.gate_processed_stream.voice,}}
        
    def audio_fx_setter(self):
        
        if not hasattr(self, 'audiofx_para'):
            self.audio_fx_getter()
            
        self.freeverb_size_dial.setValue(int(self.audiofx_para['freeverb']['size'] * 100))
        self.freeverb_damp_dial.setValue(int(self.audiofx_para['freeverb']['damp'] * 100))
        self.freeverb_bal_dial.setValue(int(self.audiofx_para['freeverb']['bal'] * 100))
        self.freeveerb_amp_dial.setValue(int(self.audiofx_para['freeverb']['mul'] * 100))
        self.freeverb_bypass.setChecked(not bool(self.audiofx_para['freeverb']['bypass']))
        
        self.chrous_depth_dial.setValue(int(self.audiofx_para['chrous']['depth'] * 100))
        self.chrous_feedback_dial.setValue(int(self.audiofx_para['chrous']['feedback'] * 100))
        self.chrous_bal_dial.setValue(int(self.audiofx_para['chrous']['bal'] * 100))
        self.chrous_amp_dial.setValue(int(self.audiofx_para['chrous']['mul'] * 100))
        self.chrous_bypass.setChecked(not bool(self.audiofx_para['chrous']['bypass']))
        
        self.clip_min_dial.setValue(int(self.audiofx_para['clip']['min'] * 100))
        self.clip_max_dial.setValue(int(self.audiofx_para['clip']['max'] * 100))
        self.clip_amp_dial.setValue(int(self.audiofx_para['clip']['mul'] * 100))
        self.clip_bypass.setChecked(not bool(self.audiofx_para['clip']['bypass']))
        
        self.expand_upthresh_dial.setValue(int(self.audiofx_para['comex']['exp_upthresh']))
        self.expand_downthresh_dial.setValue(int(self.audiofx_para['comex']['exp_downthresh']))
        self.expand_fall_dial.setValue(int(self.audiofx_para['comex']['exp_falltime'] * 100))
        self.expand_rise_dial.setValue(int(self.audiofx_para['comex']['exp_risetime'] * 100))
        self.expand_look_dial.setValue(int(self.audiofx_para['comex']['exp_lookahead']))
        self.expand_ratio_dial.setValue(int(self.audiofx_para['comex']['exp_ratio'] * 100))
        self.expand_amp_dial.setValue(int(self.audiofx_para['comex']['exp_mul'] * 100))
        
        self.compress_thresh_dial.setValue(int(self.audiofx_para['comex']['comp_thresh']))
        self.compress_ratio_dial.setValue(int(self.audiofx_para['comex']['comp_ratio'] * 100))
        self.compress_fall_dial.setValue(int(self.audiofx_para['comex']['comp_risetime'] * 100))
        self.compress_rise_dial.setValue(int(self.audiofx_para['comex']['comp_falltime'] * 100))
        self.compress_look_dial.setValue(int(self.audiofx_para['comex']['comp_lookahead']))
        self.compress_knee_dial.setValue(int(self.audiofx_para['comex']['comp_knee'] * 100))
        self.compress_amp_dial.setValue(int(self.audiofx_para['comex']['comp_mul'] * 100))
        
        self.expand_en.setChecked(True) if bool(self.audiofx_para['comex']['type']) else self.compress_en.setChecked(True)
        self.expand_bypass.setChecked(False) if bool(self.audiofx_para['comex']['bypass']) else self.expand_bypass.setChecked(True)
        self.compress_bypass.setChecked(False) if bool(self.audiofx_para['comex']['bypass']) else self.compress_bypass.setChecked(True)
        
        self.binaural_azi_dial.setValue(int(self.audiofx_para['panning']['azimuth']))
        self.binaural_azispan_dial.setValue(int(self.audiofx_para['panning']['azipan'] * 100))
        self.binaural_eleva_dial.setValue(int(self.audiofx_para['panning']['elevation']))
        self.binaural_elespan_dial.setValue(int(self.audiofx_para['panning']['ele_pan'] * 100))
        self.pan_pan_dial.setValue(int(self.audiofx_para['panning']['pan'] * 100))
        self.pan_spread_dial.setValue(int(self.audiofx_para['panning']['apread'] * 100))
        
        self.binaural_en.setChecked(True) if bool(self.audiofx_para['panning']['type']) else self.pan_en.setChecked(True)
        self.binaural_bypass.setChecked(False)  if bool(self.audiofx_para['panning']['bypass']) else self.binaural_bypass.setChecked(True)  
        self.pan_bypass.setChecked(False)  if bool(self.audiofx_para['panning']['bypass']) else self.pan_bypass.setChecked(True)
        
        self.gate_falltime_dial.setValue(int(self.audiofx_para['gate']['falltime'] * 100))
        self.gate_lookahead_dial.setValue(int(self.audiofx_para['gate']['lookahead']))
        self.gate_risetime_dial.setValue(int(self.audiofx_para['gate']['risetime'] * 100))
        self.gate_tresh_dial.setValue(int(self.audiofx_para['gate']['thresh']))
        self.gate_amp_slid.setValue(int(self.audiofx_para['gate']['mul'] * 100))
        self.gate_bypass.setChecked(not bool(self.audiofx_para['gate']['bypass']))


        self.freeverb_filter.setSize(self.audiofx_para['freeverb']['size'])
        self.freeverb_filter.setDamp(self.audiofx_para['freeverb']['damp'])
        self.freeverb_filter.setBal(self.audiofx_para['freeverb']['bal'])
        self.freeverb_filter.setMul(self.audiofx_para['freeverb']['mul'])
        self.freeverb_processed_stream.setVoice(self.audiofx_para['freeverb']['bypass'])
        
        self.chrous_filter.setDepth(self.audiofx_para['chrous']['depth'])
        self.chrous_filter.setFeedback(self.audiofx_para['chrous']['feedback'])
        self.chrous_filter.setBal(self.audiofx_para['chrous']['bal'])
        self.chrous_filter.setMul(self.audiofx_para['chrous']['mul'])
        self.chrous_processed_stream.setVoice(self.audiofx_para['chrous']['bypass'])
        
        self.clip_filter.setMin(self.audiofx_para['clip']['min'])
        self.clip_filter.setMax(self.audiofx_para['clip']['max'])
        self.clip_filter.setMul(self.audiofx_para['clip']['mul'])
        self.clip_processed_stream.setVoice(self.audiofx_para['clip']['bypass'])
        
        self.expand.setUpThresh(self.audiofx_para['comex']['exp_upthresh'])
        self.expand.setDownThresh(self.audiofx_para['comex']['exp_downthresh'])
        self.expand.setFallTime(self.audiofx_para['comex']['exp_falltime'])
        self.expand.setRiseTime(self.audiofx_para['comex']['exp_risetime'])
        self.expand.setLookAhead(self.audiofx_para['comex']['exp_lookahead'])
        self.expand.setRatio(self.audiofx_para['comex']['exp_ratio'])
        self.expand.setMul(self.audiofx_para['comex']['exp_mul'])
        
        self.compress.setThresh(self.audiofx_para['comex']['comp_thresh'])
        self.compress.setRatio(self.audiofx_para['comex']['comp_ratio'])
        self.compress.setFallTime(self.audiofx_para['comex']['comp_risetime'])
        self.compress.setRiseTime(self.audiofx_para['comex']['comp_falltime'])
        self.compress.setLookAhead(self.audiofx_para['comex']['comp_lookahead'])
        self.compress.setKnee(self.audiofx_para['comex']['comp_knee'])
        self.compress.setMul(self.audiofx_para['comex']['comp_mul'])
        
        self.comex_stream.setVoice(self.audiofx_para['comex']['type'])
        self.comex_processed_stream.setVoice(self.audiofx_para['comex']['bypass'])
        
        self.binaural_pan.setAzimuth(self.audiofx_para['panning']['azimuth'])
        self.binaural_pan.setAzispan(self.audiofx_para['panning']['azipan'])
        self.binaural_pan.setElevation(self.audiofx_para['panning']['elevation'])
        self.binaural_pan.setElespan(self.audiofx_para['panning']['ele_pan'])
        
        self.simple_pan.setPan(self.audiofx_para['panning']['pan'])
        self.simple_pan.setSpread(self.audiofx_para['panning']['apread'])
        
        self.panning_stream.setVoice(self.audiofx_para['panning']['type'])
        self.panning_processed_stream.setVoice(self.audiofx_para['panning']['bypass'])
        
        self.gate_filter.setFallTime(self.audiofx_para['gate']['falltime'])
        self.gate_filter.setLookAhead(self.audiofx_para['gate']['lookahead'])
        self.gate_filter.setRiseTime(self.audiofx_para['gate']['risetime'])
        self.gate_filter.setThresh(self.audiofx_para['gate']['thresh'])
        self.gate_filter.setMul(self.audiofx_para['gate']['mul'])
        self.gate_processed_stream.setVoice(self.audiofx_para['gate']['bypass'])        
        
    
if __name__ == "__main__":

    class Main_App():
        
        def __init__(self, window):
            self.app = QtWidgets.QApplication(sys.argv)
            self.app.setStyle('Fusion')
            self.main_app = window()
            self.main_app.closeEvent = self.closeEvent
            self.main_app.show()
            sys.exit(self.app.exec_())
    
        def closeEvent(self, event):
            self.main_app.audio_server.stop()
                
    app = Main_App(Audio_FX_Tab)    
