import math
import os
import time

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap

from apollo.media.processor import DSPInterface
from apollo.media import Mediafile


class Player:
    REPEAT_TRACK = 0
    REPEAT_QUEUE = 1
    REPEAT_NONE = 2
    SHUFFLE_NONE = 0
    SHUFFLE_TRACK = 1

    def __init__(self) -> None:
        self.dsp = DSPInterface()
        self.dsp.output()
        self.dsp.call_at_EOF = self.move_f
        self.repeat_type = self.REPEAT_NONE
        self.shuffle_type = self.SHUFFLE_NONE

    def setQueue(self, queue: list):
        self.pointer = 0
        self.queue = queue
        self.replayed = False
        self.load_track(self.getCurrentTrack(), True)

    def load_track(self, path: str, instant = False):
        if os.path.isfile(path) and Mediafile.isSupported(path):
            self.queuePositionChanged(self.pointer)
            self.dsp.replaceTable(path, instant = instant)
            self.fetchMediaData(self.dsp.get_active_stream().getMediaFile())
            self.replayed = False
        else:
            self.move_f(True)

    def reload_track(self):
        self.replayed = True
        self.dsp.replay_table()
        self.fetchMediaData(self.dsp.get_active_stream().getMediaFile())

    def seek_exact(self, time_value):
        self.dsp.seek(time_value)

    def move_f(self, instant = False):
        if not self.dsp.server.getIsStarted():
            self.play()

        if self.repeat_type == self.REPEAT_TRACK and not instant and not self.replayed:
            self.reload_track()
        else:
            if (self.pointer + 1) < len(self.queue):
                self.pointer += 1
                self.load_track(self.getCurrentTrack(), instant)
            elif (self.pointer + 1) == len(self.queue) and self.repeat_type == self.REPEAT_QUEUE:
                self.pointer = 0
                self.load_track(self.getCurrentTrack(), instant)

    def move_to(self, index, instant = False):
        if not self.dsp.server.getIsStarted():
            self.play()

        if 0 < (index) < len(self.queue):
            self.pointer = index
            self.load_track(self.getCurrentTrack(), instant)

    def move_b(self, instant = False):
        if not self.dsp.server.getIsStarted():
            self.play()

        if (self.pointer - 1) >= 0:
            self.pointer -= 1
            self.load_track(self.getCurrentTrack(), instant)
        elif (self.pointer - 1) < 0 and self.repeat_type == self.REPEAT_QUEUE:
            self.pointer = (len(self.queue) - 1)
            self.load_track(self.getCurrentTrack(), instant)

    def play(self):
        self.onPlay()
        if not self.dsp.server.getIsStarted():
            self.dsp.server.start()
        if (self.pointer + 1) == len(self.queue):
            self.move_f(True)

    def pause(self):
        self.onPause()
        self.dsp.server.stop()

    def setVolume(self, value: int):
        self.dsp.setVolume(value)

    def setRepeat(self, value):
        self.repeat_type = value

    def setShuffle(self, value):
        self.shuffle_type = value

    def getCurrentTrack(self):
        if self.shuffle_type == self.SHUFFLE_NONE:
            return self.queue[self.pointer]
        elif self.shuffle_type == self.SHUFFLE_TRACK:
            return self.queue[self.pointer]

    def fetchMediaData(self, media: [Mediafile, None]):
        ...

    def onPause(self):
        ...

    def onPlay(self):
        ...

    def queuePositionChanged(self, index):
        ...


if __name__ == '__main__':
    player = Player()
    q = [
        r'D:\Music\topntch.mp3',
        r'D:\Music\whenowhere.mp3'
    ]
    player.setQueue(q)

    # player.load_track(r'D:\Music\fold_1\ff-16b-2c-44100hz.wav')
    player.dsp.GUI(globals())
