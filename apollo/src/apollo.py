import datetime

from PySide6 import QtWidgets

from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.src.main_content import MainContent
from apollo.src.playback_bar import PlayBackBar


class Apollo(QtWidgets.QMainWindow, Apollo_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setupUX()
        self.playback_bar_controller = PlayBackBar(self)
        self.main_content_controller = MainContent(self)

        self.testing()

    def testing(self):
        self.playback_bar_controller.setTrackTimes(datetime.time(1, 45, 20))

        self.playback_bar_controller.connectSeekingSliderValueChange(lambda x: None)
        self.playback_bar_controller.connectSeekingSliderValueReleased(print)

        self.playback_bar_controller.connectVolumeSliderValueChange(lambda x: None)
        self.playback_bar_controller.connectVolumeSliderValueReleased(print)

        self.playback_bar_controller.connectPlayPushbutton(lambda: None)
        self.playback_bar_controller.connectRepeatPushbutton(lambda: None)
        self.playback_bar_controller.connectShufflePushbutton(lambda: None)

    def setupUX(self):
        self.main_content_splitterframe.setCollapsible(0, False)
