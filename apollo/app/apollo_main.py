# UI item name : <form_name>_<item type>_<others>

# Item Type:
    # Layouts:
        # 1. VIL = Vertical Layout
        # 2. HIL = Horizontal Layout
        # 3. GIL = Grid Layout
        # 4. FIL = Form Layout
        # 5. HSP = Horizontal Splitter
        # 6. VSP = Vertical Splitter

    # Spacers
        # 1. VSPC = Vertical Spacer
        # 2. HSPC = Horizontal Spacer

    # Buttons
        # 1. PSB = Push Button
        # 2. TLB = Tool Button
        # 3. RDB = Radio Button
        # 4. CKB = Check Box
        # 5. CLB = Command Link Button
        # 6. DBB = Dialog Button Box

    # Item Views
        # 1. LSV = List View
        # 2. TRV = Tree View
        # 3. TBV = Table View
        # 4. CLV = Colum View

    # Item Widgets
        # 1. LSWG = List Widget
        # 2. TRWG = Tree Widget
        # 3. TBWG = Table Widget

    # Containers
        # 1. GBX = Group Box
        # 2. SCAR = Scroll Area
        # 3. TLBX = Tool Box
        # 4. TABWG = Tab Widget
        # 5. SKWG = Stack Widget
        # 6. FR = Frame
        # 7. WDG = Widget
        # 8. MDIA = Mdi Area
        # 9. DOKWG = Dock Widget

    # Input Widgets
        # 1. CMBX = Combo Box
        # 2. FCMBX = Font Combo Box
        # 3. LEDT = Line Edit
        # 4. TXEDT = Text Edit
        # 5. SPNBX = Spin Box
        # 6. DSPBX = Double Spin Box
        # 7. TMEDT = Time Edit
        # 8. DEEDT = Date Edit
        # 9. DTEDT = Date And Time Edit
        # 10. HSCB = Horizontal Scroll Bar
        # 11. VSCB = Vertical Scroll Bar
        # 12. HSLD = Horizontal Slider
        # 13. VSLD = Vertical Slider
        # 14. KSEDT = Key Sequence Edit
        # 15. DIAL = Dial

    # Display Widgets
        # 1. LAB = Label
        # 2. HDLBD = Header Label
        # 3. PIXLB = Pixmap
        # 4. TXBRW = Text Browser
        # 5. GRPVW = Graphics View
        # 6. CLDWG = Calender Widget
        # 7. LCD = Lcd Widget
        # 8. PGBR = Progress Bar
        # 9. HLN = Horizontal Line
        # 10. VLN = Vertical Line
        # 11. GLWDG = Open Gl Widget

# Issues:
    # QTToolButton : toolmenu doesnt support multi screen menu popups
    # and displays menu on primary screen irrespective of screen

##########################################################################################

import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from apollo.app.apollo_TabBindings import ApolloTabBindings
from apollo.resources import Theme
from apollo.resources.apptheme import style


class ApolloMain(ApolloTabBindings):
    """
    Initilizes Apollo
    """
    def __init__(self):
        """Constructor"""
        super().__init__()


class ApolloExecute:
    """
    Executes Apollo
    """
    def __init__(self, style = "Fusion"):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle(style)
        self.UI = ApolloMain()
        self.UI.show()

        ThemeRefresh = lambda: self.app.setStyleSheet(Theme().GenStylesheet(eval(Theme().DefaultPallete())["THEME"]))
        ThemeRefresh()
        self.UI.apollo_PSB_play.pressed.connect(ThemeRefresh)

    def Execute(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = ApolloExecute()
    app.Execute()
