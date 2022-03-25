import os

from apollo.media.processor import DSPInterface


class Player:

    def __init__(self) -> None:
        self.dsp = DSPInterface(fadeout_time = 5)
        self.dsp.output()

    def load_track(self, path: str):
        if os.path.isfile(path):
            self.dsp.replaceTable(path)

    def seek_f(self, time):
        self.dsp.seek(time)

    def seek_b(self, time):
        self.dsp.seek(-time)

    def reload_track(self):
        self.dsp.replay_table()

    def play(self):
        self.dsp.server.start()

    def pause(self):
        self.dsp.server.stop()


if __name__ == '__main__':
    player = Player()
    player.load_track(r'D:\Music\fold_2\whenowhere30.mp3')
    # player.seek_f(15)
    # player.seek_b(10)
    # player.load_track(r'D:\Music\fold_2\ff-16b-2c-44100hz.mp3')
    # player.load_track(r'D:\Music\fold_2\whenowhere30.mp3')
    # player.load_track(r'D:\Music\fold_1\ff-16b-2c-44100hz.wav')
    player.dsp.GUI(globals())
