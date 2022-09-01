from __future__ import annotations

import random
from typing import TYPE_CHECKING

from apollo.database import Database
from apollo.database.models import Model_Provider, QueueModel
from apollo.media.player.processor import Processor
from apollo.utils import Apollo_Generic_View, get_logger
from configs import settings as CONFIG


if TYPE_CHECKING:
    from apollo.app.main import Apollo_MainWindow_UI
    from apollo.app.sub_tabs.playback_bar import STATE_REPEAT, STATE_SHUFFLE

LOGGER = get_logger(__name__)


class Player_Queue:
    """
    Player Queue
    """

    def __init__(self, parent_model: QueueModel):
        # pylint: disable=C0415
        from apollo.app.sub_tabs.playback_bar import STATE_REPEAT, STATE_SHUFFLE

        self.parent_model = parent_model
        self._queue = []
        self._queue_index = 0
        self._repeated = False

        self.repeat_type: STATE_REPEAT = STATE_REPEAT.NONE
        self.shuffle_type: STATE_SHUFFLE = STATE_SHUFFLE.NONE

        self.refresh_data()
        self.update_index(CONFIG.get("APOLLO.PLAYBACK_BAR.CURRENT_PLAYING", None))

    def __str__(self):
        return "\n".join(self._queue)

    def __repr__(self):
        return str(self)

    def repeat(self, _type: STATE_REPEAT):
        """
        Sets the queue repeat flag

        Args:
            _type (STATE_REPEAT): Repeat type
        """
        self.repeat_type = _type

    def shuffle(self, _type: STATE_SHUFFLE):
        """
        Shuffles the current queue

        Args:
            _type (STATE_SHUFFLE): Sets the shuffle type
        """
        # pylint: disable=C0415
        from apollo.app.sub_tabs.playback_bar import STATE_SHUFFLE

        if self.parent_model.rowCount() > 0:
            # noinspection PyProtectedMember
            # pylint: disable=W0212
            db: Database = self.parent_model._db
            with db.connector as conn:
                data = db.execute("SELECT queue.FILEID FROM queue ORDER BY queue.PLAYORDER", conn)
                self._queue = list(map(lambda x: x[0], data.records))

            if _type.value == STATE_SHUFFLE.SHUFFLE.value:
                random.shuffle(self._queue)

            self.shuffle_type = _type
            self._queue_index = 0

    def refresh_data(self):
        """
        Refreshes the queue data
        """
        if self.parent_model.rowCount() > 0:
            # noinspection PyProtectedMember
            # pylint: disable=W0212
            db: Database = self.parent_model._db
            with db.connector as conn:
                data = db.execute("SELECT queue.FILEID FROM queue ORDER BY queue.PLAYORDER", conn)
                self._queue = list(map(lambda x: x[0], data.records))
        else:
            self.clear_queue()
        self._queue_index = 0

    def next(self) -> str:
        """
        Returns the next track from the queue

        Returns:
            str: file id
        """
        # pylint: disable=C0415
        from apollo.app.sub_tabs.playback_bar import STATE_REPEAT

        if self._queue and 0 <= self._queue_index < len(self._queue):
            if self.repeat_type.name == STATE_REPEAT.NONE.name:
                self._queue_index += 1
                return self.current()

            if self.repeat_type.name == STATE_REPEAT.REPEAT_ONE.name:
                if not self._repeated:
                    self._repeated = True
                    return self.current()

                self._repeated = False
                self._queue_index += 1
                return self.current()

            if self.repeat_type.name == STATE_REPEAT.REPEAT.name:
                self._queue_index += 1
                if (
                    self._queue_index == len(self._queue)
                    and self.repeat_type.name == STATE_REPEAT.REPEAT.name
                ):
                    self._queue_index = 0
                return self.current()

        if (
            self._queue
            and self._queue_index >= len(self._queue)
            and self.repeat_type.name == STATE_REPEAT.REPEAT.name
        ):
            self._queue_index = 0
            return self.current()

        return ""

    def prev(self) -> str:
        """
        Returns the previous track from the queue

        Returns:
            str: file id
        """
        # pylint: disable=C0415
        from apollo.app.sub_tabs.playback_bar import STATE_REPEAT

        if self._queue and 0 <= self._queue_index < len(self._queue):
            if self.repeat_type.name == STATE_REPEAT.NONE.name:
                self._queue_index -= 1
                return self.current()

            if self.repeat_type.name == STATE_REPEAT.REPEAT_ONE.name:
                if not self._repeated:
                    self._repeated = True
                    return self.current()

                self._repeated = False
                self._queue_index -= 1
                return self.current()

            if self.repeat_type.name == STATE_REPEAT.REPEAT.name:
                self._queue_index -= 1
                if self._queue_index == -1 and self.repeat_type.name == STATE_REPEAT.REPEAT.name:
                    self._queue_index = len(self._queue) - 1
                return self.current()

        if (
            self._queue
            and self._queue_index < 0
            and self.repeat_type.name == STATE_REPEAT.REPEAT.name
        ):
            self._queue_index = len(self._queue) - 1
            return self.current()

        return ""

    def current(self) -> str:
        """
        Returns the current track from the queue

        Returns:
            str: file id
        """
        if self._queue and 0 <= self._queue_index < len(self._queue):
            return self._queue[self._queue_index]
        return ""

    def clear_queue(self):
        """
        Clears the queue
        """
        self._queue = []

    def update_index(self, fid: str):
        """
        Updates te queues lookup index

        Args:
            fid (str): file id of the track to set index to
        """
        if self._queue and fid in self._queue:
            self._queue_index = self._queue.index(fid)
        else:
            self._queue_index = 0


