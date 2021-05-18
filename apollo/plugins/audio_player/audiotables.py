import time, os, sys, argparse, queue, threading
from pprint import pprint

import pyo, av
from pyo._pyo import DataTable_base
import numpy as np


class AudioTable(pyo.DataTable):

    def __init__(self, duration, sample_rate = 44100, channels = 2):
        """
        Info: Audio Table to store decoded audio channels.
        Args:
        duration: int
            -> duration of table in seconds
        sample_rate: int
            -> samplerate of the table
        channels: int
            -> cannels of audio

        Returns: None
        Errors: None
        """
        super().__init__(int(duration * sample_rate), channels)
        self.cursor = 0

    def put(self, array, pos):
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
        array_channels = array.shape[0]
        if array_channels == self._chnls:
            # noramal one to one cration of channels
            for obj, samples in zip(self._base_objs, array):
                cursor = pos
                for sample in samples:
                    obj.put(sample, cursor)
                    cursor += 1
            self.cursor = cursor

        elif (array_channels == 1) and (self._chnls == 2):
            # for mono audio copies on both channels same audio and converts to dual
            for obj in self._base_objs:
                cursor = pos
                for sample in array:
                    obj.put(sample, cursor)
                    cursor += 1
            self.cursor = cursor

        # 2.1 channel audio support
        # 5.1 channel audio support
        # 7.1 channel audio support

        else:
            raise Exception("Audio Channels Not Compatable")

    def extend(self, array):
        self.put(array, self.cursor)

    def getTable(self):
        """
        Info: returns the table as a python list
        Args: None
        Returns: list
        Errors: None
        """
        return [obj.getTable() for obj in self._base_objs]


class AudioTable_Reader: ...


if __name__ == "__main__":
    Server = pyo.Server().boot()
    INST = AudioTable(30)
    INST.extend(np.ones([2, 44100]))
    INST.extend(np.ones([2, 44100]) / 2)
    INST.extend(np.ones([2, 44100]) / 4)
    INST.extend(np.ones([2, 44100]) / 8)
    INST.view()
    reader = pyo.TableRead(INST, INST.getRate())
    reader.out()

    Server.gui(locals())

