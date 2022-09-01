from __future__ import annotations

import logging
from typing import Optional, Union

import pyo

from apollo.media.filters import Buffered_Audio_Stream
from apollo.utils import get_logger
from configs import settings as CONFIG


LOGGER = get_logger(__name__)
DEBUG = bool(LOGGER.level == logging.DEBUG)


class Crossfaded_Input_Stream:
    """
    Crossfaded_Input_Stream
    """

    def __init__(self, stream_0: Buffered_Audio_Stream, stream_1: Buffered_Audio_Stream):
        self.stream_0, self.stream_1 = stream_0, stream_1
        self.env_duration, self.fade_duration = (
            CONFIG["SERVER.FADER_ENV"],
            CONFIG["SERVER.FADER_MIX"],
        )
        self.current_voice = 0

        in_dur = out_dur = (self.env_duration - self.fade_duration) / 2
        self.stream_fader_env = pyo.Linseg(
            [
                (0, 0),
                (in_dur, 0.5),
                (in_dur + self.fade_duration, 0.5),
                (in_dur + self.fade_duration + out_dur, 1),
            ]
        )
        self.selector = pyo.Selector(
            [self.stream_0.output(), self.stream_1.output()], voice=self.current_voice
        )

        self.switch_complete_trig = pyo.TrigFunc(
            pyo.Thresh(self.stream_fader_env, 1), self._cb_on_switch_complete
        )

    def output(self) -> pyo.PyoObject:
        """
        Returns the main output stream

        Returns:
            pyo.PyoObject: output stream
        """
        return self.selector

    def set_crossfade_env(self, env_duration: Union[float, int], fade_duration: Union[float, int]):
        """
        sets the env for the crossfader

        Args:
            env_duration (Union[float, int]): Envolope Duration
            fade_duration (Union[float, int]): Fade Duration
        """
        in_dur = out_dur = (env_duration - fade_duration) / 2
        self.stream_fader_env.setList(
            [
                (0, 0),
                (in_dur, 0.5),
                (in_dur + fade_duration, 0.5),
                (in_dur + fade_duration + out_dur, 1),
            ]
        )

    def play(self) -> Crossfaded_Input_Stream:
        """
        Plays stream

        Returns:
            Crossfaded_Input_Stream: instance itself
        """
        self.stream_fader_env.play()
        return self

    def stop(self) -> Crossfaded_Input_Stream:
        """
        Stops stream

        Returns:
            Crossfaded_Input_Stream: instance itself
        """
        self.stream_fader_env.stop()
        return self

    def crossfade(self, instant: Optional[bool] = False) -> Crossfaded_Input_Stream:
        """
        Crossfades between active and started stream

        Args:
            instant (Optional[bool]): instant transition flag

        Returns:
            Crossfaded_Input_Stream: instance itself
        """
        self.stop()

        if self.current_voice == 0:
            self.selector.setVoice(self.stream_fader_env)
            self.current_voice = 1
            if instant:
                self.cb_on_switch_complete(1)
                self.stream_0.stop()
            else:
                self._cb_on_switch_start(self.current_voice)

        elif self.current_voice == 1:
            self.selector.setVoice(pyo.Abs(self.stream_fader_env - 1))
            self.current_voice = 0
            if instant:
                self.cb_on_switch_complete(1)
                self.stream_1.stop()
            else:
                self._cb_on_switch_start(self.current_voice)

        self.play()
        return self

    # pylint: disable=R1710
    def active_stream(self) -> Optional[Buffered_Audio_Stream]:
        """
        Returns the active playing stream

        Returns:
            Optional[Buffered_Audio_Stream]: Active stream
        """
        if self.current_voice == 0:
            return self.stream_0

        if self.current_voice == 1:
            return self.stream_1

    def _cb_on_switch_start(self, current_stream: int):
        """
        On switch start

        Args:
            current_stream (int): index of started stream
        """
        self.cb_on_switch_start(current_stream)

    def _cb_on_switch_complete(self):
        """
        On switch complete
        """
        if self.current_voice == 0:
            self.cb_on_switch_complete(1)
            self.stream_1.stop()

        elif self.current_voice == 1:
            self.cb_on_switch_complete(0)
            self.stream_0.stop()

    def cb_on_switch_start(self, current_stream: int):
        """
        On switch start

        Args:
            current_stream (int): index of started stream
        """

    def cb_on_switch_complete(self, current_stream: int):
        """
        On switch complete

        Args:
            current_stream (int): index of completed stream
        """
