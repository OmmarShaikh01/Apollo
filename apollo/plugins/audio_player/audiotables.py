from apollo.utils import exe_time

import time, os, sys, argparse, queue, threading
from pprint import pprint

import pyo, av
import numpy as np


"""
Plugin Support:
# Bitrate:P
    -> 44100
# Formats:
    -> .mp3
# Channels:
    -> 2
"""

class AudioDecoder(threading.Thread):
    """
    Info: Main Interface to access all audio deccoders.
    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self, stream, buffer = None):
        """
        Info: Constructor
        Args: None
        Returns: None
        Errors: None
        """
        super().__init__()
        self.ThreadState = "ACTIVE"
        self.InputStream = stream
        self.AudioTable = buffer
        self.start()

    def run(self):
        """
        Info: threade runner
        Args: None
        Returns: None
        Errors: None
        """
        while self.ThreadState != "EXIT":
            if self.ThreadState == "DECODE":
                self.__decode()
            else:
                time.sleep(0.01)

    def stop(self):
        """
        Info: thread exit
        Args: None
        Returns: None
        Errors: None
        """
        self.ThreadState = "EXIT"

    def decode(self):
        """
        Info: sets the decoder flag for the thread to execute
        Args:
        callback:
            -> function to call after each frame is decoded

        Returns: None
        Errors: None`
        """
        self.ThreadState = "DECODE"
        return self

    @exe_time
    def __decode(self):
        """
        Info: Audio Decoder
        Args: None
        Returns: None
        Errors: None`
        """
        # variable Declaration
        self.ThreadState = "DECODING"

        # actual decoding and demuxing of file
        for packet in self.InputStream.demux(audio = 0):
            if not(packet.size <= 0):
                for frame in packet.decode():
                    self.AudioTable.extend(frame.to_ndarray())

        self.ThreadState = "DECODED"


class AudioTable(pyo.DataTable):

    def __init__(self, path, duration = None):
        """
        Info: Audio Table to store decoded audio channels.
        Args:
        path: string
            -> path to read file from
        duration: int
            -> duration of table in seconds
        sample_rate: int
            -> samplerate of the table
        channels: int
            -> cannels of audio

        Returns: None
        Errors: None
        """
        if path != None and os.path.isfile(path):
            self.CurrentFile = path
            self.InputStream = av.open(path)
            self.Decoder = AudioDecoder(self.InputStream, self)
        else:
            raise FileNotFoundError

        if duration is None:
            if path is not None:
                self.duration = int(self.InputStream.duration / 100000)
        else:
            self.duration = 30

        self.sample_rate = 44100
        self.channels = 2
        self.cursor = 0
        super().__init__(int(self.duration * self.sample_rate), self.channels)

    def decode(self):
        self.Decoder.decode()
        return self

    def write(self, array, pos):
        """
        Info: Adds given samples to the audio table.
        Args:
        array: np.array
            -> array that contains audio samples
        pos: int
            -> pos to add samples to

        Returns: None
        Errors: None
        """
        def FillSamples(obj, samples, cursor):
            for sample in samples:
                obj.put(sample, cursor)
                cursor += 1
            return cursor

        array_channels = array.shape[0]

        # noramal one to one cration of channels
        if array_channels == self._chnls:
            for index, obj in enumerate(self._base_objs):
                self.cursor = FillSamples(obj, array[index], pos)

        # for mono audio copies on both channels same audio and converts to dual
        elif (array_channels == 1) and (self._chnls == 2):
            for obj in self._base_objs:
                self.cursor = FillSamples(obj, array[0], pos)

        # 2.1 channel audio support
        # 5.1 channel audio support
        # 7.1 channel audio support

        else:
            raise Exception("Audio Channels Not Compatable")

    def extend(self, array):
        self.write(array, self.cursor)

    def seek(self, time):
        TIMEBASE_SEC = 0.026122448979591838
        TIMEBASE_PTS = 368640

        self.InputStream
        return (int((time / TIMEBASE_SEC) + 1) * TIMEBASE_PTS)

    def getTable(self):
        """
        Info: returns the table as a python list
        Args: None
        Returns: list
        Errors: None
        """
        return np.array([obj.getTable() for obj in self._base_objs])

    def exit(self):
        self.InputStream.close()
        self.Decoder.stop()

class AudioTable_Reader: ...


if __name__ == "__main__":
    from random import randint
    Server = pyo.Server().boot()

    INST = AudioTable("D:\\music\\mosesdt.mp3").decode()
    tablereader = pyo.TableRead(INST, INST.getRate()).out()
    Server.start()
    Server.setAmp(0.1)
    Server.gui(locals())
