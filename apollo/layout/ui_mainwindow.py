# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListView, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QSplitter, QTabWidget, QTableView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(807, 632)
        MainWindow.setMinimumSize(QSize(800, 632))
        font = QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(0, 600))
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_content_splitterframe = QSplitter(self.centralwidget)
        self.main_content_splitterframe.setObjectName(u"main_content_splitterframe")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.main_content_splitterframe.sizePolicy().hasHeightForWidth())
        self.main_content_splitterframe.setSizePolicy(sizePolicy)
        self.main_content_splitterframe.setMinimumSize(QSize(0, 528))
        self.main_content_splitterframe.setOrientation(Qt.Horizontal)
        self.main_content_splitterframe.setHandleWidth(0)
        self.frame_2 = QFrame(self.main_content_splitterframe)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.main_tab_widget = QTabWidget(self.frame_2)
        self.main_tab_widget.setObjectName(u"main_tab_widget")
        self.main_tab_widget.setMinimumSize(QSize(557, 528))
        self.main_tab_widget.setMovable(True)
        self.main_tab_widget.setTabBarAutoHide(True)
        self.library_tab = QWidget()
        self.library_tab.setObjectName(u"library_tab")
        self.gridLayout = QGridLayout(self.library_tab)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.library_tableview = QTableView(self.library_tab)
        self.library_tableview.setObjectName(u"library_tableview")
        self.library_tableview.setFocusPolicy(Qt.NoFocus)
        self.library_tableview.setFrameShape(QFrame.NoFrame)
        self.library_tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.library_tableview.setShowGrid(True)
        self.library_tableview.setSortingEnabled(True)
        self.library_tableview.horizontalHeader().setMinimumSectionSize(128)
        self.library_tableview.horizontalHeader().setDefaultSectionSize(128)
        self.library_tableview.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.library_tableview, 1, 0, 1, 1)

        self.frame = QFrame(self.library_tab)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 32))
        self.frame.setMaximumSize(QSize(16777215, 32))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.library_tab_add_pushbutton = QPushButton(self.frame)
        self.library_tab_add_pushbutton.setObjectName(u"library_tab_add_pushbutton")
        self.library_tab_add_pushbutton.setMinimumSize(QSize(24, 24))
        self.library_tab_add_pushbutton.setMaximumSize(QSize(24, 24))
        self.library_tab_add_pushbutton.setFlat(True)

        self.horizontalLayout_2.addWidget(self.library_tab_add_pushbutton)

        self.library_tab_min_pushbutton = QPushButton(self.frame)
        self.library_tab_min_pushbutton.setObjectName(u"library_tab_min_pushbutton")
        self.library_tab_min_pushbutton.setMinimumSize(QSize(24, 24))
        self.library_tab_min_pushbutton.setMaximumSize(QSize(24, 24))
        self.library_tab_min_pushbutton.setFlat(True)

        self.horizontalLayout_2.addWidget(self.library_tab_min_pushbutton)

        self.library_tab_lineedit = QLineEdit(self.frame)
        self.library_tab_lineedit.setObjectName(u"library_tab_lineedit")
        self.library_tab_lineedit.setMinimumSize(QSize(0, 24))
        self.library_tab_lineedit.setMaximumSize(QSize(16777215, 24))

        self.horizontalLayout_2.addWidget(self.library_tab_lineedit)

        self.library_tab_search_pushbutton = QPushButton(self.frame)
        self.library_tab_search_pushbutton.setObjectName(u"library_tab_search_pushbutton")
        self.library_tab_search_pushbutton.setMinimumSize(QSize(24, 24))
        self.library_tab_search_pushbutton.setMaximumSize(QSize(24, 24))
        self.library_tab_search_pushbutton.setFlat(True)

        self.horizontalLayout_2.addWidget(self.library_tab_search_pushbutton)


        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)

        self.main_tab_widget.addTab(self.library_tab, "")
        self.playlists_tab = QWidget()
        self.playlists_tab.setObjectName(u"playlists_tab")
        self.gridLayout_9 = QGridLayout(self.playlists_tab)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.playlists_tableview = QTableView(self.playlists_tab)
        self.playlists_tableview.setObjectName(u"playlists_tableview")
        self.playlists_tableview.setFocusPolicy(Qt.NoFocus)
        self.playlists_tableview.setFrameShape(QFrame.NoFrame)
        self.playlists_tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.playlists_tableview.setShowGrid(True)
        self.playlists_tableview.setSortingEnabled(True)
        self.playlists_tableview.horizontalHeader().setMinimumSectionSize(128)
        self.playlists_tableview.horizontalHeader().setDefaultSectionSize(128)
        self.playlists_tableview.verticalHeader().setVisible(False)

        self.gridLayout_9.addWidget(self.playlists_tableview, 0, 0, 1, 1)

        self.frame_9 = QFrame(self.playlists_tab)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 32))
        self.frame_9.setMaximumSize(QSize(16777215, 32))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.playlists_tab_add_pushbutton = QPushButton(self.frame_9)
        self.playlists_tab_add_pushbutton.setObjectName(u"playlists_tab_add_pushbutton")
        self.playlists_tab_add_pushbutton.setMinimumSize(QSize(24, 24))
        self.playlists_tab_add_pushbutton.setMaximumSize(QSize(24, 24))
        self.playlists_tab_add_pushbutton.setFlat(True)

        self.horizontalLayout_4.addWidget(self.playlists_tab_add_pushbutton)

        self.playlists_tab_min_pushbutton = QPushButton(self.frame_9)
        self.playlists_tab_min_pushbutton.setObjectName(u"playlists_tab_min_pushbutton")
        self.playlists_tab_min_pushbutton.setMinimumSize(QSize(24, 24))
        self.playlists_tab_min_pushbutton.setMaximumSize(QSize(24, 24))
        self.playlists_tab_min_pushbutton.setFlat(True)

        self.horizontalLayout_4.addWidget(self.playlists_tab_min_pushbutton)

        self.playlists_tab_menu_pushbutton = QPushButton(self.frame_9)
        self.playlists_tab_menu_pushbutton.setObjectName(u"playlists_tab_menu_pushbutton")
        self.playlists_tab_menu_pushbutton.setMinimumSize(QSize(24, 24))
        self.playlists_tab_menu_pushbutton.setMaximumSize(QSize(24, 24))
        self.playlists_tab_menu_pushbutton.setFlat(True)

        self.horizontalLayout_4.addWidget(self.playlists_tab_menu_pushbutton)

        self.playlists_tab_lineedit = QLineEdit(self.frame_9)
        self.playlists_tab_lineedit.setObjectName(u"playlists_tab_lineedit")
        self.playlists_tab_lineedit.setMinimumSize(QSize(0, 24))
        self.playlists_tab_lineedit.setMaximumSize(QSize(16777215, 24))

        self.horizontalLayout_4.addWidget(self.playlists_tab_lineedit)

        self.playlists_tab_search_pushbutton = QPushButton(self.frame_9)
        self.playlists_tab_search_pushbutton.setObjectName(u"playlists_tab_search_pushbutton")
        self.playlists_tab_search_pushbutton.setMinimumSize(QSize(24, 24))
        self.playlists_tab_search_pushbutton.setMaximumSize(QSize(24, 24))
        self.playlists_tab_search_pushbutton.setFlat(True)

        self.horizontalLayout_4.addWidget(self.playlists_tab_search_pushbutton)


        self.gridLayout_9.addWidget(self.frame_9, 1, 0, 1, 1)

        self.main_tab_widget.addTab(self.playlists_tab, "")
        self.now_playing_tab = QWidget()
        self.now_playing_tab.setObjectName(u"now_playing_tab")
        self.gridLayout_11 = QGridLayout(self.now_playing_tab)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.now_playing_tab_splitter = QSplitter(self.now_playing_tab)
        self.now_playing_tab_splitter.setObjectName(u"now_playing_tab_splitter")
        self.now_playing_tab_splitter.setOrientation(Qt.Horizontal)
        self.now_playing_tab_splitter.setHandleWidth(0)
        self.cover_pixmap_large = QLabel(self.now_playing_tab_splitter)
        self.cover_pixmap_large.setObjectName(u"cover_pixmap_large")
        sizePolicy1.setHeightForWidth(self.cover_pixmap_large.sizePolicy().hasHeightForWidth())
        self.cover_pixmap_large.setSizePolicy(sizePolicy1)
        self.cover_pixmap_large.setMinimumSize(QSize(0, 0))
        self.cover_pixmap_large.setMaximumSize(QSize(16777215, 16777215))
        self.cover_pixmap_large.setFrameShape(QFrame.StyledPanel)
        self.cover_pixmap_large.setAlignment(Qt.AlignCenter)
        self.now_playing_tab_splitter.addWidget(self.cover_pixmap_large)
        self.lyrics_groupbox = QGroupBox(self.now_playing_tab_splitter)
        self.lyrics_groupbox.setObjectName(u"lyrics_groupbox")
        self.lyrics_groupbox.setMinimumSize(QSize(250, 0))
        self.lyrics_groupbox.setFlat(True)
        self.lyrics_groupbox.setCheckable(False)
        self.gridLayout_10 = QGridLayout(self.lyrics_groupbox)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.lyrics_listview = QListView(self.lyrics_groupbox)
        self.lyrics_listview.setObjectName(u"lyrics_listview")
        self.lyrics_listview.setFrameShape(QFrame.NoFrame)

        self.gridLayout_10.addWidget(self.lyrics_listview, 0, 0, 1, 1)

        self.now_playing_tab_splitter.addWidget(self.lyrics_groupbox)

        self.gridLayout_11.addWidget(self.now_playing_tab_splitter, 0, 0, 1, 1)

        self.main_tab_widget.addTab(self.now_playing_tab, "")

        self.gridLayout_2.addWidget(self.main_tab_widget, 0, 0, 1, 1)

        self.main_content_splitterframe.addWidget(self.frame_2)
        self.frame_3 = QFrame(self.main_content_splitterframe)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.queue_groupbox = QGroupBox(self.frame_3)
        self.queue_groupbox.setObjectName(u"queue_groupbox")
        self.queue_groupbox.setMinimumSize(QSize(250, 0))
        self.queue_groupbox.setFlat(True)
        self.queue_groupbox.setCheckable(False)
        self.gridLayout_8 = QGridLayout(self.queue_groupbox)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.listView = QListView(self.queue_groupbox)
        self.listView.setObjectName(u"listView")
        self.listView.setFrameShape(QFrame.NoFrame)

        self.gridLayout_8.addWidget(self.listView, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.queue_groupbox)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 32))
        self.frame_7.setMaximumSize(QSize(16777215, 32))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.queue_tab_add_pushbutton = QPushButton(self.frame_7)
        self.queue_tab_add_pushbutton.setObjectName(u"queue_tab_add_pushbutton")
        self.queue_tab_add_pushbutton.setMinimumSize(QSize(24, 24))
        self.queue_tab_add_pushbutton.setMaximumSize(QSize(24, 24))
        self.queue_tab_add_pushbutton.setFlat(True)

        self.horizontalLayout_3.addWidget(self.queue_tab_add_pushbutton)

        self.queue_tab_min_pushbutton = QPushButton(self.frame_7)
        self.queue_tab_min_pushbutton.setObjectName(u"queue_tab_min_pushbutton")
        self.queue_tab_min_pushbutton.setMinimumSize(QSize(24, 24))
        self.queue_tab_min_pushbutton.setMaximumSize(QSize(24, 24))
        self.queue_tab_min_pushbutton.setFlat(True)

        self.horizontalLayout_3.addWidget(self.queue_tab_min_pushbutton)

        self.queue_tab_lineedit = QLineEdit(self.frame_7)
        self.queue_tab_lineedit.setObjectName(u"queue_tab_lineedit")
        self.queue_tab_lineedit.setMinimumSize(QSize(0, 24))
        self.queue_tab_lineedit.setMaximumSize(QSize(16777215, 24))

        self.horizontalLayout_3.addWidget(self.queue_tab_lineedit)

        self.queue_tab_search_pushbutton = QPushButton(self.frame_7)
        self.queue_tab_search_pushbutton.setObjectName(u"queue_tab_search_pushbutton")
        self.queue_tab_search_pushbutton.setMinimumSize(QSize(24, 24))
        self.queue_tab_search_pushbutton.setMaximumSize(QSize(24, 24))
        self.queue_tab_search_pushbutton.setFlat(True)

        self.horizontalLayout_3.addWidget(self.queue_tab_search_pushbutton)


        self.gridLayout_8.addWidget(self.frame_7, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.queue_groupbox, 0, 0, 1, 1)

        self.main_content_splitterframe.addWidget(self.frame_3)

        self.verticalLayout.addWidget(self.main_content_splitterframe)

        self.playback_footer_frame = QFrame(self.centralwidget)
        self.playback_footer_frame.setObjectName(u"playback_footer_frame")
        self.playback_footer_frame.setMinimumSize(QSize(0, 72))
        self.playback_footer_frame.setMaximumSize(QSize(16777215, 72))
        self.playback_footer_frame.setFrameShape(QFrame.NoFrame)
        self.playback_footer_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.playback_footer_frame)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.playback_footer_frame)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy2)
        self.gridLayout_5 = QGridLayout(self.frame_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 4)
        self.seeking_slider = QSlider(self.frame_5)
        self.seeking_slider.setObjectName(u"seeking_slider")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.seeking_slider.sizePolicy().hasHeightForWidth())
        self.seeking_slider.setSizePolicy(sizePolicy3)
        self.seeking_slider.setMinimumSize(QSize(272, 0))
        self.seeking_slider.setMaximumSize(QSize(16777215, 16777215))
        self.seeking_slider.setTracking(True)
        self.seeking_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.seeking_slider, 1, 1, 1, 2)

        self.completed_time_label = QLabel(self.frame_5)
        self.completed_time_label.setObjectName(u"completed_time_label")

        self.gridLayout_5.addWidget(self.completed_time_label, 1, 0, 1, 1)

        self.total_time_label = QLabel(self.frame_5)
        self.total_time_label.setObjectName(u"total_time_label")

        self.gridLayout_5.addWidget(self.total_time_label, 1, 3, 1, 1)

        self.frame_6 = QFrame(self.frame_5)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy4)
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.frame_6)
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.shuffle_pushbutton = QPushButton(self.frame_6)
        self.shuffle_pushbutton.setObjectName(u"shuffle_pushbutton")
        self.shuffle_pushbutton.setMinimumSize(QSize(32, 32))
        self.shuffle_pushbutton.setMaximumSize(QSize(32, 32))
        self.shuffle_pushbutton.setFlat(True)

        self.horizontalLayout.addWidget(self.shuffle_pushbutton)

        self.prev_pushbutton = QPushButton(self.frame_6)
        self.prev_pushbutton.setObjectName(u"prev_pushbutton")
        self.prev_pushbutton.setMinimumSize(QSize(32, 32))
        self.prev_pushbutton.setMaximumSize(QSize(32, 32))
        self.prev_pushbutton.setFlat(True)

        self.horizontalLayout.addWidget(self.prev_pushbutton)

        self.play_pushbutton = QPushButton(self.frame_6)
        self.play_pushbutton.setObjectName(u"play_pushbutton")
        self.play_pushbutton.setMinimumSize(QSize(40, 40))
        self.play_pushbutton.setMaximumSize(QSize(40, 40))
        self.play_pushbutton.setFlat(True)

        self.horizontalLayout.addWidget(self.play_pushbutton)

        self.next_pushbutton = QPushButton(self.frame_6)
        self.next_pushbutton.setObjectName(u"next_pushbutton")
        self.next_pushbutton.setMinimumSize(QSize(32, 32))
        self.next_pushbutton.setMaximumSize(QSize(32, 32))
        self.next_pushbutton.setFlat(True)

        self.horizontalLayout.addWidget(self.next_pushbutton)

        self.repeat_pushbutton = QPushButton(self.frame_6)
        self.repeat_pushbutton.setObjectName(u"repeat_pushbutton")
        self.repeat_pushbutton.setMinimumSize(QSize(32, 32))
        self.repeat_pushbutton.setMaximumSize(QSize(32, 32))
        self.repeat_pushbutton.setFlat(True)

        self.horizontalLayout.addWidget(self.repeat_pushbutton)


        self.gridLayout_5.addWidget(self.frame_6, 0, 0, 1, 4, Qt.AlignHCenter)


        self.gridLayout_4.addWidget(self.frame_5, 0, 1, 1, 1)

        self.frame_4 = QFrame(self.playback_footer_frame)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy5)
        self.frame_4.setMinimumSize(QSize(200, 0))
        self.frame_4.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_6 = QGridLayout(self.frame_4)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 1, 2, 1)

        self.cover_pixmap = QLabel(self.frame_4)
        self.cover_pixmap.setObjectName(u"cover_pixmap")
        self.cover_pixmap.setMinimumSize(QSize(72, 72))
        self.cover_pixmap.setMaximumSize(QSize(72, 72))
        self.cover_pixmap.setFrameShape(QFrame.StyledPanel)
        self.cover_pixmap.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.cover_pixmap, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.playback_footer_frame)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy5.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy5)
        self.frame_8.setMinimumSize(QSize(200, 0))
        self.frame_8.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_7 = QGridLayout(self.frame_8)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(6)
        self.gridLayout_7.setVerticalSpacing(8)
        self.gridLayout_7.setContentsMargins(0, 0, 4, 0)
        self.audio_fx_pushbutton = QPushButton(self.frame_8)
        self.audio_fx_pushbutton.setObjectName(u"audio_fx_pushbutton")
        self.audio_fx_pushbutton.setMinimumSize(QSize(28, 28))
        self.audio_fx_pushbutton.setMaximumSize(QSize(28, 28))
        self.audio_fx_pushbutton.setFlat(True)

        self.gridLayout_7.addWidget(self.audio_fx_pushbutton, 1, 2, 1, 1)

        self.switch_audio_pushbutton = QPushButton(self.frame_8)
        self.switch_audio_pushbutton.setObjectName(u"switch_audio_pushbutton")
        self.switch_audio_pushbutton.setMinimumSize(QSize(28, 28))
        self.switch_audio_pushbutton.setMaximumSize(QSize(28, 28))
        self.switch_audio_pushbutton.setFlat(True)

        self.gridLayout_7.addWidget(self.switch_audio_pushbutton, 1, 3, 1, 1)

        self.settings_pushbutton = QPushButton(self.frame_8)
        self.settings_pushbutton.setObjectName(u"settings_pushbutton")
        self.settings_pushbutton.setMinimumSize(QSize(28, 28))
        self.settings_pushbutton.setMaximumSize(QSize(28, 28))
        self.settings_pushbutton.setFlat(True)

        self.gridLayout_7.addWidget(self.settings_pushbutton, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 0, 2, 1)

        self.volume_slider = QSlider(self.frame_8)
        self.volume_slider.setObjectName(u"volume_slider")
        sizePolicy3.setHeightForWidth(self.volume_slider.sizePolicy().hasHeightForWidth())
        self.volume_slider.setSizePolicy(sizePolicy3)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_7.addWidget(self.volume_slider, 0, 2, 1, 3)

        self.volume_pushbutton = QPushButton(self.frame_8)
        self.volume_pushbutton.setObjectName(u"volume_pushbutton")
        self.volume_pushbutton.setMinimumSize(QSize(28, 28))
        self.volume_pushbutton.setMaximumSize(QSize(28, 28))
        self.volume_pushbutton.setFlat(True)

        self.gridLayout_7.addWidget(self.volume_pushbutton, 0, 1, 1, 1)

        self.queue_pushbutton = QPushButton(self.frame_8)
        self.queue_pushbutton.setObjectName(u"queue_pushbutton")
        self.queue_pushbutton.setMinimumSize(QSize(28, 28))
        self.queue_pushbutton.setMaximumSize(QSize(28, 28))
        self.queue_pushbutton.setFlat(True)

        self.gridLayout_7.addWidget(self.queue_pushbutton, 1, 4, 1, 1)


        self.gridLayout_4.addWidget(self.frame_8, 0, 2, 1, 1, Qt.AlignVCenter)


        self.verticalLayout.addWidget(self.playback_footer_frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 807, 20))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)

        self.main_tab_widget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Apollo", None))
        self.library_tab_add_pushbutton.setText("")
        self.library_tab_min_pushbutton.setText("")
        self.library_tab_search_pushbutton.setText("")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.library_tab), QCoreApplication.translate("MainWindow", u"Library", None))
        self.playlists_tab_add_pushbutton.setText("")
        self.playlists_tab_min_pushbutton.setText("")
        self.playlists_tab_menu_pushbutton.setText("")
        self.playlists_tab_search_pushbutton.setText("")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.playlists_tab), QCoreApplication.translate("MainWindow", u"Playlists", None))
        self.cover_pixmap_large.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lyrics_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Lyrics", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.now_playing_tab), QCoreApplication.translate("MainWindow", u"Now Playing", None))
        self.queue_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Currently Playing", None))
        self.queue_tab_add_pushbutton.setText("")
        self.queue_tab_min_pushbutton.setText("")
        self.queue_tab_search_pushbutton.setText("")
        self.completed_time_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.total_time_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.shuffle_pushbutton.setText("")
        self.prev_pushbutton.setText("")
        self.play_pushbutton.setText("")
        self.next_pushbutton.setText("")
        self.repeat_pushbutton.setText("")
        self.cover_pixmap.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.audio_fx_pushbutton.setText("")
        self.switch_audio_pushbutton.setText("")
        self.settings_pushbutton.setText("")
        self.volume_pushbutton.setText("")
        self.queue_pushbutton.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

