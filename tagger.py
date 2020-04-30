from PyQt5 import QtCore, QtGui, QtWidgets
import mutagen 
import tinytag 
import beets 
import time 
import os 
import json
import tagger_ui


class file_tagger(tagger_ui.Ui_MainWindow, QtWidgets.QMainWindow):
    
    def __init__(self):
        super(file_tagger, self).__init__()
        self.setupUi(self)    
    
    
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = file_tagger()
    main_window.show()
    sys.exit(app.exec_())
