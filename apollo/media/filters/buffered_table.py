from __future__ import annotations

import logging
import os.path
from pathlib import PurePath
from typing import Union

import av
import numpy as np
import pyo

from apollo.media import Mediafile
from apollo.utils import ApolloWarning, get_logger
from configs import settings as CONFIG


LOGGER = get_logger(__name__)
DEBUG = bool(LOGGER.level == logging.DEBUG)


class Buffered_Audio_Stream:
    """
    Buffered_Audio_Stream
    """

    def __init__(self, buffer_size: int = 10, chnls: int = 2):
        self.buffer_size = buffer_size
        self.chnls = chnls
        self.sr = CONFIG["SERVER.RATE"]
        self._pitch_scaling = 2  # scaling the time to keep correct pitch of the stream

        # CHANGES WHEN BUFFER IS RESET
        self._loaded_track: Union[str, PurePath, None] = None
        self.media_file: Union[Mediafile, None] = None
        self.decoder_eof = False  # notifies when decoder has no more smaples to decoder
        self.eof_approaching_raised = False  # notifies when decoder has no more smaples to decoder
        self._memorized_pos = 0  # only used to track index changes
        self._writeahead_duration = 1000  # samples between the read and write ahead
        self._read_head_pos = 0  # Read Head position
        self._write_head_pos = 0  # Write Head position

        # DATA TABLE CONTROLLER AND PLAYER
        self._data_table = pyo.DataTable(size=buffer_size * self.sr, chnls=chnls)
        self._data_table_index = pyo.Linseg(
            [(0, 0), (buffer_size / self._pitch_scaling, 1)], loop=True
        )
        self._data_table_reader = pyo.Pointer2(self._data_table, self._data_table_index)
        self._data_table_write_trig = pyo.TrigFunc(
            pyo.Change(self._data_table_index), self._cb_on_lineseg_value_change
        )
        self._shared_data_array = self.get_buffer()

    def load_track(self, file_path: Union[str, PurePath]):
        """
        Load track and initilizes decoder

        Args:
            file_path (Union[str, PurePath]): file to decode
        """
        if isinstance(file_path, str):
            file_path = PurePath(file_path)

        if os.path.isfile(file_path) and Mediafile.isSupported(file_path):
            self.stop()
            self.clear()

            self._loaded_track = file_path
            self.decoder_eof = False
            self.eof_approaching_raised = False
            self.media_file = Mediafile(file_path)
            self.fetch_more()

            self.play()
        else:
            msg = f"Tried to Load Unsupported File Format '{os.path.splitext(file_path)[1]}'"
            ApolloWarning(msg)

    def reload(self):
        """
        Reloads the last played track
        """
        self.load_track(self._loaded_track)

    def get_buffer(self) -> list:
        """
        Gets the shared memory buffer

        Returns:
            list: shared memory buffer
        """
        # noinspection PyProtectedMember
        # pylint: disable=protected-access
        return [
            np.asarray(self._data_table._base_objs[chnl].getTableStream())
            for chnl in range(self.chnls)
        ]

    def seek(self, time: Union[int, float]):
        """
        Seeks the read pointer to a time stamp

        Args:
            time (Union[int, float]): time stamp to seek to
        """
        total_time = self.media_file.SynthTags.get("SONGLEN", 0)[0]
        if 0 <= time <= total_time:
            self._read_head_pos = time * self.sr * self._pitch_scaling
            self.media_file.Decoder.seek(time)
            if not self.is_playing():
                self.play()
        else:
            ApolloWarning(f"Tried to seek invalid timestamp {time}, Last loc {total_time}")

    def is_playing(self) -> bool:
        """
        Returns the State of the stream

        Returns:
            bool: True if playing, otherwise False
        """
        return self._data_table_index.isPlaying()

    def play(self) -> Buffered_Audio_Stream:
        """
        Plays the stream

        Returns:
            Buffered_Audio_Stream: Instance itself
        """
        self._data_table_index.play()
        self._data_table_reader.play()
        LOGGER.debug(self._loaded_track)
        return self

    def stop(self) -> Buffered_Audio_Stream:
        """
        Stops the stream

        Returns:
            Buffered_Audio_Stream: Instance itself
        """
        self._data_table_index.pause()
        self._data_table_reader.stop()
        LOGGER.debug(self._loaded_track)
        return self

    def clear(self):
        """
        Clears the stream
        """
        self._data_table_index.clear()
        self._memorized_pos = 0
        self._write_head_pos = 0
        self._read_head_pos = 0
        self.media_file = None
        self._loaded_track = None
        for chan in range(self.chnls):
            self._shared_data_array[chan].fill(0)

    def output(self) -> pyo.Pointer2:
        """
        Returns the streams main output

        Returns:
            pyo.Pointer2: Stream Output
        """
        return self._data_table_reader

    def fetch_more(self):
        """
        Fetch and write more samples from the decoder
        """
        if not (self.decoder_eof and self.media_file.Decoder.is_seeking):
            data = self.get_audio_frame()
            if data is not None:
                self.sequential_write(data)
            else:
                self.decoder_eof = True
                self.cb_on_decoder_eof()

    # pylint: disable=R1710
    def get_audio_frame(self) -> Union[np.ndarray, None]:
        """
        Gets an audio frame form the decoder

        Returns:
            Union[np.ndarray, None]: audio frame
        """
        if self.media_file is not None:
            decoder = self.media_file.Decoder
            # noinspection PyUnresolvedReferences
            try:
                frame: av.audio.AudioFrame = decoder.get()
                if frame is not None:
                    return decoder.normalize_frame(frame)
            except (
                av.error.ValueError,
                av.error.InvalidDataError,
                av.error.EOFError,
            ) as e:
                self.stop()
                ApolloWarning(f"stream ended unexpectedly with {e}")

    def sequential_write(self, samples: np.ndarray):
        """
        Sequentially write samples to the shared buffer

        Args:
            samples (np.ndarray): Samples to write
        """
        estimated_last_pos = self._write_head_pos + samples.shape[1]
        write_range = range(self._write_head_pos, estimated_last_pos)
        wrapped_pos = (
            0 + (estimated_last_pos - self._data_table.size)
            if estimated_last_pos >= self._data_table.size
            else estimated_last_pos
        )

        # update write head pos
        if estimated_last_pos == self._data_table.size:
            self._write_head_pos = 0
        elif estimated_last_pos > self._data_table.size:
            self._write_head_pos = wrapped_pos
        else:
            self._write_head_pos = estimated_last_pos

        for chan in range(self._data_table.chnls):
            if samples.shape[0] == 1:
                self._shared_data_array[chan].put(write_range, samples[0], "wrap")
            elif samples.shape[0] == 2:
                self._shared_data_array[chan].put(write_range, samples[chan], "wrap")

        if DEBUG:
            self._data_table.refreshView()

    def update_time_info(self):
        """
        Updates the current played time info
        """
        _time = round((self._read_head_pos / self.sr) / self._pitch_scaling, 2)
        self.cb_return_current_time(_time)
        if self.media_file is not None:
            _total_time = self.media_file.SynthTags.get("SONGLEN", 0)[0]
            if not self.eof_approaching_raised and _time >= (
                _total_time - CONFIG["SERVER.FADER_ENV"]
            ):
                self.eof_approaching_raised = True
                self.cb_reaching_eof()
            elif _time >= _total_time + 0.01:
                self.stop()
        else:
            self.stop()

    def _cb_on_lineseg_value_change(self):
        """
        Handles Line seg value change events
        """
        pos = int(self._data_table.size * self._data_table_index.get())
        if self._memorized_pos != pos:
            if pos - self._memorized_pos < 0:
                self._read_head_pos += pos
            else:
                self._read_head_pos += abs(pos - self._memorized_pos)
            self._memorized_pos = pos
            if (self._write_head_pos - self._memorized_pos) <= self._writeahead_duration:
                self.fetch_more()
                self.update_time_info()

    def cb_on_decoder_eof(self):
        """
        Handles decoder EOF
        """

    def cb_return_current_time(self, time: float):
        """
        Handles get Current time events

        Args:
            time (float): time in seconds
        """

    def cb_reaching_eof(self):
        """
        Handles reaching EOF
        """


# pylint: disable=W0212
if __name__ == "__main__":
    from av import logging

    server = (
        pyo.Server(
            sr=CONFIG["SERVER.RATE"],
            nchnls=CONFIG["SERVER.CHNL"],
            buffersize=CONFIG["SERVER.BUFFER_SIZE"],
        )
        .boot()
        .start()
    )
    server.deactivateMidi()

    table = Buffered_Audio_Stream(chnls=CONFIG["SERVER.CHNL"])
    table.load_track(r"D:\Music\13 Wasted.mp3")

    table.cb_on_decoder_eof = lambda *x: LOGGER.info(("cb_on_decoder_eof", x))
    # table.cb_return_current_time = lambda *x: LOGGER.info(("cb_return_current_time", x))
    table.cb_reaching_eof = lambda *x: LOGGER.info(("cb_reaching_eof", x))

    table.seek(10)
    table.seek(20)
    table.seek(30)
    table.seek(40)
    table.seek(50)
    table.seek(60)

    table._data_table.view()
    spec = pyo.Spectrum(table.output().out())

    server.setAmp(0.0001)
    server.gui(locals())
