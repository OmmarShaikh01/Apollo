# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListView, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QSplitter, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.navbar_header_frame = QFrame(self.centralwidget)
        self.navbar_header_frame.setObjectName(u"navbar_header_frame")
        self.navbar_header_frame.setMinimumSize(QSize(0, 28))
        self.navbar_header_frame.setMaximumSize(QSize(16777215, 28))
        self.navbar_header_frame.setFrameShape(QFrame.NoFrame)
        self.navbar_header_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.navbar_header_frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.navbar_header_button_frame = QFrame(self.navbar_header_frame)
        self.navbar_header_button_frame.setObjectName(u"navbar_header_button_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.navbar_header_button_frame.sizePolicy().hasHeightForWidth())
        self.navbar_header_button_frame.setSizePolicy(sizePolicy)
        self.navbar_header_button_frame.setMinimumSize(QSize(0, 24))
        self.navbar_header_button_frame.setMaximumSize(QSize(16777215, 24))
        self.navbar_header_button_frame.setFrameShape(QFrame.NoFrame)
        self.navbar_header_button_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.navbar_header_button_frame)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(2, 0, 2, 0)
        self.library_tab_switch_button = QPushButton(self.navbar_header_button_frame)
        self.library_tab_switch_button.setObjectName(u"library_tab_switch_button")
        self.library_tab_switch_button.setMinimumSize(QSize(0, 24))
        self.library_tab_switch_button.setMaximumSize(QSize(16777215, 24))
        self.library_tab_switch_button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.library_tab_switch_button, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.now_playing_tab_switch_button = QPushButton(self.navbar_header_button_frame)
        self.now_playing_tab_switch_button.setObjectName(u"now_playing_tab_switch_button")
        self.now_playing_tab_switch_button.setMinimumSize(QSize(0, 24))
        self.now_playing_tab_switch_button.setMaximumSize(QSize(16777215, 24))
        self.now_playing_tab_switch_button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.now_playing_tab_switch_button)

        self.playlist_tab_switch_button = QPushButton(self.navbar_header_button_frame)
        self.playlist_tab_switch_button.setObjectName(u"playlist_tab_switch_button")
        self.playlist_tab_switch_button.setMinimumSize(QSize(0, 24))
        self.playlist_tab_switch_button.setMaximumSize(QSize(16777215, 24))
        self.playlist_tab_switch_button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.playlist_tab_switch_button)

        self.audiofx_tab_switch_button = QPushButton(self.navbar_header_button_frame)
        self.audiofx_tab_switch_button.setObjectName(u"audiofx_tab_switch_button")
        self.audiofx_tab_switch_button.setMinimumSize(QSize(0, 24))
        self.audiofx_tab_switch_button.setMaximumSize(QSize(16777215, 24))
        self.audiofx_tab_switch_button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.audiofx_tab_switch_button)


        self.horizontalLayout_3.addWidget(self.navbar_header_button_frame, 0, Qt.AlignVCenter)

        self.horizontalSpacer_2 = QSpacerItem(81, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.navbar_header_search_frame = QFrame(self.navbar_header_frame)
        self.navbar_header_search_frame.setObjectName(u"navbar_header_search_frame")
        self.navbar_header_search_frame.setMinimumSize(QSize(220, 0))
        self.navbar_header_search_frame.setMaximumSize(QSize(220, 16777215))
        self.navbar_header_search_frame.setFrameShape(QFrame.NoFrame)
        self.navbar_header_search_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.navbar_header_search_frame)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(2)
        self.gridLayout_6.setVerticalSpacing(0)
        self.gridLayout_6.setContentsMargins(2, 0, 2, 0)
        self.settings_button = QPushButton(self.navbar_header_search_frame)
        self.settings_button.setObjectName(u"settings_button")
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
        self.search_button.setObjectName(u"search_button")
        sizePolicy1.setHeightForWidth(self.search_button.sizePolicy().hasHeightForWidth())
        self.search_button.setSizePolicy(sizePolicy1)
        self.search_button.setMinimumSize(QSize(24, 24))
        self.search_button.setMaximumSize(QSize(24, 24))
        self.search_button.setFlat(True)

        self.gridLayout_6.addWidget(self.search_button, 0, 2, 1, 1, Qt.AlignVCenter)

        self.lineEdit = QLineEdit(self.navbar_header_search_frame)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy2)
        self.lineEdit.setMinimumSize(QSize(160, 24))
        self.lineEdit.setMaximumSize(QSize(160, 24))
        self.lineEdit.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit, 0, 1, 1, 1)


        self.horizontalLayout_3.addWidget(self.navbar_header_search_frame, 0, Qt.AlignVCenter)


        self.gridLayout.addWidget(self.navbar_header_frame, 0, 0, 1, 1)

        self.playback_footer_frame = QFrame(self.centralwidget)
        self.playback_footer_frame.setObjectName(u"playback_footer_frame")
        self.playback_footer_frame.setMinimumSize(QSize(0, 48))
        self.playback_footer_frame.setMaximumSize(QSize(16777215, 48))
        self.playback_footer_frame.setFrameShape(QFrame.NoFrame)
        self.playback_footer_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.playback_footer_frame)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.playback_footer_frame_L = QFrame(self.playback_footer_frame)
        self.playback_footer_frame_L.setObjectName(u"playback_footer_frame_L")
        self.playback_footer_frame_L.setMinimumSize(QSize(160, 48))
        self.playback_footer_frame_L.setMaximumSize(QSize(16777215, 48))
        self.playback_footer_frame_L.setFrameShape(QFrame.NoFrame)
        self.playback_footer_frame_L.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.playback_footer_frame_L)
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.playback_button_prev = QPushButton(self.playback_footer_frame_L)
        self.playback_button_prev.setObjectName(u"playback_button_prev")
        self.playback_button_prev.setMinimumSize(QSize(32, 32))
        self.playback_button_prev.setMaximumSize(QSize(32, 32))
        self.playback_button_prev.setFlat(True)

        self.horizontalLayout_2.addWidget(self.playback_button_prev, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.playback_button_play_pause = QPushButton(self.playback_footer_frame_L)
        self.playback_button_play_pause.setObjectName(u"playback_button_play_pause")
        self.playback_button_play_pause.setMinimumSize(QSize(40, 40))
        self.playback_button_play_pause.setMaximumSize(QSize(40, 40))
        self.playback_button_play_pause.setFlat(True)

        self.horizontalLayout_2.addWidget(self.playback_button_play_pause, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.playback_button_next = QPushButton(self.playback_footer_frame_L)
        self.playback_button_next.setObjectName(u"playback_button_next")
        self.playback_button_next.setMinimumSize(QSize(32, 32))
        self.playback_button_next.setMaximumSize(QSize(32, 32))
        self.playback_button_next.setFlat(True)

        self.horizontalLayout_2.addWidget(self.playback_button_next, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.horizontalLayout.addWidget(self.playback_footer_frame_L, 0, Qt.AlignLeft)

        self.playback_footer_frame_M = QFrame(self.playback_footer_frame)
        self.playback_footer_frame_M.setObjectName(u"playback_footer_frame_M")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.playback_footer_frame_M.sizePolicy().hasHeightForWidth())
        self.playback_footer_frame_M.setSizePolicy(sizePolicy3)
        self.playback_footer_frame_M.setMinimumSize(QSize(0, 48))
        self.playback_footer_frame_M.setMaximumSize(QSize(800, 48))
        self.gridLayout_4 = QGridLayout(self.playback_footer_frame_M)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(4)
        self.gridLayout_4.setVerticalSpacing(2)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 2)
        self.label_9 = QLabel(self.playback_footer_frame_M)
        self.label_9.setObjectName(u"label_9")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy4)
        self.label_9.setMinimumSize(QSize(0, 28))
        self.label_9.setMaximumSize(QSize(16777215, 28))
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_11 = QLabel(self.playback_footer_frame_M)
        self.label_11.setObjectName(u"label_11")
        sizePolicy4.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy4)
        self.label_11.setMinimumSize(QSize(0, 28))
        self.label_11.setMaximumSize(QSize(16777215, 28))
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_11, 0, 2, 1, 1, Qt.AlignVCenter)

        self.label_10 = QLabel(self.playback_footer_frame_M)
        self.label_10.setObjectName(u"label_10")
        sizePolicy3.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy3)
        self.label_10.setMinimumSize(QSize(0, 28))
        self.label_10.setMaximumSize(QSize(16777215, 28))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(True)
        self.label_10.setFont(font)
        self.label_10.setScaledContents(False)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_10, 0, 1, 1, 1)

        self.horizontalSlider_2 = QSlider(self.playback_footer_frame_M)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        sizePolicy2.setHeightForWidth(self.horizontalSlider_2.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_2.setSizePolicy(sizePolicy2)
        self.horizontalSlider_2.setMinimumSize(QSize(0, 8))
        self.horizontalSlider_2.setMaximumSize(QSize(16777215, 8))
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSlider_2, 1, 0, 1, 3)


        self.horizontalLayout.addWidget(self.playback_footer_frame_M)

        self.playback_footer_frame_R = QFrame(self.playback_footer_frame)
        self.playback_footer_frame_R.setObjectName(u"playback_footer_frame_R")
        sizePolicy.setHeightForWidth(self.playback_footer_frame_R.sizePolicy().hasHeightForWidth())
        self.playback_footer_frame_R.setSizePolicy(sizePolicy)
        self.playback_footer_frame_R.setMinimumSize(QSize(160, 0))
        self.playback_footer_frame_R.setMaximumSize(QSize(16777215, 16777215))
        self.playback_footer_frame_R.setFrameShape(QFrame.NoFrame)
        self.playback_footer_frame_R.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.playback_footer_frame_R)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 8, 2)
        self.playback_button_play_shuffle = QPushButton(self.playback_footer_frame_R)
        self.playback_button_play_shuffle.setObjectName(u"playback_button_play_shuffle")
        self.playback_button_play_shuffle.setMinimumSize(QSize(28, 28))
        self.playback_button_play_shuffle.setMaximumSize(QSize(28, 28))
        self.playback_button_play_shuffle.setCheckable(True)
        self.playback_button_play_shuffle.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_play_shuffle, 0, 2, 1, 1)

        self.playback_button_play_repeat = QPushButton(self.playback_footer_frame_R)
        self.playback_button_play_repeat.setObjectName(u"playback_button_play_repeat")
        self.playback_button_play_repeat.setMinimumSize(QSize(28, 28))
        self.playback_button_play_repeat.setMaximumSize(QSize(28, 28))
        self.playback_button_play_repeat.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_play_repeat, 0, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 0, 2, 1)

        self.playback_button_volume_control = QPushButton(self.playback_footer_frame_R)
        self.playback_button_volume_control.setObjectName(u"playback_button_volume_control")
        self.playback_button_volume_control.setMinimumSize(QSize(28, 28))
        self.playback_button_volume_control.setMaximumSize(QSize(28, 28))
        self.playback_button_volume_control.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_volume_control, 0, 1, 1, 1)

        self.playback_button_play_settings = QPushButton(self.playback_footer_frame_R)
        self.playback_button_play_settings.setObjectName(u"playback_button_play_settings")
        self.playback_button_play_settings.setMinimumSize(QSize(28, 28))
        self.playback_button_play_settings.setMaximumSize(QSize(28, 28))
        self.playback_button_play_settings.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_play_settings, 0, 4, 1, 1)

        self.playback_button_audio_bypass = QPushButton(self.playback_footer_frame_R)
        self.playback_button_audio_bypass.setObjectName(u"playback_button_audio_bypass")
        self.playback_button_audio_bypass.setMinimumSize(QSize(28, 28))
        self.playback_button_audio_bypass.setMaximumSize(QSize(28, 28))
        self.playback_button_audio_bypass.setCheckable(True)
        self.playback_button_audio_bypass.setFlat(True)

        self.gridLayout_5.addWidget(self.playback_button_audio_bypass, 0, 5, 1, 1)

        self.horizontalSlider = QSlider(self.playback_footer_frame_R)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMinimumSize(QSize(0, 8))
        self.horizontalSlider.setMaximumSize(QSize(16777215, 8))
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.horizontalSlider, 1, 1, 1, 5)


        self.horizontalLayout.addWidget(self.playback_footer_frame_R, 0, Qt.AlignRight)


        self.gridLayout.addWidget(self.playback_footer_frame, 2, 0, 1, 1, Qt.AlignBottom)

        self.main_tabs_frame = QSplitter(self.centralwidget)
        self.main_tabs_frame.setObjectName(u"main_tabs_frame")
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
        self.main_tabs_stack_frame.setObjectName(u"main_tabs_stack_frame")
        sizePolicy3.setHeightForWidth(self.main_tabs_stack_frame.sizePolicy().hasHeightForWidth())
        self.main_tabs_stack_frame.setSizePolicy(sizePolicy3)
        self.main_tabs_stack_frame.setMinimumSize(QSize(578, 0))
        self.main_tabs_stack_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.main_tabs_stack_frame)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(2, 2, 2, 2)
        self.stackedWidget = QStackedWidget(self.main_tabs_stack_frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFrameShape(QFrame.StyledPanel)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout_10.addWidget(self.stackedWidget, 0, 0, 1, 1)

        self.main_tabs_frame.addWidget(self.main_tabs_stack_frame)
        self.main_tabs_queue_frame = QFrame(self.main_tabs_frame)
        self.main_tabs_queue_frame.setObjectName(u"main_tabs_queue_frame")
        self.main_tabs_queue_frame.setMinimumSize(QSize(220, 0))
        self.main_tabs_queue_frame.setFrameShape(QFrame.NoFrame)
        self.main_tabs_queue_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.main_tabs_queue_frame)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.main_tabs_queue_frame_splitter = QSplitter(self.main_tabs_queue_frame)
        self.main_tabs_queue_frame_splitter.setObjectName(u"main_tabs_queue_frame_splitter")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(1)
        sizePolicy6.setHeightForWidth(self.main_tabs_queue_frame_splitter.sizePolicy().hasHeightForWidth())
        self.main_tabs_queue_frame_splitter.setSizePolicy(sizePolicy6)
        self.main_tabs_queue_frame_splitter.setOrientation(Qt.Vertical)
        self.main_tabs_queue_frame_splitter.setHandleWidth(0)
        self.main_tabs_queue_frame_queue = QFrame(self.main_tabs_queue_frame_splitter)
        self.main_tabs_queue_frame_queue.setObjectName(u"main_tabs_queue_frame_queue")
        sizePolicy.setHeightForWidth(self.main_tabs_queue_frame_queue.sizePolicy().hasHeightForWidth())
        self.main_tabs_queue_frame_queue.setSizePolicy(sizePolicy)
        self.main_tabs_queue_frame_queue.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(8)
        self.main_tabs_queue_frame_queue.setFont(font1)
        self.main_tabs_queue_frame_queue.setFrameShape(QFrame.NoFrame)
        self.gridLayout_8 = QGridLayout(self.main_tabs_queue_frame_queue)
        self.gridLayout_8.setSpacing(2)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(2, 2, 2, 2)
        self.listView = QListView(self.main_tabs_queue_frame_queue)
        self.listView.setObjectName(u"listView")
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMinimumSize(QSize(0, 156))

        self.gridLayout_8.addWidget(self.listView, 1, 0, 1, 1)

        self.label_19 = QLabel(self.main_tabs_queue_frame_queue)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(0, 24))
        self.label_19.setMaximumSize(QSize(16777215, 24))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setKerning(False)
        font2.setStyleStrategy(QFont.PreferDefault)
        self.label_19.setFont(font2)

        self.gridLayout_8.addWidget(self.label_19, 0, 0, 1, 1)

        self.main_tabs_queue_frame_splitter.addWidget(self.main_tabs_queue_frame_queue)
        self.main_tabs_queue_frame_trackinfo = QFrame(self.main_tabs_queue_frame_splitter)
        self.main_tabs_queue_frame_trackinfo.setObjectName(u"main_tabs_queue_frame_trackinfo")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.main_tabs_queue_frame_trackinfo.sizePolicy().hasHeightForWidth())
        self.main_tabs_queue_frame_trackinfo.setSizePolicy(sizePolicy7)
        self.main_tabs_queue_frame_trackinfo.setMinimumSize(QSize(0, 240))
        self.main_tabs_queue_frame_trackinfo.setFont(font1)
        self.main_tabs_queue_frame_trackinfo.setFrameShape(QFrame.NoFrame)
        self.gridLayout_9 = QGridLayout(self.main_tabs_queue_frame_trackinfo)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.label_17 = QLabel(self.main_tabs_queue_frame_trackinfo)
        self.label_17.setObjectName(u"label_17")
        sizePolicy3.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(16)
        font3.setBold(True)
        self.label_17.setFont(font3)
        self.label_17.setFrameShape(QFrame.StyledPanel)
        self.label_17.setScaledContents(True)
        self.label_17.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label_17, 6, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, -1, -1, -1)
        self.label_12 = QLabel(self.main_tabs_queue_frame_trackinfo)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.verticalLayout.addWidget(self.label_12)

        self.label_13 = QLabel(self.main_tabs_queue_frame_trackinfo)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout.addWidget(self.label_13)

        self.label_14 = QLabel(self.main_tabs_queue_frame_trackinfo)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout.addWidget(self.label_14)

        self.label_15 = QLabel(self.main_tabs_queue_frame_trackinfo)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout.addWidget(self.label_15)

        self.label_16 = QLabel(self.main_tabs_queue_frame_trackinfo)
        self.label_16.setObjectName(u"label_16")
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(7)
        self.label_16.setFont(font4)

        self.verticalLayout.addWidget(self.label_16)


        self.gridLayout_9.addLayout(self.verticalLayout, 5, 0, 1, 1)

        self.label_18 = QLabel(self.main_tabs_queue_frame_trackinfo)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(0, 24))
        self.label_18.setMaximumSize(QSize(16777215, 24))
        self.label_18.setFont(font2)

        self.gridLayout_9.addWidget(self.label_18, 0, 0, 1, 1)

        self.main_tabs_queue_frame_splitter.addWidget(self.main_tabs_queue_frame_trackinfo)

        self.gridLayout_7.addWidget(self.main_tabs_queue_frame_splitter, 0, 0, 1, 1)

        self.main_tabs_frame.addWidget(self.main_tabs_queue_frame)

        self.gridLayout.addWidget(self.main_tabs_frame, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 20))
        self.menubar.setMinimumSize(QSize(0, 20))
        self.menubar.setMaximumSize(QSize(16777215, 20))
        self.menubar.setDefaultUp(True)
        self.menubar.setNativeMenuBar(True)
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.playback_button_play_pause.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.library_tab_switch_button.setText(QCoreApplication.translate("MainWindow", u"Library", None))
        self.now_playing_tab_switch_button.setText(QCoreApplication.translate("MainWindow", u"Now Playing", None))
        self.playlist_tab_switch_button.setText(QCoreApplication.translate("MainWindow", u"Playlist", None))
        self.audiofx_tab_switch_button.setText(QCoreApplication.translate("MainWindow", u"Audio FX", None))
        self.settings_button.setText("")
        self.search_button.setText("")
        self.lineEdit.setInputMask("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.playback_button_prev.setText("")
        self.playback_button_play_pause.setText("")
        self.playback_button_next.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Apollo - Media Player", None))
        self.playback_button_play_shuffle.setText("")
        self.playback_button_play_repeat.setText("")
        self.playback_button_volume_control.setText("")
        self.playback_button_play_settings.setText("")
        self.playback_button_audio_bypass.setText("")
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Playing Queue", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Cover Art", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Track Title", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Misc Info 1", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Misc Info 2", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Misc Info 3", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Stream Info", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Track Information", None))
    # retranslateUi

