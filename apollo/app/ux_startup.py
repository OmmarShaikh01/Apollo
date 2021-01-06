from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from apollo.gui.apollo_ui import Ui_MainWindow as Apollo_MainWindow
from apollo.resources import Theme
from apollo.utils import ConfigManager, exe_time

class ApolloStartup(Apollo_MainWindow, QtWidgets.QMainWindow):
    """
    Controls the startup and UX operation of the application
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.CONF_MANG = ConfigManager()     
        self.SetFrameless()        
        self.LoadIconPack()
        
        self._setup()
        self._uxsetup()
       
        self.apollo_PSB_LBT_addtrack.pressed.connect(self.RefreshTheme)    
        
    def _setup(self):
        self.apollo_HDLBD_nowplayong_queue.setText("Current Queue")
        self.apollo_TBV_LBT_maintable.horizontalHeader().setSectionsMovable(True)
        self.apollo_TBV_LBT_grouptable.horizontalHeader().setSectionsMovable(True)
        self.apollo_TBV_NPQ_maintable.horizontalHeader().setSectionsMovable(True)
        
    def _uxsetup(self):
        self.apollo_TABWG_main.currentChanged.connect(lambda index: self._hideFooter(index))
        
        # needs to be in a unified stylesheet
        self.apollo_HDLBD_main_header.setStyleSheet("color: #ffffff")        
        
        # declares the minimize max and close buttons
        self.apollo_PSB_minimizemain.pressed.connect(self.showMinimized)
        self.apollo_PSB_closemain.pressed.connect(self.close)
        self.apollo_PSB_resizemain.pressed.connect(self.Maximize_Resizing)
        
        # helps in moving the window as a whole
        self.apollo_HDLBD_main_header.mouseMoveEvent = self.moveWindow
        self.apollo_HDLBD_main_header.mousePressEvent = self.Header_mousePressEvent
        
        # performs all the resize functions
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.mouseMoveEvent = self.ResizeEventFilter
        
        # resets the cursor as an arrow 
        self.apollo_HSP_central.enterEvent = lambda event: self.centralwidget.setCursor(Qt.ArrowCursor)
        self.apollo_HDLBD_main_header.enterEvent = lambda event: self.centralwidget.setCursor(Qt.ArrowCursor)

                        
    def ResizeEventFilter(self, event):        
        position_x, position_y = event.pos().x(), event.pos().y()
        max_x, max_y = self.centralwidget.width(), self.centralwidget.height()
        if position_x in [0, max_x] or position_y in [0, max_y]:
            self.centralwidget.setCursor(Qt.SizeAllCursor)
        else:            
            self.centralwidget.setCursor(Qt.ArrowCursor)                
 
 
    def Header_mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        
        
    def moveWindow(self, event):
        # MOVE WINDOW
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
            
        
    def RefreshTheme(self):
        """
        Gets a stylesheet and sets it as the current theme
        """
        #resource, sheet = Theme().LoadStyleSheet()
        #with open(sheet) as FH:
            #self.setStyleSheet(FH.read())
            
        Sheet = Theme().GenStylesheet(eval(Theme().DefaultPallete())["THEME"])
        self.setStyleSheet(Sheet)
        
    def GetAppTheme(self):
        """
        Gets an app stylesheet
        """
        #resource, sheet = Theme().LoadStyleSheet()
        #with open(sheet) as FH:
            #sheet = self.setStyleSheet(FH.read())
            
        Sheet = Theme().GenStylesheet(eval(Theme().DefaultPallete())["THEME"])
        resource = 1
        return (resource, Sheet)


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

        
    def SetFrameless(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showMaximized()
        self.WINDOW_STATE = 1
        
        
    def Maximize_Resizing(self):
        #  window is maximized
        if self.WINDOW_STATE == 1:
            # resize it to normal
            self.showNormal()
            self.WINDOW_STATE = 0
        
        #  window is normal
        if self.WINDOW_STATE == 0:
            # resize it to max
            self.showMaximized()
            self.WINDOW_STATE = 1                  
        
        
    def LoadIconPack(self):
        self.apollo_PSB_LBT_addtrack
        
if __name__ == "__main__":
    from apollo.resources.apptheme import style
    from apollo.app.apollo_exe import ApolloExecute
    #app = ApolloExecute()
    #app.Execute()    

    from apollo.resources.apptheme import style
    from apollo.test.testUtilities import TesterObjects

    App = QtWidgets.QApplication([])
    Inst = ApolloStartup()
    Inst.RefreshTheme()
    _, TableModel = TesterObjects.Gen_TableModel(size=(50,60))
    
    Inst.apollo_TBV_LBT_grouptable.setModel(TableModel)
    Inst.apollo_TBV_LBT_maintable.setModel(TableModel)   
    Inst.apollo_TBV_NPQ_maintable.setModel(TableModel)
    
    Inst.show()    
    App.exec_()
