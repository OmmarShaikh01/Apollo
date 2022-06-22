import abc
import enum
import math
import time
from pathlib import PurePath
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.assets import AppIcons
from apollo.db.models import LibraryModel, ModelProvider, QueueModel
from apollo.layout.mainwindow import Ui_MainWindow as Apollo
from apollo.media import Mediafile
from apollo.utils import get_logger
from configs import settings

CONFIG = settings
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
    MUTE = 'MUTE'
    QUARTER = 'QUARTER'
    HALF = 'HALF'
    FULL = 'FULL'


class TrackRatingWidget(QtWidgets.QWidget):
    """
    Rating Widget, modifies and displays track rating
    """
    RatingChangedSignal = QtCore.Signal(float)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        """
        Constructor

        Args:
            parent (Optional[QtWidgets.QWidget]): Parent widget
        """
        super().__init__(parent)
        self.setMouseTracking(True)
        self.rating = 0
        self._rating = 0
        self._temp_rating = self._rating

    def setRating(self, rating: Optional[float] = 0):
        """
        Modifies the currently displayed rating

        Args:
            rating (Optional[float]): rating to set
        """
        self._rating = rating
        self.rating = rating
        self.RatingChangedSignal.emit(rating)
        self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        width = (round(self.mapFromGlobal(QtGui.QCursor.pos()).x() / self.width(), 1) / 2) * 10
        self._rating = width
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        width = (round(self.mapFromGlobal(QtGui.QCursor.pos()).x() / self.width(), 1) / 2) * 10
        self._rating = width
        self.rating = width
        self.update()
        self.RatingChangedSignal.emit(width)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self._rating = self.rating
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        image = QtGui.QImage().scaled(self.width(), self.height())
        image.fill(QtGui.QColor.fromRgb(0, 0, 0, 0))
        painter.drawImage(0, 0, image)
        self.drawStars(self._rating, painter)

    def drawStars(self, stars: float, painter: QtGui.QPainter):
        painter.save()
        size = 24
        if stars == 0:
            for index, pos in enumerate(range(0, (size - 5) * 5, (size - 5))):
                self.paint_star(AppIcons.STAR_OUTLINE.secondary, painter, pos, size)
        elif stars == 5:
            for index, pos in enumerate(range(0, (size - 5) * 5, (size - 5))):
                self.paint_star(AppIcons.STAR.secondary, painter, pos, size)
        else:
            for index, pos in enumerate(range(0, (size - 5) * 5, (size - 5))):
                if math.ceil(stars) == (index + 1):
                    self.paint_star(AppIcons.STAR_HALF.secondary, painter, pos, size)
                elif (index + 1) <= math.floor(stars):
                    self.paint_star(AppIcons.STAR.secondary, painter, pos, size)
                else:
                    self.paint_star(AppIcons.STAR_OUTLINE.secondary, painter, pos, size)
        painter.end()

    @staticmethod
    def paint_star(star: str, painter: QtGui.QPainter, pos: int, size: int):
        """
        Paints a star pixmap

        Args:
            star (str): location of the image file
            painter (QtGui.QPainter): Widget painter
            pos (int): Position to draw star at
            size (int): Size of the pixmap
        """
        painter.drawPixmap(QtCore.QPoint(pos, 6), QtGui.QPixmap.fromImage(QtGui.QImage(star)).scaled(size, size))


