import math
import os
import random
import time

import numpy as np
import pyo

from apollo.media import Mediafile


def tryit(method):
    def exec(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except Exception as e:
            print(e)
            raise e

    return exec


def timeit(method):
    def exec(*args, **kwargs):
        try:
            t1 = time.time()
            method(*args, **kwargs)
            print(round(time.time() - t1, 5))
        except Exception as e:
            print(e)
            raise e

    return exec


class BufferTable:

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

        self.media = Mediafile(self.path)
        self.audio_decoder = self.media.Decoder
        self.time_length = round(math.ceil(float(self.media.Tags['length'])))
        self.buffer_virtual_length = round(int(self.media.Tags['samplerate']) * float(self.media.Tags['length']))

        self.buffer_time = 30
        self.buffer_length = int(self.media.Tags['samplerate']) * self.buffer_time
        self.indexes = pyo.Linseg([(0, 0), (self.buffer_time, 1)], loop = True)

        self.table = pyo.DataTable(self.buffer_length, chnls = 2, init = np.zeros((2, self.buffer_length)).tolist())
        self.shared_buffer = [np.asarray(self.table._base_objs[chnl].getTableStream()) for chnl in
                              range(self.table.chnls)]
        self.temp_buffer = np.asarray([np.asarray([]) for chnl in range(self.table.chnls)])

        self.reader = pyo.Pointer2(table = self.table, index = self.indexes).mix(2)

    def mapTimetoIndex(self, time: float) -> int:
        return int(self.buffer_length * time)

    @timeit
    def fetchMore(self):
        sample_diff = 4410
        if not hasattr(self, 'head_pos'):
            self.head_pos = 0
            # initilize and move ahead the initial samples
            self.writeSamples(self.getSamples())
            return None

        self.read_pos = self.mapTimetoIndex(self.indexes.get())

        if self.read_pos < self.head_pos and (abs(self.read_pos - self.head_pos) < sample_diff):
            self.writeSamples(self.getSamples())
        elif self.read_pos > self.head_pos:
            if not self.temp_buffer.shape[1] == 0:
                self.writeSamples(self.temp_buffer)
                self.temp_buffer = np.asarray([[] for chnl in range(self.table.chnls)])
            if (abs(self.read_pos - self.head_pos) > sample_diff):
                self.writeSamples(self.getSamples())
        else:
            pass

    def getSamples(self):
        array: np.ndarray = self.audio_decoder.get().to_ndarray()
        return array

    @timeit
    def writeSamples(self, samples):
        index = 0
        hasdump = False
        for chan in range(self.table.chnls):
            for index, sample in enumerate(samples[chan]):
                if (self.head_pos + index) < self.buffer_length:
                    self.shared_buffer[chan][self.head_pos + index] = sample
                    self.head_pos += 1
                else:
                    self.head_pos = 0
                    hasdump = True
                    break
        if hasdump:
            self.temp_buffer = np.asarray([samples[chan][index - 1:] for chan in range(self.table.chnls)])
        self.table.refreshView()

    def play(self):
        self.indexes.play()

    def pause(self):
        self.indexes.pause()

    def __del__(self) -> None:
        pass


class DSPInterface:

    def __init__(self, fadeout_time = 5) -> None:
        super().__init__()
        self.config_dict = {
            "fadeout_time": fadeout_time
        }
        self.server = pyo.Server(nchnls = 2, duplex = 0).boot()
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

    def replaceTable(self, path: str):
        if self.current_stream == 2:
            self.input_stream_1 = BufferTable(path)
            self.main_input.setInput(self.input_stream_1.reader, self.config_dict.get("fadeout_time"))
            self.input_stream_1.fetchMore()
            self.input_stream_1.play()
            self.current_stream = 1
            self.addToCallbackChain(self.input_stream_1.fetchMore)
            if hasattr(self, "input_stream_2"):
                self.popFromCallbackChain(self.input_stream_2.fetchMore)

        elif self.current_stream == 1:
            self.input_stream_2 = BufferTable(path)
            self.main_input.setInput(self.input_stream_2.reader, self.config_dict.get("fadeout_time"))
            self.input_stream_2.fetchMore()
            self.input_stream_2.play()
            self.current_stream = 2
            self.addToCallbackChain(self.input_stream_2.fetchMore)
            if hasattr(self, "input_stream_1"):
                self.popFromCallbackChain(self.input_stream_1.fetchMore)
            self.input_stream_2.table.graph()

    def init_processing_chain(self):
        # Creating Silent Input Stream
        self.current_stream = 1

        # Creating the main input fader; an entry point for multiple input feeds
        self.main_input = pyo.InputFader(pyo.Sine(freq = [0, 0]))

        self.main_output = pyo.Clip(self.main_input)

    def stop(self):
        self.server.stop()

    def exit(self):
        self.server.stop()

    def output(self):
        self.main_output.out()

    def GUI(self):
        self.spectrum = pyo.Spectrum(self.main_output)
        self.server.gui(globals())

    def ServerInfo(self):
        """
        Gets server and device info
        """
        info = {}
        info["pa_count_devices"] = pyo.pa_count_devices()
        info["pa_get_default_input"] = pyo.pa_get_default_input()
        info["pa_get_default_output"] = pyo.pa_get_default_output()
        info["pm_get_input_devices"] = pyo.pm_get_input_devices()
        info["pa_count_host_apis"] = pyo.pa_count_host_apis()
        info["pa_get_default_host_api"] = pyo.pa_get_default_host_api()
        info["pm_count_devices"] = pyo.pm_count_devices()
        info["pa_get_input_devices"] = pyo.pa_get_input_devices()
        info["pm_get_default_input"] = pyo.pm_get_default_input()
        info["pm_get_output_devices"] = pyo.pm_get_output_devices()
        info["pm_get_default_output"] = pyo.pm_get_default_output()
        info["pa_get_devices_infos"] = pyo.pa_get_devices_infos()
        info["pa_get_version"] = pyo.pa_get_version()
        info["pa_get_version_text"] = pyo.pa_get_version_text()
        return info


class Player:

    def __init__(self) -> None:
        self.dsp = DSPInterface(fadeout_time = 5)
        self.dsp.output()

    def load_track(self, path: str):
        if os.path.isfile(path):
            self.dsp.replaceTable(path)

    def play(self):
        self.dsp.server.start()

    def pause(self):
        self.dsp.server.stop()


if __name__ == '__main__':
    player = Player()
    player.load_track(r'D:\Music\fold_2\whenowhere.mp3')
    # player.load_track(r'D:\Music\fold_1\ff-16b-2c-44100hz.wav')
    player.dsp.GUI()
