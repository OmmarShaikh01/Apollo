from dsp_player import Dsp_player, Decoder
from main_library_tab import Main_window
import utils

from PyQt5 import QtWidgets
import pyo

import sys, threading

class Bindings(Dsp_player, Main_window):
    """"""

    def __init__(self):
        """Constructor"""
        super(Bindings, self).__init__()
        self.database_statrup()
        self.startup_dsp()        
        self.button_binder()        
        self.audio_state = None
        
    def button_binder(self): 
        self.play_button.pressed.connect(lambda: self.play_track())
        self.stop_button.pressed.connect(lambda: self.stop_track())
        self.pause_button.pressed.connect(lambda: self.pause_track())
        self.next_button.pressed.connect(lambda: self.next_track())
        self.prev_button.pressed.connect(lambda: self.prev_track())
        
    def label_pixmap_seeker(self, event):
        lenth = (self.seek_pixmap.rect().width())
        data = round(((event.x() / lenth)*self.track_duration), 2)
    
    def Servercallback_stack(self):
        self.time_updater()
        self.stopper()
        self.label_style()
        
    def label_style(self):
        self.track_currpos
        
    def stopper(self):
        if self.track_currpos == 1:
            self.dec.decoder_stopper()
            self.output_switch.stop()
            self.next_button.click()
            
    def  time_updater(self):
        self.track_currpos = round((self.dec.current_time) / self.track_duration, 2)
        
        
    def decoder_init(self):
        pos, self.path = self.audio_queue.current()
        if  self.path == "EOF":
            return None
        
        if hasattr(self, "dec"):
            self.dec.kill_decoder()
            self.process_in.setInput(pyo.Sine(0))
            del self.dec
            
        self.dec = Decoder(self.audio_server)
        self.dec.fopen(self.path)
        self.track_duration = self.dec.duration
        
        # modifies the attribute of mouse press event inside the label and adds costom function
        self.seek_pixmap.mousePressEvent = self.label_pixmap_seeker
        self.dec.executionslot = [self.Servercallback_stack]
        
        osc = self.dec.play()
        self.output_switch.out()
        if osc != None:
            self.process_in.setInput(osc,0.5)
        else:
            print(osc)
        self.audio_state = "INIT"
        
    def play_track(self):
        if self.audio_state != "INIT":
            self.decoder_init()
        else:
            self.dec.reader.Play()
            self.output_switch.out()
            
    def pause_track(self):
        self.output_switch.stop()
        self.dec.reader.Pause()
    
    def stop_track(self):
        self.output_switch.stop()
        self.dec.reader.Stop()
        
    def next_track(self):
        self.audio_queue._next()
        self.decoder_init()
        
    def prev_track(self):
        self.audio_queue.prev()
        self.decoder_init()
        
    def seekf_track(self, sec = 5):
        time = self.cur_time + 5
        self.dec.reader.fseek(time)
    
    def seekb_track(self, sec = 5):
        time = self.cur_time - 5
        self.dec.reader.fseek(time)   


class Main_exe(Bindings, QtWidgets.QMainWindow):
    """Main Python file binding all class for execution"""

    def __init__(self):
        """Constructor"""
        super(Main_exe, self).__init__()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    main_app = Main_exe()
    main_app.show()
    sys.exit(app.exec_())
    
