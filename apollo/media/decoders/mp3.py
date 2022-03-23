import random
import numpy as np
import av


class MP3_Decoder():
    def __init__(self, path: str) -> None:
        self.file_path = path
        self.InputStream = av.open(path)
        self.decoder = self.decode()

    def decode(self):
        # actual decoding and demuxing of file
        for packet in self.InputStream.demux(audio = 0):
            if not (packet.size <= 0):
                for frame in packet.decode():
                    yield frame
            else:
                yield None

    def get(self):
        return next(self.decoder)

    def reset_buffer(self):
        self.InputStream.close()
        self.InputStream = av.open(self.file_path)
        self.decoder = self.decode()