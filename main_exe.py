from dsp_player import Dsp_player, Decoder
from main_library_tab import Main_window

from PyQt5 import QtWidgets
import pyo

import sys

class Bindings(Dsp_player, Main_window):
    """"""

    def __init__(self):
        """Constructor"""
        super(Bindings, self).__init__()
        self.database_statrup()
        self.startup_dsp()        
        self.button_binder()        
        
    def button_binder(self): 
        self.play_button.pressed.connect(lambda: self.play_track())
        self.stop_button.pressed.connect(lambda: self.stop_track())

    def play_track(self):
        self.path = self.audio_queue.get()
        self.dec = Decoder(self.audio_server)
        self.dec.fopen(self.path)
        osc = self.dec.play()     
        if osc != None: self.process_in.setInput(osc)

    def pause_track(self):
        self.output_switch.stop()
    
    def stop_track(self):
        self.output_switch.stop()
        self.dec.reader.fseek(0)
        self.audio_queue.put(self.path)
        
    def next_track(self):
        self.audio_queue.next()
        
    def prev_track(self):
        self.audio_queue.prev()
    
    def seekf_track(self, sec = 5):
        pass
    
    def seekb_track(self, sec = 5):
        pass   

class Main_exe(Bindings, QtWidgets.QMainWindow):
    """Main Python file binding all class for execution"""

    def __init__(self):
        """Constructor"""
        super(Main_exe, self).__init__()


    def closeEvent(self, event):
        sys.exit()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    main_app = Main_exe()
    main_app.show()
    app.exec_()
    
