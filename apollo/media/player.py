import math
import os
import random
import sys
import time
import traceback

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

        self.media = Mediafile(self.path)
        self.audio_decoder = self.media.Decoder
        self.time_length = round(math.ceil(float(self.media.Tags['length'])))
        self.buffer_virtual_length = round(int(self.media.Tags['samplerate']) * float(self.media.Tags['length']))

        self.buffer_time = 10
        self.buffer_length = int(self.media.Tags['samplerate']) * self.buffer_time
        self.indexes = pyo.Linseg([(0, 0), (self.buffer_time * 1, self.buffer_length)], loop = True)

        self.table = pyo.DataTable(self.buffer_length, chnls = 2, init = np.zeros((2, self.buffer_length)).tolist())
        self.shared_buffer = self.getBuffer()

        self.reader = pyo.TableIndex(table = self.table, index = self.indexes).mix(2)
        self.EOF = False

    def getBuffer(self):
        return [np.asarray(self.table._base_objs[chnl].getTableStream()) for chnl in range(self.table.chnls)]

    def mapTimetoIndex(self, time: float) -> int:
        return int(self.buffer_length * time)

    def fetchMore(self):
        if self.indexes.isPlaying():
            space = 4410
            if not hasattr(self, 'head_pos'):
                self.head_pos = 0
                # initilize and move ahead the initial samples
                self.writeSamples(self.getSamples())
                return None

            self.read_pos = self.indexes.get()
            if (self.read_pos <= self.head_pos) and ((self.head_pos - self.read_pos) < space):
                if not self.writeSamples(self.getSamples()):
                    self.pause()
            elif (self.head_pos <= self.read_pos) and (self.buffer_length - (self.read_pos - self.head_pos) < space):
                if not self.writeSamples(self.getSamples()):
                    self.pause()
            else:
                return None

    def getSamples(self):
        if not self.EOF:
            array: np.ndarray = self.audio_decoder.get()
            if array is not None:
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

    def play(self):
        self.indexes.play()
        self.reader.play()

    def pause(self):
        self.indexes.pause()
        self.reader.stop()

    def reset(self):
        self.audio_decoder.reset_buffer()
        for chan in range(self.table.chnls):
            self.shared_buffer[chan].put(range(0, self.buffer_length), np.zeros(self.buffer_length), 'wrap')
        self.EOF = False

    def __del__(self) -> None:
        self.pause()
        del self.table
        del self.shared_buffer
        del self.audio_decoder


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

    def replaceTable(self, path: str):
        # manage then input switch rest works
        if self.current_stream == 2:
            self.input_stream_1 = BufferTable(path)
            self.input_stream_1.fetchMore()
            self.input_stream_1.play()
            self.current_stream = 1
            self.addToCallbackChain(self.input_stream_1.fetchMore)

            self.main_input.setInputs([self.input_stream_2, self.input_stream_1])
            self.main_input.setVoice(self.fader.play())

        elif self.current_stream == 1:
            self.input_stream_2 = BufferTable(path)
            self.input_stream_2.fetchMore()
            self.input_stream_2.play()
            self.current_stream = 2
            self.addToCallbackChain(self.input_stream_2.fetchMore)

            self.main_input.setInputs([self.input_stream_1, self.input_stream_2])
            self.main_input.setVoice(self.fader.play())

    def init_processing_chain(self):
        # Creating Silent Input Stream
        self.input_stream_2 = pyo.Sine(freq = [1000, 1000])
        self.input_stream_1 = pyo.Sine(freq = [100, 100])
        self.current_stream = 1

        # Creating the main input fader; an entry point for multiple input feeds
        self.fader = pyo.Fader(fadein = 0.5, fadeout = 3, dur = self.config_dict.get("fadeout_time"))
        self.fader_callback = pyo.TrigFunc(self.fader, self.remove_faded_table)

        self.main_input = pyo.Selector([self.input_stream_1, self.input_stream_2])
        self.main_output = pyo.Clip(self.main_input)

    def remove_faded_table(self):
        if hasattr(self, "input_stream_2"):
            if not isinstance(self.input_stream_2, pyo.Sine):
                self.popFromCallbackChain(self.input_stream_2.fetchMore)
                del self.input_stream_2
                self.input_stream_2 = pyo.Sine(freq = [0, 0]).stop()
        if hasattr(self, "input_stream_1"):
            if not isinstance(self.input_stream_1, pyo.Sine):
                self.popFromCallbackChain(self.input_stream_1.fetchMore)
                del self.input_stream_1
                self.input_stream_1 = pyo.Sine(freq = [0, 0]).stop()
        self.fader.stop()

    def replay_table(self):
        if hasattr(self, "input_stream_1"):
            self.input_stream_1.reset()
            self.input_stream_1.play()
        elif hasattr(self, "input_stream_2"):
            self.input_stream_2.reset()
            self.input_stream_2.play()

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


class Player:

    def __init__(self) -> None:
        self.dsp = DSPInterface(fadeout_time = 5)
        self.dsp.output()

    def load_track(self, path: str):
        if os.path.isfile(path):
            self.dsp.replaceTable(path)

    def reload_track(self):
        self.dsp.replay_table()

    def play(self):
        self.dsp.server.start()

    def pause(self):
        self.dsp.server.stop()


if __name__ == '__main__':
    player = Player()
    player.load_track(r'D:\Music\fold_2\whenowhere30.mp3')
    # player.load_track(r'D:\Music\fold_2\ff-16b-2c-44100hz.mp3')
    # player.load_track(r'D:\Music\fold_1\ff-16b-2c-44100hz.wav')
    player.dsp.GUI()
