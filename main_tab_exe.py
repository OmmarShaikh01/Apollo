from utils import *
from audio_fx_tab import *
from music_tab import *
from search_tab import *
from now_playing_tab import *
from playlist_tab import *
from audiobk_tab import * 
from ui_init import * 

from PyQt5 import QtWidgets

import sys, threading, re, logging, queue, json

    
class Inbox_Tab(Main_widget):
    
    def __init__(self, *args):
        super(Inbox_Tab, self).__init__()    

    
class Binding_Tab(Music_Tab, Search_Tab, Now_playing_Tab, Playlist_Tab, Audio_bk_Tab, Inbox_Tab, Audio_FX_Tab):
    # Calls all tabs without DSP
    
    def __init__(self, *args):
        super(Binding_Tab, self).__init__()         
        self.playing_queue()
        
        
class Main_App():
    
    def __init__(self, window):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle('Fusion')
        self.main_app = window()
        self.main_app.show()
        sys.exit(self.app.exec_())        
        
if __name__ == "__main__":
    app = Main_App(Binding_Tab)
