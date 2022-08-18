# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setWindowOpacity(1.000000000000000)
        MainWindow.setStyleSheet("")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.navbar_header_frame = QFrame(self.centralwidget)
        self.navbar_header_frame.setObjectName("navbar_header_frame")
        self.navbar_header_frame.setMinimumSize(QSize(0, 28))
        self.navbar_header_frame.setMaximumSize(QSize(16777215, 28))
        self.navbar_header_frame.setFrameShape(QFrame.NoFrame)
        self.navbar_header_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.navbar_header_frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.navbar_header_button_frame = QFrame(self.navbar_header_frame)
        self.navbar_header_button_frame.setObjectName("navbar_header_button_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.navbar_header_button_frame.sizePolicy().hasHeightForWidth()
        )
        self.navbar_header_button_frame.setSizePolicy(sizePolicy)
        self.navbar_header_button_frame.setMinimumSize(QSize(0, 24))
        self.navbar_header_button_frame.setMaximumSize(QSize(16777215, 24))
        self.navbar_header_button_frame.setFrameShape(QFrame.NoFrame)
        self.navbar_header_button_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.navbar_header_button_frame)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(2, 0, 2, 0)
        self.library_tab_switch_button = QPushButton(self.navbar_header_button_frame)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.library_tab_switch_button)
        self.library_tab_switch_button.setObjectName("library_tab_switch_button")
        self.library_tab_switch_button.setMinimumSize(QSize(0, 24))
        self.library_tab_switch_button.setMaximumSize(QSize(16777215, 24))
        self.library_tab_switch_button.setCheckable(True)
        self.library_tab_switch_button.setChecked(True)
        self.library_tab_switch_button.setFlat(True)

        self.horizontalLayout_4.addWidget(
            self.library_tab_switch_button, 0, Qt.AlignLeft | Qt.AlignVCenter
        )

        self.now_playing_tab_switch_button = QPushButton(self.navbar_header_button_frame)
        self.buttonGroup.addButton(self.now_playing_tab_switch_button)
        self.now_playing_tab_switch_button.setObjectName("now_playing_tab_switch_button")
        self.now_playing_tab_switch_button.setMinimumSize(QSize(0, 24))
        self.now_playing_tab_switch_button.setMaximumSize(QSize(16777215, 24))
        self.now_playing_tab_switch_button.setCheckable(True)
        self.now_playing_tab_switch_button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.now_playing_tab_switch_button)

        self.playlist_tab_switch_button = QPushButton(self.navbar_header_button_frame)
        self.buttonGroup.addButton(self.playlist_tab_switch_button)
        self.playlist_tab_switch_button.setObjectName("playlist_tab_switch_button")
        self.playlist_tab_switch_button.setMinimumSize(QSize(0, 24))
        self.playlist_tab_switch_button.setMaximumSize(QSize(16777215, 24))
        self.playlist_tab_switch_button.setCheckable(True)
        self.playlist_tab_switch_button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.playlist_tab_switch_button)

        self.audiofx_tab_switch_button = QPushButton(self.navbar_header_button_frame)
        self.buttonGroup.addButton(self.audiofx_tab_switch_button)
        self.audiofx_tab_switch_button.setObjectName("audiofx_tab_switch_button")
        self.audiofx_tab_switch_button.setMinimumSize(QSize(0, 24))
        self.audiofx_tab_switch_button.setMaximumSize(QSize(16777215, 24))
        self.audiofx_tab_switch_button.setCheckable(True)
        self.audiofx_tab_switch_button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.audiofx_tab_switch_button)

        self.horizontalLayout_3.addWidget(self.navbar_header_button_frame, 0, Qt.AlignVCenter)

        self.horizontalSpacer_2 = QSpacerItem(81, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.navbar_header_search_frame = QFrame(self.navbar_header_frame)
        self.navbar_header_search_frame.setObjectName("navbar_header_search_frame")
        self.navbar_header_search_frame.setMinimumSize(QSize(220, 0))
        self.navbar_header_search_frame.setMaximumSize(QSize(220, 16777215))
        self.navbar_header_search_frame.setFrameShape(QFrame.NoFrame)
        self.navbar_header_search_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.navbar_header_search_frame)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(2)
        self.gridLayout_6.setVerticalSpacing(0)
        self.gridLayout_6.setContentsMargins(2, 0, 2, 0)
        self.settings_button = QPushButton(self.navbar_header_search_frame)
        self.settings_button.setObjectName("settings_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.settings_button.sizePolicy().hasHeightForWidth())
        self.settings_button.setSizePolicy(sizePolicy1)
        self.settings_button.setMinimumSize(QSize(24, 24))
        self.settings_button.setMaximumSize(QSize(24, 24))
        self.settings_button.setFlat(True)

        self.gridLayout_6.addWidget(self.settings_button, 0, 0, 1, 1, Qt.AlignVCenter)

        self.search_button = QPushButton(self.navbar_header_search_frame)
        self.search_button.setObjectName("search_button")
        sizePolicy1.setHeightForWidth(self.search_button.sizePolicy().hasHeightForWidth())
        self.search_button.setSizePolicy(sizePolicy1)
        self.search_button.setMinimumSize(QSize(24, 24))
        self.search_button.setMaximumSize(QSize(24, 24))
        self.search_button.setFlat(True)

        self.gridLayout_6.addWidget(self.search_button, 0, 2, 1, 1, Qt.AlignVCenter)

        self.search_lineEdit = QLineEdit(self.navbar_header_search_frame)
        self.search_lineEdit.setObjectName("search_lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.search_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_lineEdit.setSizePolicy(sizePolicy2)
        self.search_lineEdit.setMinimumSize(QSize(160, 24))
        self.search_lineEdit.setMaximumSize(QSize(160, 24))
        self.search_lineEdit.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.search_lineEdit, 0, 1, 1, 1)

        self.horizontalLayout_3.addWidget(self.navbar_header_search_frame, 0, Qt.AlignVCenter)

        self.gridLayout.addWidget(self.navbar_header_frame, 0, 0, 1, 1)

        self.playback_footer_frame = QFrame(self.centralwidget)
        self.playback_footer_frame.setObjectName("playback_footer_frame")
        self.playback_footer_frame.setMinimumSize(QSize(0, 48))
        self.playback_footer_frame.setMaximumSize(QSize(16777215, 48))
        self.playback_footer_frame.setFrameShape(QFrame.NoFrame)
        self.playback_footer_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.playback_footer_frame)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.playback_footer_frame_L = QFrame(self.playback_footer_frame)
        self.playback_footer_frame_L.setObjectName("playback_footer_frame_L")
        self.playback_footer_frame_L.setMinimumSize(QSize(160, 48))
        self.playback_footer_frame_L.setMaximumSize(QSize(16777215, 48))
        self.playback_footer_frame_L.setFrameShape(QFrame.NoFrame)
        self.playback_footer_frame_L.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.playback_footer_frame_L)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.playback_button_prev = QPushButton(self.playback_footer_frame_L)
        self.playback_button_prev.setObjectName("playback_button_prev")
        self.playback_button_prev.setMinimumSize(QSize(32, 32))
        self.playback_button_prev.setMaximumSize(QSize(32, 32))
        self.playback_button_prev.setFlat(True)

        self.horizontalLayout_2.addWidget(
            self.playback_button_prev, 0, Qt.AlignHCenter | Qt.AlignVCenter
        )

        self.playback_button_play_pause = QPushButton(self.playback_footer_frame_L)
        self.playback_button_play_pause.setObjectName("playback_button_play_pause")
        self.playback_button_play_pause.setMinimumSize(QSize(40, 40))
        self.playback_button_play_pause.setMaximumSize(QSize(40, 40))
        self.playback_button_play_pause.setFlat(True)

        self.horizontalLayout_2.addWidget(
            self.playback_button_play_pause, 0, Qt.AlignHCenter | Qt.AlignVCenter
        )

        self.playback_button_next = QPushButton(self.playback_footer_frame_L)
        self.playback_button_next.setObjectName("playback_button_next")
        self.playback_button_next.setMinimumSize(QSize(32, 32))
        self.playback_button_next.setMaximumSize(QSize(32, 32))
        self.playback_button_next.setFlat(True)

        self.horizontalLayout_2.addWidget(
            self.playback_button_next, 0, Qt.AlignHCenter | Qt.AlignVCenter
        )

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalLayout.addWidget(self.playback_footer_frame_L, 0, Qt.AlignLeft)

        self.playback_footer_frame_M = QFrame(self.playback_footer_frame)
        self.playback_footer_frame_M.setObjectName("playback_footer_frame_M")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.playback_footer_frame_M.sizePolicy().hasHeightForWidth())
        self.playback_footer_frame_M.setSizePolicy(sizePolicy3)
        self.playback_footer_frame_M.setMinimumSize(QSize(0, 48))
        self.playback_footer_frame_M.setMaximumSize(QSize(800, 48))
        self.playback_footer_frame_M.setMouseTracking(True)
        self.gridLayout_4 = QGridLayout(self.playback_footer_frame_M)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 6)
        self.playback_footer_frame_M_info = QFrame(self.playback_footer_frame_M)
        self.playback_footer_frame_M_info.setObjectName("playback_footer_frame_M_info")
        self.playback_footer_frame_M_info.setMouseTracking(True)
        self.playback_footer_frame_M_info.setFrameShape(QFrame.NoFrame)
        self.playback_footer_frame_M_info.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.playback_footer_frame_M_info)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.playback_footer_track_rating = QWidget(self.playback_footer_frame_M_info)
        self.playback_footer_track_rating.setObjectName("playback_footer_track_rating")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.playback_footer_track_rating.sizePolicy().hasHeightForWidth()
        )
        self.playback_footer_track_rating.setSizePolicy(sizePolicy4)
        self.playback_footer_track_rating.setMinimumSize(QSize(100, 28))
        self.playback_footer_track_rating.setMaximumSize(QSize(100, 28))
        self.playback_footer_track_rating.setMouseTracking(True)

        self.horizontalLayout_5.addWidget(self.playback_footer_track_rating)

        self.playback_footer_track_title = QLabel(self.playback_footer_frame_M_info)
        self.playback_footer_track_title.setObjectName("playback_footer_track_title")
        sizePolicy3.setHeightForWidth(
            self.playback_footer_track_title.sizePolicy().hasHeightForWidth()
        )
        self.playback_footer_track_title.setSizePolicy(sizePolicy3)
        self.playback_footer_track_title.setMinimumSize(QSize(0, 28))
        self.playback_footer_track_title.setMaximumSize(QSize(16777215, 28))
        font = QFont()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(10)
        font.setBold(True)
        self.playback_footer_track_title.setFont(font)
        self.playback_footer_track_title.setScaledContents(False)
        self.playback_footer_track_title.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.playback_footer_track_title)

        self.playback_footer_track_elapsed = QLabel(self.playback_footer_frame_M_info)
        self.playback_footer_track_elapsed.setObjectName("playback_footer_track_elapsed")
        sizePolicy4.setHeightForWidth(
            self.playback_footer_track_elapsed.sizePolicy().hasHeightForWidth()
        )
        self.playback_footer_track_elapsed.setSizePolicy(sizePolicy4)
        self.playback_footer_track_elapsed.setMinimumSize(QSize(100, 28))
        self.playback_footer_track_elapsed.setMaximumSize(QSize(100, 28))
        self.playback_footer_track_elapsed.setFont(font)
        self.playback_footer_track_elapsed.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )

        self.horizontalLayout_5.addWidget(self.playback_footer_track_elapsed)

        self.gridLayout_4.addWidget(self.playback_footer_frame_M_info, 0, 0, 1, 2)

        self.playback_footer_track_seek_slider = QSlider(self.playback_footer_frame_M)
        self.playback_footer_track_seek_slider.setObjectName("playback_footer_track_seek_slider")
        sizePolicy2.setHeightForWidth(
            self.playback_footer_track_seek_slider.sizePolicy().hasHeightForWidth()
        )
        self.playback_footer_track_seek_slider.setSizePolicy(sizePolicy2)
        self.playback_footer_track_seek_slider.setMinimumSize(QSize(0, 8))
        self.playback_footer_track_seek_slider.setMaximumSize(QSize(16777215, 8))
        self.playback_footer_track_seek_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.playback_footer_track_seek_slider, 1, 0, 1, 2)

        self.horizontalLayout.addWidget(self.playback_footer_frame_M)

        self.playback_footer_frame_R = QFrame(self.playback_footer_frame)
        self.playback_footer_frame_R.setObjectName("playback_footer_frame_R")
        sizePolicy.setHeightForWidth(self.playback_footer_frame_R.sizePolicy().hasHeightForWidth())
        self.playback_footer_frame_R.setSizePolicy(sizePolicy)
        self.playback_footer_frame_R.setMinimumSize(QSize(160, 0))
        self.playback_footer_frame_R.setMaximumSize(QSize(16777215, 16777215))
        self.playback_footer_frame_R.setFrameShape(QFrame.NoFrame)
        self.playback_footer_frame_R.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.playback_footer_frame_R)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 8, 6)
        self.playback_button_volume_control = QPushButton(self.playback_footer_frame_R)
        self.playback_button_volume_control.setObjectName("playback_button_volume_control")
        self.playback_button_volume_control.setMinimumSize(QSize(28, 28))
        self.playback_button_volume_control.setMaximumSize(QSize(28, 28))
        self.playback_button_volume_control.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_volume_control, 0, 1, 1, 1)

        self.playback_button_play_settings = QPushButton(self.playback_footer_frame_R)
        self.playback_button_play_settings.setObjectName("playback_button_play_settings")
        self.playback_button_play_settings.setMinimumSize(QSize(28, 28))
        self.playback_button_play_settings.setMaximumSize(QSize(28, 28))
        self.playback_button_play_settings.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_play_settings, 0, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 0, 2, 1)

        self.playback_button_play_repeat = QPushButton(self.playback_footer_frame_R)
        self.playback_button_play_repeat.setObjectName("playback_button_play_repeat")
        self.playback_button_play_repeat.setMinimumSize(QSize(28, 28))
        self.playback_button_play_repeat.setMaximumSize(QSize(28, 28))
        self.playback_button_play_repeat.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_play_repeat, 0, 3, 1, 1)

        self.playback_slider_volume_control = QSlider(self.playback_footer_frame_R)
        self.playback_slider_volume_control.setObjectName("playback_slider_volume_control")
        self.playback_slider_volume_control.setMinimumSize(QSize(0, 8))
        self.playback_slider_volume_control.setMaximumSize(QSize(16777215, 8))
        self.playback_slider_volume_control.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.playback_slider_volume_control, 1, 1, 1, 5)

        self.playback_button_play_shuffle = QPushButton(self.playback_footer_frame_R)
        self.playback_button_play_shuffle.setObjectName("playback_button_play_shuffle")
        self.playback_button_play_shuffle.setMinimumSize(QSize(28, 28))
        self.playback_button_play_shuffle.setMaximumSize(QSize(28, 28))
        self.playback_button_play_shuffle.setCheckable(False)
        self.playback_button_play_shuffle.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_play_shuffle, 0, 2, 1, 1)

        self.playback_button_audio_bypass = QPushButton(self.playback_footer_frame_R)
        self.playback_button_audio_bypass.setObjectName("playback_button_audio_bypass")
        self.playback_button_audio_bypass.setMinimumSize(QSize(28, 28))
        self.playback_button_audio_bypass.setMaximumSize(QSize(28, 28))
        self.playback_button_audio_bypass.setCheckable(True)
        self.playback_button_audio_bypass.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_audio_bypass, 0, 5, 1, 1)

        self.horizontalLayout.addWidget(self.playback_footer_frame_R, 0, Qt.AlignRight)

        self.gridLayout.addWidget(self.playback_footer_frame, 2, 0, 1, 1, Qt.AlignBottom)

        self.main_tabs_frame = QSplitter(self.centralwidget)
        self.main_tabs_frame.setObjectName("main_tabs_frame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.main_tabs_frame.sizePolicy().hasHeightForWidth())
        self.main_tabs_frame.setSizePolicy(sizePolicy5)
        self.main_tabs_frame.setFrameShape(QFrame.NoFrame)
        self.main_tabs_frame.setOrientation(Qt.Horizontal)
        self.main_tabs_frame.setHandleWidth(0)
        self.main_tabs_frame.setChildrenCollapsible(False)
        self.main_tabs_stack_frame = QFrame(self.main_tabs_frame)
        self.main_tabs_stack_frame.setObjectName("main_tabs_stack_frame")
        sizePolicy3.setHeightForWidth(self.main_tabs_stack_frame.sizePolicy().hasHeightForWidth())
        self.main_tabs_stack_frame.setSizePolicy(sizePolicy3)
        self.main_tabs_stack_frame.setMinimumSize(QSize(578, 0))
        self.main_tabs_stack_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.main_tabs_stack_frame)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_10.setContentsMargins(2, 2, 2, 2)
        self.main_tabs_stack_widget = QStackedWidget(self.main_tabs_stack_frame)
        self.main_tabs_stack_widget.setObjectName("main_tabs_stack_widget")
        self.main_tabs_stack_widget.setFrameShape(QFrame.StyledPanel)
        self.library_main_tab = QWidget()
        self.library_main_tab.setObjectName("library_main_tab")
        self.verticalLayout_3 = QVBoxLayout(self.library_main_tab)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.library_main_listview = QListView(self.library_main_tab)
        self.library_main_listview.setObjectName("library_main_listview")
        self.library_main_listview.setFrameShape(QFrame.NoFrame)
        self.library_main_listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.library_main_listview.setProperty("showDropIndicator", False)
        self.library_main_listview.setDefaultDropAction(Qt.IgnoreAction)
        self.library_main_listview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.library_main_listview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.library_main_listview.setSpacing(1)
        self.library_main_listview.setUniformItemSizes(True)
        self.library_main_listview.setItemAlignment(Qt.AlignLeading)

        self.verticalLayout_3.addWidget(self.library_main_listview)

        self.main_tabs_stack_widget.addWidget(self.library_main_tab)
        self.now_playing_main_tab = QWidget()
        self.now_playing_main_tab.setObjectName("now_playing_main_tab")
        self.main_tabs_stack_widget.addWidget(self.now_playing_main_tab)
        self.playlist_main_tab = QWidget()
        self.playlist_main_tab.setObjectName("playlist_main_tab")
        self.main_tabs_stack_widget.addWidget(self.playlist_main_tab)
        self.audiofx_main_tab = QWidget()
        self.audiofx_main_tab.setObjectName("audiofx_main_tab")
        self.main_tabs_stack_widget.addWidget(self.audiofx_main_tab)

        self.gridLayout_10.addWidget(self.main_tabs_stack_widget, 0, 0, 1, 1)

        self.main_tabs_frame.addWidget(self.main_tabs_stack_frame)
        self.main_tabs_queue_frame = QFrame(self.main_tabs_frame)
        self.main_tabs_queue_frame.setObjectName("main_tabs_queue_frame")
        self.main_tabs_queue_frame.setMinimumSize(QSize(220, 0))
        self.main_tabs_queue_frame.setFrameShape(QFrame.NoFrame)
        self.main_tabs_queue_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.main_tabs_queue_frame)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.main_tabs_queue_frame_splitter = QSplitter(self.main_tabs_queue_frame)
        self.main_tabs_queue_frame_splitter.setObjectName("main_tabs_queue_frame_splitter")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(1)
        sizePolicy6.setHeightForWidth(
            self.main_tabs_queue_frame_splitter.sizePolicy().hasHeightForWidth()
        )
        self.main_tabs_queue_frame_splitter.setSizePolicy(sizePolicy6)
        self.main_tabs_queue_frame_splitter.setOrientation(Qt.Vertical)
        self.main_tabs_queue_frame_splitter.setHandleWidth(0)
        self.main_tabs_queue_frame_queue = QFrame(self.main_tabs_queue_frame_splitter)
        self.main_tabs_queue_frame_queue.setObjectName("main_tabs_queue_frame_queue")
        sizePolicy.setHeightForWidth(
            self.main_tabs_queue_frame_queue.sizePolicy().hasHeightForWidth()
        )
        self.main_tabs_queue_frame_queue.setSizePolicy(sizePolicy)
        self.main_tabs_queue_frame_queue.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setFamilies(["Segoe UI"])
        font1.setPointSize(8)
        self.main_tabs_queue_frame_queue.setFont(font1)
        self.main_tabs_queue_frame_queue.setFrameShape(QFrame.NoFrame)
        self.gridLayout_8 = QGridLayout(self.main_tabs_queue_frame_queue)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setVerticalSpacing(2)
        self.gridLayout_8.setContentsMargins(2, 2, 2, 2)
        self.queue_main_listview = QListView(self.main_tabs_queue_frame_queue)
        self.queue_main_listview.setObjectName("queue_main_listview")
        sizePolicy3.setHeightForWidth(self.queue_main_listview.sizePolicy().hasHeightForWidth())
        self.queue_main_listview.setSizePolicy(sizePolicy3)
        self.queue_main_listview.setMinimumSize(QSize(0, 156))
        self.queue_main_listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.queue_main_listview.setProperty("showDropIndicator", False)
        self.queue_main_listview.setDefaultDropAction(Qt.IgnoreAction)
        self.queue_main_listview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.queue_main_listview.setSpacing(1)
        self.queue_main_listview.setUniformItemSizes(True)
        self.queue_main_listview.setItemAlignment(Qt.AlignLeading)

        self.gridLayout_8.addWidget(self.queue_main_listview, 1, 0, 1, 1)

        self.label_19 = QLabel(self.main_tabs_queue_frame_queue)
        self.label_19.setObjectName("label_19")
        self.label_19.setMinimumSize(QSize(0, 24))
        self.label_19.setMaximumSize(QSize(16777215, 24))
        font2 = QFont()
        font2.setFamilies(["Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setKerning(False)
        font2.setStyleStrategy(QFont.PreferDefault)
        self.label_19.setFont(font2)

        self.gridLayout_8.addWidget(self.label_19, 0, 0, 1, 2)

        self.main_tabs_queue_frame_splitter.addWidget(self.main_tabs_queue_frame_queue)
        self.main_tabs_queue_frame_trackinfo = QFrame(self.main_tabs_queue_frame_splitter)
        self.main_tabs_queue_frame_trackinfo.setObjectName("main_tabs_queue_frame_trackinfo")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(
            self.main_tabs_queue_frame_trackinfo.sizePolicy().hasHeightForWidth()
        )
        self.main_tabs_queue_frame_trackinfo.setSizePolicy(sizePolicy7)
        self.main_tabs_queue_frame_trackinfo.setMinimumSize(QSize(0, 240))
        self.main_tabs_queue_frame_trackinfo.setFont(font1)
        self.main_tabs_queue_frame_trackinfo.setFrameShape(QFrame.NoFrame)
        self.gridLayout_9 = QGridLayout(self.main_tabs_queue_frame_trackinfo)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.label_18 = QLabel(self.main_tabs_queue_frame_trackinfo)
        self.label_18.setObjectName("label_18")
        self.label_18.setMinimumSize(QSize(0, 24))
        self.label_18.setMaximumSize(QSize(16777215, 24))
        self.label_18.setFont(font2)

        self.gridLayout_9.addWidget(self.label_18, 0, 0, 1, 1)

        self.main_tabs_track_info_frame = QFrame(self.main_tabs_queue_frame_trackinfo)
        self.main_tabs_track_info_frame.setObjectName("main_tabs_track_info_frame")
        self.main_tabs_track_info_frame.setFrameShape(QFrame.StyledPanel)
        self.main_tabs_track_info_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.main_tabs_track_info_frame)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(2, -1, -1, -1)
        self.track_info_title = QLabel(self.main_tabs_track_info_frame)
        self.track_info_title.setObjectName("track_info_title")
        self.track_info_title.setFont(font)

        self.verticalLayout.addWidget(self.track_info_title)

        self.track_info_misc_1 = QLabel(self.main_tabs_track_info_frame)
        self.track_info_misc_1.setObjectName("track_info_misc_1")

        self.verticalLayout.addWidget(self.track_info_misc_1)

        self.track_info_misc_2 = QLabel(self.main_tabs_track_info_frame)
        self.track_info_misc_2.setObjectName("track_info_misc_2")

        self.verticalLayout.addWidget(self.track_info_misc_2)

        self.track_info_misc_3 = QLabel(self.main_tabs_track_info_frame)
        self.track_info_misc_3.setObjectName("track_info_misc_3")

        self.verticalLayout.addWidget(self.track_info_misc_3)

        self.track_info_stream = QLabel(self.main_tabs_track_info_frame)
        self.track_info_stream.setObjectName("track_info_stream")
        font3 = QFont()
        font3.setFamilies(["Segoe UI"])
        font3.setPointSize(7)
        self.track_info_stream.setFont(font3)

        self.verticalLayout.addWidget(self.track_info_stream)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.track_info_cover_pixmap = QLabel(self.main_tabs_track_info_frame)
        self.track_info_cover_pixmap.setObjectName("track_info_cover_pixmap")
        sizePolicy3.setHeightForWidth(self.track_info_cover_pixmap.sizePolicy().hasHeightForWidth())
        self.track_info_cover_pixmap.setSizePolicy(sizePolicy3)
        font4 = QFont()
        font4.setFamilies(["Segoe UI"])
        font4.setPointSize(16)
        font4.setBold(True)
        self.track_info_cover_pixmap.setFont(font4)
        self.track_info_cover_pixmap.setFrameShape(QFrame.StyledPanel)
        self.track_info_cover_pixmap.setScaledContents(True)
        self.track_info_cover_pixmap.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.track_info_cover_pixmap)

        self.gridLayout_9.addWidget(self.main_tabs_track_info_frame, 1, 0, 1, 1)

        self.main_tabs_queue_frame_splitter.addWidget(self.main_tabs_queue_frame_trackinfo)

        self.gridLayout_7.addWidget(self.main_tabs_queue_frame_splitter, 0, 0, 1, 1)

        self.main_tabs_frame.addWidget(self.main_tabs_queue_frame)

        self.gridLayout.addWidget(self.main_tabs_frame, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.menubar.setMinimumSize(QSize(0, 24))
        self.menubar.setMaximumSize(QSize(16777215, 24))
        self.menubar.setDefaultUp(True)
        self.menubar.setNativeMenuBar(True)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        sizePolicy7.setHeightForWidth(self.menuFile.sizePolicy().hasHeightForWidth())
        self.menuFile.setSizePolicy(sizePolicy7)
        self.menuFile.setMinimumSize(QSize(0, 0))
        self.menuFile.setMaximumSize(QSize(16777215, 16777215))
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        sizePolicy7.setHeightForWidth(self.menuEdit.sizePolicy().hasHeightForWidth())
        self.menuEdit.setSizePolicy(sizePolicy7)
        self.menuEdit.setMinimumSize(QSize(0, 0))
        self.menuEdit.setMaximumSize(QSize(16777215, 16777215))
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        sizePolicy7.setHeightForWidth(self.menuTools.sizePolicy().hasHeightForWidth())
        self.menuTools.setSizePolicy(sizePolicy7)
        self.menuTools.setMinimumSize(QSize(0, 0))
        self.menuTools.setMaximumSize(QSize(16777215, 16777215))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        sizePolicy7.setHeightForWidth(self.menuHelp.sizePolicy().hasHeightForWidth())
        self.menuHelp.setSizePolicy(sizePolicy7)
        self.menuHelp.setMinimumSize(QSize(0, 0))
        self.menuHelp.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)

        self.playback_button_play_pause.setDefault(False)
        self.main_tabs_stack_widget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Apollo", None))
        self.library_tab_switch_button.setText(
            QCoreApplication.translate("MainWindow", "Library", None)
        )
        self.now_playing_tab_switch_button.setText(
            QCoreApplication.translate("MainWindow", "Now Playing", None)
        )
        self.playlist_tab_switch_button.setText(
            QCoreApplication.translate("MainWindow", "Playlist", None)
        )
        self.audiofx_tab_switch_button.setText(
            QCoreApplication.translate("MainWindow", "Audio FX", None)
        )
        self.settings_button.setText("")
        self.search_button.setText("")
        self.search_lineEdit.setInputMask("")
        self.search_lineEdit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Search", None)
        )
        self.playback_button_prev.setText("")
        self.playback_button_play_pause.setText("")
        self.playback_button_next.setText("")
        self.playback_footer_track_title.setText(
            QCoreApplication.translate("MainWindow", "Apollo - Media Player", None)
        )
        self.playback_footer_track_elapsed.setText(
            QCoreApplication.translate("MainWindow", "-00:00:00", None)
        )
        self.playback_button_volume_control.setText("")
        self.playback_button_play_settings.setText("")
        self.playback_button_play_repeat.setText("")
        self.playback_button_play_shuffle.setText("")
        self.playback_button_audio_bypass.setText("")
        self.label_19.setText(QCoreApplication.translate("MainWindow", "Playing Queue", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", "Track Information", None))
        self.track_info_title.setText(QCoreApplication.translate("MainWindow", "Track Title", None))
        self.track_info_misc_1.setText(
            QCoreApplication.translate("MainWindow", "Misc Info 1", None)
        )
        self.track_info_misc_2.setText(
            QCoreApplication.translate("MainWindow", "Misc Info 2", None)
        )
        self.track_info_misc_3.setText(
            QCoreApplication.translate("MainWindow", "Misc Info 3", None)
        )
        self.track_info_stream.setText(
            QCoreApplication.translate("MainWindow", "Stream Info", None)
        )
        self.track_info_cover_pixmap.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", "Edit", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", "Tools", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))

    # retranslateUi
