import inspect
import itertools
import math
import sys
import traceback

import av
import numpy as np
import pyo

import apollo.utils
from apollo.media import Mediafile


class BufferTable:
    def __init__(self, path: str = None) -> None:
        super().__init__()
        self.sample_rate = 44100
        self.path = path
        self.read(path)

        self.buffer_time = 10
        self.buffer_length = int(44100) * self.buffer_time
        self.indexes = pyo.Linseg([(0, 0), (self.buffer_time * 1, self.buffer_length)], loop = True)
        self.table = pyo.DataTable(self.buffer_length, chnls = 2, init = np.zeros((2, self.buffer_length)).tolist())
        self.shared_buffer = self.getBuffer()
        self.reader = pyo.TableIndex(table = self.table, index = self.indexes)

    def read(self, path: str):
        if path is not None:
            self.media = Mediafile(path)
            self.audio_decoder = self.media.Decoder
            self.time_length = round(math.ceil(float(self.media.Tags['length'])))
            self.buffer_virtual_length = round(int(self.media.Tags['samplerate']) * float(self.media.Tags['length']))

        self.call_at_SOF()
        self.frame_pos = 0
        self.actual_pos = 0
        self.EOF = False
        self.isPlaying = False
        self.repeat = False

    def getBuffer(self):
        return [np.asarray(self.table._base_objs[chnl].getTableStream()) for chnl in range(self.table.chnls)]

    def fetchMore(self):
        if self.isPlaying:
            space = 4410
            if not hasattr(self, 'head_pos'):
                self.head_pos = 0
                # initilize and move ahead the initial samples
                if not self.writeSamples(self.getSamples()):
                    self.stop()
                return None

            self.read_pos = self.indexes.get()
            if (self.read_pos <= self.head_pos) and ((self.head_pos - self.read_pos) < space):
                if not self.writeSamples(self.getSamples()):
                    self.stop()
            elif (self.head_pos <= self.read_pos) and (self.buffer_length - (self.read_pos - self.head_pos) < space):
                if not self.writeSamples(self.getSamples()):
                    self.stop()
            else:
                return None

    def getSamples(self):
        if not self.EOF:
            array: av.audio.AudioFrame = self.audio_decoder.get()
            if array is not None:
                self.frame_pos = array.time
                return array.to_ndarray()
            else:
                self.call_at_EOF()
                self.EOF = True
                if self.repeat:
                    self.reset()
                    self.repeat = False
                return None

    def writeSamples(self, samples):
        if samples is not None:
            sample_len = len(samples[0])
            rng = range(self.head_pos, (self.head_pos + sample_len))
            for chan in range(self.table.chnls):
                if self.table.chnls == 1:
                    self.shared_buffer[chan].put(rng, samples[0], 'wrap')
                elif self.table.chnls == 2:
                    self.shared_buffer[chan].put(rng, samples[chan], 'wrap')
            if (self.head_pos + sample_len) < self.buffer_length:
                self.head_pos = self.head_pos + sample_len
            elif (self.head_pos + sample_len) > self.buffer_length:
                self.head_pos = (self.head_pos + sample_len) - self.buffer_length
            self.actual_pos += sample_len
            return True
        else:
            return False

    def seek(self, time):
        if (0 <= time) and (time) <= self.time_length:
            self.audio_decoder.seek(time)
            self.actual_pos = self.mapTimetoIndex(time)
        else:
            return None

    def play(self):
        self.isPlaying = True
        self.indexes.play()
        self.reader.play()

    def stop(self):
        self.isPlaying = False
        self.indexes.stop()
        self.reader.stop()

    def reset(self):
        self.call_at_SOF()
        self.frame_pos = 0
        self.audio_decoder.reset_buffer()
        self.clear()
        self.EOF = False

    def clear(self):
        for chan in range(self.table.chnls):
            self.shared_buffer[chan].fill(0)
        if hasattr(self, "head_pos"):
            del self.head_pos

    def mapIndextoTime(self, index: int, sr: int = 44100):
        time = int(index) / int(sr)
        return time

    def mapTimetoIndex(self, time: float, sr: int = 44100):
        time = int(time) * int(sr)
        return time

    def getCurrentTime(self):
        if not hasattr(self, 'head_pos'):
            return 0
        else:
            return self.mapIndextoTime(self.actual_pos)

    def time_to_end(self):
        if not hasattr(self, 'time_length'):
            return 0
        else:
            return self.time_length - self.mapIndextoTime(self.actual_pos, 44100)

    def getMediaFile(self):
        if hasattr(self, "media"):
            return self.media
        else:
            return None

    def call_at_EOF(self):
        ...

    def call_at_SOF(self):
        ...


