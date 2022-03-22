import datetime
import os
import pathlib
import typing

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap

from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo


class PlayBackBar:

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.setupUI()

    def setupUI(self):
        # TODO save initial states into a temporary dump
        self.ui.volume_pushbutton.setProperty('volume_level', 'HALF')
        self.ui.play_pushbutton.setProperty('play_type', 'PLAY')
        self.ui.repeat_pushbutton.setProperty('repeat', 'NONE')
        self.ui.shuffle_pushbutton.setProperty('shuffle', 'NONE')

        self.ui.cover_pixmap.clear()
        self.setAlbumCoverImage()
        self.ui.volume_slider.setValue(50)
        self.ui.volume_pushbutton.clicked.connect(self.volumeChangeCycle)
        self.ui.queue_pushbutton.clicked.connect(lambda: (
            self.ui.main_content_splitterframe.setSizes((
                int(self.ui.centralwidget.width() * 0.7),
                int(self.ui.centralwidget.width() * 0.3)
            ))
        ))
        self.ui.audio_fx_pushbutton.clicked.connect(lambda: (
            self.ui.main_tab_widget.setCurrentIndex(3)
        ))

    def connectSeekingSliderValueChange(self, callback: typing.Callable):
        """
        Signal Connector

        :param callback: is a callable that recieves the value of the slider
        :return: None
        """
        self.ui.seeking_slider.valueChanged.connect(lambda value: (
            self.updateElapsedTime(datetime.timedelta(seconds = value)),
            callback(value)
        ))

    def connectSeekingSliderValueReleased(self, callback: typing.Callable):
        """
        Signal Connector

        :param callback: is a callable that recieves the value of the slider
        :return: None
        """
        self.ui.seeking_slider.sliderReleased.connect(lambda: (
            callback(self.ui.seeking_slider.value())
        ))

    def connectVolumeSliderValueChange(self, callback: typing.Callable):
        """
        Signal Connector

        :param callback: is a callable that recieves the value of the slider
        :return: None
        """
        self.ui.volume_slider.valueChanged.connect(lambda value: (
            self.reactTovolumeChanges(value),
            callback(value)
        ))

    def connectVolumeSliderValueReleased(self, callback: typing.Callable):
        """
        Signal Connector

        :param callback: is a callable that recieves the value of the slider
        :return: None
        """
        self.ui.volume_slider.sliderReleased.connect(lambda: (
            callback(self.ui.volume_slider.value()),
            self.reactTovolumeChanges(self.ui.volume_slider.value())
        ))

    def connectPlayPushbutton(self, callback: typing.Callable):
        self.ui.play_pushbutton.clicked.connect(lambda: (
            self.reactToPlaybackChanges()
        ))

    def connectRepeatPushbutton(self, callback: typing.Callable):
        self.ui.repeat_pushbutton.clicked.connect(lambda: (
            self.reactToPlaybackTypeChanges()
        ))

    def connectShufflePushbutton(self, callback: typing.Callable):
        self.ui.shuffle_pushbutton.clicked.connect(lambda: (
            self.reactToShuffleTypeChanges()
        ))

    def connectEffectsSwitchPushbutton(self, callback: typing.Callable):
        self.ui.switch_audio_pushbutton.clicked.connect(lambda: (
            callback()
        ))

    def connectSettingsPushbutton(self, callback: typing.Callable):
        self.ui.settings_pushbutton.clicked.connect(lambda: (
            callback()
        ))

    def volumeChangeCycle(self):
        value = self.ui.volume_slider.value()
        if value == 0:
            self.ui.volume_pushbutton.setProperty('volume_level', 'NORMAL')
            self.ui.volume_slider.setValue(25)
        elif 0 < value < 50:
            self.ui.volume_pushbutton.setProperty('volume_level', 'HALF')
            self.ui.volume_slider.setValue(75)
        elif 50 <= value < 100:
            self.ui.volume_pushbutton.setProperty('volume_level', 'FULL')
            self.ui.volume_slider.setValue(100)
        elif value == 100:
            self.ui.volume_pushbutton.setProperty('volume_level', 'MUTE')
            self.ui.volume_slider.setValue(0)
        else:
            pass
        self.ui.volume_pushbutton.style().unpolish(self.ui.volume_pushbutton)
        self.ui.volume_pushbutton.style().polish(self.ui.volume_pushbutton)

    def reactTovolumeChanges(self, value):
        if value == 0:
            self.ui.volume_pushbutton.setProperty('volume_level', 'MUTE')
        elif 0 < value < 50:
            self.ui.volume_pushbutton.setProperty('volume_level', 'NORMAL')
        elif 50 <= value < 100:
            self.ui.volume_pushbutton.setProperty('volume_level', 'HALF')
        elif value == 100:
            self.ui.volume_pushbutton.setProperty('volume_level', 'FULL')
        else:
            pass
        self.ui.volume_pushbutton.style().unpolish(self.ui.volume_pushbutton)
        self.ui.volume_pushbutton.style().polish(self.ui.volume_pushbutton)

    def reactToPlaybackChanges(self):
        if self.ui.play_pushbutton.property('play_type') != 'PLAY':
            self.ui.play_pushbutton.setProperty('play_type', 'PLAY')
        elif self.ui.play_pushbutton.property('play_type') != 'PAUSE':
            self.ui.play_pushbutton.setProperty('play_type', 'PAUSE')
        else:
            pass
        self.ui.play_pushbutton.style().unpolish(self.ui.play_pushbutton)
        self.ui.play_pushbutton.style().polish(self.ui.play_pushbutton)

    def reactToPlaybackTypeChanges(self):
        if self.ui.repeat_pushbutton.property('repeat') == 'QUEUE':
            self.ui.repeat_pushbutton.setProperty('repeat', 'NONE')
        elif self.ui.repeat_pushbutton.property('repeat') == 'NONE':
            self.ui.repeat_pushbutton.setProperty('repeat', 'SINGLE')
        elif self.ui.repeat_pushbutton.property('repeat') == 'SINGLE':
            self.ui.repeat_pushbutton.setProperty('repeat', 'QUEUE')
        else:
            pass
        self.ui.repeat_pushbutton.style().unpolish(self.ui.repeat_pushbutton)
        self.ui.repeat_pushbutton.style().polish(self.ui.repeat_pushbutton)

    def reactToShuffleTypeChanges(self):
        if self.ui.shuffle_pushbutton.property('shuffle') == 'SHUFFLE':
            self.ui.shuffle_pushbutton.setProperty('shuffle', 'NONE')
        elif self.ui.shuffle_pushbutton.property('shuffle') == 'NONE':
            self.ui.shuffle_pushbutton.setProperty('shuffle', 'SHUFFLE')
        else:
            pass
        self.ui.shuffle_pushbutton.style().unpolish(self.ui.shuffle_pushbutton)
        self.ui.shuffle_pushbutton.style().polish(self.ui.shuffle_pushbutton)

    def setTrackTimes(self, total: datetime.time):
        self.ui.total_time_label.setText(str(total))
        self.ui.completed_time_label.setText(str(datetime.timedelta(seconds = 0)))
        self.ui.seeking_slider.setMaximum((total.hour * 60 * 60) + (total.minute * 60) + total.second)
        self.ui.seeking_slider.setSingleStep(5)

    def updateElapsedTime(self, elapsed: typing.Union[datetime.time, datetime.timedelta]):
        self.ui.completed_time_label.setText(str(elapsed))
        if isinstance(elapsed, datetime.timedelta):
            self.ui.seeking_slider.setValue(elapsed.total_seconds())
        if isinstance(elapsed, datetime.time):
            self.ui.seeking_slider.setValue((elapsed.hour * 60 * 60) + (elapsed.minute * 60) + elapsed.second)

    def setAlbumCoverImage(self, data: QPixmap = None):
        if data is None:
            default = (
                os.path.join(pathlib.Path.home(), '.qt_material', 'theme_custom', 'primary', 'music-note-2.4.svg'))
            data = QIcon(default).pixmap(
                    QSize(int(self.ui.cover_pixmap.width() * 0.8), int(self.ui.cover_pixmap.height() * 0.8)))
        self.ui.cover_pixmap.setPixmap(data)
