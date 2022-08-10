import abc
import datetime
import enum
import math
import os.path
import time
from pathlib import PurePath
from typing import Optional, Union

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.assets import AppIcons, AppTheme
from apollo.assets.stylesheets import luminosity
from apollo.db.models import LibraryModel, ModelProvider, QueueModel
from apollo.layout.mainwindow import Ui_MainWindow as Apollo_MainWindow
from apollo.media import Mediafile
from apollo.src.views.delegates import ViewDelegates, set_delegate
from apollo.utils import Apollo_Main_UI_TypeAlias, get_logger
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
    MUTE = "MUTE"
    QUARTER = "QUARTER"
    HALF = "HALF"
    FULL = "FULL"


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
        if self.underMouse():
            width = (round(self.mapFromGlobal(QtGui.QCursor.pos()).x() / self.width(), 1) / 2) * 10
            self._rating = width
            self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.underMouse():
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
        painter.end()

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
        painter.restore()

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
        painter.drawPixmap(
            QtCore.QPoint(pos, 6), QtGui.QPixmap.fromImage(QtGui.QImage(star)).scaled(size, size)
        )


class Playback_Bar_Interactions(abc.ABC):
    """
    Playback Bar Interactions
    """

    _STATE_PLAY = CONFIG.get("APOLLO.PLAYBACK_BAR.STATE_PLAY", STATE_PLAY.PAUSE.name)
    _STATE_SHUFFLE = CONFIG.get("APOLLO.PLAYBACK_BAR.STATE_SHUFFLE", STATE_SHUFFLE.NONE.name)
    _STATE_REPEAT = CONFIG.get("APOLLO.PLAYBACK_BAR.STATE_REPEAT", STATE_REPEAT.NONE.name)
    _STATE_VOLUME_LEVEL = STATE_VOLUME_LEVEL.HALF.name
    _VOLUME_LEVEL = CONFIG.get("APOLLO.PLAYBACK_BAR.VOLUME_LEVEL", 50)
    _LOADED_TRACK = CONFIG.get("APOLLO.PLAYBACK_BAR.LOADED_TRACK", None)
    _BYPASS_PROCESSOR = CONFIG.get("APOLLO.PLAYBACK_BAR.BYPASS_PROCESSOR", True)
    _ELAPSED_TIME = CONFIG.get("APOLLO.PLAYBACK_BAR.ELAPSED_TIME", 0)
    _CURRENT_PLAYING = CONFIG.get("APOLLO.PLAYBACK_BAR.CURRENT_PLAYING", None)

    def __init__(self, ui: Apollo_Main_UI_TypeAlias) -> None:
        """
        Constructor

        Args:
            ui (Apollo): UI objects
        """
        self.UI = ui
        self.UI.playback_footer_track_rating = TrackRatingWidget(self.UI.playback_footer_frame_M)

        self.setup_interactions()
        self.setup_defaults()

    def setup_interactions(self):
        """
        Sets up interactions
        """
        self.UI.playback_button_play_pause.pressed.connect(lambda: (self.state_change_play()))
        self.UI.playback_button_prev.pressed.connect(lambda: self.cb_track_prev())
        self.UI.playback_button_next.pressed.connect(lambda: self.cb_track_next())
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
            lambda x: self.cb_track_rating(x)
        )
        self.UI.queue_main_listview.doubleClicked.connect(
            lambda x: self.cb_queue_list_item_Dclick(x)
        )
        self.UI.SIGNALS.PlayTrackSignal.connect(lambda fid: self.cb_load_track_info(fid))

    def setup_defaults(self):
        """
        Sets up default states
        """
        self.state_change_play(self._STATE_PLAY)
        self.state_change_shuffle(self._STATE_SHUFFLE)
        self.state_change_repeat(self._STATE_REPEAT)
        self.state_change_volume_level(self._VOLUME_LEVEL)
        self.UI.playback_slider_volume_control.setValue(self._VOLUME_LEVEL)
        self.state_change_processor_bypass(self._BYPASS_PROCESSOR)
        self.UI.playback_footer_track_seek_slider.setValue(self._ELAPSED_TIME)
        self.load_rating()

        QueueModel.CURRENT_FILE_ID = self._CURRENT_PLAYING
        self.UI.queue_main_listview.repaint()

    def save_states(self):
        """
        saves session states of Apollo
        """
        CONFIG["APOLLO.PLAYBACK_BAR.STATE_PLAY"] = self._STATE_PLAY
        CONFIG["APOLLO.PLAYBACK_BAR.STATE_SHUFFLE"] = self._STATE_SHUFFLE
        CONFIG["APOLLO.PLAYBACK_BAR.STATE_REPEAT"] = self._STATE_REPEAT
        CONFIG["APOLLO.PLAYBACK_BAR.VOLUME_LEVEL"] = self._VOLUME_LEVEL
        CONFIG["APOLLO.PLAYBACK_BAR.LOADED_TRACK"] = self._LOADED_TRACK
        CONFIG["APOLLO.PLAYBACK_BAR.BYPASS_PROCESSOR"] = self._BYPASS_PROCESSOR
        value = self.UI.playback_footer_track_seek_slider.value()
        CONFIG["APOLLO.PLAYBACK_BAR.ELAPSED_TIME"] = value
        value: QueueModel = self.UI.queue_main_listview.model()
        CONFIG["APOLLO.PLAYBACK_BAR.CURRENT_PLAYING"] = value.CURRENT_FILE_ID

    def state_change_processor_bypass(self, state: bool):
        """
        Enables and disables the bypass of output through the processor

        Args:
            state (bool): bypass state
        """
        self._BYPASS_PROCESSOR = state
        self.cb_bypass_processor(state)

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

        # APPLIES CONTROL CHANGES TODO
        self.cb_state_change_play(self._STATE_PLAY)

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

        # APPLIES CONTROL CHANGES TODO
        self.cb_state_change_shuffle(self._STATE_SHUFFLE)

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

        # APPLIES CONTROL CHANGES TODO
        self.cb_state_change_repeat(self._STATE_REPEAT)

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

            # APPLIES CONTROL CHANGES TODO
            self._VOLUME_LEVEL = level
            self.cb_state_change_volume_level(level)

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
        self.cb_state_change_seek_slider(value)

    @abc.abstractmethod
    def cb_state_change_seek_slider(self, time_s: int):
        ...

    @abc.abstractmethod
    def cb_state_change_play(self, state: Optional[Union[STATE_PLAY, str]]):
        ...

    @abc.abstractmethod
    def cb_state_change_shuffle(self, state: Optional[Union[STATE_SHUFFLE, str]]):
        ...

    @abc.abstractmethod
    def cb_state_change_repeat(self, state: Optional[Union[STATE_REPEAT, str]]):
        ...

    @abc.abstractmethod
    def cb_state_change_volume_level(self, volume: int):
        ...

    @abc.abstractmethod
    def cb_track_prev(self):
        ...

    @abc.abstractmethod
    def cb_track_next(self):
        ...

    @abc.abstractmethod
    def cb_track_rating(self, rating: float):
        ...

    @abc.abstractmethod
    def cb_bypass_processor(self, state: bool):
        ...

    @abc.abstractmethod
    def cb_queue_list_item_Dclick(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        ...

    @abc.abstractmethod
    def cb_load_track_info(self, fid: Optional[str] = None):
        ...


class Playback_Bar_Controller:
    """
    Playback_Bar_Controller
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.library_model = ModelProvider.get_model(LibraryModel)
        self.queue_model = ModelProvider.get_model(QueueModel)

    def bind_models(self, view: QtWidgets.QAbstractItemView):
        """
        Binds models with Views

        Args:
            view (QtWidgets.QAbstractItemView): view to bind models to
        """
        view.viewport().setStyleSheet(
            f"background-color: {luminosity(AppTheme['QTCOLOR_PRIMARYDARKCOLOR'], 0.125)}"
        )
        view.setModel(self.queue_model)
        set_delegate(view, ViewDelegates.TrackDelegate_Small_Queue)
        # noinspection PyUnresolvedReferences
        view.verticalScrollBar().valueChanged.connect(lambda x: (self._cb_scroll_paging(view, x)))
        self.queue_model.fetch_data(self.queue_model.FETCH_DATA_DOWN)
        view.ensurePolished()

    def _cb_scroll_paging(self, view: QtWidgets.QAbstractItemView, value: int):
        """
        On scroll Loader for paged models

        Args:
            view (QtWidgets.QAbstractItemView): View to get scroll event from
            value (int): Scroll value
        """

        def reset_slider():
            view.verticalScrollbarValueChanged = lambda x: None
            view.verticalScrollBar().setValue(int(view.verticalScrollBar().maximum() / 2))
            view.verticalScrollbarValueChanged = lambda x: (self._cb_scroll_paging(view, x))

        if value == view.verticalScrollBar().minimum():
            if self.queue_model.fetch_data(self.queue_model.FETCH_DATA_UP):
                reset_slider()
        if value == view.verticalScrollBar().maximum():
            if self.queue_model.fetch_data(self.queue_model.FETCH_DATA_DOWN):
                reset_slider()

    def save_states(self):
        """
        saves session states of Apollo
        """
        pass


class Playback_Bar(Playback_Bar_Interactions, Playback_Bar_Controller):  # TODO: Documentation
    """
    Playback_Bar
    """

    def __init__(self, ui: Apollo_Main_UI_TypeAlias) -> None:
        self.UI = ui
        Playback_Bar_Interactions.__init__(self, self.UI)
        Playback_Bar_Controller.__init__(self)
        self.bind_models(self.UI.queue_main_listview)

    def save_states(self):
        """
        Shutdown callback
        """
        Playback_Bar_Interactions.save_states(self)
        Playback_Bar_Controller.save_states(self)

    def cb_load_track_info(self, fid: Optional[str] = None):
        """
        Loads the track fid into the UI

        Args:
            fid (Optional[Mediafile]): Audio Metadata
        """
        if fid is None:
            self.UI.playback_footer_track_title.setText("Apollo - Media Player")
            self.UI.playback_footer_track_seek_slider.setRange(0, 100)
            self.UI.playback_footer_track_seek_slider.setSingleStep(5)
            self.load_rating(0)
            elapsed_time = time.strftime(
                "%H:%M:%S", time.gmtime(self.UI.playback_footer_track_seek_slider.maximum())
            )
            self.UI.playback_footer_track_elapsed.setText(f"-{elapsed_time}")
            self.UI.track_info_title.setText(f"Title: NA")
            self.UI.track_info_misc_1.setText(f"Artist: NA")
            self.UI.track_info_misc_2.setText(f"Album: NA")
            self.UI.track_info_misc_3.setText(f"Mood: NA")
            self.UI.track_info_stream.setText("NA, NA, NA")

        elif fid is not None:
            tags = self.library_model.fetch_track_info(fid)
            self._LOADED_TRACK = PurePath(tags.get(("FILEPATH", 0))).as_posix()

            # POPULATE FOOTER ITEMS
            self.UI.playback_footer_track_title.setText(
                tags.get(("TITLE", 0), "Apollo - Media Player")
            )

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

    def cb_queue_list_item_Dclick(
        self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]
    ):
        data = self.queue_model.index(index.row(), 1)
        if data.row() != -1:
            self.queue_model.CURRENT_FILE_ID = data.data()
            self.UI.queue_main_listview.repaint()
            self.UI.SIGNALS.PlayTrackSignal.emit(self.queue_model.CURRENT_FILE_ID)

    def cb_search(self):
        if self.UI.main_tabs_stack_widget.currentIndex() == 1:
            self.queue_model.set_filter(self.UI.search_lineEdit.text())

    def cb_clear_search(self):
        if self.UI.main_tabs_stack_widget.currentIndex() == 1:
            self.queue_model.clear_filter()

    def cb_state_change_play(self, state: Optional[Union[STATE_PLAY, str]]):
        LOGGER.debug(state)

    def cb_state_change_shuffle(self, state: Optional[Union[STATE_SHUFFLE, str]]):
        LOGGER.debug(state)

    def cb_state_change_repeat(self, state: Optional[Union[STATE_REPEAT, str]]):
        LOGGER.debug(state)

    def cb_state_change_volume_level(self, volume: int):
        LOGGER.debug(volume)

    def cb_track_prev(self):
        LOGGER.debug("prev")

    def cb_track_next(self):
        LOGGER.debug("next")

    def cb_track_rating(self, rating: float):
        LOGGER.debug(rating)

    def cb_bypass_processor(self, state: bool):
        LOGGER.debug(state)

    def cb_state_change_seek_slider(self, time_s: int):
        LOGGER.debug(time_s)