class DSPInterface:

    def __init__(self) -> None:
        super().__init__()
        self.config_dict = {
            "fadeout_time": 5,
            "server_volume": 50,
        }
        self.server = pyo.Server(nchnls = 2, duplex = 0).boot()
        self.server.start()
        self.setVolume(self.config_dict.get("server_volume"))
        self.init_processing_chain()
        self.server.setCallback(self.server_callback)
        self.addToCallbackChain(self.check_for_end)
        self.addToCallbackChain(self.getCurrentStreamElapsedTime)

    def server_callback(self):
        for callback in self.callback_chain:
            try:
                callback()
            except Exception as e:
                print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))

    def addToCallbackChain(self, item):
        for index, callback in enumerate(self.callback_chain):
            if item == callback:
                self.callback_chain[index] = item
        else:
            self.callback_chain.append(item)

    def popFromCallbackChain(self, item):
        for index, callback in enumerate(self.callback_chain):
            if item == callback:
                self.callback_chain.pop(index)

    def init_processing_chain(self):
        # Creating the main input fader; an entry point for multiple input feeds
        self.callback_chain = []
        self.fader = pyo.Linseg([(0, 0), (self.config_dict.get('fadeout_time') + 0.5, 1)])
        self.fader_callback = pyo.TrigFunc(pyo.Thresh(self.fader, 0.99), self.remove_faded_table)
        self.input_stream_0 = BufferTable()
        self.input_stream_1 = BufferTable()
        self.voices = itertools.cycle([
            [(0, 1), (self.config_dict.get("fadeout_time"), 0)],
            [(0, 0), (self.config_dict.get("fadeout_time"), 1)]
        ])

        self.voice_switch = pyo.Linseg(next(self.voices))
        self.main_input = pyo.Selector([self.input_stream_0.reader, self.input_stream_1.reader], self.voice_switch)
        self.main_output = pyo.Clip(self.main_input)
        self.current_stream = 0
        self.current_stream_obj = None

    def remove_faded_table(self):
        if self.current_stream == 1 and hasattr(self, "input_stream_0"):
            self.popFromCallbackChain(self.input_stream_0.fetchMore)
            self.input_stream_0.stop()
        elif self.current_stream == 0 and hasattr(self, "input_stream_1"):
            self.popFromCallbackChain(self.input_stream_1.fetchMore)
            self.input_stream_1.stop()
        self.fader.stop()

    def replay_table(self):
        stream = self.get_active_stream()
        if stream is not None:
            stream.reset()
            stream.play()

    def get_active_stream(self) -> BufferTable:
        return self.current_stream_obj

    def replaceTable(self, path: str, instant = False):
        if instant:
            self.remove_faded_table()

        if self.current_stream == 0 and hasattr(self, "input_stream_0"):
            stream = self.input_stream_1
            self.current_stream = 1
            self.current_stream_obj = stream
        elif self.current_stream == 1 and hasattr(self, "input_stream_1"):
            stream = self.input_stream_0
            self.current_stream = 0
            self.current_stream_obj = stream
        else:
            return None
        # manage then input switch rest works
        if stream is not None:
            self.voice_switch.setList(next(self.voices))
            stream.clear()
            stream.read(path)
            stream.fetchMore()
            stream.play()
            self.addToCallbackChain(stream.fetchMore)

        if instant:
            self.fader.replace([(0, 0), (self.config_dict.get('fadeout_time') + 0.5, 1)])
            self.main_input.setVoice(self.current_stream)
        else:
            self.main_input.setVoice(self.voice_switch)
            self.fader.play()
            self.voice_switch.play()

    def check_for_end(self):
        stream = self.get_active_stream()
        if stream is not None:
            switch = (0 < (self.config_dict.get("fadeout_time") - (stream.time_to_end())) <= 0.1)
            if switch and (not self.fader.isPlaying()):
                self.call_at_EOF()

    def seek(self, time):
        stream = self.get_active_stream()
        if stream is not None:
            stream.seek(float(time / 100))

    def getCurrentStreamElapsedTime(self):
        stream = self.get_active_stream()
        if stream is not None:
            self.call_for_ElapsedTime(float(stream.getCurrentTime()))

    def stop(self):
        self.server.stop()

    def exit(self):
        self.server.stop()

    def output(self):
        self.main_output.out()

    def GUI(self, vars):
        self.spectrum = pyo.Spectrum(self.main_output)
        self.server.gui(vars)

    def ServerInfo(self):
        info = dict(
                pa_count_devices = pyo.pa_count_devices(),
                pa_get_default_input = pyo.pa_get_default_input(),
                pa_get_default_output = pyo.pa_get_default_output(),
                pm_get_input_devices = pyo.pm_get_input_devices(),
                pa_count_host_apis = pyo.pa_count_host_apis(),
                pa_get_default_host_api = pyo.pa_get_default_host_api(),
                pm_count_devices = pyo.pm_count_devices(),
                pa_get_input_devices = pyo.pa_get_input_devices(),
                pm_get_default_input = pyo.pm_get_default_input(),
                pm_get_output_devices = pyo.pm_get_output_devices(),
                pm_get_default_output = pyo.pm_get_default_output(),
                pa_get_devices_infos = pyo.pa_get_devices_infos(),
                pa_get_version = pyo.pa_get_version(),
                pa_get_version_text = pyo.pa_get_version_text()
        )
        return info

    def setVolume(self, value: int):
        value = ((2 * pow(value, 2)) / 100) * 0.01
        self.server.setAmp(value if value >= 0.0001 else 0.0001)

    def call_at_EOF(self):
        ...

    def call_for_ElapsedTime(self, time: float):
        ...
