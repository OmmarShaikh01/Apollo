import random
import numpy as np
import av


class MP3_Decoder():

    def __init__(self, path: str) -> None:
        self.file_path = path
        self.InputStream: av.container.InputContainer = av.open(path)
        self.decoder = self.decode()

    def decode(self):
        # actual decoding and demuxing of file
        for packet in self.InputStream.demux(audio = 0):
            if not (packet.size <= 0):
                for frame in packet.decode():
                    yield frame
            else:
                yield None

    def get(self) -> av.audio.frame.AudioFrame:
        return next(self.decoder)

    def seek(self, time):
        print(time)
        self.InputStream.seek(int(time * av.time_base), any_frame = True)

    def reset_buffer(self):
        self.InputStream.close()
        self.InputStream = av.open(self.file_path)
        self.decoder = self.decode()


if __name__ == '__main__':
    player = MP3_Decoder(r'D:\Music\fold_2\whenowhere30.mp3')
    print(player.get().time)
    player.seek(12)
    print(player.get().time)
