import itertools
import math
import os
import sys
import traceback
from typing import Optional, Union

import av
import numpy as np
import pyo

import apollo.utils
from apollo.media import Mediafile
from apollo.utils import ApolloSignal


class BufferTable:
    """
    Circular Audio Buffer to put and read audio samples.
    """

    EOF_SIGNAL = ApolloSignal()
    SOF_SIGNAL = ApolloSignal()
    STOP_SIGNAL = ApolloSignal()
    PLAY_SIGNAL = ApolloSignal()

    def __init__(
        self,
        time: float,
        path: Optional[str] = None,
        chnls: Optional[int] = 2,
        sr: Optional[int] = 44100,
    ):
        """
        Constructor

        Args:
            time (float): Audio buffer time
            path (str): path of the file to read samples from
            chnls (int): channels of the audio table
            sr (int): sampling rate
        """
        self.buffer_time = time
        self.chnls = chnls
        self.sample_rate = sr
        self.path = path

        self.buffer_sample_length = int(self.sample_rate) * self.buffer_time
        self.table = pyo.DataTable(self.buffer_sample_length, chnls=self.chnls)
        self.shared_buffer = self.getBuffer()
        self.indexes = pyo.Linseg(
            [(0, 0), (self.buffer_time * 1, self.buffer_sample_length)], loop=True
        )
        self.reader = pyo.TableIndex(table=self.table, index=self.indexes)

        if path is not None:
            self.read(path)
        else:
            self.media = None
            self.audio_decoder = None
            self.time_length = 0
            self.buffer_virtual_length = 0

            self.frame_pos = 0
            self.actual_pos = 0
            self.EOF = False
            self.isPlaying = False
            self.repeat = False

    def read(self, path: str):
        """
        Reads the audio file and creates a decoded samples generator object

        Args:
            path (str): path to the audio file
        """
        self.media = Mediafile(path)
        self.audio_decoder = self.media.Decoder
        self.time_length = round(math.ceil(float(self.media.Tags["length"])))
        self.buffer_virtual_length = round(
            int(self.media.Tags["samplerate"]) * float(self.media.Tags["length"])
        )

        # Resets all flags
        self.frame_pos = 0
        self.actual_pos = 0
        self.EOF = False
        self.isPlaying = False
        self.repeat = False

        self.SOF_SIGNAL.emit(self.media)

    def getBuffer(self) -> list[np.array]:
        """Initializes the shared buffer to write to"""
        # noinspection PyProtectedMember
        return [
            np.asarray(self.table._base_objs[chnl].getTableStream()) for chnl in range(self.chnls)
        ]

    def getSamples(self) -> Union[np.array, None]:
        """
        Gets sample arrays from the decoder

        Returns:
            Union[np.array, None]: numpy array filled of samples
        """
        if not self.EOF:
            array: av.audio.AudioFrame = self.audio_decoder.get()
            if array is not None:
                self.frame_pos = array.time
                return array.to_ndarray()
            else:
                self.EOF_SIGNAL.emit()
                self.EOF = True
                if self.repeat:
                    self.reset()
                    self.repeat = False
                return None

    def writeSamples(self, samples: np.array) -> bool:
        """
        Writes the fetched samples to the next available position.

        Args:
            samples (np.array): samples to write

        Returns:
            bool: if written true, otherwise false
        """
        if samples is not None:
            sample_len = len(samples[0])
            rng = range(self.write_pos, (self.write_pos + sample_len))

            for chan in range(self.table.chnls):
                # converts mono audio into stereo channel
                if self.table.chnls == 1:
                    self.shared_buffer[chan].put(rng, samples[0], "wrap")
                # stereo audio
                elif self.table.chnls == 2:
                    self.shared_buffer[chan].put(rng, samples[chan], "wrap")

            # updates the head position
            if (self.write_pos + sample_len) < self.buffer_sample_length:
                self.write_pos = self.write_pos + sample_len
            elif (self.write_pos + sample_len) > self.buffer_sample_length:
                self.write_pos = (self.write_pos + sample_len) - self.buffer_sample_length
            self.actual_pos += sample_len

            return True
        else:
            return False

    def fetchMore(self):
        """
        Callback to fetch and  write more samples into the buffer
        """
        if self.isPlaying:
            space = self.sample_rate / 10
            # initialize and move ahead the initial samples
            if not hasattr(self, "write_pos"):
                self.write_pos = 0
                self.writeSamples(self.getSamples())
                if not self.writeSamples(self.getSamples()):
                    self.stop()
                return None

            self.read_pos = self.indexes.get()  # gets the read head position in samples

            if (self.read_pos <= self.write_pos) and ((self.write_pos - self.read_pos) < space):
                if not self.writeSamples(self.getSamples()):
                    self.stop()
            elif (self.write_pos <= self.read_pos) and (
                self.buffer_sample_length - (self.read_pos - self.write_pos) < space
            ):
                if not self.writeSamples(self.getSamples()):
                    self.stop()
            else:
                return None

    def seek(self, time: float):
        """
        Seeks to a time stamp on the audio file

        Args:
            time (float): time to seek to
        """
        if 0 <= time <= self.time_length:
            self.audio_decoder.seek(time)
            self.actual_pos = self.map_time_toindex(time)
        else:
            return None

    def play(self):
        """starts playing the audio reader"""
        self.isPlaying = True
        self.indexes.play()
        self.reader.play()
        self.PLAY_SIGNAL.emit()

    def stop(self):
        """stops playing the audio reader"""
        self.isPlaying = False
        self.indexes.stop()
        self.reader.stop()
        self.STOP_SIGNAL.emit()

    def reset(self):
        """resets the audio buffer and decoder"""
        self.SOF_SIGNAL.emit(self.media)
        self.frame_pos = 0
        self.audio_decoder.reset_buffer()
        self.clear()
        self.EOF = False
        if hasattr(self, "write_pos"):
            del self.write_pos

    def clear(self):
        """clears the audio buffer"""
        for chan in range(self.table.chnls):
            self.shared_buffer[chan].fill(0)
        if hasattr(self, "write_pos"):
            del self.write_pos

    def time_to_end(self) -> float:
        """
        Time till EOF

        Returns:
            float: Time till EOF
        """
        if not hasattr(self, "time_length"):
            return 0
        else:
            return self.time_length - self.map_index_totime(self.actual_pos, 44100)

    def getCurrentTime(self) -> float:
        """
        Gets current time of the writer head

        Returns:
            float: current time of the writer head
        """
        if not hasattr(self, "write_pos"):
            return 0
        else:
            return self.map_index_totime(self.actual_pos)

    def getMediaFile(self) -> Union[Mediafile, None]:
        """
        Gets the currently loaded media file

        Returns:
            Union[Mediafile, None]: currently loaded media file
        """
        if hasattr(self, "media"):
            return self.media
        else:
            return None

    @staticmethod
    def map_index_totime(index: int, sr: int = 44100) -> float:
        """
        maps index to time

        Args:
            index (int): index value corresponding to sample-rate
            sr (int): sample-rate

        Returns:
            float: corresponding time stamp
        """
        time = int(index) / int(sr)
        return time

    @staticmethod
    def map_time_toindex(time: float, sr: int = 44100) -> int:
        """
        maps time to index

        Args:
            time (float): time value corresponding to index
            sr (int): sample-rate

        Returns:
            int: corresponding index
        """
        index = int(time) * int(sr)
        return index


