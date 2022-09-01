from __future__ import annotations

from pathlib import PurePath
from typing import Any, Optional, Union

import pyo

from apollo.media.filters import Buffered_Audio_Stream, Crossfaded_Input_Stream
from apollo.utils import ApolloSignal, get_logger
from configs import settings as CONFIG


LOGGER = get_logger(__name__)


class Processor:
    """
    Main Processing class for apollos backend
    """

    PlayNextTrack_Signal = ApolloSignal()
    PlayingTrackTime_Signal = ApolloSignal()

    def __init__(self):
        self._server = pyo.Server(
            sr=CONFIG["SERVER.RATE"],
            nchnls=CONFIG["SERVER.CHNL"],
            buffersize=CONFIG["SERVER.BUFFER_SIZE"],
        ).boot()
        self._server.deactivateMidi()

        self._table_0 = Buffered_Audio_Stream(chnls=CONFIG["SERVER.CHNL"])
        self._table_1 = Buffered_Audio_Stream(chnls=CONFIG["SERVER.CHNL"])
        self._crossfader = Crossfaded_Input_Stream(self._table_0, self._table_1)
        self._clip = pyo.Clip(self._crossfader.output())
        self._filter_chain = pyo.Sine(0)

        self._bypass_selector_switch_fader = pyo.Linseg(
            [(0, 0), (0.25, 0.5), (0.45, 0.5), (0.5, 1)]
        )
        self._bypass_selector = pyo.Selector([self._clip, self._filter_chain])

        self.setup_conections()
        self.setup_defaults()

    def setup_conections(self):
        """
        Sets up conections
        """
        self._table_0.cb_reaching_eof = lambda: (Processor.PlayNextTrack_Signal.emit())
        self._table_0.cb_return_current_time = lambda _time: (
            Processor.PlayingTrackTime_Signal.emit(_time)
            if self._crossfader.current_voice == 0
            else None
        )
        self._table_1.cb_reaching_eof = lambda: (Processor.PlayNextTrack_Signal.emit())
        self._table_1.cb_return_current_time = lambda _time: (
            Processor.PlayingTrackTime_Signal.emit(_time)
            if self._crossfader.current_voice == 1
            else None
        )

    def setup_defaults(self):
        """
        Sets up defaults
        """
        if CONFIG.get("APOLLO.PLAYBACK_BAR.BYPASS_PROCESSOR", True):
            self._bypass_selector.setVoice(0)
            LOGGER.info("Bypass Filters")
        else:
            self._bypass_selector.setVoice(1)
            LOGGER.info("Enable Filters")

    def play(self, file_path: Union[str, PurePath], instant: Optional[bool] = False):
        """
        Plays Track

        Args:
            file_path ( Union[str, PurePath]): file to load
            instant (Optional[bool]): switch instantly
        """
        if self._crossfader.current_voice == 0:
            self._table_1.load_track(file_path)
            self._crossfader.crossfade(instant)
        elif self._crossfader.current_voice == 1:
            self._table_0.load_track(file_path)
            self._crossfader.crossfade(instant)

    def seek(self, time: Union[int, float]):
        """
        Seeks the read pointer to a time stamp

        Args:
            time (Union[int, float]): time stamp to seek to
        """
        self._crossfader.active_stream().seek(time)

    def shutdown(self) -> Processor:
        """
        Shutdowns server

        Returns:
            Processor: instance itself
        """
        self._server.shutdown()
        LOGGER.info("Server Shutdown")
        return self

    def stop(self) -> Processor:
        """
        Stops server

        Returns:
            Processor: instance itself
        """
        self._server.stop()
        LOGGER.info("Server Stopped")
        return self

    def start(self) -> Processor:
        """
        Starts server

        Returns:
            Processor: instance itself
        """
        self._server.start()
        LOGGER.info("Server Started")
        return self

    def output(self) -> pyo.Selector:
        """
        Returns the main output stream

        Returns:
            pyo.Selector: main output stream
        """
        return self._bypass_selector

    def bypass_filters(self):
        """
        Bypasses Filters
        """
        self._bypass_selector.setVoice(pyo.Abs(self._bypass_selector_switch_fader - 1))
        self._bypass_selector_switch_fader.play()
        LOGGER.info("Bypass Filters")

    def enable_filters(self):
        """
        Enables Filters
        """
        self._bypass_selector.setVoice(self._bypass_selector_switch_fader)
        self._bypass_selector_switch_fader.play()
        LOGGER.info("Enable Filters")

    def set_server_amp(self, amp: float):
        """
        Sets the servers amp

        Args:
            amp (float): amplitude value
        """
        self._server.setAmp(amp)

    def debug_gui(self, _locals: dict[str, Any]):
        """
        Starts up the servers internal GUI

        Args:
            _locals (dict[str, Any]): locals
        """
        self._server.gui(_locals)


if __name__ == "__main__":
    processor = Processor().start()
    # processor.PlayingTrackTime_Signal.connect(lambda *x: LOGGER.info(x))
    processor.PlayNextTrack_Signal.connect(lambda *x: LOGGER.info(x))

    processor.play(r"D:\Music\01. Big Michael.mp3", instant=True)

    spectrum = pyo.Spectrum(processor.output().out())
    processor.debug_gui(locals())
