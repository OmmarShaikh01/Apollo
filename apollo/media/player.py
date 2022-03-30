import os

from apollo.media.processor import DSPInterface, timeit


class Player:
    REPEAT_TRACK = 0
    REPEAT_QUEUE = 1
    REPEAT_NONE = 2

    def __init__(self) -> None:
        self.dsp = DSPInterface(fadeout_time = 5)
        self.dsp.output()
        self.dsp.call_at_EOF = self.move_f
        self.repeat_type = self.REPEAT_QUEUE

    def setQueue(self, queue: list):
        self.pointer = 0
        self.queue = queue
        self.load_track(self.queue[self.pointer])

    def load_track(self, path: str):
        if os.path.isfile(path):
            self.dsp.replaceTable(path)

    def reload_track(self):
        self.dsp.replay_table()

    def seek_f(self, time):
        self.dsp.seek(time)

    def seek_b(self, time):
        self.dsp.seek(-time)

    def move_f(self):
        if (self.pointer + 1) < len(self.queue):
            self.pointer += 1
            self.load_track(self.queue[self.pointer])
        elif (self.pointer + 1) == len(self.queue) and self.repeat_type == self.REPEAT_QUEUE:
            self.pointer = 0
            self.load_track(self.queue[self.pointer])
        else:
            self.pointer = 0
            self.pause()

    def move_b(self):
        if (self.pointer - 1) >= 0:
            self.pointer -= 1
            self.load_track(self.queue[self.pointer])
        elif (self.pointer - 1) < 0 and self.repeat_type == self.REPEAT_QUEUE:
            self.pointer = (self.queue - 1)
            self.pause()

    def play(self):
        self.dsp.server.start()

    def pause(self):
        self.dsp.server.stop()


if __name__ == '__main__':
    player = Player()
    q = [
        r'D:\Music\fold_2\whenowhere30.mp3',
        r'D:\Music\fold_2\whenowhere30.mp3'
    ]
    player.setQueue(q)

    # player.load_track(r'D:\Music\fold_1\ff-16b-2c-44100hz.wav')
    player.dsp.GUI(globals())