class DynamicProcessingChain:
    """
    Dynamic Processing chain that handles all the DSP based functions.
    """

    FADED = ApolloSignal()
    STREAM_ABOUT_TOEND = ApolloSignal()
    STREAM_ELAPSEDTIME = ApolloSignal()

    def __init__(self):
        """Constructor"""
        # main fading envelope
        self.env_time = 5
        self.repeat_current_buffer = False
        self.stream_reset = False
        self.voices = itertools.cycle([[(0, 1), (self.env_time, 0)], [(0, 0), (self.env_time, 1)]])
        self.voice_switch = pyo.Linseg(next(self.voices))
        self.loaded_stream = 0

        # corresponding fader to notify end of a fading env
        self.fader = pyo.Linseg([(0, 0), (self.env_time + 0.5, 1)])
        self.fader_callback = pyo.TrigFunc(
            pyo.Thresh(self.fader, 0.99), (lambda: self.FADED.emit())
        )

        # top level processing chain
        self.input_stream_0, self.input_stream_1 = BufferTable(10), BufferTable(10)
        self.main_input = pyo.Selector(
            [self.input_stream_0.reader, self.input_stream_1.reader], self.voice_switch
        )
        self.main_bypass = pyo.Selector([pyo.Sine(freq=0), self.main_input], 1)
        self.main_output = pyo.Clip(self.main_bypass).out()

    def set_fade_env(self, time: float):
        """
        Sets the cross fading Envelope

        Args:
            time (float): envelope time
        """
        self.env_time = time
        self.voices = itertools.cycle([[(0, 1), (time, 0)], [(0, 0), (time, 1)]])
        self.fader.setList([(0, 0), (time + 0.5, 1)])

    def set_bypass(self, bypass: bool):
        """
        Bypasses the processing chain and plays buffers without any post-processing

        Args:
            bypass (bool): Bypasses the processing chain and plays buffer directly
        """
        if bypass:
            self.main_bypass.setVoice(1)
        else:
            self.main_bypass.setVoice(0)

    def load_track(self, path: str, instant: bool = True):
        """
        Loads the track into the buffer and cross-fades between both

        Args:
            path (str): path to read into an audio buffer
            instant (bool): instantly switches between the audio buffer rather than cross-fading.
        """
        if self.loaded_stream == 0:
            stream = self.input_stream_1
            self.loaded_stream = 1
        else:
            stream = self.input_stream_0
            self.loaded_stream = 0

        # manages the stream loading
        if stream is not None:
            stream.clear()
            stream.read(path)
            stream.fetchMore()
            stream.play()
            self.stream_reset = False
            self.voice_switch.setList(next(self.voices))

        # manages the cross-fading
        if instant:
            self.fader.replace([(0, 0), (self.env_time + 0.5, 1)])
            self.main_input.setVoice(self.loaded_stream)
            self.stop_faded_table()
        else:
            self.main_input.setVoice(self.voice_switch)
            self.fader.play()
            self.voice_switch.play()

    def stop_faded_table(self):
        """stops the secondary table"""
        if self.loaded_stream == 1:
            self.input_stream_0.stop()
        elif self.loaded_stream == 0:
            self.input_stream_1.stop()
        self.fader.stop()

    def recurring_server_callback(self):
        """recurring callback attached to server. executed each time new samples are loaded"""
        self.check_stream_end()
        self.fetch_samples_intoStreams()

    def fetch_samples_intoStreams(self):
        """fetches new samples from a decoder into the playing buffer"""
        if self.input_stream_0.isPlaying:
            self.input_stream_0.fetchMore()
        if self.input_stream_1.isPlaying:
            self.input_stream_1.fetchMore()

    def check_stream_end(self):
        """checks for the EOF of the stream in time elapsed"""
        stream = self.active_stream
        self.STREAM_ELAPSEDTIME.emit(float(stream.getCurrentTime()))
        if 0 < (self.env_time - (stream.time_to_end())) <= 0.1:
            if self.repeat_current_buffer and not self.stream_reset:
                self.replay()
            elif not self.fader.isPlaying():
                self.STREAM_ABOUT_TOEND.emit()

    def replay(self):
        """replays the actively playing stream"""
        stream = self.active_stream
        self.stream_reset = True
        stream.reset()
        stream.play()

    def play(self):
        """starts the processing"""
        return self.main_output.play()

    def stop(self):
        """stops the processing"""
        return self.main_output.stop()

    def output_sprectrum(self):
        """render the audio spectrum"""
        # noinspection PyAttributeOutsideInit
        self.spectrum_1 = pyo.Spectrum(self.main_output)

    @property
    def active_stream(self) -> BufferTable:
        """
        Returns the Primary audio buffer

        Returns:
            (BufferTable): Primary Audio Buffer
        """
        if self.loaded_stream == 0:
            return self.input_stream_0
        else:
            return self.input_stream_1


if __name__ == "__main__":
    player = pyo.Server().boot().start()
    chain = DynamicProcessingChain()
    chain.main_output.out()
    player.setCallback(chain.recurring_server_callback)
    chain.load_track(r"D:\Music\03. Crown.mp3")
    player.gui(locals())
