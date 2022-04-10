import datetime
import os
import pathlib
import typing
import time

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap

from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo
from apollo.media.player import Player
from apollo.media import Mediafile
from apollo.db.models import Provider, QueueModel
from apollo.utils import ROOT


class PlayBackBar:
    QUEUE_POINTER_CHANGED = QtCore.Signal()

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.Player = Player()
        self.init_queue()
        self.setupUI()

    def init_queue(self):
        self.model = Provider.get_model(QueueModel)

    # SETUP: START
    def setupUI(self):
        # TODO save initial states into a temporary dump

        # Sets Defaults
        self.ui.volume_pushbutton.setProperty('volume_level', 'HALF')
        self.ui.play_pushbutton.setProperty('play_type', 'PAUSE')
        self.ui.repeat_pushbutton.setProperty('repeat', 'NONE')
        self.ui.shuffle_pushbutton.setProperty('shuffle', 'NONE')

        self.setTrackTimes(0)
        self.setAlbumCoverImage(self.ui.cover_pixmap)
        self.reactTovolumeChanges(25)
        # END REGION

        self.ui.volume_pushbutton.clicked.connect(self.volumeChangeCycle)
        self.ui.queue_pushbutton.clicked.connect(self.reactQueueButtonPressed)
        self.ui.audio_fx_pushbutton.clicked.connect(lambda: (
            self.ui.main_tab_widget.setCurrentIndex(3)
        ))

        self.Player.fetchMediaData = self.setMediaData
        self.Player.dsp.call_for_ElapsedTime = self.updateElapsedTime
        self.Player.onPlay = self.changeViewToPlaybackChanges
        self.Player.onPause = self.changeViewToPlaybackChanges
        self.connectVolumeSliderValueReleased()
        self.connectVolumeSliderValueChange()
        self.connectSeekingSliderValueReleased()
        self.connectRepeatPushbutton()
        self.connectShufflePushbutton()
        self.connectPlayPushbutton()
        self.connectOffPushbutton()
        self.connectNextTrackPushbutton()
        self.connectPreviousTrackPushbutton()
        self.connectQueueValueChange()

        self.updatePlayerQueue()
        self.ui.play_pushbutton.click()

    def connectQueueValueChange(self, callback: typing.Callable = lambda x: None):
        """
        Signal Connector

        :param callback: is a callable that recieves the value of the slider
        :return: None
        """
        self.model.TABLE_UPDATE.connect(lambda: self.updatePlayerQueue())

    def connectSeekingSliderValueChange(self, callback: typing.Callable = lambda x: None):
        """
        Signal Connector

        :param callback: is a callable that recieves the value of the slider
        :return: None
        """
        self.ui.seeking_slider.valueChanged.connect(lambda value: (
            self.Player.seek_exact(value),
            callback(value)
        ))

    def connectSeekingSliderValueReleased(self, callback: typing.Callable = lambda x: None):
        """
        Signal Connector

        :param callback: is a callable that recieves the value of the slider
        :return: None
        """
        self.ui.seeking_slider.sliderReleased.connect(lambda: (
            self.Player.seek_exact(self.ui.seeking_slider.value()),
            callback(self.ui.seeking_slider.value())
        ))

    def connectVolumeSliderValueChange(self, callback: typing.Callable = lambda x: None):
        """
        Signal Connector

        :param callback: is a callable that recieves the value of the slider
        :return: None
        """
        self.ui.volume_slider.valueChanged.connect(lambda value: (
            self.reactTovolumeChanges(value),
            callback(value)
        ))

    def connectVolumeSliderValueReleased(self, callback: typing.Callable = lambda x: None):
        """
        Signal Connector

        :param callback: is a callable that recieves the value of the slider
        :return: None
        """
        self.ui.volume_slider.sliderReleased.connect(lambda: (
            callback(self.ui.volume_slider.value()),
            self.reactTovolumeChanges(self.ui.volume_slider.value())
        ))

    def connectPlayPushbutton(self, callback: typing.Callable = lambda: None):
        self.ui.play_pushbutton.clicked.connect(lambda: (
            self.reactToPlaybackChanges()
        ))

    def connectOffPushbutton(self, callback: typing.Callable = lambda: None):
        self.ui.switch_audio_pushbutton.clicked.connect(lambda: (
            self.reactToPlaybackChanges()
        ))

    def connectRepeatPushbutton(self, callback: typing.Callable = lambda: None):
        self.ui.repeat_pushbutton.clicked.connect(lambda: (
            self.reactToPlaybackTypeChanges()
        ))

    def connectShufflePushbutton(self, callback: typing.Callable = lambda: None):
        self.ui.shuffle_pushbutton.clicked.connect(lambda: (
            self.reactToShuffleTypeChanges()
        ))

    def connectEffectsSwitchPushbutton(self, callback: typing.Callable = lambda: None):
        self.ui.switch_audio_pushbutton.clicked.connect(lambda: (
            callback()
        ))

    def connectSettingsPushbutton(self, callback: typing.Callable = lambda: None):
        self.ui.settings_pushbutton.clicked.connect(lambda: (
            callback()
        ))

    def connectNextTrackPushbutton(self, callback: typing.Callable = lambda: None):
        self.ui.next_pushbutton.clicked.connect(lambda: (
            self.Player.move_f(True)
        ))

    def connectPreviousTrackPushbutton(self, callback: typing.Callable = lambda: None):
        self.ui.prev_pushbutton.clicked.connect(lambda: (
            self.Player.move_b(True)
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
        self.ui.volume_slider.setValue(value)
        self.Player.setVolume(self.ui.volume_slider.value())

    def reactToPlaybackChanges(self):
        if self.ui.play_pushbutton.property('play_type') == 'PLAY':
            self.Player.play()
        elif self.ui.play_pushbutton.property('play_type') == 'PAUSE':
            self.Player.pause()
        else:
            pass

    def changeViewToPlaybackChanges(self):
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
            self.Player.setRepeat(Player.REPEAT_NONE)
        elif self.ui.repeat_pushbutton.property('repeat') == 'NONE':
            self.ui.repeat_pushbutton.setProperty('repeat', 'SINGLE')
            self.Player.setRepeat(Player.REPEAT_TRACK)
        elif self.ui.repeat_pushbutton.property('repeat') == 'SINGLE':
            self.ui.repeat_pushbutton.setProperty('repeat', 'QUEUE')
            self.Player.setRepeat(Player.REPEAT_QUEUE)
        else:
            pass
        self.ui.repeat_pushbutton.style().unpolish(self.ui.repeat_pushbutton)
        self.ui.repeat_pushbutton.style().polish(self.ui.repeat_pushbutton)

    def reactToShuffleTypeChanges(self):
        if self.ui.shuffle_pushbutton.property('shuffle') == 'SHUFFLE':
            self.ui.shuffle_pushbutton.setProperty('shuffle', 'NONE')
            self.Player.setShuffle(Player.SHUFFLE_NONE)
        elif self.ui.shuffle_pushbutton.property('shuffle') == 'NONE':
            self.ui.shuffle_pushbutton.setProperty('shuffle', 'SHUFFLE')
            self.Player.setShuffle(Player.SHUFFLE_TRACK)
        else:
            pass
        self.ui.shuffle_pushbutton.style().unpolish(self.ui.shuffle_pushbutton)
        self.ui.shuffle_pushbutton.style().polish(self.ui.shuffle_pushbutton)

    def reactQueueButtonPressed(self):
        if self.ui.main_content_splitterframe.sizes()[-1] <= 10:
            self.ui.main_content_splitterframe.setSizes((
                int(self.ui.centralwidget.width() * 0.7),
                int(self.ui.centralwidget.width() * 0.3)
            ))
        else:
            self.ui.main_content_splitterframe.setSizes((
                int(self.ui.centralwidget.width() * 1),
                int(self.ui.centralwidget.width() * 0)
            ))

    def setTrackTimes(self, total: float):
        DT = time.gmtime(total)
        start = ':'.join(str(datetime.timedelta(seconds = 0)).split(".")[0].split(":")[1:])
        end = ':'.join(str(datetime.timedelta(seconds = total)).split(".")[0].split(":")[1:])
        self.ui.total_time_label.setText(end)
        self.ui.completed_time_label.setText(start)
        self.ui.seeking_slider.setMaximum(((DT.tm_hour * 60 * 60) + (DT.tm_min * 60) + DT.tm_sec) * 100)
        self.ui.seeking_slider.setSingleStep(5)

    def updateElapsedTime(self, elapsed: float):
        if not self.ui.seeking_slider.underMouse():
            elapsed = datetime.timedelta(seconds = elapsed)
            _time = round(elapsed.total_seconds(), 3) * 100
            start = ':'.join(str(elapsed).split(".")[0].split(":")[1:])
            self.ui.completed_time_label.setText(start)
            self.ui.seeking_slider.setValue(_time)

    def setAlbumCoverImage(self, widget, data: QIcon = None):
        size = QSize(int(widget.width() * 0.98), int(widget.height() * 0.98))
        if data is None:
            default = (os.path.join(ROOT, 'assets', 'generated', 'theme_custom', 'primary', 'music-note-2.4.svg'))
            data = QIcon(default)
            data = data.pixmap(size)
            widget.clear()
            widget.setPixmap(data)
        elif data is QIcon:
            data = data.pixmap(size)
            widget.clear()
            widget.setPixmap(data)
        elif isinstance(data, bytes):
            data = QtGui.QImage().fromData(data).scaled(size)
            data = (QtGui.QPixmap.fromImage(data))
            widget.clear()
            widget.setPixmap(data)

    def setMediaData(self, media: Mediafile = None):
        if media is not None:
            self.setTrackTimes(float(media.Tags['length']))
            self.setAlbumCoverImage(self.ui.cover_pixmap, media.Artwork)
            self.setAlbumCoverImage(self.ui.cover_pixmap_large, media.Artwork)
        else:
            self.setTrackTimes(0)

    def updatePlayerQueue(self):
        queue = []
        col = [col for col in range(self.model.columnCount()) if self.model.database.library_columns[col] == 'file_path']
        for row in range(self.model.rowCount()):
            queue.append(self.model.index(row, col[0]).data())
        if len(queue) > 0:
            self.Player.setQueue(queue)

    def play_File(self, f_id: str):
        queue = []
        col = [col for col in range(self.model.columnCount()) if self.model.database.library_columns[col] == 'file_id']
        for index, row in enumerate(range(self.model.rowCount())):
            if self.model.index(row, col[0]).data() == f_id:
                self.Player.move_to(index, True)
                break

    # SETUP: END REGION
