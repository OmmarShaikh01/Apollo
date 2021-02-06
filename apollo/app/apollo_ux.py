from PyQt5 import QtWidgets, QtCore, QtGui

from apollo.gui.apollo_ui import Ui_MainWindow as ApolloUi
from apollo.utils import ConfigManager, exe_time

class ApolloUX(QtWidgets.QMainWindow, ApolloUi):
    """docstring for ApolloUX"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.CONF_MANG = ConfigManager()
        self.Init_UX()


    def Init_UX(self):
        self.PushButton_Behaviours()

        # controls the hide/show when switching btwn NowPlaying and other Tabs
        self.apollo_TABWG_main.currentChanged.connect(lambda index: self.HideFooter(index))

        # controls the collasping of different tabs
        self.splitter.setCollapsible(1, False)
        self.apollo_HSP_subMain.setCollapsible(0, False)

    def HideFooter(self, index):
        """
        hides the footer playback controller is tab index is 1
        """
        if index == 1:
            self.apollo_FR_footer.hide()
        elif self.apollo_FR_footer.isHidden():
            self.apollo_FR_footer.show()
        else:
            pass


    def PushButton_Behaviours(self):
        """
        QPushButton Default behaviour declaration
        """
        self.apollo_PSB_NPQ_volume_main.setFlat(True)
        self.apollo_PSB_NPQ_volume_main.setText("")

        self.apollo_PSB_NPQ_playstyle.setFlat(True)
        self.apollo_PSB_NPQ_playstyle.setText("")

        self.apollo_PSB_NPQ_options.setFlat(True)
        self.apollo_PSB_NPQ_options.setText("")

        self.apollo_PSB_NPQ_seekf.setFlat(True)
        self.apollo_PSB_NPQ_seekf.setText("")

        self.apollo_PSB_NPQ_skipback.setFlat(True)
        self.apollo_PSB_NPQ_skipback.setText("")

        self.apollo_PSB_NPQ_seekb.setFlat(True)
        self.apollo_PSB_NPQ_seekb.setText("")

        self.apollo_PSB_NPQ_stop.setFlat(True)
        self.apollo_PSB_NPQ_stop.setText("")

        self.apollo_PSB_NPQ_skipfront.setFlat(True)
        self.apollo_PSB_NPQ_skipfront.setText("")

        self.apollo_PSB_NPQ_pause.setFlat(True)
        self.apollo_PSB_NPQ_pause.setText("")

        self.apollo_PSB_NPQ_play.setFlat(True)
        self.apollo_PSB_NPQ_play.setText("")

        self.apollo_PSB_volume_main.setFlat(True)
        self.apollo_PSB_volume_main.setText("")

        self.apollo_PSB_playstyle.setFlat(True)
        self.apollo_PSB_playstyle.setText("")

        self.apollo_PSB_options.setFlat(True)
        self.apollo_PSB_options.setText("")

        self.apollo_PSB_seekf.setFlat(True)
        self.apollo_PSB_seekf.setText("")

        self.apollo_PSB_skipback.setFlat(True)
        self.apollo_PSB_skipback.setText("")

        self.apollo_PSB_seekb.setFlat(True)
        self.apollo_PSB_seekb.setText("")

        self.apollo_PSB_stop.setFlat(True)
        self.apollo_PSB_stop.setText("")

        self.apollo_PSB_skipfront.setFlat(True)
        self.apollo_PSB_skipfront.setText("")

        self.apollo_PSB_pause.setFlat(True)
        self.apollo_PSB_pause.setText("")

        self.apollo_PSB_play.setFlat(True)
        self.apollo_PSB_play.setText("")

if __name__ == "__main__":
    from apollo.app.apollo_main import ApolloExecute
    app = ApolloExecute()
    app.Execute()
