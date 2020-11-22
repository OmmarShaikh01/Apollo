from PyQt5 import QtWidgets, QtGui, QtCore

from apollo.gui.apollo_ui import Ui_MainWindow as Apollo_MainWindow
from apollo.resources.qtstyle import Qtstyle 
from apollo.utils import ConfigManager

class ApolloStartup(Apollo_MainWindow, QtWidgets.QMainWindow):
    """
    Controls the startup and UX operation of the application
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.CONF_MANG = ConfigManager()     
        
        self._setup()
        self._uxsetup()
        self.apollo_PSB_LBT_addtrack.pressed.connect(self.refresh_theme)
        
        
    def _setup(self):
        self.apollo_HDLBD_nowplayong_queue.setText("Current Queue")
        self.apollo_TBV_LBT_maintable.horizontalHeader().setSectionsMovable(True)
        self.apollo_TBV_LBT_grouptable.horizontalHeader().setSectionsMovable(True)
        self.apollo_TBV_NPQ_maintable.horizontalHeader().setSectionsMovable(True)
        
        
        
    def _uxsetup(self):
        self.apollo_TABWG_main.currentChanged.connect(lambda index: self._hideFooter(index))
        
    def refresh_theme(self):
        """
        Gets a stylesheet and sets it as the current theme
        """
        self.setStyleSheet(Qtstyle.stylesheet())
        
    def GetAppTheme(self):
        """
        Gets an app stylesheet
        """
        return Qtstyle.stylesheet() 

    def _hideFooter(self, index):
        """
        hides the footer playback controller is tab index is 1
        """
        if index == 1:
            self.apollo_FR_footer.hide()
        elif self.apollo_FR_footer.isHidden():
            self.apollo_FR_footer.show()
        else:
            pass
