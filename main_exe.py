from audio_fx_tab import Decoder
from main_tab_exe import Binding_Tab
import utils

from PyQt5 import QtWidgets
import pyo

import sys, threading, time

class Bindings(Binding_Tab):
    """"""

    def __init__(self):
        """Constructor"""
        super(Bindings, self).__init__()       
        self.button_binder()        
        self.audio_state = None
        
    def button_binder(self): 
        self.play_button.pressed.connect(lambda: self.play_track())
        self.stop_button.pressed.connect(lambda: self.stop_track())
        self.pause_button.pressed.connect(lambda: self.pause_track())
        self.next_button.pressed.connect(lambda: self.next_track())
        self.prev_button.pressed.connect(lambda: self.prev_track())
        self.seek_back_button.pressed.connect(lambda: self.seekf_track())
        self.seek_fowd_button.pressed.connect(lambda: self.seekf_track())
        
        
    def label_pixmap_seeker(self, event):
        lenth = (self.seek_pixmap.rect().width())
        data = round(((event.x() / lenth)*self.track_duration), 2)
    
    def Servercallback_stack(self):
        self.current_track_time()
        self.time_updater()
        self.stopper()
        self.label_style()
        
    def label_style(self):
        self.track_currpos
        
    def stopper(self):
        if self.track_currpos == 1:
            self.dec.decoder_stopper()
            self.main_output.stop()
            self.next_button.click()
            
    def  time_updater(self):
        self.track_currpos = round((self.current_time) / self.track_duration, 2)
   
    def current_track_time(self):
        self.current_time = self.file_timer(flag = "A")
        
    def decoder_init(self):
        pos, self.path = self.audio_queue.current()
        if  self.path == "EOF":
            return None
        
        if hasattr(self, "dec"):
            self.dec.kill_decoder()
            self.main_input.setInput(pyo.Sine(0))
            del self.dec, self.current_time, self.mod
            
        self.dec = Decoder(self.audio_server)
        self.dec.fopen(self.path)
        self.track_duration = self.dec.duration
        osc = self.dec.play()
        self.main_output.out()
        self.start_time = time.monotonic()
        # modifies the attribute of mouse press event inside the label and adds costom function
        self.seek_pixmap.mousePressEvent = self.label_pixmap_seeker
        self.dec.executionslot = [self.Servercallback_stack]        
        
        if osc != None:
            self.main_input.setInput(osc,0.5)
        else:
            pass
        self.audio_state = "INIT"
        
    def play_track(self):
        if self.audio_state != "INIT":
            self.decoder_init()
        else:
            self.dec.reader.Play()
            self.main_output.out()
            
    def pause_track(self):
        self.main_output.stop()
        self.dec.reader.Pause()
    
    def stop_track(self):
        self.main_output.stop()
        self.dec.reader.Stop()
        
    def next_track(self):
        _, data = self.audio_queue._next()
        if data != "EOF":
            self.decoder_init()
        
    def prev_track(self):
        _, data = self.audio_queue.prev()
        if data != "EOF":
            self.decoder_init()
     
    def file_timer(self, mod = 0, flag = None):
        if not hasattr(self, "start_time"):
            self.start_time = time.monotonic()
        if not hasattr(self, "current_time"):     
                self.current_time = (time.monotonic() - self.start_time)
        if not hasattr(self, "mod"):
            self.mod = 0
            
        if flag == "A":
            self.mod += mod
            self.current_time = (self.current_time + mod)
            self.start_time = time.monotonic()
        else:
            self.mod += mod
            self.current_time = (time.monotonic() - self.mod) - (self.start_time - self.mod)
        return self.current_time
    
                
    def seekf_track(self, sec = 5):
        if self.audio_state == "INIT":
            stime = self.file_timer(sec, "A")
            if stime > self.dec.duration:
                stime = self.dec.duration
            self.dec.dec_seek(stime)

    
    def seekb_track(self, sec = 5):
        
        if not hasattr(self, "current_time"):
            self.current_time = (time.monotonic() - self.start_time)
        stime = self.current_time - sec
        if stime < 0:
            stime = 0
        self.dec.reader.fseek(stime)  
    
    def closeEvent(self, event):
        self.audio_server.stop()
        if hasattr(self, "dec"):
            self.dec.reader.Kill()    

class Main_exe(QtWidgets.QApplication):
    """Main Python file binding all class for execution"""

    def __init__(self):
        """Constructor"""
        super(Main_exe, self).__init__([])        
        self.main_window = Bindings()
        self.setStyle("Fusion")
        self.main_window.show()
             
if __name__ == "__main__":
    app = Main_exe()
    sys.exit(app.exec_())
    