class Player(Apollo_Generic_View):
    """
    Audio Player Interface
    """

    def __init__(self, ui: Apollo_MainWindow_UI):
        self.UI = ui
        self.PROCESSOR = Processor()

        self.MODEL_PROVIDER = Model_Provider
        self.QUEUE = Player_Queue(self.MODEL_PROVIDER.QueueModel())

        self.setup_conections()
        self.setup_defaults()

        self.PROCESSOR.output().out()

    def setup_conections(self):
        self.MODEL_PROVIDER.QueueModel().ModelUpdatedSignal.connect(
            lambda: self.QUEUE.refresh_data()
        )
        self.PROCESSOR.PlayNextTrack_Signal.connect(lambda: self.play_next())
        self.PROCESSOR.PlayingTrackTime_Signal.connect(
            lambda _time: self.UI.playback_footer_track_seek_slider.setValue(_time)
            if not (self.UI.playback_footer_track_seek_slider.underMouse())
            else None
        )

    def setup_defaults(self):
        pass

    def save_states(self):
        self.shutdown()

    def _play(self, fid: str, instant: bool = False):
        """
        Plays the track using file id

        Args:
            fid (str): fileid of the track to play
            instant (bool): instant transition between tracks
        """
        data = self.MODEL_PROVIDER.LibraryModel().fetch_track_info(fid)
        if fid and data:
            self.MODEL_PROVIDER.QueueModel().CURRENT_FILE_ID = fid
            self.SIGNALS.BeginPlayTrackSignal.emit(fid)
            self.QUEUE.update_index(fid)
            self.PROCESSOR.play(data[("FILEPATH", 0)], instant)
            self.UI.queue_main_listview.repaint()

    def play_current(self, fid: str) -> str:
        """
        play current track

        Args:
            fid (str): current track file id
        """
        self._play(fid, True)
        return fid

    def play_next(self) -> str:
        """
        play next track

        Returns:
            str: next track file id
        """
        fid = self.QUEUE.next()
        self._play(fid)
        return fid

    def play_prev(self) -> str:
        """
        play prev track

        Returns:
            str: prev track file id
        """
        fid = self.QUEUE.prev()
        self._play(fid)
        return fid

    def shutdown(self):
        """
        Shutdowns server
        """
        self.PROCESSOR.shutdown()

    def start(self):
        """
        Starts server
        """
        self.PROCESSOR.start()

    def stop(self):
        """
        Stops server
        """
        self.PROCESSOR.stop()

    def bypass(self, state: bool):
        """
        Bypasses Filter

        Args:
            state (bool): Toggles filters
        """
        if state:
            self.PROCESSOR.bypass_filters()
        else:
            self.PROCESSOR.enable_filters()

    def repeat(self, _type: STATE_REPEAT):
        """
        Repeats Track

        Args:
            _type (STATE_REPEAT): Player Repeat type
        """
        self.QUEUE.repeat(_type)

    def shuffle(self, _type: STATE_SHUFFLE):
        """
        Shuffles Track

        Args:
            _type (STATE_SHUFFLE): Player Shuffle type
        """
        self.QUEUE.shuffle(_type)

    def seek(self, time: float):
        """
        Seeks active stream to a time stamp

        Args:
            time (float): time to seek to
        """
        self.PROCESSOR.seek(time)

    def set_player_volume(self, level: int):
        """
        Set player volume

        Args:
            level (int): Set player volume
        """
        level = ((2 * pow(level, 2)) / 100) * 0.01
        level = round(level, 4) if level >= 0.0001 else 0.0001
        self.PROCESSOR.set_server_amp(level)
