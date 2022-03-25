import itertools
import math
import sys
import time
import traceback

import av
import numpy as np
import pyo

from apollo.media import Mediafile


def tryit(method):
    def exec(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except Exception as e:
            print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
            raise e

    return exec


def timeit(method):
    def exec(*args, **kwargs):
        try:
            t1 = time.time()
            method(*args, **kwargs)
            print(round(time.time() - t1, 8))
        except Exception as e:
            print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
            raise e

    return exec


class BufferTable:

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
        self.read(path)

        self.buffer_time = 10
        self.buffer_length = int(self.media.Tags['samplerate']) * self.buffer_time
        self.indexes = pyo.Linseg([(0, 0), (self.buffer_time * 1, self.buffer_length)], loop = True)

        self.table = pyo.DataTable(self.buffer_length, chnls = 2, init = np.zeros((2, self.buffer_length)).tolist())
        self.shared_buffer = self.getBuffer()

        self.reader = pyo.TableIndex(table = self.table, index = self.indexes)

    def read(self, path: str):
        self.media = Mediafile(self.path)
        self.audio_decoder = self.media.Decoder
        self.frame_pos = 0
        self.time_length = round(math.ceil(float(self.media.Tags['length'])))
        self.buffer_virtual_length = round(int(self.media.Tags['samplerate']) * float(self.media.Tags['length']))

        self.EOF = False
        self.isPlaying = False

    def getBuffer(self):
        return [np.asarray(self.table._base_objs[chnl].getTableStream()) for chnl in range(self.table.chnls)]

    def fetchMore(self):
        if self.isPlaying:
            space = 4410
            if not hasattr(self, 'head_pos'):
                self.head_pos = 0
                # initilize and move ahead the initial samples
                self.writeSamples(self.getSamples())
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
                self.EOF = True
                return None

    def writeSamples(self, samples):
        if samples is not None:
            sample_len = len(samples[0])
            for chan in range(self.table.chnls):
                self.shared_buffer[chan].put(range(self.head_pos, (self.head_pos + sample_len)), samples[chan], 'wrap')
            if (self.head_pos + sample_len) < self.buffer_length:
                self.head_pos = self.head_pos + sample_len
            elif (self.head_pos + sample_len) > self.buffer_length:
                self.head_pos = (self.head_pos + sample_len) - self.buffer_length
            return True
        else:
            return False

    def seek(self, time):
        cur_time = self.frame_pos
        if (0 <= time) and (cur_time + time) <= self.time_length:
            self.audio_decoder.seek(cur_time + time)
        elif (time <= 0) and 0 <= (cur_time + time) <= self.time_length:
            self.audio_decoder.seek(cur_time + time)
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
        self.frame_pos = 0
        self.audio_decoder.reset_buffer()
        for chan in range(self.table.chnls):
            self.shared_buffer[chan].put(range(0, self.buffer_length), np.zeros(self.buffer_length), 'wrap')
        self.EOF = False

    def clear(self):
        for chan in range(self.table.chnls):
            self.shared_buffer[chan].put(range(0, self.buffer_length), np.zeros(self.buffer_length), 'wrap')

    def mapIndextoTime(self, index: int, sr: int):
        time = int(index) / int(sr)
        return time


class DSPInterface:

    def __init__(self, fadeout_time = 5) -> None:
        super().__init__()
        self.config_dict = {
            "fadeout_time": fadeout_time
        }
        self.server = pyo.Server(nchnls = 2, duplex = 0).boot()
        self.server.setAmp(0.0001)
        self.server.start()
        self.init_processing_chain()
        self.server.setCallback(self.server_callback)

    def server_callback(self):
        if not hasattr(self, 'callback_chain'):
            self.callback_chain = []
        for callback in self.callback_chain:
            callback()

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
        self.fader = pyo.Linseg([(0, 0), (self.config_dict.get('fadeout_time') + 0.5, 1)])
        self.fader_callback = pyo.TrigFunc(pyo.Thresh(self.fader, 0.99), self.remove_faded_table)
        self.voices = itertools.cycle([
            [(0, 0), (self.config_dict.get("fadeout_time"), 1)],
            [(0, 1), (self.config_dict.get("fadeout_time"), 0)],
        ])
        self.voice_switch = pyo.Linseg(next(self.voices))
        self.main_input = pyo.Selector([pyo.Sine([0, 0]), pyo.Sine([0, 0])], self.voice_switch)
        self.main_output = pyo.Clip(self.main_input)
        self.current_stream = 1

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
        if self.current_stream == 0 and hasattr(self, "input_stream_0"):
            return self.input_stream_0
        elif self.current_stream == 1 and hasattr(self, "input_stream_1"):
            return self.input_stream_1
        else:
            return None

    def replaceTable(self, path: str):
        # manage then input switch rest works
        if self.current_stream == 1:
            if not hasattr(self, "input_stream_0"):
                self.input_stream_0 = BufferTable(path)
            else:
                self.input_stream_1.clear()
                self.input_stream_0.read(path)
            self.input_stream_0.fetchMore()
            self.input_stream_0.play()
            self.current_stream = 0
            self.addToCallbackChain(self.input_stream_0.fetchMore)

        elif self.current_stream == 0:
            if not hasattr(self, "input_stream_1"):
                self.input_stream_1 = BufferTable(path)
            else:
                self.input_stream_1.clear()
                self.input_stream_1.read(path)
            self.input_stream_1.fetchMore()
            self.input_stream_1.play()
            self.current_stream = 1
            self.addToCallbackChain(self.input_stream_1.fetchMore)

        if hasattr(self, "input_stream_0") and hasattr(self, "input_stream_1"):
            self.main_input.setInputs([self.input_stream_0.reader, self.input_stream_1.reader])
        else:
            self.main_input.setInputs([self.input_stream_0.reader, pyo.Sine([0, 0])])

        self.voice_switch.setList(next(self.voices))
        self.voice_switch.play()
        self.fader.play()

    def seek(self, time):
        stream = self.get_active_stream()
        if stream is not None:
            stream.seek(time)

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