class Playback_Bar_Interactions(abc.ABC):
    """
    Playback Bar Interactions
    """
    _STATE_PLAY = CONFIG.get('APOLLO.PLAYBACK_BAR.STATE_PLAY', STATE_PLAY.PAUSE.name)
    _STATE_SHUFFLE = CONFIG.get('APOLLO.PLAYBACK_BAR.STATE_SHUFFLE', STATE_SHUFFLE.NONE.name)
    _STATE_REPEAT = CONFIG.get('APOLLO.PLAYBACK_BAR.STATE_REPEAT', STATE_REPEAT.NONE.name)
    _STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.HALF.name
    _VOLUME_LEVEL = CONFIG.get('APOLLO.PLAYBACK_BAR.VOLUME_LEVEL', 50)
    _LOADED_TRACK = CONFIG.get('APOLLO.PLAYBACK_BAR.LOADED_TRACK', None)
    _BYPASS_PROCESSOR = CONFIG.get('APOLLO.PLAYBACK_BAR.BYPASS_PROCESSOR', True)
    _ELAPSED_TIME = CONFIG.get('APOLLO.PLAYBACK_BAR.ELAPSED_TIME', 0)

    def __init__(self, ui: Apollo) -> None:
        """
        Constructor

        Args:
            ui (Apollo): UI objects
        """
        self.ui = ui
        self.ui.playback_footer_track_rating = TrackRatingWidget(self.ui.playback_footer_frame_M)

        self.setup_interactions()
        self.setup_defaults()

    def setup_interactions(self):
        """
        Sets up interactions
        """
        self.ui.playback_button_play_pause.pressed.connect(lambda: (self.state_change_play()))
        self.ui.playback_button_prev.pressed.connect(lambda: self.call_track_prev())
        self.ui.playback_button_next.pressed.connect(lambda: self.call_track_next())
        self.ui.playback_button_audio_bypass.clicked.connect(
                lambda: self.state_change_processor_bypass(self.ui.playback_button_audio_bypass.isChecked()))
        self.ui.playback_footer_track_seek_slider.valueChanged.connect(lambda x: (self.state_change_seek_slider(x)))
        self.ui.playback_button_play_shuffle.pressed.connect(lambda: (self.state_change_shuffle()))
        self.ui.playback_button_play_repeat.pressed.connect(lambda: (self.state_change_repeat()))
        self.ui.playback_slider_volume_control.valueChanged.connect(lambda x: (self.state_change_volume_level(x)))
        self.ui.playback_button_volume_control.pressed.connect(lambda: (self.state_change_volume_level()))
        self.ui.playback_button_play_settings.pressed.connect(lambda: (self.ui.audiofx_tab_switch_button.click()))
        self.ui.playback_footer_track_rating.RatingChangedSignal.connect(lambda x: self.call_track_rating(x))

    def setup_defaults(self):
        """
        Sets up default states
        """
        self.state_change_play(self._STATE_PLAY)
        self.state_change_shuffle(self._STATE_SHUFFLE)
        self.state_change_repeat(self._STATE_REPEAT)
        self.state_change_volume_level(self._VOLUME_LEVEL)
        self.ui.playback_slider_volume_control.setValue(self._VOLUME_LEVEL)
        self.state_change_processor_bypass(self._BYPASS_PROCESSOR)
        self.load_track_info()
        self.ui.playback_footer_track_seek_slider.setValue(self._ELAPSED_TIME)
        self.load_rating()

    def save_states(self):
        """
        saves session states of Apollo
        """
        CONFIG['APOLLO.PLAYBACK_BAR.STATE_PLAY'] = self._STATE_PLAY
        CONFIG['APOLLO.PLAYBACK_BAR.STATE_SHUFFLE'] = self._STATE_SHUFFLE
        CONFIG['APOLLO.PLAYBACK_BAR.STATE_REPEAT'] = self._STATE_REPEAT
        CONFIG['APOLLO.PLAYBACK_BAR.VOLUME_LEVEL'] = self._VOLUME_LEVEL
        CONFIG['APOLLO.PLAYBACK_BAR.LOADED_TRACK'] = self._LOADED_TRACK
        CONFIG['APOLLO.PLAYBACK_BAR.BYPASS_PROCESSOR'] = self._BYPASS_PROCESSOR
        CONFIG['APOLLO.PLAYBACK_BAR.ELAPSED_TIME'] = self.ui.playback_footer_track_seek_slider.value()

    def shutdown(self):
        """
        Shutdown callback
        """
        self.call_on_shutdown()
        self.save_states()

    def state_change_processor_bypass(self, state: bool):
        """
        Enables and disables the bypass of output through the processor

        Args:
            state (bool): bypass state
        """
        self._BYPASS_PROCESSOR = state
        self.call_bypass_processor(state)

    def state_change_play(self, state: Optional[Union[STATE_PLAY, str]] = None):
        """
        plays and pauses the audio stream

        Args:
            state (Optional[Union[STATE_PLAY, str]]): PLAY/PAUSE state
        """
        # APPLIES VISUAL CHANGES
        button = self.ui.playback_button_play_pause
        if state is not None:
            if isinstance(state, STATE_PLAY):
                button.setProperty('STATE_PLAY', state.name)
                self._STATE_PLAY = state.name
            else:
                button.setProperty('STATE_PLAY', state)
                self._STATE_PLAY = state
        else:
            current = button.property('STATE_PLAY')
            if (current is not None) and (current == STATE_PLAY.PLAY.name):
                self._STATE_PLAY = STATE_PLAY.PAUSE.name
            elif (current is not None) and (current == STATE_PLAY.PAUSE.name):
                self._STATE_PLAY = STATE_PLAY.PLAY.name
            else:
                pass
            button.setProperty('STATE_PLAY', self._STATE_PLAY)

        button.style().unpolish(button)
        button.style().polish(button)

        # APPLIES CONTROL CHANGES TODO
        self.call_state_change_play(self._STATE_PLAY)

    def state_change_shuffle(self, state: Optional[Union[STATE_SHUFFLE, str]] = None):
        """
        Shuffles and orders the current playing queue

        Args:
            state (Optional[Union[STATE_SHUFFLE, str]]): SHUFFLE/NONE states
        """
        # APPLIES VISUAL CHANGES
        button = self.ui.playback_button_play_shuffle
        if state is not None:
            if isinstance(state, STATE_SHUFFLE):
                button.setProperty('STATE_SHUFFLE', state.name)
                self._STATE_SHUFFLE = state.name
            else:
                button.setProperty('STATE_SHUFFLE', state)
                self._STATE_SHUFFLE = state
        else:
            current = button.property('STATE_SHUFFLE')
            if (current is not None) and (current == STATE_SHUFFLE.NONE.name):
                self._STATE_SHUFFLE = STATE_SHUFFLE.SHUFFLE.name
            elif (current is not None) and (current == STATE_SHUFFLE.SHUFFLE.name):
                self._STATE_SHUFFLE = STATE_SHUFFLE.NONE.name
            else:
                pass
            button.setProperty('STATE_SHUFFLE', self._STATE_SHUFFLE)

        button.style().unpolish(button)
        button.style().polish(button)

        # APPLIES CONTROL CHANGES TODO
        self.call_state_change_shuffle(self._STATE_SHUFFLE)

    def state_change_repeat(self, state: Optional[Union[STATE_REPEAT, str]] = None):
        """
        Repeats the current queue or track

        Args:
            state (Optional[Union[STATE_REPEAT, str]]): REPEAT/REPEAT_ONE/NONE states
        """
        # APPLIES VISUAL CHANGES
        button = self.ui.playback_button_play_repeat
        if state is not None:
            if isinstance(state, STATE_REPEAT):
                button.setProperty('STATE_REPEAT', state.name)
                self._STATE_REPEAT = state.name
            else:
                button.setProperty('STATE_REPEAT', state)
                self._STATE_REPEAT = state
        else:
            current = button.property('STATE_REPEAT')
            if (current is not None) and (current == STATE_REPEAT.NONE.name):
                self._STATE_REPEAT = STATE_REPEAT.REPEAT.name
            elif (current is not None) and (current == STATE_REPEAT.REPEAT.name):
                self._STATE_REPEAT = STATE_REPEAT.REPEAT_ONE.name
            elif (current is not None) and (current == STATE_REPEAT.REPEAT_ONE.name):
                self._STATE_REPEAT = STATE_REPEAT.NONE.name
            else:
                pass
            button.setProperty('STATE_REPEAT', self._STATE_REPEAT)

        button.style().unpolish(button)
        button.style().polish(button)

        # APPLIES CONTROL CHANGES TODO
        self.call_state_change_repeat(self._STATE_REPEAT)

    def state_change_volume_level(self, level: Optional[int] = None):
        """
        Modifies the volume level of the processing server

        Args:
            level (Optional[int]): Audio Level (0 - 99)
        """
        button = self.ui.playback_button_volume_control
        # APPLIES VISUAL CHANGES
        if level is not None and isinstance(level, int):
            if level == 0:
                self._STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.MUTE.name
                button.setProperty('STATE_VOLUME_LEVEL', self._STATE_VOLUME_LEVEL)
            elif 0 < level <= 25:
                self._STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.QUARTER.name
                button.setProperty('STATE_VOLUME_LEVEL', self._STATE_VOLUME_LEVEL)
            elif 25 < level <= 50:
                self._STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.HALF.name
                button.setProperty('STATE_VOLUME_LEVEL', self._STATE_VOLUME_LEVEL)
            elif 50 < level <= 99:
                self._STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.FULL.name
                button.setProperty('STATE_VOLUME_LEVEL', self._STATE_VOLUME_LEVEL)
            else:
                pass

            button.style().unpolish(button)
            button.style().polish(button)

            # APPLIES CONTROL CHANGES TODO
            self._VOLUME_LEVEL = level
            self.call_state_change_volume_level(level)

        else:
            current = button.property('STATE_VOLUME_LEVEL')
            if current == STATE_VOLUME_LEVEL.MUTE.name:
                self.ui.playback_slider_volume_control.setValue(25)
            elif current == STATE_VOLUME_LEVEL.QUARTER.name:
                self.ui.playback_slider_volume_control.setValue(50)
            elif current == STATE_VOLUME_LEVEL.HALF.name:
                self.ui.playback_slider_volume_control.setValue(99)
            elif current == STATE_VOLUME_LEVEL.FULL.name:
                self.ui.playback_slider_volume_control.setValue(0)
            else:
                pass

    def load_track_info(self, metadata: Optional[Mediafile] = None):
        """
        Loads the track metadata into the UI

        Args:
            metadata (Optional[Mediafile]): Audio Metadata
        """
        if metadata is None:
            self.ui.playback_footer_track_title.setText('Apollo - Media Player')
            self.ui.playback_footer_track_seek_slider.setRange(0, 100)
            self.ui.playback_footer_track_seek_slider.setSingleStep(5)
            elapsed_time = time.strftime('%H:%M:%S', time.gmtime(self.ui.playback_footer_track_seek_slider.maximum()))
            self.ui.playback_footer_track_elapsed.setText(f"-{elapsed_time}")
            self.ui.track_info_title.setText(f'Title: NA')
            self.ui.track_info_misc_1.setText(f'Artist: NA')
            self.ui.track_info_misc_2.setText(f'Album: NA')
            self.ui.track_info_misc_3.setText(f'Mood: NA')
            self.ui.track_info_stream.setText("NA, NA, NA")
        else:
            tags = metadata.SynthTags
            self._LOADED_TRACK = PurePath(tags['FILEPATH'][0]).as_posix()

            # POPULATE FOOTER ITEMS
            self.ui.playback_footer_track_title.setText(tags.get('TITLE', ['Apollo - Media Player'])[0])
            self.ui.playback_footer_track_rating.setText('')

            time_sec = int(tags.get('SONGLEN', 0)[0])
            self.ui.playback_footer_track_elapsed.setText(f"-{time.strftime('%H:%M:%S', time.gmtime(time_sec))}")
            self.ui.playback_footer_track_seek_slider.setRange(0, time_sec)
            self.ui.playback_footer_track_seek_slider.setSingleStep(5)

            # POPULATE TRACK INFORMATION WIDGET
            TITLE = tags.get('TITLE')[0] if len(tags.get('TITLE')) != 0 else 'NA'
            self.ui.track_info_title.setText(f'Title: {TITLE}')
            ARTIST = tags.get('ARTIST')[0] if len(tags.get('ARTIST')) != 0 else 'NA'
            self.ui.track_info_misc_1.setText(f'Artist: {ARTIST}')
            ALBUM = tags.get('ALBUM')[0] if len(tags.get('ALBUM')) != 0 else 'NA'
            self.ui.track_info_misc_2.setText(f'Album: {ALBUM}')
            MOOD = tags.get('MOOD')[0] if len(tags.get('MOOD')) != 0 else 'NA'
            self.ui.track_info_misc_3.setText(f'Mood: {MOOD}')

            BITRATE = tags.get('BITRATE')[0] if len(tags.get('BITRATE')) != 0 else 0
            BITRATE = 'NA' if BITRATE is None else f'{int(BITRATE / 1000)}Kbps'
            CHANNELS = tags.get('CHANNELS')[0] if len(tags.get('CHANNELS')) != 0 else 0
            CHANNELS = 'NA' if CHANNELS is None else f'{CHANNELS} Channels'
            SAMPLERATE = tags.get('SAMPLERATE')[0] if len(tags.get('SAMPLERATE')) != 0 else 0
            SAMPLERATE = 'NA' if SAMPLERATE is None else f'{SAMPLERATE}Hz'

            self.ui.track_info_stream.setText("{0}, {1}, {2}".format(BITRATE, CHANNELS, SAMPLERATE))
            self.load_rating(tags.get('POPULARIMETER', 0))

            widget = self.ui.track_info_cover_pixmap
            if tags.get('PICTURE')[0]:
                image = QtGui.QImage().fromData(metadata.Artwork[0].data)
                pixmap = QtGui.QPixmap.fromImage(image)
                widget.setPixmap(pixmap)

    def load_rating(self, rating: Optional[float] = 0):
        """
        Loads the user defined rating of the current track

        Args:
            rating (Optional[float]): track rating
        """
        widget: TrackRatingWidget = self.ui.playback_footer_track_rating
        widget.setRating(rating)

    def state_change_seek_slider(self, value: int):
        """
        Seeks to a given time on the audio buffer

        Args:
            value (int): Value in seconds
        """
        if value != 0:
            value = self.ui.playback_footer_track_seek_slider.maximum() - value
            self.ui.playback_footer_track_elapsed.setText(f"-{time.strftime('%H:%M:%S', time.gmtime(value))}")
        else:
            value = self.ui.playback_footer_track_seek_slider.maximum()
            self.ui.playback_footer_track_elapsed.setText(f"-{time.strftime('%H:%M:%S', time.gmtime(value))}")
        self.call_state_change_seek_slider(value)

    @abc.abstractmethod
    def call_state_change_seek_slider(self, time_s: int): ...

    @abc.abstractmethod
    def call_state_change_play(self, state: Optional[Union[STATE_PLAY, str]]): ...

    @abc.abstractmethod
    def call_state_change_shuffle(self, state: Optional[Union[STATE_SHUFFLE, str]]): ...

    @abc.abstractmethod
    def call_state_change_repeat(self, state: Optional[Union[STATE_REPEAT, str]]): ...

    @abc.abstractmethod
    def call_state_change_volume_level(self, volume: int): ...

    @abc.abstractmethod
    def call_track_prev(self): ...

    @abc.abstractmethod
    def call_track_next(self): ...

    @abc.abstractmethod
    def call_track_rating(self, rating: float): ...

    @abc.abstractmethod
    def call_bypass_processor(self, state: bool): ...

    @abc.abstractmethod
    def call_on_shutdown(self): ...


