from __future__ import annotations

import datetime
import enum
import os
import time
from pathlib import PurePath
from typing import TYPE_CHECKING, Optional, Union

from app.custom_widgets import TrackRatingWidget
from PySide6 import QtGui

from apollo.database.models import Model_Provider
from apollo.utils import Apollo_Generic_View, get_logger
from configs import settings as CONFIG


if TYPE_CHECKING:
    from apollo.app.main import Apollo_MainWindow_UI

LOGGER = get_logger(__name__)


class STATE_PLAY(enum.Enum):
    PLAY = "PLAY"
    PAUSE = "PAUSE"


class STATE_SHUFFLE(enum.Enum):
    NONE = "NONE"
    SHUFFLE = "SHUFFLE"


class STATE_REPEAT(enum.Enum):
    NONE = "NONE"
    REPEAT = "REPEAT"
    REPEAT_ONE = "REPEAT_ONE"


class STATE_VOLUME_LEVEL(enum.Enum):
    MUTE = "MUTE"
    QUARTER = "QUARTER"
    HALF = "HALF"
    FULL = "FULL"


class PlayBack_Bar(Apollo_Generic_View):

    _STATE_PLAY = CONFIG.get("APOLLO.PLAYBACK_BAR.STATE_PLAY", STATE_PLAY.PAUSE.name)
    _STATE_SHUFFLE = CONFIG.get("APOLLO.PLAYBACK_BAR.STATE_SHUFFLE", STATE_SHUFFLE.NONE.name)
    _STATE_REPEAT = CONFIG.get("APOLLO.PLAYBACK_BAR.STATE_REPEAT", STATE_REPEAT.NONE.name)
    _STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.HALF.name
    _VOLUME_LEVEL = CONFIG.get("APOLLO.PLAYBACK_BAR.VOLUME_LEVEL", 50)
    _BYPASS_PROCESSOR = CONFIG.get("APOLLO.PLAYBACK_BAR.BYPASS_PROCESSOR", True)
    _ELAPSED_TIME = CONFIG.get("APOLLO.PLAYBACK_BAR.ELAPSED_TIME", 0)
    _CURRENT_PLAYING = CONFIG.get("APOLLO.PLAYBACK_BAR.CURRENT_PLAYING", None)

    def __init__(self, ui: Apollo_MainWindow_UI):
        self.UI = ui
        self.MODEL_PROVIDER = Model_Provider

        self.UI.playback_footer_track_rating = TrackRatingWidget(self.UI.playback_footer_frame_M)
        self.setup_conections()
        self.setup_defaults()

    def setup_conections(self):
        self.SIGNALS.PlayTrackSignal.connect(lambda x: self._cb_load_track_onto_player())
        self.UI.playback_button_play_pause.pressed.connect(lambda: (self.state_change_play()))
        self.UI.playback_button_prev.pressed.connect(lambda: self._cb_track_prev())
        self.UI.playback_button_next.pressed.connect(lambda: self._cb_track_next())
        self.UI.playback_button_audio_bypass.clicked.connect(
            lambda: self.state_change_processor_bypass(
                self.UI.playback_button_audio_bypass.isChecked()
            )
        )
        self.UI.playback_footer_track_seek_slider.valueChanged.connect(
            lambda x: (self.state_change_seek_slider(x))
        )
        self.UI.playback_button_play_shuffle.pressed.connect(lambda: (self.state_change_shuffle()))
        self.UI.playback_button_play_repeat.pressed.connect(lambda: (self.state_change_repeat()))
        self.UI.playback_slider_volume_control.valueChanged.connect(
            lambda x: (self.state_change_volume_level(x))
        )
        self.UI.playback_button_volume_control.pressed.connect(
            lambda: (self.state_change_volume_level())
        )
        self.UI.playback_button_play_settings.pressed.connect(
            lambda: (self.UI.audiofx_tab_switch_button.click())
        )
        self.UI.playback_footer_track_rating.RatingChangedSignal.connect(
            lambda x: self._cb_track_rating(x)
        )

    def setup_defaults(self):
        self.state_change_play(self._STATE_PLAY)
        self.state_change_shuffle(self._STATE_SHUFFLE)
        self.state_change_repeat(self._STATE_REPEAT)
        self.state_change_volume_level(self._VOLUME_LEVEL)
        self.UI.playback_slider_volume_control.setValue(self._VOLUME_LEVEL)
        self.state_change_processor_bypass(self._BYPASS_PROCESSOR)
        self.UI.playback_footer_track_seek_slider.setValue(self._ELAPSED_TIME)
        self.load_rating()

        if self._CURRENT_PLAYING:
            self.MODEL_PROVIDER.QueueModel().CURRENT_FILE_ID = self._CURRENT_PLAYING
            self._cb_load_track_onto_player()
            self.UI.queue_main_listview.repaint()

    def save_states(self):
        CONFIG["APOLLO.PLAYBACK_BAR.STATE_PLAY"] = self._STATE_PLAY
        CONFIG["APOLLO.PLAYBACK_BAR.STATE_SHUFFLE"] = self._STATE_SHUFFLE
        CONFIG["APOLLO.PLAYBACK_BAR.STATE_REPEAT"] = self._STATE_REPEAT
        CONFIG["APOLLO.PLAYBACK_BAR.VOLUME_LEVEL"] = self._VOLUME_LEVEL
        CONFIG["APOLLO.PLAYBACK_BAR.BYPASS_PROCESSOR"] = self._BYPASS_PROCESSOR
        value = self.UI.playback_footer_track_seek_slider.value()
        CONFIG["APOLLO.PLAYBACK_BAR.ELAPSED_TIME"] = value
        value = self.MODEL_PROVIDER.QueueModel()
        CONFIG["APOLLO.PLAYBACK_BAR.CURRENT_PLAYING"] = value.CURRENT_FILE_ID

    def _cb_load_track_onto_player(self):
        fid = self.MODEL_PROVIDER.QueueModel().CURRENT_FILE_ID
        self.load_track_info()

    def load_track_info(self, reset_defaults=False):
        """
        Loads track information into the UI

        Args:
            reset_defaults (boolean): Resets the UI information
        """
        if reset_defaults:
            self.UI.playback_footer_track_title.setText("Apollo - Media Player")
            self.UI.playback_footer_track_seek_slider.setRange(0, 100)
            self.UI.playback_footer_track_seek_slider.setSingleStep(5)
            self.load_rating()
            elapsed_time = time.strftime(
                "%H:%M:%S", time.gmtime(self.UI.playback_footer_track_seek_slider.maximum())
            )
            self.UI.playback_footer_track_elapsed.setText(f"-{elapsed_time}")
            self.UI.track_info_title.setText(f"Title: NA")
            self.UI.track_info_misc_1.setText(f"Artist: NA")
            self.UI.track_info_misc_2.setText(f"Album: NA")
            self.UI.track_info_misc_3.setText(f"Mood: NA")
            self.UI.track_info_stream.setText("NA, NA, NA")

        fid = self.MODEL_PROVIDER.QueueModel().CURRENT_FILE_ID
        tags = self.MODEL_PROVIDER.LibraryModel().fetch_track_info(fid)

        # POPULATE FOOTER ITEMS
        self.UI.playback_footer_track_title.setText(tags.get(("TITLE", 0), "Apollo - Media Player"))

        time_sec = datetime.timedelta(seconds=float(tags.get(("SONGLEN", 0), 0)))
        self.UI.playback_footer_track_elapsed.setText(f"{time_sec}")
        self.UI.playback_footer_track_seek_slider.setRange(0, int(time_sec.seconds))
        self.UI.playback_footer_track_seek_slider.setSingleStep(5)

        # POPULATE TRACK INFORMATION WIDGET
        TITLE = tags.get(("TITLE", 0)) if (tags.get(("TITLE", 0))) else "NA"
        self.UI.track_info_title.setText(f"Title: {TITLE}")
        ARTIST = tags.get(("ARTIST", 0)) if (tags.get(("ARTIST", 0))) else "NA"
        self.UI.track_info_misc_1.setText(f"Artist: {ARTIST}")
        ALBUM = tags.get(("ALBUM", 0)) if (tags.get(("ALBUM", 0))) else "NA"
        self.UI.track_info_misc_2.setText(f"Album: {ALBUM}")
        MOOD = tags.get(("MOOD", 0)) if (tags.get(("MOOD", 0))) else "NA"
        self.UI.track_info_misc_3.setText(f"Mood: {MOOD}")

        BITRATE = tags.get(("BITRATE", 0)) if (tags.get(("BITRATE", 0))) else 0
        BITRATE = "NA" if BITRATE is None else f"{int(BITRATE / 1000)}Kbps"
        CHANNELS = tags.get(("CHANNELS", 0)) if (tags.get(("CHANNELS", 0))) else 0
        CHANNELS = "NA" if CHANNELS is None else f"{CHANNELS} Channels"
        SAMPLERATE = tags.get(("SAMPLERATE", 0)) if (tags.get(("SAMPLERATE", 0))) else 0
        SAMPLERATE = "NA" if SAMPLERATE is None else f"{SAMPLERATE}Hz"

        self.UI.track_info_stream.setText("{0}, {1}, {2}".format(BITRATE, CHANNELS, SAMPLERATE))
        self.load_rating(tags.get(("POPULARIMETER", 0), 0))

        if tags.get(("PICTURE", 0)) and os.path.exists(PurePath(tags.get(("FILEPATH", 0)))):
            widget = self.UI.track_info_cover_pixmap
            pixmap = QtGui.QPixmap()
            # noinspection PyUnresolvedReferences
            pixmap.loadFromData(bytes(metadata.Artwork[0].data))
            widget.setPixmap(pixmap)

    def state_change_processor_bypass(self, state: bool):
        """
        Enables and disables the bypass of output through the processor

        Args:
            state (bool): bypass state
        """
        self._BYPASS_PROCESSOR = state
        self._cb_bypass_processor(state)

    def state_change_play(self, state: Optional[Union[STATE_PLAY, str]] = None):
        """
        plays and pauses the audio stream

        Args:
            state (Optional[Union[STATE_PLAY, str]]): PLAY/PAUSE state
        """
        # APPLIES VISUAL CHANGES
        button = self.UI.playback_button_play_pause
        if state is not None:
            if isinstance(state, STATE_PLAY):
                button.setProperty("STATE_PLAY", state.name)
                self._STATE_PLAY = state.name
            else:
                button.setProperty("STATE_PLAY", state)
                self._STATE_PLAY = state
        else:
            current = button.property("STATE_PLAY")
            if (current is not None) and (current == STATE_PLAY.PLAY.name):
                self._STATE_PLAY = STATE_PLAY.PAUSE.name
            elif (current is not None) and (current == STATE_PLAY.PAUSE.name):
                self._STATE_PLAY = STATE_PLAY.PLAY.name
            else:
                pass
            button.setProperty("STATE_PLAY", self._STATE_PLAY)

        button.style().unpolish(button)
        button.style().polish(button)

        self._cb_state_change_play(self._STATE_PLAY)

    def state_change_shuffle(self, state: Optional[Union[STATE_SHUFFLE, str]] = None):
        """
        Shuffles and orders the current playing queue

        Args:
            state (Optional[Union[STATE_SHUFFLE, str]]): SHUFFLE/NONE states
        """
        # APPLIES VISUAL CHANGES
        button = self.UI.playback_button_play_shuffle
        if state is not None:
            if isinstance(state, STATE_SHUFFLE):
                button.setProperty("STATE_SHUFFLE", state.name)
                self._STATE_SHUFFLE = state.name
            else:
                button.setProperty("STATE_SHUFFLE", state)
                self._STATE_SHUFFLE = state
        else:
            current = button.property("STATE_SHUFFLE")
            if (current is not None) and (current == STATE_SHUFFLE.NONE.name):
                self._STATE_SHUFFLE = STATE_SHUFFLE.SHUFFLE.name
            elif (current is not None) and (current == STATE_SHUFFLE.SHUFFLE.name):
                self._STATE_SHUFFLE = STATE_SHUFFLE.NONE.name
            else:
                pass
            button.setProperty("STATE_SHUFFLE", self._STATE_SHUFFLE)

        button.style().unpolish(button)
        button.style().polish(button)

        self._cb_state_change_shuffle(self._STATE_SHUFFLE)

    def state_change_repeat(self, state: Optional[Union[STATE_REPEAT, str]] = None):
        """
        Repeats the current queue or track

        Args:
            state (Optional[Union[STATE_REPEAT, str]]): REPEAT/REPEAT_ONE/NONE states
        """
        # APPLIES VISUAL CHANGES
        button = self.UI.playback_button_play_repeat
        if state is not None:
            if isinstance(state, STATE_REPEAT):
                button.setProperty("STATE_REPEAT", state.name)
                self._STATE_REPEAT = state.name
            else:
                button.setProperty("STATE_REPEAT", state)
                self._STATE_REPEAT = state
        else:
            current = button.property("STATE_REPEAT")
            if (current is not None) and (current == STATE_REPEAT.NONE.name):
                self._STATE_REPEAT = STATE_REPEAT.REPEAT.name
            elif (current is not None) and (current == STATE_REPEAT.REPEAT.name):
                self._STATE_REPEAT = STATE_REPEAT.REPEAT_ONE.name
            elif (current is not None) and (current == STATE_REPEAT.REPEAT_ONE.name):
                self._STATE_REPEAT = STATE_REPEAT.NONE.name
            else:
                pass
            button.setProperty("STATE_REPEAT", self._STATE_REPEAT)

        button.style().unpolish(button)
        button.style().polish(button)

        self._cb_state_change_repeat(self._STATE_REPEAT)

    def state_change_volume_level(self, level: Optional[int] = None):
        """
        Modifies the volume level of the processing server

        Args:
            level (Optional[int]): Audio Level (0 - 99)
        """
        button = self.UI.playback_button_volume_control
        # APPLIES VISUAL CHANGES
        if level is not None and isinstance(level, int):
            if level == 0:
                self._STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.MUTE.name
                button.setProperty("STATE_VOLUME_LEVEL", self._STATE_VOLUME_LEVEL)
            elif 0 < level <= 25:
                self._STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.QUARTER.name
                button.setProperty("STATE_VOLUME_LEVEL", self._STATE_VOLUME_LEVEL)
            elif 25 < level <= 50:
                self._STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.HALF.name
                button.setProperty("STATE_VOLUME_LEVEL", self._STATE_VOLUME_LEVEL)
            elif 50 < level <= 99:
                self._STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.FULL.name
                button.setProperty("STATE_VOLUME_LEVEL", self._STATE_VOLUME_LEVEL)
            else:
                pass

            button.style().unpolish(button)
            button.style().polish(button)

            self._VOLUME_LEVEL = level
            self._cb_state_change_volume_level(level)

        else:
            current = button.property("STATE_VOLUME_LEVEL")
            if current == STATE_VOLUME_LEVEL.MUTE.name:
                self.UI.playback_slider_volume_control.setValue(25)
            elif current == STATE_VOLUME_LEVEL.QUARTER.name:
                self.UI.playback_slider_volume_control.setValue(50)
            elif current == STATE_VOLUME_LEVEL.HALF.name:
                self.UI.playback_slider_volume_control.setValue(99)
            elif current == STATE_VOLUME_LEVEL.FULL.name:
                self.UI.playback_slider_volume_control.setValue(0)
            else:
                pass

    def load_rating(self, rating: Optional[float] = 0):
        """
        Loads the user defined rating of the current track

        Args:
            rating (Optional[float]): track rating
        """
        widget: TrackRatingWidget = self.UI.playback_footer_track_rating
        widget.setRating(rating)

    def state_change_seek_slider(self, value: int):
        """
        Seeks to a given time on the audio buffer

        Args:
            value (int): Value in seconds
        """
        if value != 0:
            value = self.UI.playback_footer_track_seek_slider.maximum() - value
            self.UI.playback_footer_track_elapsed.setText(
                f"-{time.strftime('%H:%M:%S', time.gmtime(value))}"
            )
        else:
            value = self.UI.playback_footer_track_seek_slider.maximum()
            self.UI.playback_footer_track_elapsed.setText(
                f"-{time.strftime('%H:%M:%S', time.gmtime(value))}"
            )
        self._cb_state_change_seek_slider(value)

    def _cb_state_change_seek_slider(self, time_s: int):
        # TODO: Implementation
        LOGGER.info("Implementation Required")

    def _cb_state_change_play(self, state: Optional[Union[STATE_PLAY, str]]):
        # TODO: Implementation
        LOGGER.info("Implementation Required")

    def _cb_state_change_shuffle(self, state: Optional[Union[STATE_SHUFFLE, str]]):
        # TODO: Implementation
        LOGGER.info("Implementation Required")

    def _cb_state_change_repeat(self, state: Optional[Union[STATE_REPEAT, str]]):
        # TODO: Implementation
        LOGGER.info("Implementation Required")

    def _cb_state_change_volume_level(self, volume: int):
        # TODO: Implementation
        LOGGER.info("Implementation Required")

    def _cb_track_prev(self):
        # TODO: Implementation
        LOGGER.info("Implementation Required")

    def _cb_track_next(self):
        # TODO: Implementation
        LOGGER.info("Implementation Required")

    def _cb_track_rating(self, rating: float):
        fid = self.MODEL_PROVIDER.QueueModel().CURRENT_FILE_ID
        self.MODEL_PROVIDER.LibraryModel().update_current_track_rating(rating, fid)

    def _cb_bypass_processor(self, state: bool):
        # TODO: Implementation
        LOGGER.info("Implementation Required")

    def _cb_load_track_info(self, fid: Optional[str] = None):
        # TODO: Implementation
        LOGGER.info("Implementation Required")
