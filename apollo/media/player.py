import math
import os
import time

from apollo.media.processor import DSPInterface
from apollo.media import Mediafile


class Player:
    REPEAT_TRACK = 0
    REPEAT_QUEUE = 1
    REPEAT_NONE = 2

    def __init__(self) -> None:
        self.dsp = DSPInterface()
        self.dsp.output()
        self.dsp.call_at_EOF = self.move_f
        self.repeat_type = self.REPEAT_NONE

    def setQueue(self, queue: list):
        self.pointer = 0
        self.queue = queue
        self.replayed = False
        self.load_track(self.queue[self.pointer])

    def load_track(self, path: str, instant = False):
        if os.path.isfile(path):
            self.dsp.replaceTable(path, instant = instant)
            self.fetchMediaData(self.dsp.get_active_stream().getMediaFile())
            self.replayed = False

    def reload_track(self):
        self.replayed = True
        self.dsp.replay_table()
        self.fetchMediaData(self.dsp.get_active_stream().getMediaFile())

    def seek_exact(self, time_value):
        self.dsp.seek(time_value)

    def move_f(self, instant = False):
        print(time.time())
        if not self.dsp.server.getIsStarted():
            self.play()

        if self.repeat_type == self.REPEAT_TRACK and not instant and not self.replayed:
            self.reload_track()
        else:
            if (self.pointer + 1) < len(self.queue):
                self.pointer += 1
                self.load_track(self.queue[self.pointer], instant)
            elif (self.pointer + 1) == len(self.queue) and self.repeat_type == self.REPEAT_QUEUE:
                self.pointer = 0
                self.load_track(self.queue[self.pointer], instant)

    def move_b(self, instant = False):
        if not self.dsp.server.getIsStarted():
            self.play()

        if (self.pointer - 1) >= 0:
            self.pointer -= 1
            self.load_track(self.queue[self.pointer], instant)
        elif (self.pointer - 1) < 0 and self.repeat_type == self.REPEAT_QUEUE:
            self.pointer = (len(self.queue) - 1)
            self.load_track(self.queue[self.pointer], instant)

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

    def fetchMediaData(self, media: [Mediafile, None]): ...

    def onPause(self): ...

    def onPlay(self): ...


if __name__ == '__main__':
    player = Player()
    q = [
        r'D:\Music\fold_2\whenowhere30.mp3',
        r'D:\Music\fold_2\whenowhere30.mp3'
    ]
    player.setQueue(q)

    # player.load_track(r'D:\Music\fold_1\ff-16b-2c-44100hz.wav')
    player.dsp.GUI(globals())