class Playback_Bar_Controller:

    def __init__(self) -> None:
        self.library_model = ModelProvider.get_model(LibraryModel)
        self.queue_model = ModelProvider.get_model(QueueModel)

    def bind_models(self, view: QtWidgets.QAbstractItemView):
        view.setModel(self.queue_model)
        view.verticalScrollbarValueChanged = lambda x: (self.scroll_paging(view, x))
        self.queue_model.fetch_data(self.queue_model.FETCH_SCROLL_DOWN)

    def scroll_paging(self, view: QtWidgets.QAbstractItemView, value: int):
        if value == view.verticalScrollBar().minimum():
            if self.queue_model.fetch_data(self.queue_model.FETCH_SCROLL_UP):
                view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))
        if value == view.verticalScrollBar().maximum():
            if self.queue_model.fetch_data(self.queue_model.FETCH_SCROLL_DOWN):
                view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))


class Playback_Bar(Playback_Bar_Interactions, Playback_Bar_Controller):  # TODO: Documentation

    def __init__(self, ui: Apollo) -> None:
        Playback_Bar_Interactions.__init__(self, ui)
        Playback_Bar_Controller.__init__(self)
        self.bind_models(self.ui.queue_main_listview)

    def call_state_change_play(self, state: Optional[Union[STATE_PLAY, str]]):
        LOGGER.debug(state)

    def call_state_change_shuffle(self, state: Optional[Union[STATE_SHUFFLE, str]]):
        LOGGER.debug(state)

    def call_state_change_repeat(self, state: Optional[Union[STATE_REPEAT, str]]):
        LOGGER.debug(state)

    def call_state_change_volume_level(self, volume: int):
        LOGGER.debug(volume)

    def call_track_prev(self):
        LOGGER.debug('prev')

    def call_track_next(self):
        LOGGER.debug('next')

    def call_track_rating(self, rating: float):
        LOGGER.debug(rating)

    def call_bypass_processor(self, state: bool):
        LOGGER.debug(state)

    def call_state_change_seek_slider(self, time_s: int):
        LOGGER.debug(time_s)

    def call_on_shutdown(self):
        LOGGER.debug('SHUTDOWN')
